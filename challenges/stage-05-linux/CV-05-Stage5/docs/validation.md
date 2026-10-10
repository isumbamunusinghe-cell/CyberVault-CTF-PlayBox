**# CV-05 validation and operations record**

**\*\*Status:\*\*** Standalone implementation tested in the local VirtualBox lab. Results below reflect command output reported during participant-guided testing; they are not an independent audit of the VM.

**## Environment and deployment**

\- Kali Linux 2026.1 participant VM and Ubuntu Server 24.04.4 Docker host VM in Oracle VirtualBox.
\- Docker Engine 29.8.2 and Docker Compose v5.6.0.
\- Image: \`cybervault-cv05:dev\`; observed image ID \`sha256:0bc78b34b96eba33ba98a7a516e495acd9a39b3f893807b10b6d39e4e6041551\`.
\- SSH endpoint: Ubuntu host-only address \`192.168.60.50:2222\`, published to container port 22.
\- Kali host-only address used by firewall rules: \`192.168.60.100\`.
\- Container address: \`172.30.50.10\` on bridge \`br-cv05\`, subnet \`172.30.50.0/24\`.
\- Compose uses a non-internal bridge because Docker did not apply port publishing on the original internal bridge. Isolation is enforced by scoped IPv4 and IPv6 firewall rules; the configured container DNS upstream is loopback.

**## Checks observed passing**

\- Docker build and sudoers syntax validation; container SSH service started and host port mapped to \`192.168.60.50:2222\`.
\- Fresh SSH player login returned \`uid=1001(player)\` with supplementary group \`cvmaint\`.
\- The launcher was root-owned and not writable; the maintenance helper was group-writable; direct player access to \`/root/evidence/incident-report.txt\` was denied.
\- \`sudo -n -l\` listed only the no-argument maintenance launcher. Unrelated root commands and launcher invocation with arguments were denied by sudo.
\- The unchanged maintenance workflow ran as root; it created a root-owned log and did not change the helper SHA-256.
\- Remote forwarding and client-requested TCP forwarding were rejected. An actual root SSH login was rejected, with the server log stating root was not listed in \`AllowUsers\`.
\- Container root lacked \`NET_ADMIN\`, \`SYS_ADMIN\`, and \`NET_RAW\`; seccomp was active; AppArmor reported \`docker-default (enforce)\`; the container was not privileged, had no host mounts or devices, used private IPC and the default PID namespace, and had configured memory, CPU, PID, and log limits.
\- Isolation probes showed player and container root timing out to a temporary listener on the Docker host bridge address and to a temporary Kali host-only listener. A temporary default-bridge probe timed out against the published host-only and Ubuntu NAT addresses. A routed direct-container test timed out while the published SSH endpoint remained reachable.
\- Step 10 intended path recovered \`CTF{linux_privilege_found}\`. Before testing, the in-container helper was copied to a host checkpoint; the recorded SHA-256 was \`8d187dad65f49a10a8210efa54abac980853cce408bf8bbdb4699b9614d67e4f\`.
\- Reset was performed with Compose down/create using the existing image, firewall reapplication, and container start. The fresh container helper, host source helper, and checkpoint all had the recorded original SHA-256. A fresh player session again could not read the evidence directly.

**## Limitations and remaining verification**

\- The solution was not repeated after reset. The clean-state checks passed, but a second end-to-end solve was not performed.
\- VirtualBox NAT-interface ingress was not independently tested from an external peer. Do not claim that test passed.
\- Firewall rules are runtime state and disappeared on Ubuntu reboot. After every host reboot, run \`sudo bash ./apply-firewall.sh\` before starting CV-05. Compose has restart policy \`no\`.
\- Container recreation generates new SSH host keys. Verify the new fingerprint out of band and remove/update the stale client \`known_hosts\` entry before reconnecting. Kali's old known-hosts file was retained as \`\~/.ssh/known_hosts.old\` during the observed reset.
\- The build uses the mutable \`ubuntu:24.04\` tag and unpinned APT packages. Rebuilding later may produce a different image. The tested image ID is the known-good development image; save/export it if binary-identical recovery is required.
\- The development password is intentionally synthetic and fixed for this isolated lab. Change it before any separately approved multi-user deployment and protect access to the Docker host and source files.
\- Docker containers share the Ubuntu VM kernel. Keep this intentionally vulnerable challenge on the isolated VM and host-only lab; do not expose it to the public Internet or connect it to production/CTFd service networks.

**## Checkpoint and reset procedure**

Before an authorized privilege-path test, preserve the existing helper and record the image/configuration identity:

\`\`\`bash
cd /home/lahirubernal/cybervault/cv-05
mkdir -p checkpoints
sudo docker cp cybervault-cv05-cv05-1:/opt/cybervault/maintenance/collect-evidence.sh checkpoints/collect-evidence.step10-original.sh
sudo chmod 0444 checkpoints/collect-evidence.step10-original.sh
sha256sum checkpoints/collect-evidence.step10-original.sh
sudo docker inspect cybervault-cv05-cv05-1 --format 'Image={{.Image}} Status={{.State.Status}}'
sha256sum compose.yaml apply-firewall.sh
\`\`\`

After the test, from the Ubuntu Docker host VM:

\`\`\`bash
cd /home/lahirubernal/cybervault/cv-05
sudo docker compose down
sudo docker compose create --no-build
sudo bash ./apply-firewall.sh
sudo docker compose start cv05
sudo docker compose ps --all
sudo docker compose port cv05 22
\`\`\`

Verify the helper hash and direct evidence denial from a fresh player session. Reapply the firewall after a reboot before starting the challenge. Do not use \`down -v\`; there are no challenge volumes to remove.
