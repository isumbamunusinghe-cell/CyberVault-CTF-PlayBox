#!/usr/bin/env python3
"""Check the CV-06 PCAP structure and confirm its intended stream is recoverable."""

import base64
import hashlib
import json
import struct
from collections import defaultdict
from pathlib import Path

CAPTURE = Path(__file__).resolve().parents[1] / "player" / "final-trace.pcap"
FLAG = "CTF{final_trace_complete}"


def ones_sum(data):
    if len(data) & 1:
        data += b"\0"
    total = sum(struct.unpack(f"!{len(data)//2}H", data))
    while total >> 16:
        total = (total & 0xffff) + (total >> 16)
    return total


def main():
    raw = CAPTURE.read_bytes()
    if raw[:4] != bytes.fromhex("d4c3b2a1"):
        raise SystemExit("FAIL: unexpected PCAP magic or byte order")
    linktype = struct.unpack_from("<I", raw, 20)[0]
    if linktype != 1:
        raise SystemExit(f"FAIL: expected Ethernet link type 1, got {linktype}")

    offset, count = 24, 0
    streams = defaultdict(list)
    destinations = set()
    while offset < len(raw):
        _, _, caplen, origlen = struct.unpack_from("<IIII", raw, offset)
        offset += 16
        frame = raw[offset:offset+caplen]
        offset += caplen
        count += 1
        if caplen != origlen or len(frame) < 54 or frame[12:14] != b"\x08\x00":
            raise SystemExit("FAIL: malformed or truncated Ethernet/IPv4 frame")
        ip = frame[14:34]
        if ip[0] != 0x45 or ones_sum(ip) != 0xffff:
            raise SystemExit("FAIL: malformed IPv4 header or checksum")
        proto = ip[9]
        if proto != 6:
            continue
        src, dst = ".".join(map(str, ip[12:16])), ".".join(map(str, ip[16:20]))
        ihl = (ip[0] & 0x0f) * 4
        total_len = struct.unpack_from("!H", ip, 2)[0]
        tcp = frame[14+ihl:14+total_len]
        pseudo = ip[12:20] + struct.pack("!BBH", 0, 6, len(tcp))
        if ones_sum(pseudo + tcp) != 0xffff:
            raise SystemExit("FAIL: malformed TCP checksum")
        sport, dport, seq, ack = struct.unpack_from("!HHII", tcp)
        tcp_hlen = (tcp[12] >> 4) * 4
        payload = tcp[tcp_hlen:]
        destinations.add(dst)
        if payload:
            streams[(src, dst, sport, dport)].append((seq, payload))

    requests = []
    for (src, dst, sport, dport), segments in streams.items():
        stream = b"".join(payload for _, payload in sorted(segments))
        if stream.startswith(b"POST /sync/v3/archive "):
            requests.append((dst, stream))
    if count != 27 or len(requests) != 1:
        raise SystemExit(f"FAIL: expected 27 packets and one archive POST; got {count} and {len(requests)}")

    dst, request = requests[0]
    headers, body = request.split(b"\r\n\r\n", 1)
    decoded = json.loads(base64.b64decode(body))
    if dst != "203.0.113.77" or decoded.get("flag") != FLAG:
        raise SystemExit("FAIL: expected synthetic transfer endpoint or flag not found")
    if FLAG.encode() in raw:
        raise SystemExit("FAIL: flag appears in plaintext in the capture")

    print("PASS: valid classic PCAP with 27 complete Ethernet/IPv4/TCP packets and checksums")
    print("PASS: unique archive POST reaches synthetic documentation address 203.0.113.77")
    print("PASS: base64 evidence decodes to the expected flag; flag is not plaintext in capture")
    print(f"SHA-256: {hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
