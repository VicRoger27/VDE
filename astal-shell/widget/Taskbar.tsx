/**
 * VDE Main Taskbar Window
 * Windows 11 Centered Floating Dock on Wayland Layer-Shell
 */

import { Astal, Gtk } from "astal/gtk4";
import { execAsync } from "astal";
import StartButton from "./StartButton";
import TaskItems from "./TaskItems";
import QuickSettingsPill from "./QuickSettingsPill";
import Clock from "./Clock";

interface TaskbarProps {
    gdkmonitor: any;
    assetsDir: string;
}

export default function Taskbar({ gdkmonitor, assetsDir }: TaskbarProps) {
    return (
        <window
            name="vde-bar"
            className="vde-taskbar-window"
            gdkmonitor={gdkmonitor}
            exclusivity={Astal.Exclusivity.EXCLUSIVE}
            anchor={
                Astal.WindowAnchor.BOTTOM |
                Astal.WindowAnchor.LEFT |
                Astal.WindowAnchor.RIGHT
            }
            marginBottom={6}
            marginStart={12}
            marginEnd={12}
            layer={Astal.Layer.TOP}
        >
            <centerbox className="vde-taskbar-container">
                {/* Left Side: Widgets / Spacing */}
                <box className="taskbar-left-zone" halign={Gtk.Align.START} spacing={8}>
                    {/* Subtle placeholder for local desktop / workspace indicator */}
                    <button
                        className="vde-workspace-pill"
                        tooltipText="Task View (Win+Tab)"
                        onClicked={() => {
                            execAsync(["wlr-randr"]).catch(() => {});
                        }}
                    >
                        <image file={`${assetsDir}/icons/all-apps-dark.svg`} pixelSize={18} />
                    </button>
                </box>

                {/* Center Side: Windows 11 Centered Launchers */}
                <box className="taskbar-center-dock" halign={Gtk.Align.CENTER} spacing={6}>
                    <StartButton assetsDir={assetsDir} />
                    <TaskItems assetsDir={assetsDir} />
                </box>

                {/* Right Side: Tray, Quick Settings Pill, Clock, and Show Desktop */}
                <box className="taskbar-right-zone" halign={Gtk.Align.END} spacing={8}>
                    <QuickSettingsPill assetsDir={assetsDir} />
                    <Clock />
                    {/* Windows 11 "Show Desktop" thin strip at extreme right */}
                    <button
                        className="show-desktop-strip"
                        tooltipText="Show Desktop"
                        onClicked={() => {
                            execAsync(["wlrctl", "toplevel", "minimize"]).catch(() => {});
                        }}
                    />
                </box>
            </centerbox>
        </window>
    );
}
