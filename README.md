# herdr-snap

Community packaging for [Herdr](https://herdr.dev) as a classic Snap.

This repository intentionally **repackages the official upstream Linux binaries** instead of rebuilding Herdr from source. The upstream stable version and SHA-256 checksums are pinned in `snap/snapcraft.yaml`.

## Why classic confinement?

Herdr is a terminal runtime: it needs to launch host programs such as shells and coding agents, work in arbitrary project directories, and interact with normal host processes and terminals. Strict confinement is therefore not a good fit for the intended functionality.

A classic snap must be installed with `--classic`, and publication in the public Snap Store requires classic-confinement review.

## Build locally

Prerequisites:

```bash
sudo snap install snapcraft --classic
```

Then:

```bash
git clone https://github.com/lekoOwO/herdr-snap.git
cd herdr-snap
snapcraft --platform amd64
```

For an arm64 package, use `snapcraft --platform arm64`.

Install the locally-built package:

```bash
sudo snap install --dangerous --classic ./herdr_*.snap
herdr --version
```

`--dangerous` only means the sideloaded snap is not signed by a store.

## Test the important host-integration paths

After installation, verify at least:

```bash
herdr --version
herdr
```

Inside Herdr, verify that it can:

- start the normal login shell;
- start `codex`, `claude`, or other host-installed agent CLIs;
- use a project located outside the snap's own data directories;
- create, detach, and reattach a session;
- find the same tools through `PATH` that are available outside the snap.

The final item is a known Snap integration risk. Snapd rewrites `PATH` even for classic snaps to the fixed system path `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games`. If your `codex`, `claude`, `mise`, Cargo, Bun, npm, or other tools live only in a user-specific path, verify this explicitly before relying on the package. This first packaging version intentionally does not source the user's shell startup files automatically.

## Update to a new Herdr stable release

Run:

```bash
scripts/update-upstream.py
git diff -- snap/snapcraft.yaml
```

The script reads `https://herdr.dev/latest.json` and updates:

- the packaged Herdr version;
- the amd64 SHA-256 checksum;
- the arm64 SHA-256 checksum.

Review the diff before committing.

The scheduled `check upstream release` workflow only detects drift. It deliberately does not push commits or publish packages automatically.

## Snap Store publishing

Do not register or publish the `herdr` name until ownership is agreed with upstream.

Once a store package exists, configure a GitHub Actions environment named `snap-store` and add the repository secret:

```text
SNAPCRAFT_STORE_CREDENTIALS
```

Then run the `publish` workflow manually and choose a channel. Start with `edge` until the package has been tested through the store.

## Upstream relationship

Herdr currently does not accept unsolicited implementation pull requests. The intended path is:

1. validate this package independently;
2. open a short GitHub Discussion describing the real enterprise Snap-only use case;
3. ask maintainers whether they want official Snap support and where they want packaging maintained;
4. if upstream adopts the package, transfer ownership rather than keeping a competing unofficial package.

One Herdr-side improvement is still desirable: when `SNAP` is present, Herdr should treat itself as package-manager managed and direct upgrades to `snap refresh herdr` rather than trying to self-update.
