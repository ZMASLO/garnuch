from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QlabelFactory:
    def memeFactory(self, image):
            qlabel = QLabel()
            qlabel.setPixmap(image)
            return qlabel

    def titleFactory(self, text):
            qlabel = QLabel()
            qlabel.setText(text)
            return qlabel