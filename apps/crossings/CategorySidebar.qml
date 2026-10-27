import QtQuick
import QtQuick.Controls
import "../../qt-launcher/tokens"

Rectangle {
    id: root

    property int activeIndex: 0
    property string assetsDir: "../../assets"
    signal categorySelected(int index, string id, string title)

    width: 260
    color: ThemeTokens.surface_base
    border.color: ThemeTokens.border_subtle
    border.width: 1

    ListModel {
        id: categoriesModel
        ListElement { catId: "system"; name: "System"; icon: "/icons/settings-dark.svg" }
        ListElement { catId: "bluetooth"; name: "Bluetooth & Devices"; icon: "/icons/bluetooth-dark.svg" }
        ListElement { catId: "network"; name: "Network & Internet"; icon: "/icons/wifi-dark.svg" }
        ListElement { catId: "personalization"; name: "Personalization"; icon: "/icons/theme-switch-dark.svg" }
        ListElement { catId: "apps"; name: "Apps"; icon: "/icons/all-apps-dark.svg" }
        ListElement { catId: "privacy"; name: "Privacy & Security"; icon: "/icons/tray-lock-dark.svg" }
    }

    Column {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 12

        // 1. User Header Chip
        Row {
            spacing: 10
            width: parent.width
            height: 40

            Rectangle {
                width: 36
                height: 36
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

            Column {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 1

                Text {
                    text: "Victor"
                    font.family: ThemeTokens.fontFamily
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                    color: ThemeTokens.text_primary
                }

                Text {
                    text: "VDE Live OS"
                    font.family: ThemeTokens.fontFamily
                    font.pixelSize: 11
                    color: ThemeTokens.text_tertiary
                }
            }
        }

        // 2. Search Settings Box
        Rectangle {
            width: parent.width
            height: 34
            radius: ThemeTokens.radius_md
            color: ThemeTokens.surface_input
            border.color: searchInput.activeFocus ? ThemeTokens.border_focus : ThemeTokens.border_default
            border.width: 1

            Row {
                anchors.fill: parent
                anchors.leftMargin: 10
                anchors.rightMargin: 10
                spacing: 8

                Image {
                    anchors.verticalCenter: parent.verticalCenter
                    width: 14
                    height: 14
                    source: root.assetsDir + "/icons/search-dark.svg"
                }

                TextField {
                    id: searchInput
                    anchors.verticalCenter: parent.verticalCenter
                    width: parent.width - 24
                    font.family: ThemeTokens.fontFamily
                    font.pixelSize: 12
                    color: ThemeTokens.text_primary
                    placeholderText: "Find a setting..."
                    placeholderTextColor: ThemeTokens.text_tertiary
                    background: null
                }
            }
        }

        // 3. Category List
        ListView {
            id: catList
            width: parent.width
            height: parent.height - 110
            model: categoriesModel
            spacing: 4
            interactive: false

            delegate: Rectangle {
                id: catItem
                width: catList.width
                height: 40
                radius: ThemeTokens.radius_sm
                color: root.activeIndex === index
                    ? ThemeTokens.surface_cardHover
                    : (catMouse.containsMouse ? ThemeTokens.surface_card : "transparent")

                // Active left accent indicator bar
                Rectangle {
                    visible: root.activeIndex === index
                    width: 3
                    height: 18
                    radius: 2
                    color: ThemeTokens.accent_primary
                    anchors.left: parent.left
                    anchors.leftMargin: 2
                    anchors.verticalCenter: parent.verticalCenter
                }

                Row {
                    anchors.fill: parent
                    anchors.leftMargin: 12
                    spacing: 12

                    Image {
                        anchors.verticalCenter: parent.verticalCenter
                        width: 18
                        height: 18
                        source: root.assetsDir + model.icon
                    }

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: model.name
                        font.family: ThemeTokens.fontFamily
                        font.pixelSize: 12
                        font.weight: root.activeIndex === index ? Font.DemiBold : Font.Normal
                        color: root.activeIndex === index ? ThemeTokens.text_primary : ThemeTokens.text_secondary
                    }
                }

                MouseArea {
                    id: catMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        root.activeIndex = index;
                        root.categorySelected(index, model.catId, model.name);
                    }
                }
            }
        }
    }
}
