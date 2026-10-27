/**
 * VDE Shell Entrypoint (Astal GTK4 Shell Daemon)
 */

import { App } from "astal/gtk4";
import GLib from "gi://GLib";
import Taskbar from "./widget/Taskbar";
import QuickSettings from "./widget/QuickSettings";

function resolveAssetsDir(): string {
    const currentDir = GLib.get_current_dir();
    const candidatePaths = [
        `${currentDir}/../assets`,
        `${currentDir}/assets`,
        "/usr/local/share/vde/assets",
        "/usr/share/vde/assets"
    ];

    for (const p of candidatePaths) {
        if (GLib.file_test(p, GLib.FileTest.IS_DIR)) {
            return p;
        }
    }
    return `${currentDir}/../assets`;
}

App.start({
    instanceName: "vde-shell",
    css: "./style.css",
    main() {
        const assetsDir = resolveAssetsDir();
        console.log(`[VDE Shell] Initialized with assets dir: ${assetsDir}`);

        // Launch taskbar on each connected monitor
        App.get_monitors().map(monitor => (
            Taskbar({ gdkmonitor: monitor, assetsDir })
        ));

        // Launch Quick Settings flyout
        QuickSettings({ assetsDir });
    }
});
