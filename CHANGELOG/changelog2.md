# VDE Changelog — Milestone 2

All notable changes introduced in Phase 4 of the Victor Desktop Environment (VDE).

---

## [Phase 4: Qt6 Start Menu & Search Runner] - 2026-10-27

### Added
- **In-Process C++ Fast Application Indexer (`src/AppIndexer.h`, `src/AppIndexer.cpp`)**:
  - Direct in-memory parsing of standard XDG `.desktop` files across `/usr/share/applications`, `/usr/local/share/applications`, and `~/.local/share/applications`.
  - Directory change tracking via `QFileSystemWatcher` without persistent background disk polling.
  - Multi-tiered fuzzy search scoring (Exact Match > Prefix > Keyword > Executable > Comment) with sub-10ms response latency.
  - Automatic argument sanitization (stripping `%f`, `%u`, `%F`, `%U`).

- **On-Demand Multi-Threaded File Searcher (`src/FileSearcher.h`, `src/FileSearcher.cpp`)**:
  - Non-blocking asynchronous file crawler running on `QtConcurrent` thread pool.
  - Searches user directories (`~/Documents`, `~/Downloads`, `~/Pictures`, `~/Desktop`) dynamically on user query.
  - Completely eliminates persistent SQLite indexing daemons and background disk churn.

- **Local Multimodal AI Vision Client (`src/LocalAiClient.h`, `src/LocalAiClient.cpp`)**:
  - Native HTTP client targeting local `llama.cpp` server (default `http://127.0.0.1:8080/v1/chat/completions`).
  - Dedicated support for MiniCPM-V 4.7 (1B Dense GGUF) with strictly zero Ollama dependency.
  - Emits real-time `inferenceStateChanged(state, model)` signals (`active` during query, `idle` when ready, `offline` on failure) to drive the dynamic Start button indicator in the Astal taskbar.
  - Surfaces local matching image thumbnails directly inside the search view.

- **D-Bus Session Service (`src/LauncherAdaptor.h`, `src/LauncherManager.h`)**:
  - Registers `org.vde.Launcher` on the D-Bus session bus.
  - Exposes slots: `Toggle()`, `Show()`, `Hide()`, `Query(QString)`.
  - Bridges D-Bus method invocations from Astal shell and Labwc keybindings (`Super` / `Super+Space`).

- **QML Windows 11 Fluent Start Menu UI (`qml/`)**:
  - **`Main.qml`**: Translucent frameless Start Menu drawer (`580x650px`) with hardware-accelerated frosted acrylic surface and auto-focused search box.
  - **`AcrylicSurface.qml`**: Dark Mica/Acrylic rounded surface (`16px` radius) with sub-pixel borders (`border_strong`).
  - **`PinnedGrid.qml`**: Windows 11 6x3 pinned grid (18 slots) with smooth hover scaling and click-to-launch actions.
  - **`AllAppsList.qml`**: Alphabetical vertical drawer with smooth scrolling and app categories.
  - **`SearchResultsView.qml`**: Unified zero-telemetry search view combining Top Match, Apps, Local Documents, and Local AI Vision thumbnails.
  - **Minimalist Footer**: Clean user profile avatar and Power Action flyout (Sleep, Restart, Shutdown) stripped of all debug banners and telemetry feeds.

- **Build & Executable Runner**:
  - CMake build specification (`CMakeLists.txt`) linking Qt6 Quick, DBus, Network, and Concurrent.
  - Standalone wrapper script `vde-launcher` supporting background `--daemon` mode.
