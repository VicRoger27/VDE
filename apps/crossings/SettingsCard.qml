import QtQuick
import QtQuick.Controls
import "../../qt-launcher/tokens"

Rectangle {
    id: root

    property string title: ""
    property string description: ""
    property string iconSource: ""
    property alias actionItem: actionContainer.data
    property bool isClickable: false

    signal clicked()

    width: parent ? parent.width : 500
    height: Math.max(56, contentRow.implicitHeight + 16)
    radius: ThemeTokens.radius_md
    color: (isClickable && mouseArea.containsMouse) ? ThemeTokens.surface_cardHover : ThemeTokens.surface_card
    border.color: ThemeTokens.border_default
    border.width: 1

    Behavior on color {
        ColorAnimation { duration: 120 }
    }

    Row {
        id: contentRow
        anchors.fill: parent
        anchors.leftMargin: 16
        anchors.rightMargin: 16
        spacing: 14

        // Card Icon
        Image {
            id: icon
            anchors.verticalCenter: parent.verticalCenter
            width: 20
            height: 20
            visible: root.iconSource.length > 0
            source: root.iconSource
            fillMode: Image.PreserveAspectFit
        }

        // Text labels
        Column {
            anchors.verticalCenter: parent.verticalCenter
            width: parent.width - (icon.visible ? 34 : 0) - actionContainer.width - 20
            spacing: 2

            Text {
                text: root.title
                font.family: ThemeTokens.fontFamily
                font.pixelSize: 13
                font.weight: Font.DemiBold
                color: ThemeTokens.text_primary
                elide: Text.ElideRight
                width: parent.width
            }

            Text {
                visible: root.description.length > 0
                text: root.description
                font.family: ThemeTokens.fontFamily
                font.pixelSize: 11
                color: ThemeTokens.text_tertiary
                elide: Text.ElideRight
                width: parent.width
            }
        }

        // Interactive control container (Switch, Slider, etc.)
        Item {
            id: actionContainer
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            width: childrenRect.width
            height: childrenRect.height
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        enabled: root.isClickable
        hoverEnabled: root.isClickable
        cursorShape: root.isClickable ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: root.clicked()
    }
}
