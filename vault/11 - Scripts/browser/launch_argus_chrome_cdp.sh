#!/usr/bin/env bash
set -euo pipefail

PROFILE_DIR="${ARGUS_CHROME_CDP_PROFILE:-$HOME/.cache/argus-chrome-agent-profile}"
CDP_HOST="${ARGUS_CHROME_CDP_HOST:-127.0.0.1}"
CDP_PORT="${ARGUS_CHROME_CDP_PORT:-9222}"
CHROME_BINARY="${ARGUS_CHROME_BINARY:-/usr/bin/google-chrome}"
EGRESS_PROXY="${ARGUS_BROWSER_EGRESS_PROXY:-http://127.0.0.1:9219}"
PYTHON_BINARY="${ARGUS_PYTHON_BINARY:-/usr/bin/python3}"
LEARNING_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../learning" && pwd)"

if [[ ! -x "$CHROME_BINARY" ]]; then
  printf 'Chrome binary is not executable: %s\n' "$CHROME_BINARY" >&2
  exit 1
fi
if [[ "$CDP_HOST" != "127.0.0.1" && "$CDP_HOST" != "::1" ]]; then
  printf 'Refusing to expose Chrome DevTools outside loopback: %s\n' "$CDP_HOST" >&2
  exit 2
fi
if [[ ! -x "$PYTHON_BINARY" ]]; then
  printf 'Python binary is not executable: %s\n' "$PYTHON_BINARY" >&2
  exit 3
fi
if ! EGRESS_PROXY="$($PYTHON_BINARY -c '
import sys
sys.path.insert(0, sys.argv[1])
from network_policy import validate_loopback_http_proxy_url
print(validate_loopback_http_proxy_url(sys.argv[2]))
' "$LEARNING_DIR" "$EGRESS_PROXY" 2>/dev/null)"; then
  printf 'ARGUS_BROWSER_EGRESS_PROXY must be a credential-free loopback HTTP proxy\n' >&2
  exit 4
fi

install -d -m 700 "$PROFILE_DIR"
exec "$CHROME_BINARY" \
  --headless=new \
  --remote-debugging-address="$CDP_HOST" \
  --remote-debugging-port="$CDP_PORT" \
  --remote-allow-origins="http://127.0.0.1:${CDP_PORT}" \
  --user-data-dir="$PROFILE_DIR" \
  --no-first-run \
  --no-default-browser-check \
  --disable-dev-shm-usage \
  --disable-background-networking \
  --disable-component-update \
  --disable-sync \
  --disable-crash-reporter \
  --disable-breakpad \
  --disable-quic \
  --disable-features=AsyncDns \
  --force-webrtc-ip-handling-policy=disable_non_proxied_udp \
  --proxy-server="$EGRESS_PROXY" \
  --proxy-bypass-list='<-loopback>' \
  --metrics-recording-only \
  about:blank
