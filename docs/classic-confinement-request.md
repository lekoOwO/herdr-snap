# Classic confinement request for `herdr`

- **name:** `herdr`
- **description:** Herdr is a terminal-based runtime, workspace manager, and multiplexer for coding agents. It manages PTYs and launches user-selected coding agents and shell commands inside arbitrary development workspaces.
- **snapcraft:** https://github.com/lekoOwO/herdr-snap/blob/main/snap/snapcraft.yaml
- **upstream:** https://github.com/herdrdev/herdr
- **upstream-relation:** Unofficial community packager. I opened an upstream Discussion proposing official Snap packaging, but the upstream project has not yet adopted or endorsed this package. The Snap Store listing clearly identifies this as an unofficial community-maintained package, and I am willing to transfer the snap to upstream if they choose to take ownership.
- **supported-category:** terminal emulators, multiplexers and shells; tools for local, non-root user-driven configuration of/switching to development workspaces/environments; agent/assistant that runs arbitrary user-directed code and needs to reach files and programs that aren’t known at build time.
- **reasoning:** Herdr's core function requires behavior that cannot be enumerated through strict-confinement interfaces at build time:
  1. Herdr owns PTYs and launches arbitrary user-selected commands and coding agents such as Codex, Claude Code, OpenCode, Qwen Code, and other tools installed on the host. The executable set is intentionally open-ended and can include binaries in user-managed toolchains such as `~/.local/bin`, Cargo, mise, nvm, pyenv, or project-local scripts.
  2. Herdr operates on arbitrary user-selected working directories. Development workspaces may be under `$HOME`, hidden configuration/toolchain directories, secondary disks, `/opt`, `/srv`, mounted filesystems, or other paths chosen at runtime.
  3. The child process environment must behave like the user's normal terminal environment. The tools Herdr launches may in turn invoke compilers, package managers, git, containers, language runtimes, build systems, or project scripts that were not known when the snap was built.
  4. Strict confinement plus a fixed set of interfaces cannot express the open-ended combination of executable lookup, arbitrary runtime working directories, PTY ownership, and user-directed child process execution without changing Herdr's core behavior.

The Snap package itself is deliberately thin: it repackages the official upstream Linux release binary and verifies it against the SHA-256 digest published by upstream. CI builds amd64 and arm64 snaps and performs an amd64 integration test that installs the snap, starts a real Herdr headless server, creates a managed workspace/PTY, and confirms that user-level host executables can be resolved and executed from a Herdr-managed pane.

I understand that strict confinement is generally preferred over classic. For Herdr, however, arbitrary user-directed process execution and development-workspace access are core product behavior rather than incidental filesystem access. This matches the documented supported classic-confinement categories for terminal multiplexers/development environments and agents that run arbitrary user-directed code.
