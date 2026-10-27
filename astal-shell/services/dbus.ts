/**
 * VDE D-Bus Session IPC Service
 * Coordinates between Astal Shell (vde-bar) and Qt6 Launcher (vde-launcher)
 */

import { execAsync, Variable } from "astal";
import Gio from "gi://Gio";
import GLib from "gi://GLib";

export type AIInferenceState = "idle" | "active" | "offline";

export interface InferenceStatus {
    state: AIInferenceState;
    model: string;
}

class VdeDbusService {
    private static instance: VdeDbusService;
    public readonly inferenceStatus = Variable<InferenceStatus>({
        state: "idle",
        model: "MiniCPM-V 4.7 1B (Local GGUF)"
    });
    public readonly quickSettingsVisible = Variable<boolean>(false);
    public readonly calendarVisible = Variable<boolean>(false);

    private connection: Gio.DBusConnection | null = null;
    private launcherProxy: Gio.DBusProxy | null = null;

    private constructor() {
        this.initDbus();
    }

    public static get_default(): VdeDbusService {
        if (!VdeDbusService.instance) {
            VdeDbusService.instance = new VdeDbusService();
        }
        return VdeDbusService.instance;
    }

    private initDbus() {
        try {
            this.connection = Gio.bus_get_sync(Gio.BusType.SESSION, null);
            if (this.connection) {
                this.registerShellServer();
                this.initLauncherClient();
            }
        } catch (e) {
            console.warn("[VDE D-Bus] Gio DBus sync init warning, using subprocess fallback:", e);
        }
    }

    private initLauncherClient() {
        try {
            if (!this.connection) return;

            // Subscribe to Launcher's InferenceStateChanged signal
            this.connection.signal_subscribe(
                "org.vde.Launcher",
                "org.vde.Launcher",
                "InferenceStateChanged",
                "/Launcher",
                null,
                Gio.DBusSignalFlags.NONE,
                (_conn, _sender, _path, _iface, _signal, parameters) => {
                    if (parameters) {
                        const [state, model] = parameters.recursiveUnpack() as [string, string];
                        this.inferenceStatus.set({
                            state: (state as AIInferenceState) || "idle",
                            model: model || "MiniCPM-V 4.7 1B"
                        });
                    }
                }
            );
        } catch (e) {
            console.warn("[VDE D-Bus] Failed to subscribe to Launcher signals:", e);
        }
    }

    private registerShellServer() {
        const introspectionXml = `
        <node>
            <interface name="org.vde.Shell">
                <method name="ToggleQuickSettings" />
                <method name="ToggleCalendar" />
                <method name="SetTheme">
                    <arg name="mode" type="s" direction="in" />
                </method>
                <signal name="ThemeChanged">
                    <arg name="mode" type="s" />
                </signal>
            </interface>
        </node>`;

        try {
            const nodeInfo = Gio.DBusNodeInfo.new_for_xml(introspectionXml);
            const ifaceInfo = nodeInfo.interfaces[0];

            this.connection?.register_object(
                "/Shell",
                ifaceInfo,
                (_conn, _sender, _path, _iface, methodName) => {
                    if (methodName === "ToggleQuickSettings") {
                        this.toggleQuickSettings();
                    } else if (methodName === "ToggleCalendar") {
                        this.toggleCalendar();
                    }
                },
                null,
                null
            );

            Gio.bus_own_name_on_connection(
                this.connection!,
                "org.vde.Shell",
                Gio.BusNameOwnerFlags.NONE,
                null,
                null
            );
        } catch (e) {
            console.warn("[VDE D-Bus] Failed to register org.vde.Shell interface:", e);
        }
    }

    /**
     * Toggles the Qt6 Start Menu runner
     */
    public toggleLauncher() {
        execAsync(["qdbus", "org.vde.Launcher", "/Launcher", "org.vde.Launcher.Toggle"])
            .catch(() => {
                // Fallback to gdbus if qdbus is not installed
                return execAsync([
                    "gdbus", "call", "--session",
                    "--dest", "org.vde.Launcher",
                    "--object-path", "/Launcher",
                    "--method", "org.vde.Launcher.Toggle"
                ]);
            })
            .catch(err => {
                console.error("[VDE D-Bus] Could not trigger Launcher Toggle:", err);
            });
    }

    /**
     * Toggles Quick Settings flyout visibility
     */
    public toggleQuickSettings() {
        this.quickSettingsVisible.set(!this.quickSettingsVisible.get());
    }

    /**
     * Toggles Calendar / Notification flyout visibility
     */
    public toggleCalendar() {
        this.calendarVisible.set(!this.calendarVisible.get());
    }
}

export default VdeDbusService.get_default();
