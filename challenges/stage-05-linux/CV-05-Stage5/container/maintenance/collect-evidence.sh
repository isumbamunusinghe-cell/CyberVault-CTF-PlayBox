#!/bin/bash
set -euo pipefail

{
    echo "CyberVault incident maintenance"
    /usr/bin/date -u
    /usr/bin/hostname
    /usr/bin/id
    echo "Protected incident evidence is held in /root/evidence."
} > /var/log/cybervault-maintenance.log

echo "Maintenance collection complete."
