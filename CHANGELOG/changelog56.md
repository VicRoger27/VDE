# Changelog 56 - Elimination of Blocking Installer Prompts & Clean VDE Handoff

### Highlights & Modifications
1. **Removed Interactive Read & TTY Blocking in `install.sh`**:
   - Web-piped scripts (`wget -qO- ... | sudo bash`) experience terminal buffering and hangs when executing `read </dev/tty`.
   - Removed blocking `read` prompt and virtual console switching (`chvt 1`) from the end of `install.sh`.
   - The installer now outputs a clean completion banner and exits cleanly with code `0`.

2. **Clean Session Launch Instructions**:
   - Instructs users to launch VDE directly on their active terminal via `vde` or restart directly with `sudo reboot`.
   - Automatically releases any lingering DRM KMS handles from GDM or Gnome-shell when starting.

3. **Updated Verification Test**:
   - Updated `tests/verify_vde_stack.py` to assert `vde-session` presence instead of deprecated `chvt 1`.
   - All verification suites pass with 100% health.
