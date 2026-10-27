import QtQuick
import QtQuick.Controls
import Vde

Item {
    id: root

    signal requestAllApps()

    Column {
        anchors.fill: parent
        spacing: 12

        // Header Row
        Row {
            width: parent.width
            height: 28

            Text {
                text: "Pinned"
                font.family: ThemeTokens.fontFamily
                font.pixelSize: 14
                font.weight: Font.DemiBold
                color: ThemeTokens.text_primary
                anchors.verticalCenter: parent.verticalCenter
            }

            Item {
                width: parent.width - 60 - allAppsBtn.width
                height: 1
            }

            Button {
                id: allAppsBtn
                text: "All apps >"
                anchors.verticalCenter: parent.verticalCenter
                font.family: ThemeTokens.fontFamily
                font.pixelSize: 12
                contentItem: Text {
                    text: allAppsBtn.text
                    font: allAppsBtn.font
                    color: allAppsBtn.hovered ? ThemeTokens.accent_primary : ThemeTokens.text_secondary
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: allAppsBtn.hovered ? ThemeTokens.surface_cardHover : "transparent"
                    radius: ThemeTokens.radius_sm
                }
                onClicked: root.requestAllApps()
            }
        }

        // Pinned Apps Grid (6x3)
        GridView {
            id: grid
            width: parent.width
            height: 380
            cellWidth: width / 6
            cellHeight: 90
            clip: true
            interactive: false

            model: appIndexer.getPinnedApps()

            delegate: Item {
                width: grid.cellWidth
                height: grid.cellHeight

                Rectangle {
                    id: tile
                    anchors.centerIn: parent
                    width: parent.width - 6
                    height: parent.height - 6
                    radius: ThemeTokens.radius_md
                    color: mouseArea.containsMouse ? ThemeTokens.surface_cardHover : "transparent"
                    scale: mouseArea.containsPress ? 0.94 : (mouseArea.containsMouse ? 1.03 : 1.0)

                    Behavior on scale {
                        NumberAnimation { duration: 120; easing.type: Easing.OutQuad }
                    }

                    Column {
                        anchors.centerIn: parent
                        spacing: 6

                        Image {
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: 36
                            height: 36
                            source: modelData.icon ? ("image://icon/" + modelData.icon) : (assetsDir + "/icons/all-apps-dark.svg")
                            sourceSize.width: 36
                            sourceSize.height: 36
                            fillMode: Image.PreserveAspectFit
                        }

                        Text {
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: tile.width - 8
                            text: modelData.name || ""
                            font.family: ThemeTokens.fontFamily
                            font.pixelSize: 11
                            color: ThemeTokens.text_primary
                            horizontalAlignment: Text.AlignHCenter
                            elide: Text.ElideRight
                            maximumLineCount: 2
                            wrapMode: Text.Wrap
                        }
                    }

                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            appIndexer.launch(modelData.exec);
                            launcherManager.hide();
                        }
                    }
                }
            }
        }
    }
}
