/**
 * VDE Centered Taskbar Items Widget
 * Pinned app launchers and active running indicators
 */

import { Gtk } from "astal/gtk4";
import { execAsync, bind, Variable } from "astal";
import dbusService from "../services/dbus";

interface TaskItemsProps {
    assetsDir: string;
}

interface PinnedApp {
    id: string;
    title: string;
    icon: string;
    command: string[];
    isRunning?: Variable<boolean>;
    isFocused?: Variable<boolean>;
}

export default function TaskItems({ assetsDir }: TaskItemsProps) {
    // Pinned applications mimicking Windows 11 taskbar defaults
    const pinnedApps: PinnedApp[] = [
        {
            id: "search",
            title: "Search (Start Menu)",
            icon: `${assetsDir}/icons/search-dark.svg`,
            command: [],
            isRunning: Variable(false),
            isFocused: Variable(false)
        },
        {
            id: "files",
            title: "File Explorer",
            icon: `${assetsDir}/icons/app-files-dark.svg`,
            command: ["xdg-open", GLib_get_home_dir()],
            isRunning: Variable(true),
            isFocused: Variable(false)
        },
        {
            id: "browser",
            title: "Web Browser",
            icon: `${assetsDir}/icons/app-browser-dark.svg`,
            command: ["x-www-browser"],
            isRunning: Variable(false),
            isFocused: Variable(false)
        },
        {
            id: "editor",
            title: "Text Editor",
            icon: `${assetsDir}/icons/app-editor-dark.svg`,
            command: ["gedit"],
            isRunning: Variable(false),
            isFocused: Variable(false)
        },
        {
            id: "terminal",
            title: "Terminal",
            icon: `${assetsDir}/icons/settings-dark.svg`, // settings or terminal
            command: ["foot"],
            isRunning: Variable(true),
            isFocused: Variable(true)
        }
    ];

    function launchApp(app: PinnedApp) {
        if (app.id === "search") {
            dbusService.toggleLauncher();
            return;
        }
        if (app.command.length > 0) {
            execAsync(app.command).catch(err => {
                console.warn(`[VDE Taskbar] Failed to launch ${app.title}:`, err);
            });
        }
    }

    return (
        <box className="vde-task-items" spacing={4} halign={Gtk.Align.CENTER}>
            {pinnedApps.map(app => (
                <button
                    className="vde-task-button"
                    tooltipText={app.title}
                    onClicked={() => launchApp(app)}
                >
                    <box orientation={Gtk.Orientation.VERTICAL} halign={Gtk.Align.CENTER} valign={Gtk.Align.CENTER}>
                        <image
                            className="task-icon"
                            file={app.icon}
                            pixelSize={24}
                        />
                        {/* Windows 11 Active Window Indicator (Running dot or focused line) */}
                        <box
                            className={bind(app.isFocused!).as(focused =>
                                focused
                                    ? "indicator-line focused"
                                    : app.isRunning!.get()
                                    ? "indicator-line running"
                                    : "indicator-line idle"
                            )}
                        />
                    </box>
                </button>
            ))}
        </box>
    );
}

function GLib_get_home_dir(): string {
    return "/home";
}
