#!/usr/bin/env python3
"""Fail-closed localhost forward proxy for Argus browser egress.

Every destination is normalized, resolved with a hard timeout, checked against all
non-public address classes, and connected by the exact validated IP. Chromium never
resolves or connects to the destination directly when configured to use this proxy.
"""
from __future__ import annotations

import argparse
import asyncio
import contextlib
import ipaddress
import signal
import socket
import sys
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

LEARNING_DIR = Path(__file__).resolve().parents[1] / "learning"
if str(LEARNING_DIR) not in sys.path:
    sys.path.insert(0, str(LEARNING_DIR))
from network_policy import is_strict_public_ip

MAX_HEADER_BYTES = 65_536
HEADER_TIMEOUT_SECONDS = 10.0
DNS_TIMEOUT_SECONDS = 5.0
CONNECT_TIMEOUT_SECONDS = 10.0
CONNECTION_LIFETIME_SECONDS = 300.0
STREAM_IDLE_TIMEOUT_SECONDS = 60.0
MAX_DNS_OUTPUT_BYTES = 64 * 1024
MAX_RESOLVED_ADDRESSES = 32
MAX_CONNECT_ATTEMPTS = 8
STREAM_CHUNK_BYTES = 64 * 1024


class DestinationBlocked(Exception):
    """Raised when a proxy destination does not meet the public-only policy."""


def _normalize_host(host: str) -> str:
    value = (host or "").strip().rstrip(".").lower()
    if not value:
        raise DestinationBlocked("missing_host")
    try:
        return value.encode("idna").decode("ascii")
    except UnicodeError as error:
        raise DestinationBlocked("invalid_host") from error


def _validated_port(port: int | None, default: int) -> int:
    value = default if port is None else int(port)
    if not 1 <= value <= 65_535:
        raise DestinationBlocked("invalid_port")
    return value


def parse_proxy_destination(method: str, target: str) -> tuple[str, int, str]:
    """Return normalized host, port, and origin-form target for a proxy request."""
    method = method.upper()
    target = (target or "").strip()
    try:
        if method == "CONNECT":
            parts = urlsplit(f"//{target}")
            if parts.username or parts.password or not parts.hostname or parts.path:
                raise DestinationBlocked("invalid_connect_authority")
            return _normalize_host(parts.hostname), _validated_port(parts.port, 443), ""

        parts = urlsplit(target)
        scheme = parts.scheme.lower()
        if scheme not in {"http", "https", "ws", "wss"}:
            raise DestinationBlocked("unsupported_scheme")
        if parts.username or parts.password:
            raise DestinationBlocked("credentialed_url")
        host = _normalize_host(parts.hostname or "")
        default_port = 443 if scheme in {"https", "wss"} else 80
        origin_target = urlunsplit(("", "", parts.path or "/", parts.query, ""))
        return host, _validated_port(parts.port, default_port), origin_target
    except ValueError as error:
        raise DestinationBlocked("invalid_destination") from error


def _public_ip(value: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    try:
        address = ipaddress.ip_address(value)
    except ValueError as error:
        raise DestinationBlocked("invalid_resolved_address") from error
    if not is_strict_public_ip(address):
        raise DestinationBlocked("non_public_destination")
    return address


async def _resolve_with_getent(host: str, timeout: float) -> list[str]:
    """Resolve in a killable subprocess so a stalled libc resolver cannot leak threads."""
    process = await asyncio.create_subprocess_exec(
        "/usr/bin/getent",
        "ahosts",
        host,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    try:
        stdout, _ = await asyncio.wait_for(
            process.communicate(), timeout=max(0.1, float(timeout))
        )
    except BaseException as error:
        if process.returncode is None:
            with contextlib.suppress(ProcessLookupError):
                process.kill()
        reap_task = asyncio.create_task(process.wait())
        while not reap_task.done():
            try:
                await asyncio.shield(reap_task)
            except asyncio.CancelledError:
                # Preserve cancellation, but never abandon a live resolver child.
                continue
        with contextlib.suppress(BaseException):
            reap_task.result()
        if isinstance(error, TimeoutError):
            raise DestinationBlocked("dns_timeout") from error
        raise
    if process.returncode != 0:
        raise DestinationBlocked("dns_failure")
    if len(stdout) > MAX_DNS_OUTPUT_BYTES:
        raise DestinationBlocked("dns_response_too_large")
    addresses: list[str] = []
    for raw_line in stdout.decode("ascii", "strict").splitlines():
        value = raw_line.split(maxsplit=1)[0] if raw_line.strip() else ""
        if value and value not in addresses:
            addresses.append(value)
    return addresses


async def resolve_public_addresses(
    host: str,
    port: int,
    *,
    timeout: float = DNS_TIMEOUT_SECONDS,
    resolver: Callable[[str, float], Awaitable[list[str]]] | None = None,
) -> list[tuple[int, str]]:
    """Resolve once, reject mixed/public-private answers, and return exact public IPs."""
    normalized = _normalize_host(host)
    try:
        literal = ipaddress.ip_address(normalized)
    except ValueError:
        literal = None
    if literal is not None:
        public = _public_ip(str(literal))
        family = socket.AF_INET6 if public.version == 6 else socket.AF_INET
        return [(family, str(public))]

    try:
        addresses = await asyncio.wait_for(
            (resolver or _resolve_with_getent)(normalized, timeout),
            timeout=max(0.1, float(timeout)) + 0.25,
        )
    except TimeoutError as error:
        raise DestinationBlocked("dns_timeout") from error
    if not addresses:
        raise DestinationBlocked("no_public_address")
    if len(addresses) > MAX_RESOLVED_ADDRESSES:
        raise DestinationBlocked("too_many_dns_answers")

    resolved: list[tuple[int, str]] = []
    seen: set[tuple[int, str]] = set()
    for value in addresses:
        public = _public_ip(str(value))
        family = socket.AF_INET6 if public.version == 6 else socket.AF_INET
        item = (family, str(public))
        if item not in seen:
            seen.add(item)
            resolved.append(item)
    if not resolved:
        raise DestinationBlocked("no_public_address")
    return resolved


async def _pipe(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while True:
            chunk = await asyncio.wait_for(
                reader.read(STREAM_CHUNK_BYTES), timeout=STREAM_IDLE_TIMEOUT_SECONDS
            )
            if not chunk:
                break
            writer.write(chunk)
            await writer.drain()
    except (ConnectionError, asyncio.CancelledError):
        pass
    finally:
        with contextlib.suppress(Exception):
            writer.write_eof()


class PublicEgressProxy:
    """Minimal HTTP CONNECT/forward proxy with exact-IP destination pinning."""

    def __init__(
        self,
        *,
        connector: Callable[..., Awaitable[tuple[asyncio.StreamReader, asyncio.StreamWriter]]] | None = None,
        resolver: Callable[[str, float], Awaitable[list[str]]] | None = None,
        max_connections: int = 64,
    ) -> None:
        self.connector = connector or asyncio.open_connection
        self.resolver = resolver
        self.semaphore = asyncio.Semaphore(max(1, int(max_connections)))

    async def open_validated_connection(
        self,
        host: str,
        port: int,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        addresses = await resolve_public_addresses(host, port, resolver=self.resolver)
        last_error: Exception | None = None
        try:
            async with asyncio.timeout(CONNECT_TIMEOUT_SECONDS):
                for family, address in addresses[:MAX_CONNECT_ATTEMPTS]:
                    try:
                        return await self.connector(address, port, family=family)
                    except OSError as error:
                        last_error = error
        except TimeoutError as error:
            last_error = error
        raise ConnectionError("validated_destination_unreachable") from last_error

    @staticmethod
    async def _respond(writer: asyncio.StreamWriter, status: bytes) -> None:
        writer.write(status + b"\r\nConnection: close\r\nContent-Length: 0\r\n\r\n")
        await writer.drain()

    async def _handle(self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter) -> None:
        remote_writer: asyncio.StreamWriter | None = None
        try:
            header = await asyncio.wait_for(
                client_reader.readuntil(b"\r\n\r\n"),
                timeout=HEADER_TIMEOUT_SECONDS,
            )
            if len(header) > MAX_HEADER_BYTES:
                raise DestinationBlocked("header_too_large")
            lines = header[:-4].split(b"\r\n")
            request_parts = lines[0].decode("ascii", "strict").split(" ")
            if len(request_parts) != 3:
                raise DestinationBlocked("invalid_request_line")
            method, target, version = request_parts
            if not version.startswith("HTTP/1."):
                raise DestinationBlocked("unsupported_http_version")
            host, port, origin_target = parse_proxy_destination(method, target)
            remote_reader, remote_writer = await self.open_validated_connection(host, port)

            if method.upper() == "CONNECT":
                client_writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
                await client_writer.drain()
            else:
                forwarded = [f"{method} {origin_target} {version}".encode("ascii")]
                for line in lines[1:]:
                    name = line.partition(b":")[0].strip().lower()
                    if name in {b"proxy-authorization", b"proxy-connection"}:
                        continue
                    forwarded.append(line)
                remote_writer.write(b"\r\n".join(forwarded) + b"\r\n\r\n")
                await remote_writer.drain()

            client_to_remote = asyncio.create_task(_pipe(client_reader, remote_writer))
            remote_to_client = asyncio.create_task(_pipe(remote_reader, client_writer))
            done, pending = await asyncio.wait(
                {client_to_remote, remote_to_client},
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            await asyncio.gather(*done, *pending, return_exceptions=True)
        except DestinationBlocked:
            with contextlib.suppress(Exception):
                await self._respond(client_writer, b"HTTP/1.1 403 Forbidden")
        except (asyncio.IncompleteReadError, UnicodeError, ValueError):
            with contextlib.suppress(Exception):
                await self._respond(client_writer, b"HTTP/1.1 400 Bad Request")
        except (ConnectionError, OSError, TimeoutError):
            with contextlib.suppress(Exception):
                await self._respond(client_writer, b"HTTP/1.1 502 Bad Gateway")
        finally:
            if remote_writer is not None:
                remote_writer.close()
                with contextlib.suppress(Exception):
                    await remote_writer.wait_closed()
            client_writer.close()
            with contextlib.suppress(Exception):
                await client_writer.wait_closed()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            async with asyncio.timeout(CONNECTION_LIFETIME_SECONDS):
                async with self.semaphore:
                    await self._handle(reader, writer)
        except TimeoutError:
            pass
        finally:
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()

    async def start(self, host: str, port: int) -> asyncio.AbstractServer:
        if host not in {"127.0.0.1", "::1"}:
            raise ValueError("proxy listener must be loopback-only")
        return await asyncio.start_server(
            self.handle_client,
            host,
            port,
            limit=MAX_HEADER_BYTES,
        )


async def async_main(host: str, port: int) -> None:
    proxy = PublicEgressProxy()
    server = await proxy.start(host, port)
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with contextlib.suppress(NotImplementedError):
            loop.add_signal_handler(sig, stop.set)
    sockets = ",".join(str(sock.getsockname()) for sock in server.sockets or [])
    print(f"Argus public-only browser egress proxy listening on {sockets}", flush=True)
    async with server:
        await stop.wait()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9219)
    args = parser.parse_args()
    asyncio.run(async_main(args.host, args.port))


if __name__ == "__main__":
    main()
