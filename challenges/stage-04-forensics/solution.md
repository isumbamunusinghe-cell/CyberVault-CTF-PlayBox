# CV-04 intended solution — maintainer only

Keep this file out of player downloads.

## Intended path

1. Review `workstation/case-readme.txt` for the evidence source and investigation time window.
2. Correlate the `file-audit.csv` archive creation/copy event with `usb-events.log`. Both identify employee24, workstation WS-24, removable device USB-7A31, and the 09:21:44Z write of `onboarding_bundle.tar`.
3. Inspect the matching removable-media `manifest.txt`. It identifies `recovery/record-003.dat` as the catalog entry for that archive event.
4. Identify that the `.dat` file contains Base64 text, decode it, and inspect the JSON record. Confirm that the case, workstation, device, event time, and archive match the other evidence before accepting its flag.

Expected flag: `CTF{forensic_evidence_found}`.

Example analysis commands, run against a working copy of the supplied evidence:

```bash
find case-FY-26-104 -type f -print
grep -R -n -E '2026-09-18T09:21:44Z|USB-7A31|onboarding_bundle.tar' case-FY-26-104
file case-FY-26-104/removable-media/recovery/record-003.dat
base64 -d case-FY-26-104/removable-media/recovery/record-003.dat
```

The same files can be reviewed in a forensic case tool as a logical evidence source. Maintain the original package and analyze an extracted working copy.
