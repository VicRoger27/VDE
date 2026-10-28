# Changelog 54: QEMU Hard Disk Persistent Boot Option Integration

**Date:** 2026-10-28
**Commit Tag:** `[changelog54]`
**Repository:** `i2qq/VDE`

### Summary of Changes:
1. **QEMU Boot Target Ergonomics**:
   - Updated `Launch_VDE_QEMU.bat` to offer Option `[1]` direct boot from installed virtual hard disk (`vde-disk.qcow2`) via `-boot c`.
   - Prevents booting into ephemeral read-only ISO RAM environments that trigger the frozen GDM installer loop on every launch.
