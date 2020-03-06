#!/usr/bin/env python3

""" Randomness task


"""

from dekla import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import time
import datetime
import yaml
import socket
import csv
import random

class General(QWidget):
        





if type(qApp.instance()) is type(None):
        app = QApplication([])

if __name__ == '__main__':
        label = RandMain()
        label.finishedExperiment.connect(qApp.quit)
        label.show()
        qApp.exec()
