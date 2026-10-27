# VDE Asset Directory

This directory holds all icon assets, vector glyphs, and surface textures required by the VDE desktop shell.

## Strict Asset Generation Protocol
- **Zero Autonomous Inline Artwork:** The agent does not autonomously create SVGs or raw raster images.
- All visual elements must be declared in [asset_manifest.json](./asset_manifest.json).
- External artists / local pipeline (GLM 5.3 for vector SVGs, Flux 1 schnell / Flux 2 klein via Unsloth for textures) render the files into `assets/icons/` and `assets/textures/`.
- The shell UI layouts use placeholder bounding boxes (`placeholder_spec` in the manifest) until rendered assets are provided.
