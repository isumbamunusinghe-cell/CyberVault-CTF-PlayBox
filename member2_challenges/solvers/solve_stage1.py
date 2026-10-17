#!/usr/bin/env python3
"""
Member 2 - LO3 Automated Solver for Stage 1 (Steganography)
Parses standard EXIF UserComment metadata to recover the hidden flag.
"""
import sys
import os
import piexif

def solve_stage1(file_path):
    print(f"[*] Analyzing artifact: {file_path}")
    if not os.path.exists(file_path):
        print(f"[-] File not found: {file_path}")
        return None

    try:
        exif_dict = piexif.load(file_path)
        raw_comment = exif_dict.get("Exif", {}).get(piexif.ExifIFD.UserComment, b"")

        if raw_comment:
            # Strip standard 8-byte charset prefix (e.g. b'ASCII\x00\x00\x00') if present
            if raw_comment.startswith(b"ASCII\x00\x00\x00"):
                recovered_flag = raw_comment[8:].decode("ascii", errors="ignore")
            else:
                recovered_flag = raw_comment.decode("utf-8", errors="ignore").strip("\x00")

            if "CTF{" in recovered_flag:
                print(f"[+] Flag successfully recovered: {recovered_flag}")
                return recovered_flag
            else:
                print(f"[*] Extracted comment: {recovered_flag}")
        else:
            print("[-] No UserComment found in EXIF tags.")
    except Exception as e:
        print(f"[-] Parsing error: {e}")
    return None

if __name__ == "__main__":
    default_path = os.path.join(os.path.dirname(__file__), "..", "stage1_stego", "evidence_photo.jpg")
    target = sys.argv[1] if len(sys.argv) > 1 else default_path
    solve_stage1(target)