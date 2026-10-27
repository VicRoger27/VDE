/**
 * VDE Quick Settings Flyout Widget
 * Windows 11 Action Center with Network, Audio, Display, and Power Controls
 */

import { Astal, Gtk } from "astal/gtk4";
import { bind, Variable, execAsync } from "astal";
import dbusService from "../services/dbus";

interface QuickSettingsProps {
    assetsDir: string;
}

export default function QuickSettings({ assetsDir }: QuickSettingsProps) {
    // Reactive toggle states
    const wifiActive = Variable(true);
    const bluetoothActive = Variable(false);
    const airplaneActive = Variable(false);
    const isDarkMode = Variable(true);

    const volumeLevel = Variable(0.65);
    const isMuted = Variable(false);
    const brightnessLevel = Variable(0.80);
    const batteryPercent = Variable(85);

    function toggleWifi() {
        wifiActive.set(!wifiActive.get());
        execAsync(["nmcli", "radio", "wifi", wifiActive.get() ? "on" : "off"]).catch(() => {});
    }

    function toggleBluetooth() {
        bluetoothActive.set(!bluetoothActive.get());
        execAsync(["bluetoothctl", "power", bluetoothActive.get() ? "on" : "off"]).catch(() => {});
    }

    function toggleAirplane() {
        airplaneActive.set(!airplaneActive.get());
        execAsync(["rfkill", airplaneActive.get() ? "block" : "unblock", "all"]).catch(() => {});
    }

    function toggleTheme() {
        isDarkMode.set(!isDarkMode.get());
    }

    function setVolume(val: number) {
        volumeLevel.set(val);
        const pct = Math.round(val * 100);
        execAsync(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", `${pct}%`]).catch(() => {
            execAsync(["amixer", "sset", "Master", `${pct}%`]).catch(() => {});
        });
    }

    function toggleMute() {
        isMuted.set(!isMuted.get());
        execAsync(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", isMuted.get() ? "1" : "0"]).catch(() => {});
    }

    function setBrightness(val: number) {
        brightnessLevel.set(val);
        const pct = Math.round(val * 100);
        execAsync(["brightnessctl", "set", `${pct}%`]).catch(() => {});
    }

    // Power actions
    function powerAction(action: "sleep" | "restart" | "shutdown") {
        dbusService.toggleQuickSettings();
        if (action === "sleep") {
            execAsync(["systemctl", "suspend"]).catch(() => {});
        } else if (action === "restart") {
            execAsync(["systemctl", "reboot"]).catch(() => {});
        } else if (action === "shutdown") {
            execAsync(["systemctl", "poweroff"]).catch(() => {});
        }
    }

    return (
        <window
            name="vde-quicksettings"
            className="vde-flyout-window"
            anchor={Astal.WindowAnchor.BOTTOM | Astal.WindowAnchor.RIGHT}
            marginEnd={12}
            marginBottom={56}
            visible={bind(dbusService.quickSettingsVisible)}
        >
            <box className="quicksettings-card" orientation={Gtk.Orientation.VERTICAL} spacing={14}>
                {/* 1. Quick Action Toggle Grid (2x2) */}
                <box orientation={Gtk.Orientation.VERTICAL} spacing={8}>
                    <box spacing={8} homogeneous>
                        {/* WiFi Toggle */}
                        <button
                            className={bind(wifiActive).as(on =>
                                on ? "toggle-tile active" : "toggle-tile"
                            )}
                            onClicked={toggleWifi}
                        >
                            <box spacing={10} halign={Gtk.Align.START} valign={Gtk.Align.CENTER}>
                                <image
                                    file={bind(wifiActive).as(on =>
                                        on
                                            ? `${assetsDir}/icons/wifi-dark.svg`
                                            : `${assetsDir}/icons/wifi-off-dark.svg`
                                    )}
                                    pixelSize={20}
                                />
                                <box orientation={Gtk.Orientation.VERTICAL}>
                                    <label className="toggle-label" label="Wi-Fi" halign={Gtk.Align.START} />
                                    <label
                                        className="toggle-status"
                                        label={bind(wifiActive).as(on => (on ? "Connected" : "Off"))}
                                        halign={Gtk.Align.START}
                                    />
                                </box>
                            </box>
                        </button>

                        {/* Bluetooth Toggle */}
                        <button
                            className={bind(bluetoothActive).as(on =>
                                on ? "toggle-tile active" : "toggle-tile"
                            )}
                            onClicked={toggleBluetooth}
                        >
                            <box spacing={10} halign={Gtk.Align.START} valign={Gtk.Align.CENTER}>
                                <image
                                    file={bind(bluetoothActive).as(on =>
                                        on
                                            ? `${assetsDir}/icons/bluetooth-dark.svg`
                                            : `${assetsDir}/icons/bluetooth-off-dark.svg`
                                    )}
                                    pixelSize={20}
                                />
                                <box orientation={Gtk.Orientation.VERTICAL}>
                                    <label className="toggle-label" label="Bluetooth" halign={Gtk.Align.START} />
                                    <label
                                        className="toggle-status"
                                        label={bind(bluetoothActive).as(on => (on ? "On" : "Off"))}
                                        halign={Gtk.Align.START}
                                    />
                                </box>
                            </box>
                        </button>
                    </box>

                    <box spacing={8} homogeneous>
                        {/* Theme Switch Toggle */}
                        <button
                            className="toggle-tile active"
                            onClicked={toggleTheme}
                        >
                            <box spacing={10} halign={Gtk.Align.START} valign={Gtk.Align.CENTER}>
                                <image file={`${assetsDir}/icons/theme-switch-dark.svg`} pixelSize={20} />
                                <box orientation={Gtk.Orientation.VERTICAL}>
                                    <label className="toggle-label" label="Theme" halign={Gtk.Align.START} />
                                    <label
                                        className="toggle-status"
                                        label={bind(isDarkMode).as(d => (d ? "Dark Mode" : "Light Mode"))}
                                        halign={Gtk.Align.START}
                                    />
                                </box>
                            </box>
                        </button>

                        {/* Flight Mode Toggle */}
                        <button
                            className={bind(airplaneActive).as(on =>
                                on ? "toggle-tile active" : "toggle-tile"
                            )}
                            onClicked={toggleAirplane}
                        >
                            <box spacing={10} halign={Gtk.Align.START} valign={Gtk.Align.CENTER}>
                                <image
                                    file={bind(airplaneActive).as(on =>
                                        on
                                            ? `${assetsDir}/icons/airplane-dark.svg`
                                            : `${assetsDir}/icons/airplane-off-dark.svg`
                                    )}
                                    pixelSize={20}
                                />
                                <box orientation={Gtk.Orientation.VERTICAL}>
                                    <label className="toggle-label" label="Airplane" halign={Gtk.Align.START} />
                                    <label
                                        className="toggle-status"
                                        label={bind(airplaneActive).as(on => (on ? "Active" : "Off"))}
                                        halign={Gtk.Align.START}
                                    />
                                </box>
                            </box>
                        </button>
                    </box>
                </box>

                {/* 2. Sliders (Volume & Brightness) */}
                <box orientation={Gtk.Orientation.VERTICAL} spacing={10}>
                    {/* Volume Slider */}
                    <box spacing={10} valign={Gtk.Align.CENTER}>
                        <button className="slider-icon-btn" onClicked={toggleMute}>
                            <image
                                file={bind(isMuted).as(m =>
                                    m
                                        ? `${assetsDir}/icons/mute-dark.svg`
                                        : `${assetsDir}/icons/volume-dark.svg`
                                )}
                                pixelSize={20}
                            />
                        </button>
                        <slider
                            className="fluent-slider"
                            hexpand
                            value={volumeLevel()}
                            onChangeValue={self => setVolume(self.value)}
                        />
                    </box>

                    {/* Brightness Slider */}
                    <box spacing={10} valign={Gtk.Align.CENTER}>
                        <image file={`${assetsDir}/icons/settings-dark.svg`} pixelSize={20} />
                        <slider
                            className="fluent-slider"
                            hexpand
                            value={brightnessLevel()}
                            onChangeValue={self => setBrightness(self.value)}
                        />
                    </box>
                </box>

                <box className="divider" />

                {/* 3. Footer: Battery info & Power Options Card */}
                <box halign={Gtk.Align.FILL} valign={Gtk.Align.CENTER}>
                    {/* Battery Indicator */}
                    <box spacing={8} halign={Gtk.Align.START} hexpand>
                        <image file={`${assetsDir}/icons/battery-dark.svg`} pixelSize={20} />
                        <label
                            className="battery-label"
                            label={bind(batteryPercent).as(p => `${p}% Battery`)}
                        />
                    </box>

                    {/* Power Action Buttons */}
                    <box spacing={6} halign={Gtk.Align.END}>
                        <button
                            className="power-btn"
                            tooltipText="Sleep (Suspend)"
                            onClicked={() => powerAction("sleep")}
                        >
                            <image file={`${assetsDir}/icons/power-sleep-dark.svg`} pixelSize={18} />
                        </button>
                        <button
                            className="power-btn"
                            tooltipText="Restart System"
                            onClicked={() => powerAction("restart")}
                        >
                            <image file={`${assetsDir}/icons/power-restart-dark.svg`} pixelSize={18} />
                        </button>
                        <button
                            className="power-btn shutdown"
                            tooltipText="Shut Down System"
                            onClicked={() => powerAction("shutdown")}
                        >
                            <image file={`${assetsDir}/icons/power-shutdown-dark.svg`} pixelSize={18} />
                        </button>
                    </box>
                </box>
            </box>
        </window>
    );
}
