import QtQuick
import QtQuick.Controls
import QtQuick.Window
import Vde

Window {
    id: root
    width: ThemeTokens.startMenuWidth
    height: ThemeTokens.startMenuHeight
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup
    color: "transparent"

    property bool showAllApps: false

    Connections {
        target: launcherManager
        function onVisibilityChanged(vis) {
            if (vis) {
                searchField.text = "";
                root.showAllApps = false;
                searchField.forceActiveFocus();
            }
        }
        function onExternalQueryRequested(q) {
            searchField.text = q;
            searchField.forceActiveFocus();
        }
    }

    // Dismiss on Escape
    Shortcut {
        sequence: "Escape"
        onActivated: launcherManager.hide()
    }

    AcrylicSurface {
        anchors.fill: parent
        anchors.margins: 6

        Column {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 16

            // 1. Windows 11 Search Input Box
            Rectangle {
                id: searchBar
                width: parent.width
                height: 42
                radius: ThemeTokens.radius_full
                color: ThemeTokens.surface_input
                border.color: searchField.activeFocus ? ThemeTokens.border_focus : ThemeTokens.border_default
                border.width: searchField.activeFocus ? 2 : 1

                Row {
                    anchors.fill: parent
                    anchors.leftMargin: 14
                    anchors.rightMargin: 14
                    spacing: 10

                    Image {
                        anchors.verticalCenter: parent.verticalCenter
                        width: 18
                        height: 18
                        source: assetsDir + "/icons/search-dark.svg"
                    }

                    TextField {
                        id: searchField
                        anchors.verticalCenter: parent.verticalCenter
                        width: parent.width - 56
                        font.family: ThemeTokens.fontFamily
                        font.pixelSize: 13
                        color: ThemeTokens.text_primary
                        placeholderText: "Type here to search apps, files, or images..."
                        placeholderTextColor: ThemeTokens.text_tertiary
                        background: null
                    }

                    // Clear button
                    Text {
                        visible: searchField.text.length > 0
                        anchors.verticalCenter: parent.verticalCenter
                        text: "×"
                        font.pixelSize: 18
                        color: ThemeTokens.text_tertiary
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: searchField.text = ""
                        }
                    }
                }
            }

            // 2. Central Content Area (Pinned vs All Apps vs Search Results)
            Item {
                width: parent.width
                height: 480

                // Search Results (active when search text is non-empty)
                SearchResultsView {
                    anchors.fill: parent
                    visible: searchField.text.length > 0
                    searchText: searchField.text
                }

                // Pinned Grid (active when search text is empty & not viewing all apps)
                PinnedGrid {
                    anchors.fill: parent
                    visible: searchField.text.length === 0 && !root.showAllApps
                    onRequestAllApps: root.showAllApps = true
                }

                // All Apps List (active when user clicks "All apps >")
                AllAppsList {
                    anchors.fill: parent
                    visible: searchField.text.length === 0 && root.showAllApps
                    onRequestBack: root.showAllApps = false
                }
            }

            // Divider
            Rectangle {
                width: parent.width
                height: 1
                color: ThemeTokens.border_divider
            }

            // 3. Bottom Minimalist Footer (User profile & Power)
            Row {
                width: parent.width
                height: 38
                anchors.bottom: parent.bottom

                // User Profile
                Row {
                    spacing: 10
                    anchors.verticalCenter: parent.verticalCenter

                    Rectangle {
                        width: 32
                        height: 32
                        radius: ThemeTokens.radius_full
                        color: ThemeTokens.accent_secondary
                        anchors.verticalCenter: parent.verticalCenter

                        Text {
                            anchors.centerIn: parent
                            text: "V"
                            font.family: ThemeTokens.fontFamily
                            font.pixelSize: 14
                            font.weight: Font.Bold
                            color: "#ffffff"
                        }
                    }

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: "Victor"
                        font.family: ThemeTokens.fontFamily
                        font.pixelSize: 13
                        font.weight: Font.Medium
                        color: ThemeTokens.text_primary
                    }
                }

                Item {
                    width: parent.width - 200
                    height: 1
                }

                // Power Button with Menu
                Rectangle {
                    id: powerBtn
                    width: 34
                    height: 34
                    radius: ThemeTokens.radius_md
                    color: powerMouse.containsMouse ? ThemeTokens.surface_cardHover : "transparent"
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right

                    Image {
                        anchors.centerIn: parent
                        width: 18
                        height: 18
                        source: assetsDir + "/icons/power-shutdown-dark.svg"
                    }

                    MouseArea {
                        id: powerMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: powerMenu.open()
                    }

                    Menu {
                        id: powerMenu
                        y: -110
                        background: Rectangle {
                            color: ThemeTokens.surface_card
                            border.color: ThemeTokens.border_strong
                            radius: ThemeTokens.radius_md
                        }

                        Action {
                            text: "Sleep"
                            onTriggered: {
                                launcherManager.hide();
                                appIndexer.launch("systemctl suspend");
                            }
                        }
                        Action {
                            text: "Restart"
                            onTriggered: {
                                launcherManager.hide();
                                appIndexer.launch("systemctl reboot");
                            }
                        }
                        Action {
                            text: "Shut down"
                            onTriggered: {
                                launcherManager.hide();
                                appIndexer.launch("systemctl poweroff");
                            }
                        }
                    }
                }
            }
        }
    }
}
