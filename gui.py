import sys
from PyQt5.QtCore import QUrl, QObject, QMetaObject, Q_ARG, QVariant, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QToolButton, QFileDialog
from PyQt5.QtQuick import QQuickView
from os import walk
import apiKhiena
import imgUrlGetter
import time


class Example(QWidget):
    @pyqtSlot(QVariant)
    def sendImgToGallery(self, aword):
        print(aword)
        #o = self.view.findChild(QObject, 'textEdit')
        #print(o)
        print("kek")

    def getTagsString(self, tagsArray):
        tagsString = ""
        for tag in tagsArray:
            tagsString += tag+", "
        return tagsString

    def buttonClicked(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if (file):
            QMetaObject.invokeMethod(
                self.view.rootObject(), "clear")
            #QMetaObject.invokeMethod(
             #   self.view.rootObject(), "showBusyIndicator")
        self.startProcessing(file)

    def selectSortDirPath(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if (file):
            self.sortDirPath = file
            QMetaObject.invokeMethod(self.view.rootObject(), "setSortDitPathTextField", Q_ARG(QVariant, file))
            
    def getAllImagePathFromDir(self, directoryPath):
        fileNameArray = []
        for (dirpath, dirnames, filenames) in walk(directoryPath):
            fileNameArray.extend(filenames)
            break
        for idx in range(len(fileNameArray)):
            fileNameArray[idx] = directoryPath+"/"+fileNameArray[idx]
        return fileNameArray

    def getImageInformationFromKhiena(self, fileNameArray):
        imgInfoArray = []
        print(fileNameArray)
        for idx in range(len(fileNameArray)):
            imgInfoArray.append(apiKhiena.imgSearch(fileNameArray[idx]))
            if (idx % 2 == 0):
                time.sleep(10)

        print("============")
        # print(imgInfoArray)
        return imgInfoArray

    def startProcessing(self, pathToDir):
        fileNameArray = self.getAllImagePathFromDir(pathToDir)
        fileImageInfoArray = self.getImageInformationFromKhiena(fileNameArray)
        imgCounter = 0
        for imageInfo in fileImageInfoArray:
            if (not imageInfo["source"]):
                continue
            imgInfo = imgUrlGetter.getImgInfoFromUrl(imageInfo["source"])
            completeSourceText = '<a href="' + \
                imageInfo["source"]+'"+>'+imageInfo["source"]+'</a>'
            print("img Path: "+imgInfo["imgLink"])
            stringTags = self.getTagsString(imgInfo["tags"])
            if (imageInfo["rating"]==0):
                stringTags += "safe, "
            elif  (imageInfo["rating"]==1):
                stringTags += "questionable, "
            elif  (imageInfo["rating"]==2):
                stringTags += "explicit, "
            
            print("RATING: ",imageInfo["rating"])

            stringTags += "artist:"+imageInfo["artist"]
            similarity = imageInfo["similarity"]
            colorRowRect = "#f2ca7d"
            if similarity < 90:
                colorRowRect = "#f04747"

            btnName = "sendBtnName"+str(imgCounter)
            value = {"similarity": similarity,
                     "source": completeSourceText,
                     "localImgPath": imageInfo["localImgPath"],
                     "remoteImgPath": imgInfo["imgLink"],
                     "tags": stringTags,
                     "colorRowRect": colorRowRect,
                     "sendBtnName":btnName}
            # print(value)
            imgCounter+=1
            QMetaObject.invokeMethod(
                self.view.rootObject(), "append", Q_ARG(QVariant, value))
            
            #print(btnName)
            #sendButton = self.view.findChild(QObject, "sendBtnName0")
            #print(sendButton)
            #sendButton.clicked.connect(self.sendImgToGallery)

        #QMetaObject.invokeMethod(
        #        self.view.rootObject(), "hideBusyIndicator")

    def on_qml_mouse_clicked(self):
        print('mouse clicked')

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.view = QQuickView()
        self.view.setSource(QUrl('mainWin.qml'))
        self.view.rootContext().setContextProperty("ex",self)
        self.sortDirPath = ""
        openFolderButton = self.view.findChild(QObject, "toolButton")
        openFolderButton.clicked.connect(self.buttonClicked)

        selectSortDirButton = self.view.findChild(QObject, "selectSortDirButton")
        selectSortDirButton.clicked.connect(self.selectSortDirPath)

        child = self.view.findChild(QObject, "limgListModel")

        imageInfo = {"idshnik": 4,
                     'similarity': 80.859408,
                     'title': "Dragons' Journeyby Selianth",
                     'source': 'https://furrynetwork.com/artwork/1382822',

                     'artist': 'selianth',
                     'rating': 0,
                     'localImgPath': '/home/ /драконы-неразр-тест/425808117_107442_11461217378126189089.jpg'}
        colorRowRect = "#f2ca7d"
        value1 = {'similarity': 97.144509,
                  'source': '<a href="https://furrynetwork.com/artwork/341709">https://furrynetwork.com/artwork/341709</a>',
                  'localImgPath': '/home/ /драконы-неразр-тест/246938919_136836_11381943016272256370.jpg',
                  'remoteImgPath': 'https://d3gz42uwgl1r1y.cloudfront.net/ko/kodar/submission/2016/02/1dac4b544380d5874a518047f24b4eb2.jpg',
                  'tags': "artist:Kodar, any, dragon, fantasy, western",
                  "colorRowRect": colorRowRect,
                  "sendBtnName":"sendBtn0"}

        value = {"similarity": imageInfo["similarity"],
                 "source": imageInfo["source"],
                 "localImgPath": imageInfo["localImgPath"],
                 }
        QMetaObject.invokeMethod(
            self.view.rootObject(), "append", Q_ARG(QVariant, value1))
        self.view.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
