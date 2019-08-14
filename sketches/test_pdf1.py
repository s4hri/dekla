#!/usr/bin/env python3

#
# nonlinear timeline for robotics/psychology experiments
#

# previous took 9ms extra after timer to actually finish showing
# an image
# VERSION WITH: buffering images
# this on average take extra 4ms after each timer

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
#from PyQt5.QtChart import * # this is external pkg!
import yaml
import popplerqt5

import time
import socket

BLUE = '34m'
ORANGE = '33m'

class CuteTime( QLabel ):
        currentPixmap = None
        def setImage(self,image):
                self.currentPixmap = QPixmap.fromImage(image)
                self.resizeEvent(None)
                #widget.setGeometry(20,20,image.width(),image.height())
        def keyPressEvent(self,event):
                print( event.key() )
                if event.key() == Qt.Key_F:
                        self.full()
                if event.key() == Qt.Key_Q:
                        app.quit()
        def full(self):
                if not self.windowState() == Qt.WindowFullScreen:
                        self.setWindowState(Qt.WindowFullScreen)
                else:
                        self.setWindowState(Qt.WindowNoState)
        def resizeEvent(self,event):
                if self.currentPixmap != None:
                        self.setPixmap( self.currentPixmap.scaled(self.size(),Qt.KeepAspectRatio) )



app = QApplication([])

d = popplerqt5.Poppler.Document.load('beam1.pdf')
d.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
page1 = d.page(0)
image = page1.renderToImage( 300,300,-1,-1,-1,-1 )

widget = CuteTime()
widget.setImage(image)

widget.show()

## Working:
#svgWidget = QSvgWidget()
#svgWidget.renderer().load('testsvg1.svg')
#svgWidget.setGeometry(100,100,300,300)
#svgWidget.show()


app.exec()
