#!/usr/bin/env python3
""" Dekla widgets

    more specific widgets for experiments-related functionality

"""

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


class CuteScore(QLabel):
        # the mainscore is the big number
        # the modscore is the small number with a plus/minus and with colours
        # commit()
        
        score = dict()
        def __init__(self):
                super().__init__()
                self.setMinimumSize( 1920,1080 )
                self.mode = 'cooperative'
                self.score['player1'] = 0
                self.score['player2'] = 0
                self.mainscore = '0'
                self.modscore = ''
                self.hidescore = True
                self.thumbs = ''
                self.thumbsUp = QImage('attcap/thumbsup.png')
                self.thumbsDown = QImage('attcap/thumbsdown.png')

                self.verticalOffset = 0
                
        def add(self,player,amount):
                self.hidescore = False
                if self.mode == 'competitive':
                        self.mainscore = str( self.score[player] )
                else:
                        self.mainscore = str( self.score['player1']+self.score['player2'] )
                if amount>0:
                        self.modscore = '+'+str(amount)
                        self.thumbs = 'up'
                else:
                        self.modscore = str(amount)
                        self.thumbs = 'down'
                if amount==0:
                        self.modscore = ''
                        self.thumbs = ''

                self.score[player] += amount
                self.update()

        def hideScore(self):
                self.hidescore = True
                print("Hiding score")
                self.update()
        def showScore(self):
                self.hidescore = False
                print("Showing score")
                self.update()
        def setCompetitive(self):
                self.mode = 'competitive'
        def setCooperative(self):
                self.mode = 'cooperative'
        def setBackground(self,imagename):
                self.setPixmap( QPixmap.fromImage(QImage(imagename)) )
        
        def paintEvent(self,event):
                super().paintEvent(event)
                painter = QPainter(self)
                
                painter.setPen(QColor('#0070C0'))
                painter.setFont( QFont( "Carlito", 80, QFont.Bold) )
                painter.drawText(QRect(1920/2-400,0,800,400),Qt.AlignCenter,"PUNTEGGIO")
                painter.setPen(Qt.black)
                painter.setFont( QFont( "Carlito", 100, QFont.Bold) )
                # TODO the resolution needs to be dynamic, background pixmap scaled / with an option to be centered and trimmed
                #if self.mode == 'competitive':
                        #painter.translate(QPoint(1920/2,1080/2))
                        #painter.drawText(QRect(-300,0,600,600),Qt.AlignCenter,str(self.score['player1']))

                        #painter.translate(QPoint(0,0))
                        #painter.rotate(180)
                        #painter.drawText(QRect(-300,0,600,600),Qt.AlignCenter,str(self.score['player2']))
                #else:
                if not self.hidescore:
                        painter.translate(QPoint(1920/2,1080/2))
                        
                        # correct colours
                        if self.thumbs == 'up':
                                painter.setPen(Qt.green)
                        if self.thumbs == 'down':
                                painter.setPen(Qt.red)
                        painter.setFont( QFont( "Carlito", 100, QFont.Bold) )

                        # mod: show only either full score or a modifier
                        if self.thumbs == '':
                                painter.drawText(QRect(-300,-300,600,600),Qt.AlignCenter,str(self.mainscore))
                        else:
                                painter.drawText(QRect(-300,-300,600,600),Qt.AlignCenter,str(self.modscore))

                        
                        
                        if self.thumbs == 'up':
                                painter.drawImage(-800,-150-self.verticalOffset, self.thumbsUp.scaledToHeight(300))
                                painter.drawImage(520,-150-self.verticalOffset, self.thumbsUp.scaledToHeight(300).mirrored(True,False))
                        if self.thumbs == 'down':
                                painter.drawImage(-800,-150-self.verticalOffset, self.thumbsDown.scaledToHeight(300))
                                painter.drawImage(520,-150-self.verticalOffset, self.thumbsDown.scaledToHeight(300).mirrored(True,False))
                painter.end()

class CuteCountDown(QLabel):
        def __init__(self):
                super().__init__()
                #self.setText("Waiting")
                self.timer = QTimer() # not actually used for time, schedules stepTimer
                self.timer.timeout.connect(self.stepTimer)
                #self.setMinimumSize(300,200)

                #self.maxTime = random.choice([30,60,90,120,150])
                self.maxTime = 10 # just a placeholder
                self.labelFont = QFont( "Carlito", 60, QFont.Bold)
                self.setAlignment(Qt.AlignCenter)
                
                self.showCountDown = True
        
        time = 0
        style = "{0:3.0f}" 
        #style = "{:03.0f}"

        def setBackground(self,imagename):
                self.setPixmap( QPixmap.fromImage(QImage(imagename)) )

       
        def paintEvent(self,event):
                super().paintEvent(event)
                if self.showCountDown:
                        painter = QPainter(self)

                        painter.translate(self.size().width()/2,self.size().height()/2)

                        painter.setPen(QColor('#FDCEF8')) # dark pink
                        painter.setBrush(QColor('#FFE0FF')) # light pink
                        painter.drawPie(-200,-200,400,400,90*16,round(360*16*self.time/self.maxTime))

                        painter.setPen(Qt.black)
                        painter.setBrush(Qt.black)
                        centerTransform = painter.worldTransform()
                        for i in [30,60,90,120,150,180,210,240,270,300,330,360]:
                                painter.rotate(i)
                                painter.drawLine(200,0,210,0)
                                painter.setWorldTransform( centerTransform )
                        

                        if self.time > 10:
                                painter.setPen(Qt.black)
                        else:
                                painter.setPen(Qt.red)
                        painter.setFont( self.labelFont )
                        painter.drawText(QRect(-300-35,-300,600,600),Qt.AlignCenter,self.style.format(math.ceil(self.time)))
                        
                        painter.setPen(QColor('#148949')) # dark green
                        painter.setFont( self.labelFont )
                        painter.drawText(QRect(-300-35,-600,600,600),Qt.AlignCenter,"TIMER")
                        painter.end()
                

        def hideCountDown(self):
                self.showCountDown = False
                self.update()

        def showCountDownPlease(self):
                self.showCountDown = True
                self.update()

        
        def setCountDown(self,maxTime):
                self.maxTime = maxTime
                self.time = self.maxTime

        def start(self):
                self.timeStart = self.timeFunction()
                self.timer.start()
                
        def stop(self):
                self.timer.stop()
                
        def timeClear(self):
                self.time = 0
                self.update()

        def timeFunction(self):
                return time.perf_counter()
        
        def timeUpdate(self):
                self.time = self.maxTime - (self.timeFunction()-self.timeStart)

        def stepTimer(self):
                self.timeUpdate()
                if self.time < 0:
                        self.time = 0
                        self.timer.stop()
                        self.timeout.emit()
                self.update()

        timeout = pyqtSignal()