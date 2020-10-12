import QtQuick 2.4
import QtQml.Models 2.4
import QtQuick.Controls 2.4

Item {
    width: 700
    height: 550
    clip: true

    Rectangle {
        id: background
        x: 0
        y: 64
        width: 700
        height: 486
        color: "#2d1d0f"
    }

    ToolBar {
        id: toolBar
        x: 0
        y: 0
        width: 700
        height: 64

        ToolButton {
            
            id: toolButton
            objectName: "toolButton"
            x: 0
            y: 0
            width: 82
            height: 51
            text: qsTr("Открыть \n папку")
            flat: true
            topPadding: 0
            wheelEnabled: false
            enabled: true
            autoExclusive: false
            checked: false
            checkable: false
        }

        ToolButton {
            id: toolButton1
            x: 88
            y: 0
            width: 82
            height: 51
            text: qsTr("О программе")
        }

        ToolButton {
            id: toolButton2
            x: 176
            y: 0
            width: 82
            height: 51
            text: qsTr("Закрыть")
        }

        Switch {
            id: element7
            x: 264
            y: 0
            width: 244
            height: 24
            text: qsTr("Перемещать отсортированные")
            checked: true
        }

        TextField {
            id: pathToSortDirTextField
            x: 264
            y: 26
            width: 127
            height: 30
            text: qsTr("")
        }

        Button {
            id: selectSortDirButton
            objectName: "selectSortDirButton"
            x: 397
            y: 26
            width: 106
            height: 30
            text: qsTr("Путь куда сорт")
        }
    }



    BusyIndicator {
        id: busyIndicator

        x: 248
        y: 219
        width: 205
        height: 177
        visible: false

        ProgressBar {
            id: progressBar
            x: 0
            y: 149
            width: 199
            height: 22
            visible: false
            to: 1
            enabled: true
            value: 0.5
        }
    }



    ListView {
        id: listView1
        clip: true
        // Размещаем его в оставшейся части окна приложения
        anchors.top: toolBar.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        /* в данном свойстве задаём вёрстку одного объекта
         * который будем отображать в списке в качестве одного элемента списка
         * */
        delegate: Item {
            width: 690
            anchors.left: parent.left
            anchors.right: parent.right
            height: 142

            // В данном элементе будет находиться одна кнопка

            Rectangle {
                id: rectangle
                x: 8
                y: 8
                width: 680
                height: 126
                color: colorRowRect
            }

            Button {
                text: "Отправить"
                anchors.fill: parent
                anchors.margins: 5
                objectName: sendBtnName

                /* самое интересное в данном объекте
                 * задаём свойству text переменную, по имени которой будем задавать
                 * свойства элемента
                 * */
                anchors.rightMargin: 18
                anchors.topMargin: 15
                anchors.leftMargin: 553
                anchors.bottomMargin: 77

                // По клику по кнопке отдаём в текстовое поле индекс элемента в ListView
                onClicked: {
                    ex.sendImgToGallery(textEdit.text)
                }
            }



            Image {
                id: image
                x: 17
                y: 24
                width: 119
                height: 103
                fillMode: Image.PreserveAspectFit
                source: localImgPath
            }



            Image {
                id: image1
                x: 142
                y: 24
                width: 119
                height: 103
                fillMode: Image.PreserveAspectFit
                source: remoteImgPath
            }



            Text {
                id: element
                x: 17
                y: 8
                width: 119
                height: 15
                text: qsTr("Исходное")
                font.pixelSize: 12
            }



            Text {
                id: element1
                x: 142
                y: 8
                width: 119
                height: 15
                text: qsTr("Найденное")
                font.pixelSize: 12
            }



            Text {
                id: element2
                x: 267
                y: 8
                text: qsTr("Процент схожести:")
                font.pixelSize: 12
            }



            Text {
                id: element3
                x: 388
                y: 8
                width: 17
                height: 15
                text: similarity
                font.pixelSize: 12
            }



            Text {
                id: element4
                x: 267
                y: 29
                text: qsTr("Источник:")
                font.pixelSize: 12
            }



            Text {
                id: element5
                x: 342
                y: 29
                width: 205
                height: 15
                text: source
                clip: true
                wrapMode:Text.Wrap
                onLinkActivated: Qt.openUrlExternally(link)
                font.pixelSize: 12
            }



            TextEdit {
                id: textEdit
                objectName:"textEdit"
                x: 311
                y: 50
                width: 236
                height: 70
                text: tags
                wrapMode: Text.WordWrap
                clip: true
                font.pixelSize: 12
            }



            Text {
                id: element6
                x: 267
                y: 50
                text: qsTr("Теги:")
                font.pixelSize: 12
            }

        }

        // Сама модель, в которой будут содержаться все элементы
        model: ListModel {
            id: limgListModel // задаём ей id для обращения
        }
    }



    function append(newElement) {
        limgListModel.append(newElement)
    }

    function clear() {
        limgListModel.clear()
    }

    function showBusyIndicator() {
        busyIndicator.visible = true
        progressBar.visible = true
    }

    function hideBusyIndicator() {
        busyIndicator.visible = false
        progressBar.visible = false
    }

    function setProgressBarValue(value) {
        progressBar.value = value
    }

    function setSortDitPathTextField(value) {
        pathToSortDirTextField.text = value
    }


}



