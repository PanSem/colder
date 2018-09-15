import  win32api
import win32gui
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame,
    QColorDialog, QApplication, QLabel, QShortcut, QInputDialog, QDialog)
from PyQt5.QtGui import QColor, QFont, QKeySequence
from PyQt5 import QtCore
import sys
import clipboard
import os

class ColorFinder(QWidget):

    def __init__(self):
        super().__init__()

        self.color_finder_ui()

    def color_finder_ui(self):

        col = QColor(0, 0, 0)

        self.color_rgb = []
        self.color_hex = []
        self.color_name = []

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())
        self.frm.setGeometry(140, 5, 120, 120)

        font = QFont("Arial", 12)
        self.lbl1 = QLabel('rgb(0, 0, 0)', self)
        self.lbl1.move(10, 10)
        self.lbl1.resize(150, 20)
        self.lbl1.setFont(font)

        self.lbl2 = QLabel('#000000', self)
        self.lbl2.move(30, 50)
        self.lbl2.resize(150, 20)
        self.lbl2.setFont(font)

        self.btn = QPushButton('Help', self)
        self.btn.move(25, 90)
        self.btn.clicked.connect(self.showDialog)

        copy_color = QShortcut(QKeySequence(QtCore.Qt.Key_C), self)
        copy_color.activated.connect(self.copyColor)

        save_color = QShortcut(QKeySequence(QtCore.Qt.Key_S), self)
        save_color.activated.connect(self.saveColor)

        export_color = QShortcut(QKeySequence(QtCore.Qt.Key_E), self)
        export_color.activated.connect(self.exportColor)

        self.setGeometry(300, 300, 270, 130)
        self.setFixedSize(270, 130)
        self.setWindowTitle('Color Finder')
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.takeColor)
        self.timer.start(0)
        self.show()

    def takeColor(self):

        col = QColor(0, 0, 0)

        mouse_pos = win32api.GetCursorPos()
        mouse_pos_x, mouse_pos_y = win32api.GetCursorPos()
        color = win32gui.GetPixel(win32gui.GetDC(None), mouse_pos_x, mouse_pos_y)
        red = color & 255
        green = (color >> 8) & 255
        blue = (color >> 16) & 255
        print("rgb(" + str(red) + "," + str(green) + "," + str(blue) + ")")
        print('#%02x%02x%02x' % (red, green, blue))

        col.setRgb(red, green, blue)

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % col.name())

        self.lbl1.setText("rgb(" + str(red) + "," + str(green) + "," + str(blue) + ")")
        self.lbl2.setText('#%02x%02x%02x' % (red, green, blue))

    def copyColor(self):
        self.timer.timeout.disconnect(self.takeColor)
        clipboard.copy(self.lbl2.text())
        self.timer.timeout.connect(self.takeColor)

    def saveColor(self):
        self.timer.timeout.disconnect(self.takeColor)
        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter color name:')

        if ok:
            self.color_rgb.append(self.lbl1.text())
            self.color_hex.append(self.lbl2.text())
            self.color_name.append(str(text))

        self.timer.timeout.connect(self.takeColor)

    def exportColor(self):
        if len(self.color_name) != 0:

            f = open(os.path.expanduser("~\\Desktop") + "\\exportColor.txt", "w")

            for i in range(0, len(self.color_name)):
                f.write(self.color_name[i] + ": " + self.color_rgb[i] + ", " + self.color_hex[i] + "\n")

            self.color_rgb = []
            self.color_hex = []
            self.color_name = []

            dialog = QDialog(self)
            dialog.setGeometry(320, 350, 230, 50)
            dialog.setFixedSize(230, 50)
            dialog.setWindowTitle('Complete')

            font = QFont("Arial", 12)
            dialog.lbl1 = QLabel('File: exportColor.txt created', dialog)
            dialog.lbl1.move(20, 7)
            dialog.lbl1.resize(200, 40)
            dialog.lbl1.setFont(font)

            dialog.show()

    def showDialog(self):

        dialog = QDialog(self)
        dialog.setGeometry(340, 270, 200, 190)
        dialog.setFixedSize(200, 190)
        dialog.setWindowTitle('Help')

        font = QFont("Arial", 12)
        dialog.lbl1 = QLabel(' Type [C] to copy \n' + 'current color value', dialog)
        dialog.lbl1.move(30, 10)
        dialog.lbl1.resize(150, 40)
        dialog.lbl1.setFont(font)

        dialog.lbl2 = QLabel('  Type [S] to save \n' + 'current color value \n' + '    in a file which \n can be exported', dialog)
        dialog.lbl2.move(30, 64)
        dialog.lbl2.resize(150, 80)
        dialog.lbl2.setFont(font)

        dialog.lbl3 = QLabel('Type [E] to export file', dialog)
        dialog.lbl3.move(27, 130)
        dialog.lbl3.resize(150, 80)
        dialog.lbl3.setFont(font)

        dialog.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ColorFinder()
    sys.exit(app.exec_())
