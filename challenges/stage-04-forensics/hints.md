# CV-04 progressive hints — maintainer copy

Release these one at a time if the platform supports progressive hints.

1. Start with the case time window. Compare the workstation logs and removable-device records.
2. Look for a file operation that occurs at the same time as a removable device write. Match the device identifier and archive name across records.
3. The matching recovery record is text encoded as Base64. Decode it after establishing that it belongs to the correlated event.
