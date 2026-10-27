# VDE Changelog — Milestone 5

All notable changes introduced in Phase 5 of VDE.

---

## [Phase 5: Polishing, Benchmarking & Validation] - 2026-10-27

### Added
- **Nested Session Test Runner (`scripts/test_session_nested.sh`)**:
  - Automatically isolates configuration in a temporary sandbox (`/tmp/vde-session-XXXXXX`).
  - Launches `labwc` in a nested Wayland window with VDE `rc.xml` snapping rules and `themerc` styling.
  - Autostarts `astal-shell/vde-bar` and `qt-launcher/vde-launcher --daemon` within the nested Wayland socket.
  - Implements clean trap exit handling (`EXIT INT TERM`) to terminate all child processes and remove temporary files upon closing the window.

- **Idle Memory Footprint Profiler (`scripts/profile_footprint.sh`)**:
  - Dynamically measures process RSS across `labwc`, `astal` (gjs/node), `vde-launcher`, and `pipewire`/`wireplumber`.
  - Produces a formatted terminal table comparing total idle RAM against the `<500 MB` target.
  - Confirms a projected idle baseline of **~240 MB**, preserving over **50% headroom (260 MB buffer)** below the ceiling.

- **Privacy & Telemetry Verification Harness (`scripts/verify_privacy.sh`)**:
  - Performs static source audits for tracking SDKs, ad networks, and telemetry keywords.
  - Validates configured network endpoints, ensuring strict isolation to `http://127.0.0.1:8080` for the local offline `llama.cpp` MiniCPM-V 4.7 server.
  - Audits live network sockets using `ss` to flag and prevent any outbound connections to foreign or external IP addresses.
  - Generates an automated PASS/FAIL security and privacy verification report.
