from requests import get
from bs4 import BeautifulSoup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from threading import Thread
from Domain.Api.api import *
from Domain.Factory.QlabelFactory import *
from Views import *
import sys

class MemeView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apiSelected = 'kwejk'
        self.apiAdapter = ApiAdapter(self.apiSelected)
        self.meme_image = None
        self.init_ui()
        self.connectSlots()
        self.qlabelFactory = QlabelFactory()

    def init_ui(self):
        self.setWindowTitle("Garnuch z memami")
        self.setCentralWidget(QWidget())
        self.buttons = QWidget()
        self.controlButtons = QWidget()
        self.display = QWidget()

        self.buttons.setFixedHeight(50)

        self.centralWidget().setLayout(QVBoxLayout())
        self.centralWidget().layout().addWidget(self.buttons)
        self.centralWidget().layout().addWidget(self.display)
        self.centralWidget().layout().addWidget(self.controlButtons)

        #scroll area section
        self.loading = QLabel()
        self.loading.setText('ładuje')
        self.imagesWidget = QWidget()
        self.imagesLayout = QVBoxLayout(self.imagesWidget)
        self.imagesLayout.addWidget(self.loading)
        self.images = []

        self.kwejkButton = QPushButton('Kwejk')
        self.jbzdyButton = QPushButton('Jbzdy')
        self.testButton = QPushButton('test')

        self.load_next_button = QPushButton('Załaduj następny')

        self.buttons.setLayout(QHBoxLayout())
        self.controlButtons.setLayout(QHBoxLayout())
        self.display.setLayout(QVBoxLayout())

        self.currentApi = QLabel()
        self.currentApi.setText('kwejk')
        self.memeTitle = QLabel()
        self.image = QLabel()

        self.memeTitle.setAlignment(Qt.AlignCenter)

        self.buttons.layout().addWidget(self.jbzdyButton)
        self.buttons.layout().addWidget(self.kwejkButton)
        self.buttons.layout().addWidget(self.testButton)

        self.controlButtons.layout().addWidget(self.load_next_button)

        self.display.layout().addWidget(self.currentApi)
        self.display.layout().addWidget(self.memeTitle)
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imagesWidget)
        self.display.layout().addWidget(self.scrollArea)
        self.display.layout().setAlignment(Qt.AlignCenter)

        self.setMinimumSize(300,600)
        self.scrollAreaHeight = 0
        self.scrollBar = self.scrollArea.verticalScrollBar()
        self.imagesWidget.setMinimumWidth(self.display.width()-100)


    @pyqtSlot(Meme)
    def memeLoaded(self, meme):
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(meme.image)
        self.pixmap = self.pixmap.scaledToWidth(self.display.width()-60)
        
        self.scrollAreaHeight += self.pixmap.height()+25
        self.imagesWidget.setMinimumHeight(self.scrollAreaHeight)
        self.imagesLayout.addWidget(self.qlabelFactory.titleFactory(meme.title))
        self.imagesLayout.addWidget(self.qlabelFactory.memeFactory(self.pixmap))
            
    def connectSlots(self):
        self.apiAdapter.memeLoaded.connect(self.memeLoaded)
        self.load_next_button.clicked.connect(self.loadMemes)
        self.jbzdyButton.clicked.connect(lambda:self.changeApi('jbzdy'))
        self.kwejkButton.clicked.connect(lambda:self.changeApi('kwejk'))
        self.testButton.clicked.connect(self.testFunction)
        self.scrollBar.valueChanged.connect(self.endOfBarDetection)
        
    def testFunction(self):
        print('no siema')
        testVar = self.loading.isVisibleTo(self.buttons)
        print(testVar)

    # if detected end of memes load more
    def endOfBarDetection(self):
        if self.scrollBar.value() == self.scrollBar.maximum():
            # for x in range(5):
            self.loadMemes()

    def changeApi(self, api):
        print(api)
        self.clearLayout(self.imagesLayout)
        self.scrollAreaHeight = 0
        self.currentApi.setText(api)
        self.apiAdapter.changeApi(api)

    def loadMemes(self):
        Thread(target=self.apiAdapter.loadMeme).run()

    def resizeEvent(self, QResizeEvent):
        print('wywoalnie')
        super().resizeEvent(QResizeEvent)
        if self.meme_image is not None:
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.meme_image)
            self.pixmap = self.pixmap.scaledToWidth(self.display.width()-60)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # layout.parentWidget().setMinimumHeight(0)

def main():
    app = QApplication([])
    window = MemeView()
    window.show()
    # Create an instance of the application
    # app = QGuiApplication(sys.argv)
    # Create QML engine
    # engine = QQmlApplicationEngine()
    # Create a calculator object
    # calculator = Calculator()
    # And register it in the context of QML
    # engine.rootContext().setContextProperty("calculator", calculator)
    # Load the qml file into the engine
    # engine.load("garnuch/Views/drawer.qml")

    app.exec()


if __name__ == '__main__':
    main()