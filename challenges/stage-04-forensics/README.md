# CV-04 Stage 4: The Employee Evidence

CV-04 is a synthetic, file-based digital forensics challenge. Players correlate workstation and removable-media records, identify the recovery artifact linked to the incident, and decode its incident record.

This folder is the **maintainer package**. Share it with the group leader privately. Do not give the entire folder or ZIP to players because it contains the solution, flag, validation notes, and source files.

## Package contents

- `player/player-brief.md` — participant instructions.
- `player/evidence-package.zip` — the evidence archive to give players.
- `evidence/case-FY-26-104/` — maintainer source evidence used to build the player archive.
- `maintainer/hints.md` — progressive hints for the challenge platform.
- `maintainer/solution.md` — intended solve path and flag; maintainer-only.
- `maintainer/validation.md` — validation record and known limits.
- `source/build_package.py` — reproducibly builds the player evidence archive.
- `source/validate_evidence.py` — checks the correlated records and archive.

## Build and verify the evidence archive

Requires Python 3 and uses only the standard library. Run from this folder:

```bash
python3 source/build_package.py
python3 source/validate_evidence.py
sha256sum player/evidence-package.zip
```

The currently validated player archive SHA-256 is:

```text
51c411c253c404c56b56dd4c70799aa5bdc2483eb5dfbdd50ed28d22b1885b2d
```

Keep the original ZIP unchanged as the reset copy. If it is rebuilt, record and distribute the new hash.

## Tested player workflow with Autopsy 2.24

Give players only `player/player-brief.md` and `player/evidence-package.zip`. They should preserve the original archive, extract it, and work from the extracted `case-FY-26-104/` folder.

The Kali image tested for this challenge has the older Autopsy 2.24 interface. In that version, the extracted folder could not be added directly as a Logical Files data source, so the tested workflow wraps a copy of the extracted case folder in an ext2 filesystem image first. In a Kali terminal, change to the directory containing `case-FY-26-104/`, then create a new image file (use a different filename if `cv04-evidence.dd` already exists):

```bash
test ! -e cv04-evidence.dd || { echo "Image already exists; choose a new filename."; exit 1; }
truncate -s 32M cv04-evidence.dd
mkfs.ext2 -F -L CV04-EVIDENCE cv04-evidence.dd
mkdir -p image-mount
sudo mount -o loop cv04-evidence.dd image-mount
sudo cp -a case-FY-26-104 image-mount/
sync
sudo umount image-mount
```

This copies the extracted case into the new image and leaves the original ZIP and extracted source folder unchanged. In Autopsy 2.24:

1. Create a case and add a host.
2. Choose **Add Image File** and enter the full path to `cv04-evidence.dd`.
3. Select **Partition** and **Symlink**, then continue.
4. Keep the detected ext filesystem, calculate and verify the image hash, and add it.
5. Select the volume and click **Analyze** to browse the evidence files.

After browsing, correlate the relevant workstation and removable-media records, inspect the recovery record, and decode it with an appropriate command-line tool. The flag is accepted by the instructor or challenge website if configured.

## Reset and flag checking

The challenge is stateless. Reset by restoring the trusted `player/evidence-package.zip`, extracting a fresh working copy, and verifying its SHA-256 against the recorded hash. No service or container reset is required.

The expected flag is stored in `maintainer/solution.md`. Keep it out of player-facing content. The group website may validate it if configured; this folder does not implement CTFd or another scoring service.

## Website handoff and access

For player downloads, publish only `player/player-brief.md` and `player/evidence-package.zip`. Configure the expected flag privately in the website and add hints through the platform's hint mechanism if supported. Keep `evidence/`, `maintainer/`, and `source/` restricted to the group and lecturer. The optional extracted evidence copy is not needed on the website.

The evidence is synthetic. Automated checks and the guided Autopsy 2.24 walkthrough passed, but a fresh player test and website flag/scoring integration still need to be completed before claiming those checks are done.
