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
            text: "Personalization"
            font.family: ThemeTokens.fontFamily
            font.pixelSize: 22
            font.weight: Font.Bold
            color: ThemeTokens.text_primary
            topPadding: 10
            bottomPadding: 6
        }

        // Card 1: Dark / Light Mode Switch
        SettingsCard {
            title: "Dark Mode"
            description: "Apply dark Mica and frosted acrylic glass palette"
            iconSource: root.assetsDir + "/icons/theme-switch-dark.svg"

            actionItem: Switch {
                checked: true
                anchors.verticalCenter: parent.verticalCenter
                onToggled: {
                    console.log("[Crossings] Theme switched:", checked ? "Dark" : "Light");
                }
            }
        }

        // Card 2: Accent Colors Picker
        SettingsCard {
            title: "Accent Color"
            description: "Select system highlight color for active windows and indicators"
            iconSource: root.assetsDir + "/icons/start-active-dark.svg"

            actionItem: Row {
                spacing: 8
                anchors.verticalCenter: parent.verticalCenter

                Repeater {
                    model: ["#60cdff", "#0078d4", "#13a10e", "#ffc83d", "#c42b1c"]
                    delegate: Rectangle {
                        width: 24
                        height: 24
                        radius: ThemeTokens.radius_full
                        color: modelData
                        border.color: modelData === "#60cdff" ? "#ffffff" : "transparent"
                        border.width: 2

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                console.log("[Crossings] Accent color selected:", modelData);
                            }
                        }
                    }
                }
            }
        }

        // Card 3: Taskbar Alignment
        SettingsCard {
            title: "Taskbar Alignment"
            description: "Position launchers in the center or left edge"
            iconSource: root.assetsDir + "/icons/all-apps-dark.svg"

            actionItem: ComboBox {
                model: ["Center (Default)", "Left"]
                anchors.verticalCenter: parent.verticalCenter
                font.family: ThemeTokens.fontFamily
                font.pixelSize: 11
                currentIndex: 0
            }
        }

        // Card 4: Frosted Acrylic Glass Shader
        SettingsCard {
            title: "Acrylic & Mica Translucency"
            description: "Hardware-accelerated GLSL blur shaders on taskbar and Start Menu"
            iconSource: root.assetsDir + "/icons/settings-dark.svg"

            actionItem: Switch {
                checked: true
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}
