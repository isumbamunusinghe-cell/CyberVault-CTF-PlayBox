#!/usr/bin/env python3
import base64

flag = "CTF{encoded_note_decoded}"
encoded = base64.b64encode(flag.encode()).decode()

content = f"""=====================================================
CYBERVAULT INCIDENT REPORT - INTERNAL MEMO
Case ID: IR-2026-OCT-01
Classification: RESTRICTED
=====================================================

Security Team Note:
During the workstation sweep, the suspect pasted this encoded
string into an unindexed draft document before disconnection:

Payload String:
{encoded}

=====================================================
"""

with open("leaked_memo.txt", "w") as f:
    f.write(content)

print("[+] Created leaked_memo.txt with encoded flag.")