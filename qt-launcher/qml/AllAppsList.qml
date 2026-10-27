import QtQuick
import QtQuick.Controls
import Vde

Item {
    id: root

    signal requestBack()

    Column {
        anchors.fill: parent
        spacing: 8

        // Header Row
        Row {
            width: parent.width
            height: 28
            spacing: 12

            Button {
                id: backBtn
                text: "< Back"
                anchors.verticalCenter: parent.verticalCenter
                font.family: ThemeTokens.fontFamily
                font.pixelSize: 12
                contentItem: Text {
                    text: backBtn.text
                    font: backBtn.font
                    color: backBtn.hovered ? ThemeTokens.accent_primary : ThemeTokens.text_secondary
                }
                background: Rectangle {
                    color: backBtn.hovered ? ThemeTokens.surface_cardHover : "transparent"
                    radius: ThemeTokens.radius_sm
                }
                onClicked: root.requestBack()
            }

            Text {
                text: "All Apps"
                font.family: ThemeTokens.fontFamily
                font.pixelSize: 14
                font.weight: Font.DemiBold
                color: ThemeTokens.text_primary
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        // Alphabetical List
        ListView {
            id: list
            width: parent.width
            height: 400
            clip: true
            spacing: 2
            model: appIndexer.getAllApps()

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
            }

            delegate: Rectangle {
                id: rowItem
                width: list.width - 12
                height: 44
                radius: ThemeTokens.radius_md
                color: rowMouse.containsMouse ? ThemeTokens.surface_cardHover : "transparent"

                Row {
                    anchors.fill: parent
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    spacing: 12

                    Image {
                        anchors.verticalCenter: parent.verticalCenter
                        width: 28
                        height: 28
                        source: modelData.icon ? ("image://icon/" + modelData.icon) : (assetsDir + "/icons/all-apps-dark.svg")
                        fillMode: Image.PreserveAspectFit
                    }

                    Column {
                        anchors.verticalCenter: parent.verticalCenter
                        width: parent.width - 50

                        Text {
                            text: modelData.name || ""
                            font.family: ThemeTokens.fontFamily
                            font.pixelSize: 13
                            color: ThemeTokens.text_primary
                            elide: Text.ElideRight
                        }

                        Text {
                            visible: text.length > 0
                            text: modelData.comment || ""
                            font.family: ThemeTokens.fontFamily
                            font.pixelSize: 11
                            color: ThemeTokens.text_tertiary
                            elide: Text.ElideRight
                        }
                    }
                }

                MouseArea {
                    id: rowMouse
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
