#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

app = QApplication([])

label  = QLabel()
layout = QVBoxLayout()

player = QMediaPlayer()
player.setMedia(QMediaContent(QUrl.fromLocalFile(QFileInfo("test1.mp4").absoluteFilePath())))
video = QVideoWidget()
player.setVideoOutput(video)

player.play()

layout.addWidget(video)
label.setLayout(layout)

label.show()

app.exec()
