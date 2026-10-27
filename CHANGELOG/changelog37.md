# Changelog 37: GTK Style Cleaning & PipeWire Duplicate Guard

## Summary
Resolved runtime warnings logged during Pixman software fallback execution:
1. **GTK CSS Property Cleanup (`waybar_style.css`)**:
   - Removed the unsupported `line-height` property from the clock widget to achieve zero-warning CSS parsing under GTK 3/4.
2. **Audio Daemon Singleton Guard (`compositor/autostart`)**:
   - Added process existence checks (`pgrep -x pipewire`, `pgrep -x wireplumber`) prior to spawning audio services, eliminating protocol lock collision errors when executed within an active session.
