# Changelog 36: Wayland XDG_RUNTIME_DIR Auto-Provisioning & Privilege Drop

## Summary
Resolved the `XDG_RUNTIME_DIR is unset` compositor exit:
1. **XDG_RUNTIME_DIR Auto-Provisioning (`/usr/local/bin/vde`)**:
   - Added automatic fallback to `/run/user/$(id -u)` with `0700` permissions whenever `XDG_RUNTIME_DIR` is missing or stripped by `sudo`.
2. **Safe Sudo Hand-off (`install.sh`)**:
   - When the installer executes `vde` at the end of a `sudo bash` session, it drops privileges to the target invoking user (`$SUDO_USER`) with their active runtime socket dir, preventing root compositor permission rejections.
