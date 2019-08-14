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

import time
import socket

BLUE = '34m'
ORANGE = '33m'

class tmp1(QLabel):
        def paintEvent(self,event):
                super().paintEvent(event)
                painter = QPainter(self)
                renderer =  QSvgRenderer('testsvg1.svg')
                #widget.resize(renderer.defaultSize())
                renderer.render(painter)
        def resizeEvent(self,event):
                super().resizeEvent(event)
                
                


app = QApplication([])

widget = tmp1()
widget.setGeometry(50,200,500,500)



widget.show()

## Working:
#svgWidget = QSvgWidget()
#svgWidget.renderer().load('testsvg1.svg')
#svgWidget.setGeometry(100,100,300,300)
#svgWidget.show()


app.exec()
