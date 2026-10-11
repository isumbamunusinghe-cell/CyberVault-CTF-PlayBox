#!/usr/bin/env python3
"""Validate the CV-04 evidence chain and generated player archive."""

import base64
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "evidence" / "case-FY-26-104"
ARCHIVE = ROOT / "player" / "evidence-package.zip"
FLAG = "CTF{forensic_evidence_found}"


def main():
    audit = (CASE / "workstation" / "file-audit.csv").read_text()
    device = (CASE / "workstation" / "usb-events.log").read_text()
    manifest = (CASE / "removable-media" / "manifest.txt").read_text()
    if not all(item in audit and item in device and item in manifest
               for item in ("USB-7A31", "onboarding_bundle.tar", "2026-09-18T09:21:44Z")):
        raise SystemExit("FAIL: event correlation fields do not agree")

    record_path = CASE / "removable-media" / "recovery" / "record-003.dat"
    record = json.loads(base64.b64decode(record_path.read_text()).decode())
    expected = {
        "case": "FY-26-104",
        "workstation": "WS-24",
        "device": "USB-7A31",
        "event_time": "2026-09-18T09:21:44Z",
        "archive": "onboarding_bundle.tar",
        "flag": FLAG,
    }
    if record != expected:
        raise SystemExit("FAIL: recovered record does not match expected case data")

    raw = b"".join(path.read_bytes() for path in CASE.rglob("*") if path.is_file())
    if FLAG.encode() in raw:
        raise SystemExit("FAIL: flag appears in plaintext in player evidence sources")
    if not ARCHIVE.is_file():
        raise SystemExit("FAIL: player evidence ZIP is missing; run source/build_package.py")
    if FLAG.encode() in ARCHIVE.read_bytes():
        raise SystemExit("FAIL: flag appears in plaintext in the player ZIP")
    with ZipFile(ARCHIVE) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise SystemExit(f"FAIL: ZIP CRC error in {bad_member}")
        if len(archive.namelist()) != len(list(CASE.rglob("*.*"))):
            raise SystemExit("FAIL: evidence ZIP file count does not match source files")
    print("PASS: workstation and removable-media records correlate on user/device/time/archive")
    print("PASS: recovery record decodes and matches the correlated incident")
    print("PASS: flag is not plaintext in evidence files; player ZIP is readable")


if __name__ == "__main__":
    main()
