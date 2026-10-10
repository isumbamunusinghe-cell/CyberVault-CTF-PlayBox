#!/usr/bin/env python3
"""Generate the synthetic CV-06 capture with Python's standard library only."""

import json
import struct
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "player" / "final-trace.pcap"
CLIENT, SERVER, AUDIT, SINK = "10.20.5.24", "10.20.5.80", "10.20.5.30", "203.0.113.77"
CMAC, SMAC = bytes.fromhex("020000000024"), bytes.fromhex("020000000080")
packets, ip_id = [], 1


def csum(data):
    if len(data) & 1:
        data += b"\0"
    words = struct.unpack(f"!{len(data)//2}H", data)
    total = sum(words)
    total = (total & 0xffff) + (total >> 16)
    total = (total & 0xffff) + (total >> 16)
    return (~total) & 0xffff


def tcp_packet(ts, src, dst, sport, dport, seq, ack, flags, payload=b"", reverse=False):
    global ip_id
    sip, dip = bytes(map(int, src.split("."))), bytes(map(int, dst.split(".")))
    tcp_len = 20 + len(payload)
    tcp0 = struct.pack("!HHIIHHHH", sport, dport, seq, ack, (5 << 12) | flags, 64240, 0, 0)
    tcp_sum = csum(sip + dip + struct.pack("!BBH", 0, 6, tcp_len) + tcp0 + payload)
    tcp = struct.pack("!HHIIHHHH", sport, dport, seq, ack, (5 << 12) | flags, 64240, tcp_sum, 0) + payload
    ip0 = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(tcp), ip_id, 0x4000, 64, 6, 0, sip, dip)
    ip_sum = csum(ip0)
    ip = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(tcp), ip_id, 0x4000, 64, 6, ip_sum, sip, dip)
    ip_id += 1
    src_mac, dst_mac = (SMAC, CMAC) if reverse else (CMAC, SMAC)
    packets.append((ts, dst_mac + src_mac + struct.pack("!H", 0x0800) + ip + tcp))


def exchange(start, dst, dport, sport, request, response):
    cseq, sseq = 10000 + sport, 50000 + sport
    tcp_packet(start, CLIENT, dst, sport, dport, cseq, 0, 0x02)
    tcp_packet(start+.01, dst, CLIENT, dport, sport, sseq, cseq+1, 0x12, reverse=True)
    tcp_packet(start+.02, CLIENT, dst, sport, dport, cseq+1, sseq+1, 0x10)
    tcp_packet(start+.03, CLIENT, dst, sport, dport, cseq+1, sseq+1, 0x18, request)
    tcp_packet(start+.04, dst, CLIENT, dport, sport, sseq+1, cseq+1+len(request), 0x10, reverse=True)
    tcp_packet(start+.05, dst, CLIENT, dport, sport, sseq+1, cseq+1+len(request), 0x18, response, reverse=True)
    tcp_packet(start+.06, CLIENT, dst, sport, dport, cseq+1+len(request), sseq+1+len(response), 0x10)
    tcp_packet(start+.07, dst, CLIENT, dport, sport, sseq+1+len(response), cseq+1+len(request), 0x11, reverse=True)
    tcp_packet(start+.08, CLIENT, dst, sport, dport, cseq+1+len(request), sseq+2+len(response), 0x10)


def response(body, mime="text/plain"):
    return f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n".encode() + body


def main():
    # Fixed synthetic capture time makes regeneration byte-for-byte repeatable.
    t = 1791504000
    req = b"GET /login HTTP/1.1\r\nHost: portal.cybervault.internal\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n"
    exchange(t, SERVER, 80, 49152, req, response(b"<html><p>Case reference FY-26-104</p></html>", "text/html"))

    body = b"service=cv05&event=healthcheck&status=ok"
    req = (b"POST /telemetry HTTP/1.1\r\nHost: logs.cybervault.internal:8080\r\nContent-Type: application/x-www-form-urlencoded\r\n"
           + f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n".encode() + body)
    exchange(t+1, AUDIT, 8080, 49153, req, response(b"accepted"))

    evidence = {"case": "FY-26-104", "source": "employee-workstation-24", "transfer": "incident-archive", "flag": "CTF{final_trace_complete}"}
    encoded = __import__("base64").b64encode(json.dumps(evidence, separators=(",", ":")).encode())
    req = (b"POST /sync/v3/archive HTTP/1.1\r\nHost: transfer-gateway.example:8080\r\nUser-Agent: archive-client/2.1\r\nContent-Type: application/octet-stream\r\n"
           + f"Content-Length: {len(encoded)}\r\nConnection: close\r\n\r\n".encode() + encoded)
    exchange(t+2, SINK, 8080, 49154, req, response(b"queued"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("wb") as f:
        f.write(struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
        for ts, frame in sorted(packets):
            sec = int(ts)
            usec = int((ts-sec)*1_000_000)
            f.write(struct.pack("<IIII", sec, usec, len(frame), len(frame)))
            f.write(frame)
    print(f"Wrote {len(packets)} packets: {OUT}")


if __name__ == "__main__":
    main()
