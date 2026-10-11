#!/usr/bin/env python3
"""Package the synthetic CV-04 evidence directory reproducibly."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "case-FY-26-104"
OUTPUT = ROOT / "player" / "evidence-package.zip"


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in EVIDENCE.rglob("*") if path.is_file())
    if not files:
        raise SystemExit("No evidence files found")
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            name = Path("case-FY-26-104") / path.relative_to(EVIDENCE)
            info = ZipInfo(name.as_posix(), date_time=(2026, 9, 18, 8, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    print(f"Packaged {len(files)} synthetic evidence files: {OUTPUT}")


if __name__ == "__main__":
    main()
