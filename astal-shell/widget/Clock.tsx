/**
 * VDE Clock & Date Widget
 * Windows 11 two-line time and date display
 */

import { Gtk } from "astal/gtk4";
import { Variable } from "astal";
import GLib from "gi://GLib";
import dbusService from "../services/dbus";

export default function Clock() {
    const time = Variable<string>("").poll(1000, () =>
        GLib.DateTime.new_now_local().format("%I:%M %p") || ""
    );

    const date = Variable<string>("").poll(60000, () =>
        GLib.DateTime.new_now_local().format("%m/%d/%Y") || ""
    );

    return (
        <button
            className="vde-clock-button"
            onClicked={() => {
                dbusService.toggleCalendar();
            }}
            tooltipText="Date and time settings"
        >
            <box orientation={Gtk.Orientation.VERTICAL} valign={Gtk.Align.CENTER} halign={Gtk.Align.END}>
                <label className="clock-time" label={time()} />
                <label className="clock-date" label={date()} />
            </box>
        </button>
    );
}
