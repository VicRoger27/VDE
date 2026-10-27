import QtQuick
import QtQuick.Effects
import Vde

Rectangle {
    id: root

    property alias content: contentItem.data
    property int cornerRadius: ThemeTokens.radius_xl
    property color surfaceColor: ThemeTokens.surface_flyout
    property color borderColor: ThemeTokens.border_strong

    color: surfaceColor
    radius: cornerRadius
    border.color: borderColor
    border.width: 1
    clip: true

    Item {
        id: contentItem
        anchors.fill: parent
    }
}
