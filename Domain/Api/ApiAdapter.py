from ..Meme.Meme import Meme
from .Kwejk.ApiKwejk import ApiKwejk
from .Jbzdy.ApiJbzdy import ApiJbzdy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ApiAdapter(QObject):
    memeLoaded = pyqtSignal(Meme)

    def __init__(self, apiName, *args, **kwargs):
        super().__init__(*args, **kwargs, )
        # default is Kwejk
        self.api = ApiKwejk()
        self.memes = self.api.loadMemes()
    
    def changeApi(self, apiName):
        if apiName == 'kwejk':
            self.api = ApiKwejk()
        elif apiName == 'jbzdy':
            self.api = ApiJbzdy()
        self.memes = self.api.loadMemes()

    def loadMeme(self):
        try:
            meme = next(self.memes)
        except StopIteration:
            self.api.nextPage()
            self.memes = self.api.loadMemes()
            meme = next(self.memes)
        finally:
            self.memeLoaded.emit(meme)

