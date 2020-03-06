#!/usr/bin/env python3


from dekla import *
from dekla.deklaWeb import *

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

app = QApplication([])

movies = { 'close left': 'movies/close_left.mp4',
           'mutual left': 'movies/mutual_left.mp4',
           'return left': 'movies/return_left.mp4',
           'close right': 'movies/close_right.mp4',
           'mutual right': 'movies/mutual_right.mp4',
           'return right': 'movies/return_right.mp4'}


class defaults:
        appName = "Dekla v0.2 - Posner Experiment"
        screens = ["main","left","right"]
        savefile = "../data/results_" # and auto-added date: %Y%m%d-%H%M%S

conditions = [
  'close',
  'close',
  'mutual',
  'mutual',
  'mutual',
  'close',
  'close',
  'close',
  'mutual',
  'close',
  'mutual',
  'mutual',
  'mutual',
  'mutual',
  'close',
  'close']


subtrials = [ (lookingside,letterside,letter)
              for lookingside in ['left','right']
              for letterside  in ['left','right']
              for letter in [ 'T','V'] ]

trials = list()

for trial in conditions:
        subtrialsTwice = subtrials.copy()
        subtrialsTwice.extend(subtrials)
        random.shuffle(subtrialsTwice)
        for subtrial in subtrialsTwice:
                place1 = trial + ' ' + subtrial[0]
                place2 = subtrial[1] + ' ' + subtrial[2]
                place3 = 'return ' + subtrial[0]
                place4 = subtrial[1] + ' empty'
                key = subtrial[2]
                
                trials.append(  dict( place1=place1,
                                      place2=place2,
                                      place3=place3,
                                      place4=place4,
                                      key=key ) )


class RandMain(CuteMain):
        def __init__(self):
                db = dict()
                #self.fileName="posner03.yaml"
                #with open(self.fileName,'r') as file:
                        #db = yaml.load(file,Loader=yaml.Loader)
                
                super().__init__(db)
                
                #movies = self.db['info']['movies']  # kyveli
                for movie in movies:
                        print(index,movie)
                        self.players[movie] = CuteVideo(movies[movie])
                        self.players[movie].player.setPosition(0)
                        self.layoutStack['main'].addWidget(self.players[movie])
                        # do this automatically next time: (not reliable)
                        self.players[movie].stackedIndex = index
                        # maybe one more dictionary that stores indices?
                        index = index + 1

                print("LEFT")
                self.left = CuteSideWindow(self)
                self.left.setWindowTitle(defaults.screen2)
                self.left.setWindowTitle('Left')
                self.layoutStack['left'] = QStackedLayout()
                self.labels["left V"] = CuteLabel("V")
                #self.labels["left V"].setFont( QFont( "Arial", 100, QFont.Bold) )
                self.labels["left V"].setStyleSheet( 'font: bold 100px'  )
                self.labels["left V"].setAlignment(Qt.AlignCenter)
                self.labels["left T"] = CuteLabel("T")
                self.labels["left T"].setFont( QFont( "Arial", 100, QFont.Bold) )
                self.labels["left T"].setAlignment(Qt.AlignCenter)
                #self.labels["left T"].setStyleSheet("border: solid 10px grey;  background-color: rgba(255, 0, 0,127); color:rgb(0,255,0)");
                self.labels["left empty"] = CuteLabel() # QWidget? 
                self.layoutStack['left'].addWidget(self.labels["left empty"])  # 0
                self.layoutStack['left'].addWidget(self.labels["left V"]) # 1
                self.layoutStack['left'].addWidget(self.labels["left T"]) # 2
                #this should be automatic:
                self.labels["left empty"].stackedIndex = 0
                self.labels["left V"].stackedIndex = 1
                self.labels["left T"].stackedIndex = 2
                self.left.setLayout(self.layoutStack['left'])
                self.left.show()

                self.labels["left empty"].stack = 'left'
                self.labels["left V"].stack = 'left'
                self.labels["left T"].stack = 'left'

                
                print("RIGHT")
                self.right = CuteSideWindow(self)
                self.right.setWindowTitle('Right')
                self.right.setWindowTitle(defaults.screen3)
                self.layoutStack['right'] = QStackedLayout()
                self.labels["right V"] = CuteLabel("V")
                self.labels["right V"].setFont( QFont( "Arial", 100, QFont.Bold) )
                self.labels["right V"].setAlignment(Qt.AlignCenter)
                self.labels["right T"] = CuteLabel("T")
                self.labels["right T"].setFont( QFont( "Arial", 100, QFont.Bold) )
                self.labels["right T"].setAlignment(Qt.AlignCenter)
                self.labels["right empty"] = CuteLabel() # QWidget? 
                self.layoutStack['right'].addWidget(self.labels["right empty"])  # 0
                self.layoutStack['right'].addWidget(self.labels["right V"]) # 1
                self.layoutStack['right'].addWidget(self.labels["right T"]) # 2
                #this should be automatic:
                self.labels["right empty"].stackedIndex = 0
                self.labels["right V"].stackedIndex = 1
                self.labels["right T"].stackedIndex = 2
                
                self.labels["right empty"].stack = 'right'
                self.labels["right V"].stack = 'right'
                self.labels["right T"].stack = 'right'
                
                print("layout")
                self.right.setLayout(self.layoutStack['right'])
                self.right.show()


                
                
                
                #self.layoutStack['main'].addWidget(self.cuteAnim)
                #self.setMinimumSize(1920,1080)

                # TODO move the webserver to a separate file
                self.webserver = CuteServer()
                self.webserver.start()
                self.webserver.setImageWidget( self )
                
                pass
        def keyPressEvent(self,event):
                super().keyPressEvent(event)
                print( event.key() )
                if event.key() == Qt.Key_Left:
                        if self.cuteAnim.anim.state() == QAbstractAnimation.Stopped:
                                self.stepExperiment(120)
                if event.key() == Qt.Key_Right:
                        if self.cuteAnim.anim.state() == QAbstractAnimation.Stopped:
                                self.stepExperiment(-120)
        def full(self):
                if not self.windowState() == Qt.WindowFullScreen:
                        self.setWindowState(Qt.WindowFullScreen)
                        self.left.setWindowState(Qt.WindowFullScreen)
                        self.right.setWindowState(Qt.WindowFullScreen)
                else:
                        self.setWindowState(Qt.WindowNoState)
                        self.left.setWindowState(Qt.WindowNoState)
                        self.right.setWindowState(Qt.WindowNoState)
        def startExperiment(self):
                self.layoutStack['main'].setCurrentIndex(1)
                
        def stepExperiment(self,choice):
                if choice == 120: #left
                        self.cuteAnim.rotateObjects(120)

                if choice == -120: #right
                        self.cuteAnim.rotateObjects(-120)
                        
                        
                randomreward = random.randint(1,3)
                if randomreward == 1:
                        self.cuteAnim.showReward(inverted=False)
                if randomreward == 2:
                        self.cuteAnim.showReward(inverted=True)
                        
        def pauseExperiment(self):
                pass
        def trialsLeft(self):
                return 0

if __name__ == '__main__':
        label = RandMain()
        label.finishedExperiment.connect(qApp.quit)
        label.show()
        qApp.exec()
