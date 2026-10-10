#!/bin/bash
set -euo pipefail

if [[ $# -ne 0 ]]; then
    echo "This maintenance task does not accept arguments." >&2
    exit 1
fi

echo "CyberVault maintenance: collecting incident evidence."
/bin/bash /opt/cybervault/maintenance/collect-evidence.sh
