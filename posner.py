#!/usr/bin/env python3


from dekla import *
from deklaVideo import *
#from dekla.deklaWeb import *

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

movies = { 'close left': 'movies/close_left.mp4',
           'mutual left': 'movies/mutual_left.mp4',
           'return left': 'movies/return_left.mp4',
           'close right': 'movies/close_right.mp4',
           'mutual right': 'movies/mutual_right.mp4',
           'return right': 'movies/return_right.mp4'}

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

class Posner(Dekla):
        def prepare(self):
                self.addStack('main')
                self.stacks['main'].addVideo( movies )





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
                #self.layoutStack['main'].setCurrentIndex(1)
                
                #self.setWindowState( Qt.WindowFullScreen )
                #self.right.setWindowState( Qt.WindowFullScreen )
                #self.left.setWindowState( Qt.WindowFullScreen )

                self.sliceTrial()

                # TODO reverse naming convention to self.resultsFile self.resultsCSV
                
                
                #datetime.datetime.now().strftime('%Y%m%d-%H%M%S')                
                
                if len(self.filenameResults):
                        self.fileResults = open(self.filenameResults,'w+') # or a+ if appending
                else:
                        # if you choose not to save, a dummy file:
                        self.fileResults = io.StringIO()
                
                
                self.csvResults = csv.DictWriter(self.fileResults,list(self.trial.keys()))
                if self.fileResults.tell()==0:
                        self.csvResults.writeheader()
                



                #self.players['close left'].player.play()

                #self.currentVideo = 'close left'
                #self.currentVideo = self.trial['place1']

                #self.layoutStack['main'].setCurrentIndex( self.players[self.currentVideo].stackedIndex )
                #self.players[self.currentVideo].player.play()
                
                #The robot has its eyes closed
                
                self.currentVideo = 'close left' # default, TODO set it to index 0
                
                # prepare
                #self.time_us = time.time_ns()/1000
                self.time_us = time.time()*1e6
                self.nextEvent = 0
#                self.timeEvent = time.time_ns()/1000
                self.timeEvent = time.time()*1e6
                
                # start
                self.timer = QTimer()
                self.timer.timeout.connect(self.stepExperiment)
                self.timer.start()
                
                #It opens its eyes
                #It either looks straight towards participants' eyes or down.
                #It looks towards the left or right screen
                #After a specific time of the initiation of the robot's lateral movement towards the left/right screen (this time is called SOA, here it should be 1s), the target letter (T or V) appears. We have prepared the videos which embed steps 1-4 with the specific SOA. That means that when the video finishes the letter should appear directly.
                #The letter should appear for 200 ms. The central robot video should be stuck to the last frame (when the letters are presented) but we also want to continue listening to the sound of the video. Participants can respond from the appearance of the letter and on. Only when they respond the video stops being presented and we go to step 7
                #The robot returns to its initial position with eyes closed and the next trial starts. We have prepared a video for this.

                
        def stepExperiment(self,choice):
                #
                #  this is from sketch11, incompatible with mods in sketch12 (dynamic .yaml interpreter)
                #    DO NOT MIX THEIR CODE !
                #
                #  requires self.currentVideo to be already set
                
                #timeNew = time.time_ns()/1000 # microseconds
                timeNew = time.time()*1e6 # microseconds
                
                # time passed since the last event:
                timePassed = (timeNew - self.timeEvent)/1000 # milliseconds
                
                #print(timeNew - self.time_us)
                if timeNew - self.time_us > self.time_max:
                        self.time_max = timeNew - self.time_us
                        print("new max",self.time_max)
                self.time_us=timeNew
                #print("time passed",timePassed)

                if self.nextEvent==0: # wait for the head to go left
                        print("DEBUG: event 0")
                        self.players[ self.currentVideo].player.setPosition(0) # grab a pencil and rewind tape
                        self.currentVideo = self.trial['place1']

                        self.layoutStack['main'].setCurrentIndex( self.players[self.currentVideo].stackedIndex )
                        self.players[self.currentVideo].player.play()
                        self.nextEvent += 1
                        self.timeEvent = timeNew # reset time

                        print(f"DEBUG: {self.nextEvent},{self.timeEvent}")
                if self.nextEvent==1: # wait for the head to go left
                        if self.players[self.currentVideo].player.state() == QMediaPlayer.PausedState:
                                print("DEBUG: paused")
                                self.nextEvent += 1
                                self.timeEvent = timeNew # reset time
                                self.correctInput = '' # clear input
                                place2 = self.trial['place2']
                                stack = self.labels[place2].stack
                                self.layoutStack[stack].setCurrentIndex(self.labels[place2].stackedIndex) # show letter
                elif self.nextEvent==2: # show letter
                        if timePassed>200:
                                place4 = self.trial['place4']
                                stack = self.labels[place4].stack
                                self.layoutStack[stack].setCurrentIndex(self.labels[place4].stackedIndex) # hide letter
                        if len(self.correctInput)>0: # check for input flag
                                if self.trial['key']==self.correctInput:
                                        print("User took:",timePassed,"ms to hit the right key")
                                        self.results['key'] = timePassed
                                place4 = self.trial['place4']
                                stack = self.labels[place4].stack
                                self.layoutStack[stack].setCurrentIndex(self.labels[place4].stackedIndex) # be sure about hiding the letter!
                                self.nextEvent += 1
                                self.timeEvent = timeNew # reset time
                        if timePassed>1500: # timeout
                                self.nextEvent += 1
                                self.timeEvent = timeNew # reset time
                                print("user input timed out")
                elif self.nextEvent==3: 
                        self.players[ self.currentVideo].player.setPosition(0) # grab a pencil and rewind tape
                        self.currentVideo = self.trial['place3']
                        self.layoutStack['main'].setCurrentIndex( self.players[self.currentVideo].stackedIndex )
                        self.players[self.currentVideo].player.play()
                        self.timeEvent = timeNew # reset time
                        self.nextEvent += 1
                elif self.nextEvent==4:
                        if timePassed>2000:
                                if self.players[self.currentVideo].player.state() == QMediaPlayer.PausedState:
                                        self.nextEvent += 1
                                        self.timeEvent = timeNew # reset time
                elif self.nextEvent==5: # reset
                        #self.players[ self.currentVideo].player.setPosition(0) # grab a pencil and rewind tape
                        #self.currentVideo = 'mutual left
                        #self.layoutStack.setCurrentIndex(1)
                        #self.players[ self.currentVideo ].player.play()
                        
                        self.timeEvent = timeNew # reset time
                        self.nextEvent += 1
                elif self.nextEvent==6:
                        self.nextEvent = 0
                        self.saveResults()
                        #if  > 0: # yaml-based
                        if self.trialsLeft()>0:
                                self.sliceTrial()
                        else:
                                self.fileResults.close()
                                self.pauseExperiment()
                                self.labels['instructions'].setText('press q to return to main menu' )
                                self.layoutStack['main'].setCurrentIndex(0)
                                
        def pauseExperiment(self):
                self.timer.stop()
                #self.players['close left'].player.stop()
                print("Max recorded delay in stepExperiment:",self.time_max,"us")
        def trialsLeft(self):
                return len(trials) # list of dictionaries
                #return len(self.db['trial']) # yaml-based dict of a dict
        def sliceTrial(self):
                # # yaml-based:
                #trialTuple = self.db['trial'].popitem() # will return a tuple (name,dict)
                #self.trial = trialTuple[1] # extract only the dictionary
                
                self.trial = trials.pop(0)
                self.results = self.trial # prepare results
        def saveResults(self):
                # DELETED, pasted into snippet_089_csv.py
                self.csvResults.writerow(self.results)
                pass
if type(qApp.instance()) is type(None):
        app = QApplication([])
if __name__ == '__main__':
        label = RandMain()
        label.finishedExperiment.connect(qApp.quit)
        label.show()
        qApp.exec()
