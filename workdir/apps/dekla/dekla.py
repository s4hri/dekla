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

# should not be a hard requirement
import yaml

import random
import io # for StringIO, dummy file
import os

import math # ceil in CuteCountDown

from pykron.core import PykronLogger

# make sure there exists a Qt5 application
# TODO this should be left to the importing file, what are the downsides to doing that here?
if type(qApp.instance()) is type(None):
        print("This version of dekla is for GUIs, creating QApplication for you...")
        app = QApplication([])

class Dekla(QObject):
        db = None
        #log = None

        manager = None
        windows = dict()
        stacks = dict() # CuteStack preferred
        widgets = dict() # all widgets
        webserver = None
        petri = dict()

        images = dict()

        timer = None
        timerList = dict() # CuteTimer only

        trials = dict()        # only current to-do trials (gets popped)
        trialsFull = dict()    # all loaded from .csv file
        trialsFileName = None  # set it or getOpenFileName is shown

        results = list()
        result = dict()

        fileResults = None
        filenameResults = None # no popup window if you declare it

        options = None
        optionFileName = None

        appName = "Dekla v0.2"
        savefile = "../data/results_" # and %Y%m%d-%H%M%S

        running = False

        logger = None

        def __init__(self):
                # WARNING not very pythonic way to check first, but I prefer it
                if hasattr(qApp,'dekla'):
                    raise Exception("Dekla can be __init__ed only once!")
                qApp.dekla = self # link to the qApp instance

                super().__init__()
                self.windows = dict()
                self.stacks = dict()
                self.options = CuteOptions()

                # old yaml-based logger can be found in the archive/DeklaLogger.py
                self.logger = PykronLogger.getInstance()

        def addStack(self,name):
                if name not in self.windows:
                        self.windows[name] = CuteWindow(self)
                        self.windows[name].setWindowTitle(name)

                self.stacks[name] = CuteStack(self.windows[name])

        def addScrollStack(self,name):
                if name not in self.windows:
                        self.windows[name] = CuteScrollArea(self)
                        self.windows[name].setWindowTitle(name)
                        self.widgets[name+'widget'] = CuteWindow(self)
                        self.windows[name].setWidget(self.widgets[name+'widget'])
                        self.stacks[name] = CuteStack(self.widgets[name+'widget'])

        fullscreen = False
        def full(self):
                # TODO check the state of the first window and flip all in accordance to it

                self.fullscreen = not self.fullscreen # TODO remove
                for window in self.windows:
                        if self.fullscreen:
                                self.windows[window].setWindowState(Qt.WindowFullScreen)
                        else:
                                self.windows[window].setWindowState(Qt.WindowNoState)

        def show(self):
                #super().show()
                for window in self.windows:
                        self.windows[window].show()

        #def keyboard(self,keys,function):
                #if type(keys) is not type(list()):
                        #keys = [keys]
                #for key in keys:
                #pass

        def loadOptions(self):
                if not self.optionsFileName:
                        self.optionsFileName, extension = QFileDialog.getOpenFileName( QWidget(), "Open options file:", '', "YAML files (*.yaml)")
                self.options.load(self.optionsFileName)

        def saveOptions(self):
                if self.optionsFileName:
                        self.options.save(self.optionsFileName)

        def loadTrials(self):
                if not self.trialsFileName:
                        self.trialsFileName, extension = QFileDialog.getOpenFileName( QWidget(), "Open trials file:", '', "CSV files (*.csv)")
                # TODO add checking if really the dialog succeeded!
                with open(self.trialsFileName,'r') as csvfile:
                        csvread = csv.DictReader(csvfile)
                        self.trialsFull = [dict(row) for row in csvread]
                self.resetTrials()

        def resetTrials(self):
                self.trials = self.trialsFull[:]
                self.trialcounter = 0

        def sliceTrial(self):
                self.trial = self.trials.pop(0)
                self.result = self.trial.copy() # prepare results
                self.trialcounter += 1

        # Note: custom class Keyboard is out, see sketch253_keyboard_handler.py
        #       storage from sketch254_keyboard_dict.py is in:
        #       TODO track and rename all instances of keyHistory to keyDict
        keyDict = dict()
        def keyPressEvent(self,event):
                print( 'Pressed:',event.key() )
                #print( 'Pressed: code {0} = {1}'.format(event.key(),QKeySequence(event.key()).toString()) )
                if event.key() == Qt.Key_F1:
                        # TODO this is a temporary information window
                        self.optionsFont = CuteFonts()
                        self.optionsFont.show()
                if event.key() == Qt.Key_Q:
                        #qApp.quit()
                        #qApp.closeAllWindows()
                        self.quitEverything()
                if event.key() == Qt.Key_F:
                        self.full()
                if event.key() == Qt.Key_S:
                        if not self.running:
                                self.prepareSave()
                                self.startExperiment()
                if event.key() in self.keyDict.keys():
                        #if event.Type() == QEvent.KeyPress:
                        self.keyDict[event.key()] = True

        def quitEverything(self):
                qApp.closeAllWindows()

        # abstraction layer to keep compatibility with 253:
        def keyTrack(self,key): # key can be an entry or a list
                # TODO make it nicer:
                if type(key) == type(list()):
                        for key1 in key:
                                if key1 not in self.keyDict.keys():
                                        self.keyDict[key1] = False
                else:
                        if key not in self.keyDict.keys():
                                self.keyDict[key] = False
        def keyRemove(self,key):
                if type(key) == type(list()):
                        for key1 in key:
                                if key1 in self.keyDict.keys():
                                        self.keyDict.pop(key1)
                else:
                        if key in self.keyDict.keys():
                                self.keyDict.pop(key)
        def keyCheck(self,key):
                if key in self.keyDict.keys():
                        return self.keyDict[key]

        def startExperiment(self):
                self.sliceTrial()
                self.timer = QTimer() # not actually used for time, schedules stepExperiment
                self.timer.timeout.connect(self.stepExperiment)
                self.timer.start()
                self.running = True
        def stepExperiment(self):
                pass

        def stopExperiment(self):
                if self.timer:
                        self.timer.stop()
                if self.fileResults:
                        self.save()
                self.running = False
                #qApp.closeAllWindows()

        def prepareSave(self):
                filename1 = self.savefile+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.csv'
                if not self.filenameResults:
                        self.filenameResults, extension = QFileDialog.getSaveFileName( QWidget(), "Save results as...", filename1)
                if len(self.filenameResults):
                        self.fileResults = open(self.filenameResults,'w+') # or a+ if appending 
                else:
                        ## if you choose not to save, a dummy file:
                        self.fileResults = io.StringIO()
        def save(self):
                # grab every possible header: (set for uniqueness, then back to list)
                #header = list( self.results[0].keys() )
                header = list( {key for res in self.results for key in res.keys()} )
                header.sort()
                self.csvResults = csv.DictWriter(self.fileResults, header)
                if self.fileResults.tell()==0:
                        self.csvResults.writeheader()
                for res in self.results:
                        self.csvResults.writerow(res)
                if len(self.filenameResults): # if this was a file:
                        self.fileResults.close()
                else:
                        print(self.fileResults.getvalue())
        def petriTimer(self,delay,var,value):
                if self.timerList:
                        newtimer = max(list(self.timerList.keys()))+1
                else:
                        newtimer = 0
                self.timerList[ newtimer ] = CuteTimer(self.petri, delay, var, value)
                self.timerList[ newtimer ].timeout.connect( self.petriTimerCleanup )

        def petriTimerCleanup(self):
                poplist = list()
                for timer in self.timerList.keys():
                        if not self.timerList[timer].running:
                                poplist.append(timer)
                for timer in poplist:
                        self.timerList.pop(timer)

class CuteOptions:
        __options__ = dict()
        def load(self,configname):
                with open(configname,'r') as configfile:
                        self.__options__ = yaml.load(configfile,Loader=yaml.Loader)

        def save(self,configname):
                with open(configname,'w') as configfile:
                        yaml.dump(self.__options__,configfile)

        def __setitem__(self, key, value):
                if key in self.__options__.keys():
                        self.__options__[key]['value'] = value
                else:
                        self.__options__[key] = {'value': value, 'desc': ''}

        def __getitem__(self, key):
                return self.__options__[key]['value']

        def keys(self):
                return self.__options__.keys()

        def values(self):
                return self.__options__.values()

        def description(self,key):
                return self.__options__[key]['desc']

        def setDescription(self,key,desc):
                self.__options__[key]['desc']=desc

        def __iter__(self):
                self.iterKeys = list(self.__options__.keys())
                self.max = len(self.iterKeys)
                self.n = 0
                return self

        def __next__(self):
                if self.n < self.max:
                        result = self.__options__[self.iterKeys[self.n]]
                        self.n += 1
                        return result
                else:
                        raise StopIteration

class CuteWindow(QWidget):
        def __init__(self,dekla):
                super().__init__()
                self.dekla = dekla
                self.setMinimumSize(1920,1080)
                self.locked = False
        def keyPressEvent(self,event):
                self.dekla.keyPressEvent(event)
        def paintEvent(self,event):
                if not self.locked:
                        self.locked = True
                        super().paintEvent(event)
                self.locked = False
        def grabImage(self):
                print("Trying to grab image")
                if not self.locked:
                        image = self.grab().toImage()
                        ba = QByteArray()
                        buf = QBuffer(ba)
                        buf.open(QIODevice.WriteOnly)
                        image.save(buf, "PNG")
                        return ba.data()


class CuteScrollArea(QScrollArea):
        def __init__(self,dekla):
                super().__init__()
                self.dekla = dekla
                self.setMinimumSize(100,100)
                self.setBackgroundRole(QPalette.Light)
                self.setWidgetResizable(True)
                self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                #QScroller.grabGesture(ui->combo->view()->viewport(),QScroller::LeftMouseButtonGesture);
                
                # make the widget able to receive flicks
                # (flickable? sounds weird)
                self.scroll = QScroller.scroller(self)
                p = self.scroll.scrollerProperties()
                # don't overshoot, ever
                p.setScrollMetric( QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff )
                p.setScrollMetric( QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff )
                # make the scrolling feel more sticky - faster stopping
                p.setScrollMetric( QScrollerProperties.DecelerationFactor, 2.0 )
                # for some reason p was a full copy, feed it back:
                self.scroll.setScrollerProperties( p )
                self.scroll.grabGesture(self,QScroller.LeftMouseButtonGesture)
                
                
        def keyPressEvent(self,event):
                self.dekla.keyPressEvent(event)



class CuteTimer(QObject):
        def __init__(self,petri,delay,var,value):
                super().__init__()
                print('Cutetimer:',delay,'var',var,'value',value)
                QTimer.singleShot(delay, self.timeoutFun)
                self.running = True
                self.petri = petri
                self.var = var
                self.value = value
        def timeoutFun(self):
                self.running = False
                self.petri[self.var] = self.value
                self.timeout.emit()
        timeout = pyqtSignal()



class CuteImage(QLabel):
        def __init__(self,imagename):
                super().__init__()
                #self.dekla = dekla
                #self.setMinimumSize(640,480)
                self.background = None
                self.setImage(imagename)
                self.setAlignment(Qt.AlignCenter)
                #self.update()
        def setImage(self,imagename,flipped=False):
                self.foreground = QImage(imagename).mirrored(False,flipped)
                self.composeImage()
        
        def setBackground(self,imagename):
                self.background = QImage(imagename)
                self.composeImage()
        def imageCenter(self,image):
                return QPoint((self.currentImage.width() - image.width()) / 2, (self.currentImage.height() - image.height()) / 2)
        def composeImage(self):
                if self.background:
                        self.currentImage = self.background.copy()
                        painter = QPainter(self.currentImage)
                        painter.setCompositionMode(QPainter.CompositionMode_Source)
                        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
                        
                        painter.drawImage(self.imageCenter(self.foreground), self.foreground)
                        painter.end()
                else:
                        self.currentImage = self.foreground
                self.currentPixmap = QPixmap.fromImage(self.currentImage)
                self.setPixmap( self.currentPixmap )
                #self.setPixmap( self.currentPixmap.scaled(self.size()) ) # maybe scale the central one?

        #def keyPressEvent(self,event):
                #self.dekla.keyPressEvent(event)


class CuteStack(QStackedLayout):
        def __init__(self,window):
                super().__init__()
                self.dekla = qApp.dekla
                window.setLayout(self)
        def addLabel(self,label):
                if type(label) is type(QLabel()):
                        pass
                else:
                        pass
        def addVideo(self,name,movie):
                #if type(movies) is type(dict()):
                        #for movie in movies:
                                #self.addWidget = CuteVideo(movies[movie])
                                #self.players[movie].player.setPosition(0)
                self.add( name, CuteVideo(movie) )
                self.dekla.widgets[name].player.setPosition(0)

        def addImage(self,name,imagename):
                self.add(name,CuteImage(imagename))
        def addCountDown(self,name):
                self.add(name,CuteCountDown())
        def addScore(self,name):
                self.add(name,CuteScore())
        
        def add(self,name,widget):
                if name not in self.dekla.widgets:
                        self.dekla.widgets[name] = widget
                self.addWidget(self.dekla.widgets[name])


class CuteVideo(QVideoWidget):
        def __init__(self,filename):
                super().__init__()
                self.setMinimumSize(640,480)

                self.player = QMediaPlayer()
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(QFileInfo(filename).absoluteFilePath())))
                self.player.setVideoOutput(self)
                #self.player.play()





