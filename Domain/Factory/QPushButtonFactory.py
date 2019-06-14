from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QPushButtonFactory:
    def imageButtonFactory(self, label):
            button = QPushButton(label)
            button.setFixedSize(QSize(100,30))
            return button