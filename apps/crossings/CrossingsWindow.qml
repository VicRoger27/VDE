import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import "../../qt-launcher/tokens"
import "pages"

Window {
    id: root

    title: "Settings — Crossings"
    width: 1000
    height: 700
    minimumWidth: 800
    minimumHeight: 600
    visible: true
    color: ThemeTokens.surface_base

    property string assetsDir: "../../assets"

    // Windows 11 Titlebar
    Rectangle {
        id: titlebar
        width: parent.width
        height: 38
        color: ThemeTokens.surface_base
        border.color: ThemeTokens.border_subtle
        border.width: 1
        z: 10

        Row {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.verticalCenter: parent.verticalCenter
            spacing: 10

            Image {
                width: 18
                height: 18
                source: root.assetsDir + "/icons/settings-dark.svg"
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                text: "Settings"
                font.family: ThemeTokens.fontFamily
                font.pixelSize: 12
                font.weight: Font.DemiBold
                color: ThemeTokens.text_primary
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        // Titlebar Window Controls
        Row {
            anchors.right: parent.right
            anchors.top: parent.top
            height: parent.height

            // Minimize
            Rectangle {
                width: 44
                height: parent.height
                color: minMouse.containsMouse ? ThemeTokens.surface_cardHover : "transparent"
                Image {
                    anchors.centerIn: parent
                    width: 14
                    height: 14
                    source: root.assetsDir + "/icons/window-minimize-dark.svg"
                }
                MouseArea {
                    id: minMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: root.showMinimized()
                }
            }

            // Maximize / Restore
            Rectangle {
                width: 44
                height: parent.height
                color: maxMouse.containsMouse ? ThemeTokens.surface_cardHover : "transparent"
                Image {
                    anchors.centerIn: parent
                    width: 14
                    height: 14
                    source: root.visibility === Window.Maximized
                        ? root.assetsDir + "/icons/window-restore-dark.svg"
                        : root.assetsDir + "/icons/window-maximize-dark.svg"
                }
                MouseArea {
                    id: maxMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        if (root.visibility === Window.Maximized) {
                            root.showNormal();
                        } else {
                            root.showMaximized();
                        }
                    }
                }
            }

            // Close
            Rectangle {
                width: 44
                height: parent.height
                color: closeMouse.containsMouse ? "#c42b1c" : "transparent"
                Image {
                    anchors.centerIn: parent
                    width: 14
                    height: 14
                    source: root.assetsDir + "/icons/window-close-dark.svg"
                }
                MouseArea {
                    id: closeMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: root.close()
                }
            }
        }
    }

    // Two-Pane Content Area
    Row {
        anchors.top: titlebar.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        // 1. Left Sidebar
        CategorySidebar {
            id: sidebar
            height: parent.height
            assetsDir: root.assetsDir
            onCategorySelected: (index, catId, catTitle) => {
                pagesStack.currentIndex = index;
            }
        }

        // 2. Right Interactive Settings Pages Stack
        Rectangle {
            width: parent.width - sidebar.width
            height: parent.height
            color: ThemeTokens.surface_mica

            StackLayout {
                id: pagesStack
                anchors.fill: parent
                currentIndex: 0

                SystemPage { assetsDir: root.assetsDir }
                Item { Text { text: "Bluetooth Settings Placeholder"; color: "white"; anchors.centerIn: parent } }
                Item { Text { text: "Network Settings Placeholder"; color: "white"; anchors.centerIn: parent } }
                PersonalizationPage { assetsDir: root.assetsDir }
                Item { Text { text: "Apps Settings Placeholder"; color: "white"; anchors.centerIn: parent } }
                PrivacyPage { assetsDir: root.assetsDir }
            }
        }
    }
}
