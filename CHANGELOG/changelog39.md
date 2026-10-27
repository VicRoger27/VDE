# Changelog 39: DRM Master Release & Atomic Connector Unlocking

## Summary
Resolved the Linux DRM KMS display lock error (`connector Virtual-1: Atomic commit failed: Device or resource busy`):
1. **DRM KMS Master Release (`install.sh`)**:
   - Added automatic termination of zombie GNOME Shell, Mutter, and Xwayland processes before taking over the DRM display device.
   - Clears active kernel atomic locks on `/dev/dri/card0` and virtual connectors (`Virtual-1`), allowing Labwc to seize direct hardware mode cleanly from any TTY context.
