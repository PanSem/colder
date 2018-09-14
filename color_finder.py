import  win32api
import win32gui
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame,
    QColorDialog, QApplication)
from PyQt5.QtGui import QColor
from PyQt5 import QtCore
import sys

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        col = QColor(0, 0, 0)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())
        self.frm.setGeometry(130, 22, 100, 100)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.showDialog)
        self.timer.start(0)
        self.show()

    def showDialog(self):

        col = QColor(0, 0, 0)

        mouse_pos = win32api.GetCursorPos()
        mouse_pos_x, mouse_pos_y = win32api.GetCursorPos()
        color = win32gui.GetPixel(win32gui.GetDC(None), mouse_pos_x, mouse_pos_y)
        red = color & 255
        green = (color >> 8) & 255
        blue = (color >> 16) & 255
        print("rgb(" + str(red) + "," + str(green) + "," + str(blue) + ")")

        col.setRgb(red, green, blue)

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % col.name())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
