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

import  win32api
import win32gui
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame,
    QLabel, QShortcut, QInputDialog, QDialog)
from PyQt5.QtGui import QColor, QFont, QKeySequence, QIcon
from PyQt5 import QtCore
import clipboard
import os

class ColorFinder(QWidget):
    """Window class"""

    def __init__(self):
        """Initialize window"""

        super().__init__()

        self.color_finder_ui()

    def color_finder_ui(self):
        """Function which sets window"""

        #Set color for the frame
        col = QColor(0, 0, 0)

        #Lists to keep color values and the name of them
        self.color_rgb = []
        self.color_hex = []
        self.color_name = []

        #Create color frame, color it and set its postion and size
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())
        self.frm.setGeometry(140, 5, 120, 120)

        #Create rgb(r, g, b) label, set its font, postion and size
        font = QFont("Arial", 12)
        self.lbl1 = QLabel("rgb(0, 0, 0)", self)
        self.lbl1.move(10, 10)
        self.lbl1.resize(150, 20)
        self.lbl1.setFont(font)

        #Create hex #xxxxxx label, set its font, postion and size
        self.lbl2 = QLabel("#000000", self)
        self.lbl2.move(30, 50)
        self.lbl2.resize(150, 20)
        self.lbl2.setFont(font)

        #Create help button and set postion
        self.btn = QPushButton("Help", self)
        self.btn.move(25, 90)
        self.btn.clicked.connect(self.showDialog)

        #Create shortcut for copy color value
        copy_color = QShortcut(QKeySequence(QtCore.Qt.Key_C), self)
        copy_color.activated.connect(self.copyColor)

        #Create shortcut for save color value
        save_color = QShortcut(QKeySequence(QtCore.Qt.Key_S), self)
        save_color.activated.connect(self.saveColor)

        #Create shortcut for export saved color values
        export_color = QShortcut(QKeySequence(QtCore.Qt.Key_E), self)
        export_color.activated.connect(self.exportColor)

        #Set postion, size and title for main window
        self.setGeometry(300, 300, 270, 130)
        self.setFixedSize(270, 130)
        self.setWindowTitle("Colder")

        #Set timer to call continuously takeColor function
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.takeColor)
        self.timer.start(0)

        #Set icon for main window
        self.setWindowIcon(QIcon("colder.png"))

        #Show window
        self.show()

    def takeColor(self):

        #Set color for the frame
        col = QColor(0, 0, 0)

        #Get mouse position
        mouse_pos = win32api.GetCursorPos()
        mouse_pos_x, mouse_pos_y = win32api.GetCursorPos()

        #Get pixel color
        color = win32gui.GetPixel(win32gui.GetDC(None), mouse_pos_x, mouse_pos_y)

        #Make color to rgb values
        red = color & 255
        green = (color >> 8) & 255
        blue = (color >> 16) & 255
        print("rgb(" + str(red) + "," + str(green) + "," + str(blue) + ")")
        print("#%02x%02x%02x" % (red, green, blue))

        #Change frame color
        col.setRgb(red, green, blue)

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % col.name())

        #Print color values to rgb and hex
        self.lbl1.setText("rgb(" + str(red) + "," + str(green) + "," + str(blue) + ")")
        self.lbl2.setText("#%02x%02x%02x" % (red, green, blue))

    def copyColor(self):
        """Function which copies color value"""

        self.timer.timeout.disconnect(self.takeColor)
        clipboard.copy(self.lbl2.text())
        self.timer.timeout.connect(self.takeColor)

    def saveColor(self):
        """Function which saves color value"""

        self.timer.timeout.disconnect(self.takeColor)

        #Take the name of the saved color value
        text, ok = QInputDialog.getText(self, "Input Dialog",
            "Enter color name:")

        #Save color value in rgb and hex and its name
        if ok:
            self.color_rgb.append(self.lbl1.text())
            self.color_hex.append(self.lbl2.text())
            self.color_name.append(str(text))

        self.timer.timeout.connect(self.takeColor)

    def exportColor(self):
        """Function which exports color values"""

        #Check if there is a value to be saved
        if len(self.color_name) != 0:

            #Open file to save color calues
            f = open(os.path.expanduser("~\\Desktop") + "\\exportColor.txt", "w")
            f.write("Color values \n")

            #Write color values to the file
            for i in range(0, len(self.color_name)):
                f.write(self.color_name[i] + ": " + self.color_rgb[i] + ", " + self.color_hex[i] + "\n")

            #Delete saved values
            self.color_rgb = []
            self.color_hex = []
            self.color_name = []

            #Create dialog window, name it and set its postion and size
            dialog_file = QDialog(self)
            dialog_file.setGeometry(320, 350, 230, 50)
            dialog_file.setFixedSize(230, 50)
            dialog_file.setWindowTitle("Complete")

            #Create label, set its font, postion and size
            font = QFont("Arial", 12)
            dialog_file.lbl1 = QLabel("File: exportColor.txt created", dialog)
            dialog_file.lbl1.move(20, 7)
            dialog_file.lbl1.resize(200, 40)
            dialog_file.lbl1.setFont(font)

            #Show dialog window
            dialog_file.show()

    def showDialog(self):
        """Function which creates help window"""

        #Create dialog window, name it and set its postion and size
        dialog = QDialog(self)
        dialog.setGeometry(340, 270, 200, 190)
        dialog.setFixedSize(200, 190)
        dialog.setWindowTitle("Help")

        #Create label, set its font, postion and size
        font = QFont("Arial", 12)
        dialog.lbl1 = QLabel(" Type [C] to copy \n" + "current color value", dialog)
        dialog.lbl1.move(30, 10)
        dialog.lbl1.resize(150, 40)
        dialog.lbl1.setFont(font)

        #Create label, set its font, postion and size
        dialog.lbl2 = QLabel("  Type [S] to save \n" + "current color value \n" + "    in a file which \n can be exported", dialog)
        dialog.lbl2.move(30, 64)
        dialog.lbl2.resize(150, 80)
        dialog.lbl2.setFont(font)

        #Create label, set its font, postion and size
        dialog.lbl3 = QLabel("Type [E] to export file", dialog)
        dialog.lbl3.move(27, 130)
        dialog.lbl3.resize(150, 80)
        dialog.lbl3.setFont(font)

        #Show dialog window
        dialog.show()
