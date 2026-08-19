#!/usr/bin/env python3
"""Exit 0 when packaging is current, 2 when a newer stable release exists."""

from __future__ import annotations

import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
text = (ROOT / "snap" / "snapcraft.yaml").read_text()
match = re.search(r'^version: "([^"]+)"$', text, re.MULTILINE)
if not match:
    raise SystemExit("cannot find version in snapcraft.yaml")
packaged = match.group(1)

req = urllib.request.Request(
    "https://herdr.dev/latest.json",
    headers={"User-Agent": "herdr-snap-updater/1"},
)
with urllib.request.urlopen(req, timeout=30) as response:
    latest = json.load(response)["version"]

print(f"packaged={packaged}")
print(f"latest={latest}")
raise SystemExit(0 if packaged == latest else 2)
