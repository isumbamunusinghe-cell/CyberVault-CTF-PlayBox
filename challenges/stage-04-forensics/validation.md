# CV-04 validation record

## Automated checks completed

- The synthetic workstation file-audit and USB event records agree on employee24, device USB-7A31, the 2026-09-18T09:21:44Z event, and `onboarding_bundle.tar`.
- The manifest points to recovery record 003.
- The Base64 recovery record decodes to JSON whose case, workstation, device, event time, archive and expected flag agree with the correlated records.
- The flag is not present as plaintext in the evidence source files.
- The generated ZIP passed its CRC test and contains all seven evidence files.
- `source/validate_evidence.py` passed after packaging.
- Current package SHA-256: `51c411c253c404c56b56dd4c70799aa5bdc2483eb5dfbdd50ed28d22b1885b2d`.

## Still to test

- Open the extracted evidence folder in Autopsy as a Logical Files data source and demonstrate the relevant file review.
- Have a fresh player follow the brief and intended path without maintainer hints.
- Test the website's flag acceptance/scoring, or document the instructor's manual validation if website integration is not ready.
- Restore the trusted ZIP and verify the SHA-256 as the reset check.

The evidence is synthetic and offline. No real employee data or external system is involved. Automated content/package checks are not a substitute for the remaining Autopsy and fresh-player tests.
