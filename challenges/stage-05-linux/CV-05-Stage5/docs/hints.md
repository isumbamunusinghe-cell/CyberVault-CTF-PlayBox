**# CV-05 progressive hints — maintainer copy**

Release hints in order. These hints point toward the intended investigation without giving the flag.

1\. **\*\*General enumeration:\*\*** Start with your identity, group memberships, available sudo permissions, and filesystem permissions.
2\. **\*\*Permission clue:\*\*** A single maintenance action is allowed with elevated privileges. Trace every script that action runs and check who can modify each one.
3\. **\*\*Strong guidance:\*\*** The root-owned launcher at \`/usr/local/sbin/cv05-maintenance\` runs \`/opt/cybervault/maintenance/collect-evidence.sh\`. The maintenance-group permissions on that helper are central to the challenge.
