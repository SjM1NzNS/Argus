from __future__ import annotations

import asyncio
import ipaddress
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR.parent / "browser"))

from browser_egress_proxy import (
    DestinationBlocked,
    PublicEgressProxy,
    _resolve_with_getent,
    parse_proxy_destination,
    resolve_public_addresses,
)


class ProxyParsingTests(unittest.TestCase):
    def test_connect_and_absolute_request_destinations_are_normalized(self) -> None:
        self.assertEqual(
            parse_proxy_destination("CONNECT", "example.com:443"),
            ("example.com", 443, ""),
        )
        self.assertEqual(
            parse_proxy_destination("GET", "http://Example.COM:8080/path?q=1"),
            ("example.com", 8080, "/path?q=1"),
        )

    def test_credentials_and_unsupported_schemes_are_rejected(self) -> None:
        for method, target in (
            ("GET", "http://user:pass@example.com/"),
            ("GET", "file:///etc/passwd"),
            ("CONNECT", "user@example.com:443"),
        ):
            with self.subTest(target=target):
                with self.assertRaises(DestinationBlocked):
                    parse_proxy_destination(method, target)


class ProxyResolutionTests(unittest.IsolatedAsyncioTestCase):
    async def test_any_private_resolution_blocks_the_destination(self) -> None:
        resolver = mock.AsyncMock(return_value=["93.184.216.34", "127.0.0.1"])
        with self.assertRaises(DestinationBlocked):
            await resolve_public_addresses("example.com", 443, timeout=1, resolver=resolver)

    async def test_special_and_mixed_answers_are_rejected(self) -> None:
        for answers in (
            ["224.0.0.1"],
            ["fec0::1"],
            ["ff02::1"],
            ["64:ff9b::7f00:1"],
            ["93.184.216.34", "ff02::1"],
        ):
            with self.subTest(answers=answers):
                resolver = mock.AsyncMock(return_value=answers)
                with self.assertRaises(DestinationBlocked):
                    await resolve_public_addresses("example.com", 443, timeout=1, resolver=resolver)

    async def test_resolution_is_pinned_to_the_validated_ip(self) -> None:
        resolver = mock.AsyncMock(return_value=["93.184.216.34"])
        connector = mock.AsyncMock(return_value=(mock.Mock(), mock.Mock()))
        proxy = PublicEgressProxy(connector=connector, resolver=resolver)
        await proxy.open_validated_connection("example.com", 443)
        connector.assert_awaited_once()
        args = connector.await_args.args
        self.assertEqual(args[:2], ("93.184.216.34", 443))
        self.assertIsInstance(ipaddress.ip_address(args[0]), ipaddress.IPv4Address)

    async def test_getent_timeout_kills_the_resolver_process(self) -> None:
        class Process:
            returncode = None
            killed = False

            async def communicate(self):
                await asyncio.sleep(10)
                return b"", b""

            def kill(self):
                self.killed = True
                self.returncode = -9

            async def wait(self):
                return self.returncode

        process = Process()
        with mock.patch(
            "browser_egress_proxy.asyncio.create_subprocess_exec",
            new=mock.AsyncMock(return_value=process),
        ):
            with self.assertRaises(DestinationBlocked):
                await _resolve_with_getent("example.com", 0.01)
        self.assertTrue(process.killed)

    async def test_direct_resolver_task_cancellation_kills_and_reaps_process(self) -> None:
        started = asyncio.Event()

        class Process:
            returncode = None
            killed = False
            waited = False

            async def communicate(self):
                started.set()
                await asyncio.sleep(10)
                return b"", b""

            def kill(self):
                self.killed = True
                self.returncode = -9

            async def wait(self):
                self.waited = True
                return self.returncode

        process = Process()
        with mock.patch(
            "browser_egress_proxy.asyncio.create_subprocess_exec",
            new=mock.AsyncMock(return_value=process),
        ):
            task = asyncio.create_task(_resolve_with_getent("example.com", 10))
            await started.wait()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertTrue(process.killed)
        self.assertTrue(process.waited)

    async def test_semaphore_wait_is_inside_connection_lifetime_deadline(self) -> None:
        class Writer:
            closed = False

            def close(self):
                self.closed = True

            async def wait_closed(self):
                return None

        proxy = PublicEgressProxy(max_connections=1)
        await proxy.semaphore.acquire()
        writer = Writer()
        try:
            with mock.patch("browser_egress_proxy.CONNECTION_LIFETIME_SECONDS", 0.05):
                await asyncio.wait_for(proxy.handle_client(mock.Mock(), writer), timeout=0.2)
        finally:
            proxy.semaphore.release()
        self.assertTrue(writer.closed)

    async def test_resolution_timeout_cancels_the_resolver_coroutine(self) -> None:
        cancelled = asyncio.Event()

        async def stalled(_host: str, _timeout: float) -> list[str]:
            try:
                await asyncio.sleep(10)
            finally:
                cancelled.set()
            return []

        with self.assertRaises(DestinationBlocked):
            await resolve_public_addresses("example.com", 443, timeout=0.05, resolver=stalled)
        self.assertTrue(cancelled.is_set())

    async def test_connect_attempts_share_one_aggregate_deadline(self) -> None:
        resolver = mock.AsyncMock(
            return_value=[f"93.184.216.{value}" for value in range(1, 13)]
        )

        async def black_hole(*_args, **_kwargs):
            await asyncio.sleep(10)

        proxy = PublicEgressProxy(connector=black_hole, resolver=resolver)
        with mock.patch("browser_egress_proxy.CONNECT_TIMEOUT_SECONDS", 0.05):
            with self.assertRaises(ConnectionError):
                await proxy.open_validated_connection("example.com", 443)

    async def test_private_connect_request_is_denied_before_any_connection(self) -> None:
        connector = mock.AsyncMock()
        proxy = PublicEgressProxy(connector=connector)
        server = await proxy.start("127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        try:
            reader, writer = await asyncio.open_connection("127.0.0.1", port)
            writer.write(b"CONNECT 127.0.0.1:80 HTTP/1.1\r\nHost: 127.0.0.1:80\r\n\r\n")
            await writer.drain()
            response = await asyncio.wait_for(reader.read(4096), timeout=2)
            self.assertIn(b"403 Forbidden", response)
            connector.assert_not_awaited()
            writer.close()
            await writer.wait_closed()
        finally:
            server.close()
            await server.wait_closed()


if __name__ == "__main__":
    unittest.main()
