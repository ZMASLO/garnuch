from bs4 import BeautifulSoup
from requests import get
from .meme import Meme
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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