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

import color_finder
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':

    #Start app
    app = QApplication(sys.argv)
    color_finder = color_finder.ColorFinder()
    sys.exit(app.exec_())
