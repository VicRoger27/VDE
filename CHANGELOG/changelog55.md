# Changelog 55: Clean VirtualBox Standardization & QEMU Deprecation

**Date:** 2026-10-28
**Commit Tag:** `[changelog55]`
**Repository:** `i2qq/VDE`

### Summary of Changes:
1. **Clean Deprecation of Legacy VM Runners**:
   - Removed obsolete `Launch_VDE_QEMU.bat`, `Launch_VDE_VM.bat`, and `tools/qemu` harness to streamline repository footprint.
   - Standardized on pure direct web installer workflow: `wget -qO- https://vde.vopple.uk/install.sh | sudo bash`.
2. **Permanent GDM Purge in VirtualBox**:
   - Confirmed immediate pre-flight GDM/GNOME neutralization in `install.sh` to prevent VirtualBox VMSVGA display hangs.
