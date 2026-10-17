#!/usr/bin/env python3
"""
Member 2 - LO3 Automated Solver for Stage 2 (Cryptography)
Extracts base64 encoded strings from the evidence note and recovers the flag.
"""
import os
import sys
import re
import base64

def solve_stage2(file_path):
    print(f"[*] Inspecting evidence note: {file_path}")
    if not os.path.exists(file_path):
        print(f"[-] File not found: {file_path}")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Match candidate Base64 strings (length >= 8, valid base64 chars with optional padding)
    candidates = re.findall(r'[A-Za-z0-9+/]{8,}={0,2}', text)

    for candidate in candidates:
        try:
            decoded = base64.b64decode(candidate).decode("utf-8", errors="ignore")
            if "CTF{" in decoded:
                print(f"[+] Discovered Flag: {decoded}")
                return decoded
        except Exception:
            continue

    print("[-] Flag pattern not found in candidate strings.")
    return None

if __name__ == "__main__":
    default_path = os.path.join(os.path.dirname(__file__), "..", "stage2_crypto", "leaked_memo.txt")
    target = sys.argv[1] if len(sys.argv) > 1 else default_path
    solve_stage2(target)