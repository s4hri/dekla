#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

app = QApplication([])

class CuteView(QLabel):
        def __init__(self):
                super().__init__()
                self.setMinimumSize(640,480)
                layout = QVBoxLayout()

                player = QMediaPlayer()
                player.setMedia(QMediaContent(QUrl.fromLocalFile("/home/anil/test1.mp4")))
                video = QVideoWidget()
                player.setVideoOutput(video)

                player.play()

                layout.addWidget(video)
                self.setLayout(layout)


label = CuteView()
label.show()

app.exec()
