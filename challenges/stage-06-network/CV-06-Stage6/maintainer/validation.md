# CV-06 validation record

## Functional player test

- The generated PCAP opened successfully in Wireshark on Kali Linux.
- Wireshark displayed 27 packets.
- Display filter `http.request.method == "POST"` showed the internal telemetry request and the archive request to `203.0.113.77`.
- Following the archive TCP stream exposed a Base64-encoded evidence body.
- Decoding the body produced the incident record and expected flag `CTF{final_trace_complete}`.
- On Kali, `sha256sum ~/cybervault/cv-06/final-trace.pcap` returned `ba06f6e593a8802ce617fbfe43e230ff83afda6911d4e7fcc4d9c1f8819b5fee`, matching the reproducibly generated artifact.

## Automated artifact checks

The included `source/validate_capture.py` passed. It confirmed the classic PCAP header, Ethernet/IPv4/TCP packet framing, IPv4 and TCP checksums, 27 complete packets, one intended archive stream to the synthetic endpoint, and the decoded expected flag. It also confirms the flag is not present as plaintext in the PCAP bytes.

## Reset and limits

CV-06 is a static, offline artifact with no stateful service. Reset means restore the original `player/final-trace.pcap` from the trusted group copy and compare its SHA-256 with the value above. The player's investigation does not modify the capture. The user-tested Kali file matched the expected hash after solving.

The CV-06 folder does not currently configure CTFd, scoring, hint deductions, or automated flag submission. Demonstrate the group's configured platform or include a clear manual flag-validation procedure before claiming that portion is implemented. No live connection to addresses in the capture is required or intended.
