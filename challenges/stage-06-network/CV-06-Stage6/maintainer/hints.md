# CV-06 progressive hints — maintainer copy

Release one hint at a time through the scoring mechanism, if configured.

1. Compare the conversations in the capture and look for a destination that does not fit routine internal activity.
2. Filter for HTTP POST traffic and inspect the destination and request path.
3. Follow the TCP stream to the synthetic transfer host. Its request body is encoded; identify the encoding and decode it.
