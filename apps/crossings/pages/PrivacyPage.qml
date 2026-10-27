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
            text: "Privacy & Security"
            font.family: ThemeTokens.fontFamily
            font.pixelSize: 22
            font.weight: Font.Bold
            color: ThemeTokens.text_primary
            topPadding: 10
            bottomPadding: 6
        }

        // Card 1: Zero Telemetry Status Badge
        Rectangle {
            width: parent.width
            height: 72
            radius: ThemeTokens.radius_md
            color: "#0d2818" // subtle dark green tint
            border.color: "#166534"
            border.width: 1

            Row {
                anchors.fill: parent
                anchors.leftMargin: 16
                anchors.rightMargin: 16
                spacing: 14

                Image {
                    anchors.verticalCenter: parent.verticalCenter
                    width: 24
                    height: 24
                    source: root.assetsDir + "/icons/tray-lock-dark.svg"
                }

                Column {
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 2
                    Text {
                        text: "Telemetry: 100% Offline & Scrubbed"
                        font.family: ThemeTokens.fontFamily
                        font.pixelSize: 13
                        font.weight: Font.Bold
                        color: "#4ade80"
                    }
                    Text {
                        text: "No background analytics, no cloud recall, no advertising identifiers, zero web query leaks."
                        font.family: ThemeTokens.fontFamily
                        font.pixelSize: 11
                        color: "#86efac"
                    }
                }
            }
        }

        // Card 2: Microphone Privacy Indicator
        SettingsCard {
            title: "Microphone Access"
            description: "Display active amber privacy dot in taskbar when apps access audio"
            iconSource: root.assetsDir + "/icons/tray-mic-active-dark.svg"

            actionItem: Switch {
                checked: true
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        // Card 3: Local Offline AI Vision Settings
        SettingsCard {
            title: "Local Multimodal Vision Search (MiniCPM-V 4.7)"
            description: "Run image queries locally via in-memory llama.cpp server (localhost:8080). Strictly zero Ollama."
            iconSource: root.assetsDir + "/icons/start-active-dark.svg"

            actionItem: Switch {
                checked: true
                anchors.verticalCenter: parent.verticalCenter
                onToggled: {
                    console.log("[Crossings] Local AI Vision:", checked ? "Enabled" : "Disabled");
                }
            }
        }

        // Card 4: Local VRAM Budget for Vision AI
        SettingsCard {
            title: "Local AI VRAM Allocation"
            description: "Offload neural layers to GPU VRAM (Auto: 1.8 GB allocated)"
            iconSource: root.assetsDir + "/icons/settings-dark.svg"

            actionItem: ComboBox {
                model: ["1.5 GB (Conservative)", "2.0 GB (Recommended)", "Disabled (CPU Only)"]
                anchors.verticalCenter: parent.verticalCenter
                currentIndex: 1
            }
        }
    }
}
