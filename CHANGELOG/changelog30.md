# Changelog 30: SHA-256 Integrity Verification & Interactive OS Reboot Prompt

## Summary
Integrated cryptographic payload validation and modern OS installer restart flow into `install.sh`:
1. **SHA-256 Checksum Integrity Verification**:
   - The installer stages downloaded release tarballs to a temporary archive and executes `sha256sum` verification, printing the verified SHA-256 hash before extraction.
2. **Interactive Reboot Prompt**:
   - Following installation and cleanup, queries the user via `/dev/tty`:
     `Would you like to restart the computer now? [Y/n]: `
   - Defaulting to restart (on Enter or 'Y'), performing a clean reboot to wipe active memory and boot directly into VDE.
   - Non-interactive and script runners cleanly fall back to status instructions.
3. **Universal TTY1 Direct Boot Configuration**:
   - Configures automatic getty login and wayland session initiation on TTY1 for clean hardware boots.
