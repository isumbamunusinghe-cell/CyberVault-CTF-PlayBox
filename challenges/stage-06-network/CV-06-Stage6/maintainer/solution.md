# CV-06 intended solution — maintainer only

Keep this file and the source scripts out of participant downloads.

## Intended player path

1. Open `player/final-trace.pcap` in Wireshark.
2. Compare the conversations and notice the HTTP POST to synthetic destination `203.0.113.77:8080`; the routine internal portal and telemetry exchanges are decoys.
3. Follow the TCP stream for the request to `/sync/v3/archive`.
4. Copy the request body and decode it as Base64. It contains JSON incident evidence and the final flag.

Expected flag: `CTF{final_trace_complete}`.

The capture uses `203.0.113.77`, an address reserved for documentation examples. The challenge is offline packet analysis; players must not connect to or scan any address from the capture.

## Rebuild and validate

From the CV-06 project root, run:

```bash
python3 source/generate_capture.py
python3 source/validate_capture.py
sha256sum player/final-trace.pcap
```

The generator uses only Python's standard library and a fixed synthetic timestamp, so the output should be reproducible byte-for-byte. The validation script checks the PCAP framing, packet count, target stream and decoded flag. Record the SHA-256 after regeneration and compare it to the committed artifact.

## Integration note

The assignment report proposes CTFd to accept the flag, but the current CV-06 handoff does not implement CTFd integration, scoring, hint deductions, or a reset API. Until integrated, validate the expected flag manually in the controlled demo or use the group's configured CTFd challenge.
