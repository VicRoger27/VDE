import QtQuick
import QtQuick.Controls
import Vde

Item {
    id: root

    property string searchText: ""
    property var appResults: appIndexer.searchApps(searchText)
    property var fileResults: []
    property var visionResults: []

    Connections {
        target: fileSearcher
        function onSearchCompleted(results) {
            root.fileResults = results;
        }
    }

    Connections {
        target: aiClient
        function onVisionResultsReady(results) {
            root.visionResults = results;
        }
    }

    onSearchTextChanged: {
        fileSearcher.searchFiles(searchText);
        aiClient.queryVision(searchText);
    }

    Flickable {
        anchors.fill: parent
        contentHeight: contentCol.height + 20
        clip: true

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
        }

        Column {
            id: contentCol
            width: parent.width - 12
            spacing: 16

            // Section 1: Best Match App
            Column {
                width: parent.width
                spacing: 8
                visible: root.appResults.length > 0

                Text {
                    text: "Best Match"
                    font.family: ThemeTokens.fontFamily
                    font.pixelSize: 12
                    font.weight: Font.DemiBold
                    color: ThemeTokens.text_secondary
                }

                Rectangle {
                    width: parent.width
                    height: 52
                    radius: ThemeTokens.radius_md
                    color: bestMouse.containsMouse ? ThemeTokens.surface_cardHover : ThemeTokens.surface_card

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        spacing: 12

                        Image {
                            anchors.verticalCenter: parent.verticalCenter
                            width: 32
                            height: 32
                            source: (root.appResults.length > 0 && root.appResults[0].icon)
                                ? ("image://icon/" + root.appResults[0].icon)
                                : (assetsDir + "/icons/all-apps-dark.svg")
                            fillMode: Image.PreserveAspectFit
                        }

                        Column {
                            anchors.verticalCenter: parent.verticalCenter
                            Text {
                                text: root.appResults.length > 0 ? root.appResults[0].name : ""
                                font.family: ThemeTokens.fontFamily
                                font.pixelSize: 13
                                font.weight: Font.Medium
                                color: ThemeTokens.text_primary
                            }
                            Text {
                                text: "Application"
                                font.family: ThemeTokens.fontFamily
                                font.pixelSize: 11
                                color: ThemeTokens.text_tertiary
                            }
                        }
                    }

                    MouseArea {
                        id: bestMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            if (root.appResults.length > 0) {
                                appIndexer.launch(root.appResults[0].exec);
                                launcherManager.hide();
                            }
                        }
                    }
                }
            }

            // Section 2: Other Apps
            Column {
                width: parent.width
                spacing: 6
                visible: root.appResults.length > 1

                Text {
                    text: "Apps"
                    font.family: ThemeTokens.fontFamily
                    font.pixelSize: 12
                    font.weight: Font.DemiBold
                    color: ThemeTokens.text_secondary
                }

                Repeater {
                    model: root.appResults.slice(1, 4)
                    delegate: Rectangle {
                        width: contentCol.width
                        height: 38
                        radius: ThemeTokens.radius_sm
                        color: appRowMouse.containsMouse ? ThemeTokens.surface_cardHover : "transparent"

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 8
                            spacing: 10

                            Image {
                                anchors.verticalCenter: parent.verticalCenter
                                width: 22
                                height: 22
                                source: modelData.icon ? ("image://icon/" + modelData.icon) : (assetsDir + "/icons/all-apps-dark.svg")
                            }

                            Text {
                                anchors.verticalCenter: parent.verticalCenter
                                text: modelData.name || ""
                                font.family: ThemeTokens.fontFamily
                                font.pixelSize: 12
                                color: ThemeTokens.text_primary
                            }
                        }

                        MouseArea {
                            id: appRowMouse
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

            // Section 3: Local Files / Documents
            Column {
                width: parent.width
                spacing: 6
                visible: root.fileResults.length > 0

                Text {
                    text: "Documents"
                    font.family: ThemeTokens.fontFamily
                    font.pixelSize: 12
                    font.weight: Font.DemiBold
                    color: ThemeTokens.text_secondary
                }

                Repeater {
                    model: root.fileResults.slice(0, 5)
                    delegate: Rectangle {
                        width: contentCol.width
                        height: 38
                        radius: ThemeTokens.radius_sm
                        color: fileMouse.containsMouse ? ThemeTokens.surface_cardHover : "transparent"

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 8
                            spacing: 10

                            Image {
                                anchors.verticalCenter: parent.verticalCenter
                                width: 20
                                height: 20
                                source: assetsDir + "/icons/app-editor-dark.svg"
                            }

                            Column {
                                anchors.verticalCenter: parent.verticalCenter
                                Text {
                                    text: modelData.name || ""
                                    font.family: ThemeTokens.fontFamily
                                    font.pixelSize: 12
                                    color: ThemeTokens.text_primary
                                    elide: Text.ElideRight
                                }
                            }
                        }

                        MouseArea {
                            id: fileMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                fileSearcher.openFile(modelData.path);
                                launcherManager.hide();
                            }
                        }
                    }
                }
            }

            // Section 4: Local Vision AI Matches (MiniCPM-V 4.7)
            Column {
                width: parent.width
                spacing: 8
                visible: root.visionResults.length > 0

                Text {
                    text: "Images (Local AI Search)"
                    font.family: ThemeTokens.fontFamily
                    font.pixelSize: 12
                    font.weight: Font.DemiBold
                    color: ThemeTokens.accent_primary
                }

                Row {
                    spacing: 8
                    Repeater {
                        model: root.visionResults.slice(0, 4)
                        delegate: Rectangle {
                            width: 72
                            height: 72
                            radius: ThemeTokens.radius_sm
                            color: ThemeTokens.surface_card
                            clip: true

                            Image {
                                anchors.fill: parent
                                source: "file://" + modelData.path
                                fillMode: Image.PreserveAspectCrop
                            }

                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    fileSearcher.openFile(modelData.path);
                                    launcherManager.hide();
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
