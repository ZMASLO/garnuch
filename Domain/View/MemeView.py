from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from threading import Thread
from Domain.Api.ApiAdapter import *
from Domain.Factory.QlabelFactory import *
from Domain.Factory.QPushButtonFactory import *

class MemeView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apiSelected = 'kwejk'
        self.apiAdapter = ApiAdapter(self.apiSelected)
        self.meme_image = None
        self.init_ui()
        self.connectSlots()
        self.qlabelFactory = QlabelFactory()
        self.qpushButtonFactory = QPushButtonFactory()

    def init_ui(self):
        self.setWindowTitle("Garnuch z memami")
        self.setCentralWidget(QWidget())
        self.buttons = QWidget()
        self.display = QWidget()

        self.centralWidget().setLayout(QVBoxLayout())
        self.centralWidget().layout().addWidget(self.buttons)
        self.centralWidget().layout().addWidget(self.display)

        self.kwejkButton = QPushButton('Kwejk')
        self.jbzdyButton = QPushButton('Jbzdy')
        self.testButton = QPushButton('test')

        self.buttons.setLayout(QHBoxLayout())
        self.display.setLayout(QVBoxLayout())

        self.currentApi = QLabel()
        self.display.layout().addWidget(self.currentApi)
        
        self.buttons.layout().addWidget(self.jbzdyButton)
        self.buttons.layout().addWidget(self.kwejkButton)
        self.buttons.layout().addWidget(self.testButton)
        
        #scroll area section
        self.imagesWidget = QWidget()
        self.imagesLayout = QVBoxLayout(self.imagesWidget)
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imagesWidget)
        self.display.layout().addWidget(self.scrollArea)
        self.display.layout().setAlignment(Qt.AlignCenter)

        self.setMinimumSize(300,600)
        self.scrollAreaHeight = 0
        self.scrollBar = self.scrollArea.verticalScrollBar()
        self.imagesWidget.resize(500, self.scrollAreaHeight)

    @pyqtSlot(Meme)
    def memeLoaded(self, meme):
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(meme.image)
        self.pixmap = self.pixmap.scaledToWidth(self.display.width()-60)
        
        self.scrollAreaHeight += self.pixmap.height()+25
        self.imagesWidget.resize(self.display.width()-60,self.scrollAreaHeight)
        self.imagesLayout.addWidget(self.qlabelFactory.titleFactory(meme.title))
        self.imagesLayout.addWidget(self.qlabelFactory.memeFactory(self.pixmap))
        self.imagesLayout.addWidget(self.imagesButtonsAdd())
        self.imagesButtonsConnect()
        
    # add buttons like save and copy
    def imagesButtonsAdd(self):
        imageButtonsWidget = QWidget()
        imageButtonsWidget.setLayout(QHBoxLayout())
        imageButtonsWidget.layout().addWidget(self.qpushButtonFactory.imageButtonFactory('Zapisz'))
        imageButtonsWidget.layout().addWidget(self.qpushButtonFactory.imageButtonFactory('Kopiuj'))
        # connect new buttons
        return imageButtonsWidget
        
    # connect slots to dynamic buttons
    def imagesButtonsConnect(self):
        # add connect button and pass to image
        itemsCount = self.imagesLayout.count()
        print(itemsCount)
        # self.imagesLayout.itemAt(itemsCount-2).widget().clicked.connect(lambda:self.imageSave(self.imagesLayout.itemAt(itemsCount-3).widget().pixmap()))
        # self.imagesLayout.itemAt(itemsCount-1).widget().clicked.connect(lambda:self.imageCopyToClipboard(self.imagesLayout.itemAt(itemsCount-3).widget().pixmap()))
        buttonsWidget = self.imagesLayout.itemAt(itemsCount-1).widget().layout()
        # save button
        buttonsWidget.itemAt(0).widget().clicked.connect(lambda:self.imageSave(self.imagesLayout.itemAt(itemsCount-2).widget().pixmap()))
        # copy button
        buttonsWidget.itemAt(1).widget().clicked.connect(lambda:self.imageCopyToClipboard(self.imagesLayout.itemAt(itemsCount-2).widget().pixmap()))

    def connectSlots(self):
        self.apiAdapter.memeLoaded.connect(self.memeLoaded)
        self.jbzdyButton.clicked.connect(lambda:self.changeApi('jbzdy'))
        self.kwejkButton.clicked.connect(lambda:self.changeApi('kwejk'))
        self.testButton.clicked.connect(self.testFunction)
        self.scrollBar.valueChanged.connect(self.endOfBarDetection)
        
    def testFunction(self):
        print('no siema')
        self.imageCopyToClipboard()
    
    def imageCopyToClipboard(self, image):
        clipboard =  QApplication.clipboard()
        clipboard.setPixmap(image)

    def imageSave(self, image):
        name, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","JPG (*.jpg);;PNG (*.png)")
        image.save(name, 'jpg')

    # if detected end of memes load more
    def endOfBarDetection(self):
        if self.scrollBar.value() == self.scrollBar.maximum():
            # for x in range(5):
            self.loadMemes()

    def changeApi(self, api):
        print(api)
        self.apiAdapter.changeApi(api)
        self.currentApi.setText(api)
        self.clearLayout(self.imagesLayout)
        self.scrollAreaHeight = 0
        self.scrollBar.setValue(0)
        self.currentApi.setText(api)
        self.loadMemes()

    def loadMemes(self):
        Thread(target=self.apiAdapter.loadMeme).run()
        self.endOfBarDetection()

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        self.imagesWidget.resize(self.display.width()-60,self.scrollAreaHeight)
        
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                child.widget = None
