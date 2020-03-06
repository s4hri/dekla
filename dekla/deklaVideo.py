#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class CuteVideo(QVideoWidget):
        def __init__(self, moviename):
                super().__init__()
                self.setMinimumSize(640,480)
                self.player = QMediaPlayer()
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(QFileInfo(moviename).absoluteFilePath())))
                self.player.setVideoOutput(self)
                self.player.setNotifyInterval(2) # ms
                self.player.positionChanged.connect(self.periodicPause)
        stackedIndex = 0
        
        def periodicPause(self,position):
                # will spit out errors:
                #  RecursionError: maximum recursion depth exceeded in comparison
                # if you use anything modifying playing position without checking State
                # do any modifications inside if statements only when paused!
                if self.player.state() == QMediaPlayer.PlayingState:
                        if self.player.duration()>0:
                                if self.player.duration()-position<10:
                                        # first pause! always first pause!
                                        self.player.pause()
                                        if self.player.isSeekable():
                                                # correct it to be precisely 10ms before the end
                                                self.player.setPosition(self.player.duration()-10)
