import QtQuick 2.12
import QtQuick.Controls 2.12

ApplicationWindow {
    id: window
    visible: true

    Drawer {
        id: drawer
        width: 0.66 * window.width
        height: window.height

        Label {
            text: "Content goes here!"
            anchors.centerIn: parent
        }
    }
}