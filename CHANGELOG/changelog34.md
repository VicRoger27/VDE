# Changelog 34: Smart Live RAM Session Hand-Off vs Installed System Reboot Flow

## Summary
Prevented accidental virtual disk boot failures when running in ephemeral Live RAM ("Try Ubuntu") sessions:
1. **Live Session Awareness (`install.sh`)**:
   - Differentiated between live RAM overlay environments (`IS_LIVE_SESSION=true`) and persistent hard drive installations.
   - For live environments, warns the user that restarting will unmount the ISO and clear RAM, and instead automatically prompts to launch VDE directly onto the screen (`exec /usr/local/bin/vde`).
   - For installed systems on virtual or physical hard disks, preserves the interactive OS reboot prompt.
2. **Eliminated "No bootable medium found" Trap**:
   - Prevents VirtualBox from auto-ejecting the live ISO and failing to boot an empty virtual hard drive.
