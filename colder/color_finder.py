"""This file is part of color_finder.

    color_finder is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>."""

import win32api
import win32gui
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame,
                             QLabel, QShortcut, QInputDialog, QDialog, QMainWindow, QLineEdit, QComboBox)
from PyQt5.QtGui import QColor, QFont, QKeySequence, QIcon, QImage, QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPoint
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
import clipboard
import os
import sys

#The svg of the icon of the program
svg_str = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="20" height="20" viewBox="0 0 184 196" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M97.963 43.9345L100.397 41.4576L126.642 15.2268L118.245 6.82163L97.963 27.1241V0H86.0776V27.1241L65.7954 6.82163L57.3986 15.2268L83.6032 41.4576L86.0776 43.9345V98.0203V152.065L83.6032 154.542L57.3986 180.773L65.7954 189.178L86.0776 168.917V196H97.963V168.917L118.245 189.178L126.642 180.773L100.397 154.542L97.963 152.065V98.0203V43.9345Z" fill="#EC3232"/>
<path d="M42.2681 119.906L38.9012 118.972L3.08289 109.39L0 120.881L27.7055 128.312L4.25926 141.833L10.1817 152.147L33.6279 138.585L26.2452 166.318L37.6843 169.404L47.298 133.55L48.1905 130.179L95.0018 103.136L141.772 76.1342L145.139 77.0275L180.917 86.6103L184 75.1191L156.335 67.6884L179.781 54.1669L173.818 43.8533L150.372 57.4153L157.795 29.6822L146.316 26.5962L136.742 62.4503L135.81 65.8206L89.0388 92.8634L42.2681 119.906Z" fill="#5ACC5A"/>
<path d="M135.81 130.179L136.742 133.55L146.316 169.404L157.795 166.318L150.372 138.585L173.818 152.147L179.781 141.833L156.335 128.312L184 120.881L180.917 109.39L145.139 118.972L141.772 119.906L95.0018 92.8634L48.1905 65.8206L47.298 62.4503L37.6843 26.5962L26.2452 29.6822L33.6279 57.4153L10.1817 43.8533L4.25926 54.1669L27.7055 67.6884L0 75.1191L3.08289 86.6103L38.9012 77.0275L42.2681 76.1342L89.0388 103.136L135.81 130.179Z" fill="#5050B5"/>
</svg>
"""

svg_bytes = bytearray(svg_str, encoding='utf-8')

class ColorFinder(QWidget):
    """Window class"""

    def __init__(self):
        """Initialize window"""

        super().__init__()

        self.mainw = QMainWindow(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.color_finder_ui()

    def color_finder_ui(self):
        """Function which sets window"""

        # Set color for the frame
        col = QColor(0, 0, 0)

        # Lists to keep color values and the name of them
        self.color_rgb = []
        self.color_hex = []
        self.color_name = []
        self.frm10 = []
        self.temp = []
        self.i = 0 #Current place which is empty of color
        self.color_places = 14 #Places in the ui in which the colors are visible

        # Create color frame, color it and set its postion and size
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
                               % col.name())
        self.frm.setGeometry(0, 40, 270, 120)

        sp = 20; #Space between the colors
        bg_color = "%02x%02x%02x" % (240, 240, 240)

        #Adjust the first seven boxes of colors
        for i in range(0, 7):
            self.frm10.append(QFrame(self))
            self.frm10[i].setStyleSheet("QWidget { background-color: #" +  str(bg_color) +"; border:1px solid #000000; border-radius: 2px;}")
            self.frm10[i].setGeometry(15+sp, 230, 20, 20)
            sp = sp + 20 + 10
            self.temp.append(bg_color)

        sp = 20;

        #Adjust the other seven boxes of colors
        for i in range(7, 14):
            self.frm10.append(QFrame(self))
            self.frm10[i].setStyleSheet("QWidget { background-color: #" +  str(bg_color) +"; border:1px solid #000000; border-radius: 2px;}")
            self.frm10[i].setGeometry(15+sp, 260, 20, 20)
            sp = sp + 20 + 10
            self.temp.append(bg_color)

        #Icon of the program
        qimage = QImage.fromData(svg_bytes)

        self.label = QLabel(self)
        pixmap = QPixmap(qimage)
        self.label.setPixmap(pixmap)
        self.label.move(20, 10)
        self.label.resize(20, 20)

        font = QFont("Arial", 12)
        self.lbl3 = QLabel("Colder", self)
        self.lbl3.setStyleSheet("QWidget { color: #5252b6; }")
        self.lbl3.move(50, 5)
        self.lbl3.resize(70, 30)
        self.lbl3.setFont(font)

        self.cb = QComboBox(self)
        self.cb.addItem("RGB")
        self.cb.addItem("HEX")
        self.cb.move(60, 180)
        self.cb.resize(50, 25)

        # Create rgb(r, g, b) label, set its font, postion and size
        font = QFont("Arial", 12)
        self.lbl1 = QLabel("#000000", self)
        self.lbl1.setStyleSheet("QWidget { color: #292930; }")
        self.lbl1.move(130, 182)
        self.lbl1.resize(100, 20)
        self.lbl1.setFont(font)

        font = QFont("Arial", 12)
        self.lbl2 = QPushButton("x", self)
        self.lbl2.setStyleSheet("QWidget { border: none; background-color: none; } \
        QWidget:hover { color: #e04343; }")

        self.lbl2.move(240, 4)
        self.lbl2.resize(20, 30)
        self.lbl2.setFont(font)
        self.lbl2.clicked.connect(self.close)

        font = QFont("Arial", 15)
        self.lbl4 = QPushButton("-", self)
        self.lbl4.setStyleSheet("QWidget { border: none; background-color: none; } \
        QWidget:hover { color: #e04343; }")

        self.lbl4.move(225, 3)
        self.lbl4.resize(20, 30)
        self.lbl4.setFont(font)
        self.lbl4.clicked.connect(lambda: self.showMinimized())

        # Create help button and set postion
        self.btn = QPushButton("Help", self)
        self.btn.move(95, 300)
        self.btn.clicked.connect(self.showDialog)

        # Create shortcut for copy color value
        copy_color = QShortcut(QKeySequence(QtCore.Qt.Key_C), self)
        copy_color.activated.connect(self.copyColor)

        # Create shortcut for save color value
        save_color = QShortcut(QKeySequence(QtCore.Qt.Key_S), self)
        save_color.activated.connect(self.saveColor)

        # Create shortcut for export saved color values
        export_color = QShortcut(QKeySequence(QtCore.Qt.Key_E), self)
        export_color.activated.connect(self.exportColor)

        # Set postion, size and title for main window
        self.setGeometry(300, 300, 270, 350)
        self.setFixedSize(270, 350)
        self.setWindowTitle("Colder")

        # Set timer to call continuously takeColor function
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.takeColor)
        self.timer.start(0)


        # Show window
        self.show()

    def takeColor(self):

        # Set color for the frame
        col = QColor(0, 0, 0)

        # Get mouse position
        mouse_pos = win32api.GetCursorPos()
        mouse_pos_x, mouse_pos_y = win32api.GetCursorPos()

        try:
            # Get pixel color
            color = win32gui.GetPixel(
                win32gui.GetDC(None), mouse_pos_x, mouse_pos_y)
        except:
            print(Error)

        # Make color to rgb values
        red = color & 255
        green = (color >> 8) & 255
        blue = (color >> 16) & 255
        print("rgb(" + str(red) + "," + str(green) + "," + str(blue) + ")")
        print("#%02x%02x%02x" % (red, green, blue))

        # Change frame color
        col.setRgb(red, green, blue)

        if col.isValid():
            self.frm.setStyleSheet("QWidget {background-color: %s }"
                                   % col.name())

        self.col = "%02x%02x%02x" % (red, green, blue)

        # Print color values to rgb and hex
        if self.cb.currentText()=="RGB":
            self.lbl1.setText(
                str(red) + " " + str(green) + " " + str(blue))
        else:
            self.lbl1.setText("%02x%02x%02x" % (red, green, blue))

    def copyColor(self):
        """Function which copies color value"""

        self.timer.timeout.disconnect(self.takeColor)
        clipboard.copy(self.lbl1.text())
        self.timer.timeout.connect(self.takeColor)
        if self.i==self.color_places:
            print(self.temp)
            self.i = 0

        #Print color value to the cmd
        if self.col in self.temp:
            print(self.col)
            return

        self.temp[self.i] = self.col

        #Put color in the right place and increment by 1 so the next place can be found
        self.frm10[self.i].setStyleSheet("QWidget { background-color: #" +  str(self.col) +"; border:1px solid #000000; border-radius: 2px;}")
        self.i = self.i + 1

    def saveColor(self):
        """Function which saves color value"""

        self.timer.timeout.disconnect(self.takeColor)

        # Take the name of the saved color value
        text, ok = QInputDialog.getText(self, "Input Dialog",
                                        "Enter color name:")

        # Save color value in rgb and hex and its name
        if ok:
            self.color_rgb.append(self.lbl1.text())
            a2 = self.lbl1.text().split(" ")
            self.color_hex.append("%02x%02x%02x" % (int(a2[0]), int(a2[1]), int(a2[2])))
            self.color_name.append(str(text))

        self.timer.timeout.connect(self.takeColor)

    def exportColor(self):
        """Function which exports color values"""

        # Check if there is a value to be saved
        if len(self.color_name) != 0:

            # Open file to save color calues
            with open(os.path.expanduser("~\\Desktop") +
                     "\\exportColor.txt", "a") as f:
                f.write("Color values \n")

                # Write color values to the file
                for i in range(0, len(self.color_name)):
                    f.write(self.color_name[i] + ": "
                            + self.color_rgb[i] + ", "
                            + self.color_hex[i] + "\n")
                f.close()

            # Delete saved values
            self.color_rgb = []
            self.color_hex = []
            self.color_name = []

            # Create dialog window, name it and set its postion and size
            dialog_file = QDialog(self)
            dialog_file.setGeometry(320, 350, 230, 50)
            dialog_file.setFixedSize(230, 50)
            dialog_file.setWindowTitle("Complete")

            # Create label, set its font, postion and size
            font = QFont("Arial", 12)
            dialog_file.lbl1 = QLabel("File: exportColor.txt created",
                                      dialog_file)
            dialog_file.lbl1.move(20, 7)
            dialog_file.lbl1.resize(200, 40)
            dialog_file.lbl1.setFont(font)

            # Show dialog window
            dialog_file.show()

    def showDialog(self):
        """Function which creates help window"""

        # Create dialog window, name it and set its postion and size
        dialog = QDialog(self)
        dialog.setGeometry(340, 270, 200, 190)
        dialog.setFixedSize(200, 190)
        dialog.setWindowTitle("Help")

        # Create label, set its font, postion and size
        font = QFont("Arial", 12)
        dialog.lbl1 = QLabel(" Type [C] to copy \n" +
                             "current color value", dialog)
        dialog.lbl1.move(30, 10)
        dialog.lbl1.resize(150, 40)
        dialog.lbl1.setFont(font)

        # Create label, set its font, postion and size
        dialog.lbl2 = QLabel("  Type [S] to save \n" +
                             "current color value \n" +
                             "    in a file which \n can be exported", dialog)
        dialog.lbl2.move(30, 64)
        dialog.lbl2.resize(150, 80)
        dialog.lbl2.setFont(font)

        # Create label, set its font, postion and size
        dialog.lbl3 = QLabel("Type [E] to export file", dialog)
        dialog.lbl3.move(27, 130)
        dialog.lbl3.resize(150, 80)
        dialog.lbl3.setFont(font)

        # Show dialog window
        dialog.show()

    def mousePressEvent(self, event):
        """Detect mouse press"""
        try:
            self.oldPos = event.globalPos()
        except:
            print("")

    def mouseMoveEvent(self, event):
        """Detect mouse movement"""
        try:
            delta = QPoint (event.globalPos() - self.oldPos)

            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except:
            print("")
