# Proposal: official Snap packaging for Herdr

I use Herdr in a corporate Linux environment where software may only be installed through Snap, so the existing release binaries/Homebrew/Nix/mise options are not usable there.

I built a small proof-of-concept Snap package that repackages Herdr's official Linux release binaries rather than rebuilding Herdr itself:

https://github.com/lekoOwO/herdr-snap

The package currently builds for amd64 and arm64 with classic confinement. CI also installs the amd64 snap and verifies that a real Herdr-managed pane can find and execute user-level tools from `~/.local/bin` using Codex/Claude shims, so the packaging path works for the main use case without requiring the actual agents in CI.

Before taking this further, I'd like to check whether the project would be interested in Snap as an officially supported distribution method.

If so, which ownership model would you prefer?

- packaging in `herdrdev/herdr`, similar to the existing Nix packaging;
- a separate `herdrdev/herdr-snap` repository; or
- an external/community-maintained Snap that simply tracks upstream releases.

There is also one small upstream integration question: a Snap-installed Herdr should ideally treat itself as package-manager-managed so `herdr update` can direct users to `snap refresh herdr` instead of trying to replace the snap-managed binary.

I'm happy to keep maintaining the packaging externally if that is preferred. I have not opened an implementation PR because the contribution guidelines ask contribution proposals and product-direction questions to start as a Discussion.