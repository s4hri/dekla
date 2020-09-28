#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import time
import datetime
import yaml
import socket
import csv
import random

if type(qApp.instance()) is type(None):
        app = QApplication([])
if __name__ == '__main__':
        scene = QGraphicsScene()
        view = QGraphicsView(scene)

        ellipse = QGraphicsEllipseItem()
        scene.addItem( ellipse )
        ellipse.setRect( 10, 10, 100, 100 )
        ellipse.setStartAngle( 90*16 )
        ellipse.setSpanAngle( 330*16 )
        
        view.show()

        qApp.exec()
