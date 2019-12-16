#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

app = QApplication([])

class CuteView(QVideoWidget):
        def __init__(self):
                super().__init__()
                self.setMinimumSize(640,480)
                
                self.player = QMediaPlayer()
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(QFileInfo("test1.mp4").absoluteFilePath())))
                self.player.setVideoOutput(self)
                self.player.play()
        def full(self):
                if not self.windowState() == Qt.WindowFullScreen:
                        self.setWindowState(Qt.WindowFullScreen)
                else:
                        self.setWindowState(Qt.WindowNoState)
        def keyPressEvent(self,event):
                print( event.key() )
                if event.key() == Qt.Key_F:
                        self.full()
                if event.key() == Qt.Key_Q:
                        app.quit()
                if event.key() == Qt.Key_S:
                        self.player.play()
                if event.key() == Qt.Key_P:
                        self.player.pause()
label = CuteView()
label.show()

app.exec()
