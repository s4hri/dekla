#!/usr/bin/env python3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import * # sound support

import popplerqt5
#from PyQt5.QtChart import * # this is external pkg!
import yaml

import time
import socket

BLUE = '34m'
ORANGE = '33m'


with open('petri1.yaml','r') as file:
        db = yaml.load(file,Loader=yaml.Loader)


app = QApplication([])
mainWidget = CuteView(db)
mainWidget.show()

app.exec()
if sock1 != None:
        sock1.close()