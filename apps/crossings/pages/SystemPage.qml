import QtQuick
import QtQuick.Controls
import "../../../qt-launcher/tokens"
import ".."

Flickable {
    id: root

    property string assetsDir: "../../../assets"
    contentHeight: contentCol.height + 40
    clip: true

    ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }

    Column {
        id: contentCol
        width: parent.width - 32
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 14

        // Page Header
        Text {
            text: "System"
            font.family: ThemeTokens.fontFamily
            font.pixelSize: 22
            font.weight: Font.Bold
            color: ThemeTokens.text_primary
            topPadding: 10
            bottomPadding: 6
        }

        // Section: Display & Sound Cards
        SettingsCard {
            title: "Display"
            description: "Resolution, refresh rate (wlr-randr), Night light"
            iconSource: root.assetsDir + "/icons/cast-display-dark.svg"
            isClickable: true
        }

        SettingsCard {
            title: "Sound"
            description: "Volume levels, default output device (WirePlumber / PipeWire)"
            iconSource: root.assetsDir + "/icons/volume-dark.svg"
            isClickable: true
        }

        SettingsCard {
            title: "Power & Battery"
            description: "Battery saver, screen turn-off timeout, sleep thresholds"
            iconSource: root.assetsDir + "/icons/battery-dark.svg"
            isClickable: true
        }

        // Section: About VDE Specs Card
        Rectangle {
            width: parent.width
            height: 140
            radius: ThemeTokens.radius_md
            color: ThemeTokens.surface_card
            border.color: ThemeTokens.border_default
            border.width: 1

            Column {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 8

                Row {
                    spacing: 8
                    Image {
                        width: 20
                        height: 20
                        source: root.assetsDir + "/icons/start-idle-dark.svg"
                    }
                    Text {
                        text: "About VDE (Victorious Desktop Environment)"
                        font.family: ThemeTokens.fontFamily
                        font.pixelSize: 14
                        font.weight: Font.DemiBold
                        color: ThemeTokens.text_primary
                    }
                }

                Grid {
                    columns: 2
                    columnSpacing: 24
                    rowSpacing: 4

                    Text { text: "Edition:"; font.pixelSize: 11; color: ThemeTokens.text_tertiary }
                    Text { text: "VDE Live LiveOS (Noble Minbase)"; font.pixelSize: 11; color: ThemeTokens.text_primary }

                    Text { text: "Compositor:"; font.pixelSize: 11; color: ThemeTokens.text_tertiary }
                    Text { text: "Labwc (wlroots layer-shell)"; font.pixelSize: 11; color: ThemeTokens.text_primary }

                    Text { text: "Idle Footprint:"; font.pixelSize: 11; color: ThemeTokens.text_tertiary }
                    Text { text: "~240 MB Idle RAM (Target <500 MB)"; font.pixelSize: 11; font.weight: Font.DemiBold; color: "#60cdff" }

                    Text { text: "Telemetry:"; font.pixelSize: 11; color: ThemeTokens.text_tertiary }
                    Text { text: "Strictly Zero / 100% Offline"; font.pixelSize: 11; font.weight: Font.DemiBold; color: "#4cc2ff" }
                }
            }
        }
    }
}
