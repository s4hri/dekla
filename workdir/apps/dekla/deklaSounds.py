#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# TODO move this inside the addVideo with a check for imports
#      if failed then return an exception for importing libs
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import * # videos

import time
import datetime
import socket
import csv

import random
import io # for StringIO, dummy file
import os

import math # ceil in CuteCountDown

class CuteSounds(QWidget):
        # TODO make this a dynamic list of sound effects, with each column corresponding
        #      to a single effect that can be called using a dictionary
        dekla = None
        def __init__(self,dekla,path):
                super().__init__()
                self.dekla = dekla
                self.path = path

                layout1 = QHBoxLayout()
                column1 = QVBoxLayout()
                self.soundsLabel1 = QLabel("choose left sound (timer)")
                column1.addWidget(self.soundsLabel1)
                self.optionsTreeSoundTimer = QTreeWidget()
                self.optionsTreeSoundTimer.setFocusPolicy( Qt.NoFocus )
                self.optionsTreeSoundTimer.setHeaderItem(QTreeWidgetItem(['File']))
                self.optionsTreeSoundTimer.itemClicked.connect(self.optionsTreeSoundTimerItemClicked)
                self.optionsTreeSoundTimerTemplates = [ f for f in os.listdir(self.path) if f.startswith('left') ]
                self.optionsTreeSoundTimerTemplatesItems = [ QTreeWidgetItem([f]) for f in self.optionsTreeSoundTimerTemplates ]
                self.optionsTreeSoundTimer.addTopLevelItems( self.optionsTreeSoundTimerTemplatesItems )
                column1.addWidget(self.optionsTreeSoundTimer)
                layout1.addLayout(column1)

                column2 = QVBoxLayout()
                self.soundsLabel2 = QLabel("choose right sound (score)")
                column2.addWidget(self.soundsLabel2)
                self.optionsTreeSoundScore = QTreeWidget()
                self.optionsTreeSoundScore.setFocusPolicy( Qt.NoFocus )
                self.optionsTreeSoundScore.setHeaderItem(QTreeWidgetItem(['File']))
                self.optionsTreeSoundScore.itemClicked.connect(self.optionsTreeSoundScoreItemClicked)
                self.optionsTreeSoundScoreTemplates = [ f for f in os.listdir(self.path) if f.startswith('right') ]
                self.optionsTreeSoundScoreTemplatesItems = [ QTreeWidgetItem([f]) for f in self.optionsTreeSoundScoreTemplates ]
                self.optionsTreeSoundScore.addTopLevelItems( self.optionsTreeSoundScoreTemplatesItems )
                column2.addWidget(self.optionsTreeSoundScore)
                layout1.addLayout(column2)

                self.setLayout(layout1)

        def optionsTreeSoundTimerItemClicked(self,item):
                print('setting sound')
                self.effectPath = 'attcap/' + self.optionsTreeSoundTimerTemplates[self.optionsTreeSoundTimerTemplatesItems.index(item)]
                self.dekla.effect.setSource(QUrl.fromLocalFile(self.effectPath) )
                self.dekla.effect.setVolume(1.00)
                self.dekla.effect.play()

        def optionsTreeSoundScoreItemClicked(self,item):
                self.effectScorePath = 'attcap/' + self.optionsTreeSoundScoreTemplates[self.optionsTreeSoundScoreTemplatesItems.index(item)]
                self.dekla.effectScore.setSource(QUrl.fromLocalFile(self.effectScorePath) )
                self.dekla.effectScore.setVolume(1.00)
                self.dekla.effectScore.play()
