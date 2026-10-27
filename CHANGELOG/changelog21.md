# Changelog 21: Full Canonical Telemetry & GNOME Purge Engine

## Summary
Updated `install.sh` so that running the one-command installer automatically strips out GNOME Shell, GDM, Canonical Snap daemon (`snapd`), and all background telemetry tracking packages by default, replacing them completely with the lightweight VDE stack.

## Exact Purge Targets
1. **Canonical Snaps**:
   - Stops and purges `snapd`, clearing `/var/lib/snapd`, `/snap`, and user snap caches.
2. **Canonical Telemetry & Metrics**:
   - Purges `whoopsie` (error submission daemon).
   - Purges `ubuntu-report` (hardware telemetry collection).
   - Purges `popularity-contest` (software usage survey).
   - Purges `apport` and `apport-symptoms` (automated crash reporting).
   - Purges `landscape-common` (remote management agent).
3. **GNOME Desktop Bloat**:
   - Stops GDM and kills running `gnome-shell` instances.
   - Purges `gnome-shell`, `gnome-session`, `gdm3`, `ubuntu-desktop`, `ubuntu-desktop-minimal`, `gnome-initial-setup`, and `mutter`.
   - Runs `apt-get autoremove -y --purge` to strip orphaned libraries.
4. **Instant RAM Recovery**:
   - Frees >1 GB of RAM immediately, bringing system idle usage down to VDE's <500 MB footprint target.
