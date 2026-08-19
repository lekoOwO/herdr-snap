#!/usr/bin/env python3
"""Cheap offline checks for packaging metadata."""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
text = (ROOT / "snap" / "snapcraft.yaml").read_text()

checks = {
    "name": r'^name: herdr$',
    "version": r'^version: "\d+\.\d+\.\d+"$',
    "classic confinement": r'^confinement: classic$',
    "amd64 checksum": r'^\s+sha256_amd64="[0-9a-f]{64}"$',
    "arm64 checksum": r'^\s+sha256_arm64="[0-9a-f]{64}"$',
    "amd64 asset": r'asset="herdr-linux-x86_64"',
    "arm64 asset": r'asset="herdr-linux-aarch64"',
}

failed = []
for name, pattern in checks.items():
    if not re.search(pattern, text, re.MULTILINE):
        failed.append(name)

if failed:
    raise SystemExit("failed checks: " + ", ".join(failed))

print("packaging metadata checks passed")
