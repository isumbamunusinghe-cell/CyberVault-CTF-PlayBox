# CV-06 Stage 6 The Final Trace

This is the initial implementation of the Stage 6 design in the group report. It is an offline packet-analysis challenge: it does not start a network service, connect to the synthetic addresses, or require a Docker container.

## Current files

- `player/player-brief.md` — participant instructions.
- `player/final-trace.pcap` — synthetic capture for Wireshark.
- `source/generate_capture.py` — reproducible, standard-library PCAP generator.
- `source/validate_capture.py` — checks PCAP structure, TCP checksums, expected stream, and decoded flag.
- `maintainer/hints.md` — progressive hints.
- `maintainer/solution.md` — solution and expected flag; maintainer-only.

## Local generation and validation

Requires Python 3. Run from this folder:

```bash
python3 source/generate_capture.py
python3 source/validate_capture.py
sha256sum player/final-trace.pcap
```

Current generated capture SHA-256: `ba06f6e593a8802ce617fbfe43e230ff83afda6911d4e7fcc4d9c1f8819b5fee`.

## Player run and reset

Give the player `player/player-brief.md` and `player/final-trace.pcap`. The player opens the capture in Wireshark and submits the recovered flag through the method the group configures. Reset is restoring the original PCAP artifact; there is no stateful challenge service to reset.

The capture passed the included standard-library checker and a live player-side Wireshark test on Kali. The player filtered the HTTP POST requests, followed the stream to the synthetic transfer destination, decoded the Base64 evidence, and recovered the intended flag. The Kali copy's SHA-256 matched the generated artifact. See `maintainer/validation.md` for the test record.

Integration with the group's scoring/flag-submission platform is still pending. The group's report proposes CTFd, but this folder does not implement that integration. A manual validation method can be used if the group documents and demonstrates it for the submission.

Keep `maintainer/` and `source/` out of any public participant download. In particular, the generator contains the expected flag to create the artifact. Store the repository privately or otherwise restrict maintainer files; the PCAP itself is intentionally solvable by players.
