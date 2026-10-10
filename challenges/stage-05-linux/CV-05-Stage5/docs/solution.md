**# CV-05 intended solution — maintainer only**

**\*\*Do not distribute this file to participants.\*\*** It names the weakness and development flag.

**## Intended path**

1\. Connect as the unprivileged \`player\` account over SSH.
2\. Enumerate identity, groups, sudo permissions, and file ownership/modes.
3\. Observe that \`player\` belongs to \`cvmaint\` and may run only \`/usr/local/sbin/cv05-maintenance\` as root, without arguments.
4\. Inspect the root-owned launcher. It invokes \`/bin/bash /opt/cybervault/maintenance/collect-evidence.sh\`.
5\. Observe that the helper is owned by \`root:cvmaint\` and group-writable. The launcher itself is not writable.
6\. In the authorized lab, replace the contents of that helper with a controlled script that identifies its effective user and reads \`/root/evidence/incident-report.txt\`.
7\. Invoke the permitted launcher with no arguments. The helper runs as root and displays the evidence.
8\. Recover the development flag: \`CTF{linux_privilege_found}\`.

**## Controlled validation example**

Run from the authenticated \`player\` shell **\*\*inside CV-05\*\***. This deliberately modifies only the helper inside the current container and reads the synthetic evidence; use the checkpoint and reset procedure in \`validation.md\` before and after this test.

\`\`\`bash
cat > /opt/cybervault/maintenance/collect-evidence.sh <<'EOF'
\#!/bin/bash
set -euo pipefail
echo "Effective UID:"
/usr/bin/id
echo "Recovered development flag:"
/usr/bin/cat /root/evidence/incident-report.txt
EOF

sudo -n /usr/local/sbin/cv05-maintenance
\`\`\`

Expected evidence is \`uid=0(root)\` and the incident report containing \`CTF{linux_privilege_found}\`. The source helper on the Ubuntu host and the image are not modified by this in-container test.

**## Reset**

The maintainer reset in \`validation.md\` removes the changed container layer and network, then creates a fresh container from the existing image, reapplies firewall rules, and starts the service. It does not rebuild or delete the image. Confirm the helper SHA-256 returns to \`8d187dad65f49a10a8210efa54abac980853cce408bf8bbdb4699b9614d67e4f\`, and confirm \`player\` cannot directly read the evidence.
