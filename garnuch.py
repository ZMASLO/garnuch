from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from Domain.View.MemeView import MemeView
import sys

def main():
    app = QApplication([])
    window = MemeView()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()