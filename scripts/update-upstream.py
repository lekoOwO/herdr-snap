#!/usr/bin/env python3
"""Update snap/snapcraft.yaml to the current stable Herdr release."""

from __future__ import annotations

import json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SNAPCRAFT = ROOT / "snap" / "snapcraft.yaml"
MANIFEST_URL = os.environ.get("HERDR_MANIFEST_URL", "https://herdr.dev/latest.json")


def fetch_manifest() -> dict:
    req = urllib.request.Request(
        MANIFEST_URL,
        headers={"User-Agent": "herdr-snap-updater/1"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def replace_once(text: str, pattern: str, replacement: str) -> str:
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"expected exactly one match for {pattern!r}, got {count}")
    return result


def main() -> int:
    manifest = fetch_manifest()
    version = manifest["version"]
    sha = manifest["sha256"]
    amd64 = sha["linux-x86_64"]
    arm64 = sha["linux-aarch64"]

    text = SNAPCRAFT.read_text()
    text = replace_once(text, r'^version: ".*"$', f'version: "{version}"')
    text = replace_once(
        text,
        r'^(\s+sha256_amd64=")[0-9a-f]{64}("\s*)$',
        rf'\g<1>{amd64}\g<2>',
    )
    text = replace_once(
        text,
        r'^(\s+sha256_arm64=")[0-9a-f]{64}("\s*)$',
        rf'\g<1>{arm64}\g<2>',
    )

    SNAPCRAFT.write_text(text)
    print(f"Updated Herdr snap metadata to v{version}")
    print(f"  amd64: {amd64}")
    print(f"  arm64: {arm64}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
