/**
 * VDE Quick Settings Trigger Pill (Taskbar)
 * Windows 11 grouped indicator for WiFi, Volume, and Battery
 */

import { Gtk } from "astal/gtk4";
import { bind, Variable } from "astal";
import dbusService from "../services/dbus";

interface QuickSettingsPillProps {
    assetsDir: string;
}

export default function QuickSettingsPill({ assetsDir }: QuickSettingsPillProps) {
    // Reactive icon paths
    const wifiIcon = `${assetsDir}/icons/wifi-dark.svg`;
    const volumeIcon = `${assetsDir}/icons/volume-dark.svg`;
    const batteryIcon = `${assetsDir}/icons/battery-dark.svg`;

    return (
        <button
            className="vde-quicksettings-pill"
            tooltipText="Quick Settings (Network, Sound, Battery)"
            onClicked={() => {
                dbusService.toggleQuickSettings();
            }}
        >
            <box spacing={6} halign={Gtk.Align.CENTER} valign={Gtk.Align.CENTER}>
                <image file={wifiIcon} pixelSize={18} />
                <image file={volumeIcon} pixelSize={18} />
                <image file={batteryIcon} pixelSize={18} />
            </box>
        </button>
    );
}
