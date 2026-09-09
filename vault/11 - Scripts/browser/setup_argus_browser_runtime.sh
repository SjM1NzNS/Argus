#!/usr/bin/env bash
set -euo pipefail
ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
VENV="${ARGUS_BROWSER_VENV:-$HOME/.local/share/argus-browser/venv}"
PYTHON_VERSION="${ARGUS_BROWSER_PYTHON_VERSION:-3.13}"
REQUIREMENTS="$ROOT/11 - Scripts/browser/browser-requirements.txt"
command -v uv >/dev/null 2>&1 || { echo 'uv is required' >&2; exit 1; }
[[ -f "$REQUIREMENTS" ]] || { echo "Missing requirements: $REQUIREMENTS" >&2; exit 1; }
CHROME_BINARY="${ARGUS_CHROME_BINARY:-/usr/bin/google-chrome}"
[[ -x "$CHROME_BINARY" ]] || { echo "Launchable system Chrome is required: $CHROME_BINARY" >&2; exit 1; }
command -v systemd-run >/dev/null 2>&1 || { echo 'systemd-run is required for browser cgroup bounds' >&2; exit 1; }
systemd-run --user --scope --quiet --collect -p MemoryMax=64M -p TasksMax=16 /usr/bin/true
uv venv --python "$PYTHON_VERSION" --allow-existing "$VENV"
uv pip sync --python "$VENV/bin/python" "$REQUIREMENTS"
ARGUS_CHROME_BINARY="$CHROME_BINARY" \
ARGUS_LEARNING_SCRIPT_DIR="$ROOT/11 - Scripts/learning" \
"$VENV/bin/python" - <<'PY'
import asyncio, os, sys, yaml
from pathlib import Path
from playwright.async_api import async_playwright
from playwright._impl._driver import compute_driver_executable

sys.path.insert(0, os.environ["ARGUS_LEARNING_SCRIPT_DIR"])
from browser_runtime import browser_launch_options, configure_playwright_node

async def smoke():
    configure_playwright_node()
    playwright = await async_playwright().start()
    browser = None
    try:
        options = browser_launch_options()
        if not options.get("chromium_sandbox"):
            raise RuntimeError("sandbox must be enabled for setup smoke")
        browser = await playwright.chromium.launch(**options)
        return browser.version
    finally:
        if browser is not None:
            await browser.close()
        await playwright.stop()

print({
    "python": sys.executable,
    "pyyaml": yaml.__version__,
    "playwright_import": bool(async_playwright),
    "playwright_driver": tuple(map(str, compute_driver_executable())),
    "system_chrome": os.environ["ARGUS_CHROME_BINARY"],
    "sandboxed_launch_version": asyncio.run(smoke()),
})
PY
