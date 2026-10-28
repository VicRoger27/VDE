# Changelog 53: Pre-Flight GDM & Display-Manager Masking in Web Installer

**Date:** 2026-10-28
**Commit Tag:** `[changelog53]`
**Repository:** `i2qq/VDE`

### Summary of Changes:
1. **Pre-Flight Display Manager Masking**:
   - Integrated immediate pre-flight stopping, killing, and masking of `gdm`, `gdm3`, and `display-manager` into Step 1 of `install.sh`.
   - Automatically sets default target to `multi-user.target` at the start of installation, freeing DRM hardware master and preventing console lockouts before dependencies are configured.
