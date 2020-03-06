#!/usr/bin/env python3

""" Randomness task


"""

from dekla import *
from dekla.deklaWeb import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#from PyQt5.QtMultimedia import *
#from PyQt5.QtMultimediaWidgets import *

import time
import datetime
import yaml
import socket
import csv
import random




class Cir(QObject):
        def __init__(self):
                super().__init__()
                cw = 200
                self.circle1 = QGraphicsEllipseItem(380-cw/2,-cw/2,cw,cw)
                self.circle2 = QGraphicsEllipseItem(380-cw/2,-cw/2,cw,cw)
                self.circle3 = QGraphicsEllipseItem(380-cw/2,-cw/2,cw,cw)
                self.circle4 = QGraphicsEllipseItem(-300/2,-300/2,300,300)
                self.circle5 = QGraphicsEllipseItem(-1000/2,-1000/2,1000,1000)
                
                self.circle1.setBrush(Qt.red)
                self.circle2.setBrush(Qt.green)
                self.circle3.setBrush(Qt.blue)
                self.circle5.setBrush(Qt.white)
                
                self.circle1.setRotation(90)
                self.circle2.setRotation(120+90)
                self.circle3.setRotation(240+90)
                
                
        def _set_pos(self, pos):
                self.circle1.setRotation(pos.x()+90)
                self.circle2.setRotation(pos.x()+120+90)
                self.circle3.setRotation(pos.x()+240+90)
        pos = pyqtProperty(QPointF, fset=_set_pos)    

class CuteAnim(QGraphicsView):
        def __init__(self):
                super().__init__()
                self.item1 = Cir()
                
                self.scene1 = QGraphicsScene()
                self.scene1.setBackgroundBrush(Qt.black)
                self.scene1.setSceneRect( -1920/2, -1080/2, 1920, 1080 )
                self.setSceneRect( self.scene1.sceneRect() )
                #self.fitInView( self.scene1.sceneRect(), Qt.KeepAspectRatio )
                self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
                self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
                
                self.scene1.addItem(self.item1.circle5)
                #self.scene1.addItem(self.item1.circle4)
                self.scene1.addItem(self.item1.circle1)
                self.scene1.addItem(self.item1.circle2)
                self.scene1.addItem(self.item1.circle3)
                
                
                

                self.aruco1 = QGraphicsPixmapItem( QPixmap.fromImage(QImage("media/M00_border.png")))
                self.scene1.addItem(self.aruco1)
                self.aruco1.setPos( -800,-500 )
                self.aruco1.setScale(0.4)
                self.aruco2 = QGraphicsPixmapItem( QPixmap.fromImage(QImage("media/M01_border.png")))
                self.scene1.addItem(self.aruco2)
                self.aruco2.setPos( 600,-500 )
                self.aruco2.setScale(0.4)
                self.aruco3 = QGraphicsPixmapItem( QPixmap.fromImage(QImage("media/M02_border.png")))
                self.scene1.addItem(self.aruco3)
                self.aruco3.setPos( 600,300 )
                self.aruco3.setScale(0.4)
                self.aruco4 = QGraphicsPixmapItem( QPixmap.fromImage(QImage("media/M03_border.png")))
                self.scene1.addItem(self.aruco4)
                self.aruco4.setPos( -800,300 )
                self.aruco4.setScale(0.4)
                
                
                
                self.currentAngle = 0
                # anim has to exist for Pause checking:
                self.anim = QPropertyAnimation(self.item1, b"pos")
                self.anim.setDuration(1000)
                self.anim.setEasingCurve(QEasingCurve.Linear)
                self.anim.finished.connect(self.finishedAnim)
                
                self.label1Item = QGraphicsSimpleTextItem("+1")
                self.label1Item.setFont(QFont( "Arial", 100, QFont.Bold))
                self.scene1.addItem(self.label1Item)
                self.label1Item.setPos( -self.label1Item.boundingRect().width()/2,-self.label1Item.boundingRect().height()/2 )
                self.label1Item.hide()

                self.label2Item = QGraphicsSimpleTextItem("+1")
                self.label2Item.setFont(QFont( "Arial", 100, QFont.Bold))
                self.scene1.addItem(self.label2Item)
                self.label2Item.setPos( self.label2Item.boundingRect().width()/2,self.label2Item.boundingRect().height()/2 )
                self.label2Item.hide()
                self.label2Item.setRotation(180)


                #self.label1 = QLabel("+1")
                #self.label1.setAlignment(Qt.AlignCenter)
                #self.label1item = self.scene1.addWidget(self.label1)
                
                        
                self.setScene(self.scene1)
        def rotateObjects(self,angle):
                self.anim.setKeyValueAt(0.0, QPointF(self.currentAngle,         0))                   
                self.anim.setKeyValueAt(1.0, QPointF(self.currentAngle + angle, 0))
                
                self.anim.start()
                self.currentAngle += angle

        def showReward(self,inverted):
                if inverted:
                        #self.label1Item.setRotation(180)
                        self.label2Item.show()
                else:
                        self.label1Item.show()
                        #self.label1Item.setRotation(0)
                #self.label1Item.show()
        def finishedAnim(self):
                # hide everything:
                self.label1Item.hide()
                self.label2Item.hide()

        def keyPressEvent(self,event):
                self.parent().keyPressEvent(event)

class RandMain(CuteMain):
        def __init__(self):
                db = dict()
                super().__init__(db)
                self.cuteAnim = CuteAnim()
                self.layoutStack['main'].addWidget(self.cuteAnim)
                self.setMinimumSize(1920,1080)

                ## TODO move the webserver to a separate file
                #self.webserver = CuteServer()
                #self.webserver.start()
                #self.webserver.setImageWidget( self )
                
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
                else:
                        self.setWindowState(Qt.WindowNoState)
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

if type(qApp.instance()) is type(None):
        app = QApplication([])
if __name__ == '__main__':
        label = RandMain()
        label.finishedExperiment.connect(qApp.quit)
        label.show()
        qApp.exec()
