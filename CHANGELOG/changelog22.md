# Changelog 22: Automatic dpkg Lock Management & Zero-Git Direct Extraction

## Summary
Resolved two critical failure modes observed during live session installation:
1. Eliminated the `Could not get lock /var/lib/dpkg/lock-frontend` error caused by Ubuntu's background software updater (`apt.systemd.daily` / `unattended-upgrades`).
2. Removed the `git` package dependency by streaming and extracting repository sources directly via native `wget` and `tar`.

## Key Changes
1. **Dpkg Lock Detection & Resolution (`install.sh`)**:
   - Added `wait_for_dpkg_lock`: Checks if `/var/lib/dpkg/lock-frontend`, `/var/lib/dpkg/lock`, or `/var/lib/apt/lists/lock` are in use.
   - Automatically stops background update timers (`apt-daily.timer`, `unattended-upgrades.service`).
   - Added `apt_run` wrapper: Retries package manager operations with automatic backoff if locks are held.

2. **Direct Tarball Streaming**:
   - Switched from requiring `git clone` (which triggered an `apt-get install git` lock conflict) to streaming the GitHub repository tarball directly via `wget -qO- ... | tar -xz`.
   - Executes in sub-second time without querying apt repositories.
