# Changelog 52: GDM Display Manager Hang Elimination & DRM KMS Release

**Date:** 2026-10-28
**Commit Tag:** `[changelog52]`
**Repository:** `i2qq/VDE`

### Summary of Changes:
1. **GDM Hang Resolution**:
   - Identified that GDM (GNOME Display Manager) was freezing on boot while attempting to start `ubuntu-desktop-bootstrap`, blocking TTY1/TTY2 and locking DRM hardware master sockets.
   - Updated `compositor/vde` and `compositor/vde-session` to proactively stop `gdm`, `gdm3`, and `display-manager` prior to launching Labwc.
2. **Permanent Masking in Installer**:
   - Updated `install.sh` to permanently mask `display-manager`, `gdm`, `gdm3`, `lightdm`, and `sddm` systemd units and set default target to `multi-user.target`.
