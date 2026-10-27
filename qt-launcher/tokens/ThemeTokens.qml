// Auto-generated from tokens/theme.json. DO NOT EDIT DIRECTLY.
pragma Singleton
import QtQuick

QtObject {
    id: root

    readonly property string fontFamily: "Segoe UI Variable"

    // Layout Dimensions
    readonly property int taskbarHeight: 48
    readonly property int taskbarIconSize: 24
    readonly property int taskbarItemWidth: 44
    readonly property int startMenuWidth: 580
    readonly property int startMenuHeight: 650
    readonly property int quickSettingsWidth: 360
    readonly property int quickSettingsHeight: 440

    // Radii
    readonly property int radius_xs: 2
    readonly property int radius_sm: 4
    readonly property int radius_md: 8
    readonly property int radius_lg: 12
    readonly property int radius_xl: 16
    readonly property int radius_full: 9999

    // Dark Surface Colors
    readonly property color surface_base: "#202020"
    readonly property color surface_mica: "#202020"
    readonly property color surface_acrylic: "rgba(32, 32, 32, 0.78)"
    readonly property color surface_card: "#2d2d2d"
    readonly property color surface_cardHover: "#383838"
    readonly property color surface_cardPressed: "#282828"
    readonly property color surface_flyout: "#2c2c2c"
    readonly property color surface_taskbar: "rgba(32, 32, 32, 0.82)"
    readonly property color surface_input: "#242424"

    // Dark Border Colors
    readonly property color border_subtle: "rgba(255, 255, 255, 0.05)"
    readonly property color border_default: "rgba(255, 255, 255, 0.09)"
    readonly property color border_strong: "rgba(255, 255, 255, 0.16)"
    readonly property color border_focus: "#60cdff"
    readonly property color border_divider: "rgba(255, 255, 255, 0.08)"

    // Dark Text Colors
    readonly property color text_primary: "#ffffff"
    readonly property color text_secondary: "rgba(255, 255, 255, 0.78)"
    readonly property color text_tertiary: "rgba(255, 255, 255, 0.54)"
    readonly property color text_disabled: "rgba(255, 255, 255, 0.38)"
    readonly property color text_onAccent: "#000000"

    // Dark Accent Colors
    readonly property color accent_primary: "#60cdff"
    readonly property color accent_secondary: "#0078d4"
    readonly property color accent_hover: "#70d6ff"
    readonly property color accent_pressed: "#50bce8"
    readonly property color accent_subtle: "rgba(96, 205, 255, 0.12)"

    // Dark Status Indicators
    readonly property color status_aiIdle: "rgba(255, 255, 255, 0.70)"
    readonly property color status_aiInference: "#60cdff"
    readonly property color status_aiInferenceGlow: "rgba(96, 205, 255, 0.45)"
    readonly property color status_aiOffline: "rgba(255, 255, 255, 0.28)"
    readonly property color status_runningIndicator: "#60cdff"
    readonly property color status_focusedIndicator: "#60cdff"
    readonly property color status_urgentIndicator: "#ff99a4"
}
