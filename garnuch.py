from requests import get
from bs4 import BeautifulSoup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from threading import Thread


class Meme():
    def __init__(self, title, image):
        self.title = title
        self.image = image

    def __str__(self):
        return '{}: {}'.format(self.title, self.image_url)

class ApiKwejk():
    def __init__(self):
        self.url = 'https://kwejk.pl/'
        self.page_number = ''

    def load_memes(self):
        page = BeautifulSoup(get(self.url).text, 'html.parser')
        for meme in page.find_all('div', attrs={'class': 'media-element'}):
            self.title = meme.find('h2').text.strip()
            self.image_url = meme['data-image']
            self.image = get(self.image_url).content
            yield Meme(self.title, self.image)

    def next_page(self):
        if self.page_number == '':
            page = get(self.url)
        else:
            page = get(self.url+'/strona/'+self.page_number)
        page = BeautifulSoup(page.text, 'html.parser')
        next_page_url = page.find('div', attrs={'class': 'pagination'}).find('a', attrs={'class': 'btn btn-next btn-gold'})['href']
        self.url = next_page_url
        print('Next page')

class ApiJbzdy():
    def __init__(self):
        self.url = 'https://jbzdy.com.pl'
        self.page_number = ''

    def load_memes(self):
        page = BeautifulSoup(get(self.url).text, 'html.parser')
        for meme in page.find_all('div', attrs={'class': 'content-info'}):
            self.title = meme.find('div', attrs={'class': 'title'}).text.strip()
            self.image_url = meme.find('img', attrs={'class': 'resource-image'})['src']
            self.image = get(self.image_url).content
            yield Meme(self.title, self.image)

    def next_page(self):
        page = get(self.url+'/str/'+self.page_number)
        page = BeautifulSoup(page.text, 'html.parser')
        next_page_url = page.find('div', attrs={'class': 'content pagg'}).find('a', attrs={'class': 'btn-next-page'})['href']
        self.url = next_page_url
        print('Next page')

class ApiAdapter(QObject):
    meme_loaded = pyqtSignal(Meme)

    def __init__(self, apiName, *args, **kwargs):
        super().__init__(*args, **kwargs, )
        # default is Kwejk
        self.api = ApiKwejk()
        self.memes = self.api.load_memes()
    
    def changeApi(self, apiName):
        if apiName == 'kwejk':
            self.api = ApiKwejk()
        elif apiName == 'jbzdy':
            self.api = ApiJbzdy()
        self.memes = self.api.load_memes()

    def load_meme(self):
        try:
            meme = next(self.memes)
        except StopIteration:
            self.api.next_page()
            self.memes = self.api.load_memes()
            meme = next(self.memes)
        finally:
            self.meme_loaded.emit(meme)

class MemeView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apiSelected = 'kwejk'
        self.apiAdapter = ApiAdapter(self.apiSelected)
        self.meme_image = None
        self.init_ui()
        self.connect_slots()

    def init_ui(self):
        self.setWindowTitle("Kwejk")
        self.setCentralWidget(QWidget())
        self.buttons = QWidget()
        self.controlButtons = QWidget()
        self.display = QWidget()
        self.buttons.setFixedHeight(50)

        self.centralWidget().setLayout(QVBoxLayout())
        self.centralWidget().layout().addWidget(self.buttons)
        self.centralWidget().layout().addWidget(self.display)
        self.centralWidget().layout().addWidget(self.controlButtons)

        self.kwejkButton = QPushButton('Kwejk')
        self.jbzdyButton = QPushButton('Jbzdy')

        self.load_next_button = QPushButton('Załaduj następny')

        self.buttons.setLayout(QHBoxLayout())
        self.controlButtons.setLayout(QHBoxLayout())
        self.display.setLayout(QVBoxLayout())

        self.meme_title = QLabel()
        self.image = QLabel()

        self.meme_title.setAlignment(Qt.AlignCenter)

        self.buttons.layout().addWidget(self.jbzdyButton)
        self.buttons.layout().addWidget(self.kwejkButton)

        self.controlButtons.layout().addWidget(self.load_next_button)

        self.display.layout().addWidget(self.meme_title)
        self.display.layout().addWidget(self.image)
        
        
        self.display.layout().setAlignment(Qt.AlignCenter)

        self.setMinimumSize(300,600)


    @pyqtSlot(Meme)
    def meme_loaded(self, meme):
        self.meme_title.setText(meme.title)
        self.meme_image = meme.image
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(meme.image)
        self.pixmap = self.pixmap.scaled(self.display.width(), self.display.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image.setPixmap(self.pixmap)


    def connect_slots(self):
        self.apiAdapter.meme_loaded.connect(self.meme_loaded)
        self.load_next_button.clicked.connect(self.load_memes)
        self.jbzdyButton.clicked.connect(lambda:self.changeApi('jbzdy'))
        self.kwejkButton.clicked.connect(lambda:self.changeApi('kwejk'))
        

    def changeApi(self, api):
        print(api)
        self.setWindowTitle(api)
        self.apiAdapter.changeApi(api)

    def load_memes(self):
        Thread(target=self.apiAdapter.load_meme).run()

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        if self.meme_image is not None:
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.meme_image)
            self.pixmap = self.pixmap.scaled(self.display.width(), self.display.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image.setPixmap(self.pixmap)

def main():
    app = QApplication([])
    window = MemeView()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()