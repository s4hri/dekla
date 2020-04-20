#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import time
import datetime
import socket
import csv
import random
import math

#
# check 1 : 208500 Hz - silent
# check 2 : 99331 Hz  - with print(self.fps_counter)


class RandMain(QLabel):
        def __init__(self):
                super().__init__()
                self.setText("Press S to start, q to quit")
                self.timer = QTimer()
                self.timer.timeout.connect(self.stepExperiment)
                self.setMinimumSize(600,200)

                self.maxTime = 10
                self.setFont( QFont( "Arial", 20, QFont.Bold) )
        
        currentTime = 0
        style = "{0:3.0f} {0}" 
        #style = "{:03.0f}"
        fps_counter = 0
        
        def keyPressEvent(self,event):
                super().keyPressEvent(event)
                print( 'Pressed: code {0} = {1}'.format(event.key(),QKeySequence(event.key()).toString()) )
                if event.key() == Qt.Key_S:
                        self.timeStart = self.time()
                        self.timer.start()
                        self.fps_counter = 0
                if event.key() == Qt.Key_Q:
                        qApp.quit()

        def time(self):
                return time.perf_counter()
        
        def stepExperiment(self):
                self.currentTime = self.maxTime - (self.time()-self.timeStart)
                self.fps_counter += 1
                #print(self.fps_counter) # don't, lowers fps
                if self.currentTime < 0:
                        self.currentTime = 0
                        self.timer.stop()
                        
                        print("Refresh Hz: ",self.fps_counter/self.maxTime)
                        self.setText("Refresh Hz: "+str(self.fps_counter/self.maxTime))
                else:
                        self.setText( self.style.format(math.ceil(self.currentTime)) )
                

if type(qApp.instance()) is type(None):
        app = QApplication([])
if __name__ == '__main__':
        label = RandMain()
        #label.finishedExperiment.connect(qApp.quit)
        label.show()
        qApp.exec()
