/**
 * VDE Dynamic Start Button Widget
 * Windows 11 Fluent 4-tile emblem with local AI neural status indicator
 */

import { Gtk } from "astal/gtk4";
import { bind, Variable } from "astal";
import GLib from "gi://GLib";
import dbusService, { AIInferenceState } from "../services/dbus";

interface StartButtonProps {
    assetsDir: string;
}

export default function StartButton({ assetsDir }: StartButtonProps) {
    // Determine icon path based on D-Bus inference state
    const iconPath = bind(dbusService.inferenceStatus).as(status => {
        switch (status.state) {
            case "active":
                return `${assetsDir}/icons/start-active-dark.svg`;
            case "offline":
                return `${assetsDir}/icons/start-offline-dark.svg`;
            case "idle":
            default:
                return `${assetsDir}/icons/start-idle-dark.svg`;
        }
    });

    const tooltipText = bind(dbusService.inferenceStatus).as(status => {
        if (status.state === "active") {
            return `Start (VDE AI: Active Inference - ${status.model})`;
        } else if (status.state === "offline") {
            return `Start (VDE AI: Offline)`;
        }
        return `Start (${status.model})`;
    });

    const isInferring = bind(dbusService.inferenceStatus).as(
        s => s.state === "active"
    );

    return (
        <button
            className={bind(isInferring).as(active =>
                active ? "vde-start-button active-inference" : "vde-start-button"
            )}
            tooltipText={tooltipText}
            onClicked={() => {
                dbusService.toggleLauncher();
            }}
        >
            <box className="start-icon-wrapper" halign={Gtk.Align.CENTER} valign={Gtk.Align.CENTER}>
                <image
                    file={iconPath}
                    pixelSize={24}
                />
            </box>
        </button>
    );
}
