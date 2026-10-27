# Changelog 33: CDN Cache-Busting & Live Propagation Hardening

## Summary
Addressed GitHub and edge CDN caching latency for live tarball extraction:
1. **Timestamped CDN Cache Invalidation (`install.sh`)**:
   - Added a dynamic timestamp cache-buster query parameter (`?v=$(date +%s)`) to the release archive URL.
   - Prevents stale edge-node caching on GitHub's Fastly CDN, guaranteeing that live installs pull the exact newest commit instantly with zero seconds of cache lag.
