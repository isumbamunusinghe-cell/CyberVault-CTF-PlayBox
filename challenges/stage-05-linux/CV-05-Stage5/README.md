# CyberVault CV-05 — Stage 5

CV-05 is a Linux privilege-escalation challenge. The player connects to an Ubuntu-based challenge container over SSH as the low-privilege `player` account, investigates its permitted maintenance command and file permissions, and recovers the incident evidence.

This is a **maintainer handoff**. It contains the challenge source and maintainer material. Share it with the group leader privately for integration and deployment; do not upload this complete folder or ZIP as a player download.

## Package contents

- `compose.yaml` — runs the CV-05 container and publishes SSH on the lab host's `192.168.60.50:2222` address.
- `Dockerfile` and `container/` — build context, SSH setup, player account, maintenance scripts, and protected evidence.
- `apply-firewall.sh` — applies the tested IPv4 and IPv6 host firewall rules for the isolated VirtualBox lab.
- `docs/player-brief.md` — participant instructions. Replace lab-specific connection details and credentials before issuing it for another run.
- `docs/hints.md` — progressive maintainer hints for the challenge platform.
- `docs/solution.md` — maintainer-only intended solution and flag. Never provide this to players.
- `docs/validation.md` — recorded test results, reset steps, and known limitations.

The ZIP also has a top-level `cv-05/` directory. Open that directory before running Docker commands.

## Tested lab layout

The tested setup used an Ubuntu Server VM as the Docker host and a Kali VM as the participant machine:

- Ubuntu host-only IP: `192.168.60.50`
- Kali host-only IP: `192.168.60.100`
- SSH endpoint: `192.168.60.50:2222` forwarded to container port 22
- Docker bridge: `br-cv05`, subnet `172.30.50.0/24`
- Container address: `172.30.50.10`

The Compose file and firewall script are specific to this lab layout. The Ubuntu host must have the expected host-only address and network interface (`enp0s3` in the tested setup). Do not expose this intentionally vulnerable challenge to the public Internet or a production network.

## Build and start on the tested Ubuntu VM

Install Docker Engine and the Docker Compose plugin on the Ubuntu host, copy the complete `cv-05/` directory to `/home/lahirubernal/cybervault/cv-05`, and confirm the host-only network configuration. From the project directory:

```bash
cd /home/lahirubernal/cybervault/cv-05
sudo docker build -t cybervault-cv05:dev .
sudo docker compose create cv05
sudo bash ./apply-firewall.sh
sudo docker compose start cv05
sudo docker compose ps --all
sudo docker compose port cv05 22
```

The final command should report `192.168.60.50:2222`. The firewall script requires the container to exist and be stopped. It limits access to the configured Kali host-only address. Firewall rules are runtime state and must be reapplied after an Ubuntu reboot before starting the container.

## Reset after a player run

Recreate the container from the built image, reapply the firewall, and start it:

```bash
cd /home/lahirubernal/cybervault/cv-05
sudo docker compose down
sudo docker compose create --no-build cv05
sudo bash ./apply-firewall.sh
sudo docker compose start cv05
sudo docker compose ps --all
sudo docker compose port cv05 22
```

Then follow `docs/validation.md` to confirm a fresh player login, the original helper checksum, and denied direct access to the evidence. Do not use `docker compose down -v`.

Container recreation creates new SSH host keys. Verify the new host-key fingerprint with the challenge administrator and update the player's `known_hosts` entry before reconnecting.

## Player and maintainer files

For participant downloads, provide only `docs/player-brief.md` after replacing the lab-specific endpoint and development credential with the values issued for that run. Configure the flag privately in the challenge platform. Add hints through the platform's hint mechanism if supported.

Keep `docs/solution.md`, `docs/validation.md`, the Docker source, and the evidence source restricted to maintainers. The Docker source and evidence necessarily contain the challenge implementation and flag, so never publish this maintainer ZIP as a public download.

## Platform integration and current limits

This package runs CV-05 as a standalone Docker Compose challenge. It does not itself integrate with CTFd or provide per-player containers, automatic scoring, or multi-player isolation. A CTF website can manage the challenge description, flag submission, scoring, and hints, but the vulnerable SSH container still needs to be deployed and networked by a separate container host/orchestration service. Configure and test that integration before advertising CV-05 as available on the website.

The tested environment and remaining verification limits are recorded in `docs/validation.md`. In particular, do not claim tests beyond those recorded there.
