"""
MIT License

Copyright (c) 2020 Davide De Tommaso, Adam Lukomski - Social Cognition in Human-Robot Interaction

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from dekla.core import DeklaModule

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GUIConfig:
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    FULLSCREEN_DEFAULT = False

"""
class DStack(QStackedLayout):

    def __init__(self, window):
        super().__init__()
        window.setLayout(self)
"""
"""
class DWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(GUIConfig.WINDOW_MIN_WIDTH, GUIConfig.WINDOW_MIN_HEIGHT)
        self._lock = threading.Lock()

    def paintEvent(self, event):
        with self._lock:
            super().paintEvent(event)

    def saveImage(self):
        with self._lock:
            image = self.grab().toImage()
            ba = QByteArray()
            buf = QBuffer(ba)
            buf.open(QIODevice.WriteOnly)
            image.save(buf, "PNG")
            return ba.data()
"""

class DWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # changing the background color to yellow
        self.setStyleSheet("background-color: yellow;")

        # set the title
        self.setWindowTitle("Color")

        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)

        # creating a label widget
        self.label = QLabel("Yellow", self)

        # moving position
        self.label.move(100, 100)

        # setting up border
        self.label.setStyleSheet("border: 1px solid black;")

        # show all the widgets
        self.show()

class MainWindow(QMainWindow):

    def __init__(self, guimanager):
        QMainWindow.__init__(self)
        self.setWindowTitle("Dekla")
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.view_menu = self.menu.addMenu("View")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        fullscreen_action = QAction("Fullscreen mode", self)
        fullscreen_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_F))
        fullscreen_action.triggered.connect(lambda x: self.setWindowState(Qt.WindowFullScreen))

        window_action = QAction("Window mode", self)
        window_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_W))
        window_action.triggered.connect(lambda x: self.setWindowState(Qt.WindowNoState))

        self.file_menu.addAction(exit_action)
        self.view_menu.addAction(fullscreen_action)
        self.view_menu.addAction(window_action)
        self.status = self.statusBar()
        self.status.showMessage("status bar ...")

class QtGUIManager(DeklaModule, QObject):

    def __init__(self, deklamaster_address=('localhost', 9966)):
        DeklaModule.__init__(self, deklamaster_address)
        self._QApp = QApplication([])
        self._widgets = dict()
        self._widgets['main'] = MainWindow(self)
        self._fullscreen_mode = GUIConfig.FULLSCREEN_DEFAULT
        self.show()
        self._QApp.exec()

    def show(self):
        for widget in self._widgets.values():
            widget.show()

    def setFullscreen(self):
        self._fullscreen_mode = not self._fullscreen_mode
        for widget in self._widgets.values():
            if self._fullscreen_mode:
                widget.setWindowState(Qt.WindowFullScreen)
            else:
                widget.setWindowState(Qt.WindowNoState)
