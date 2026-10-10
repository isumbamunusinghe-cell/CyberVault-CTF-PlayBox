#!/bin/bash
set -euo pipefail

install -d -m 0755 /run/sshd
ssh-keygen -A
/usr/sbin/sshd -t

exec /usr/sbin/sshd -D -e
