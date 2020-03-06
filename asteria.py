#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import time
import datetime
import socket
import csv
import random

import json

class Asteria(QMainWindow):
        def __init__(self):
                super().__init__()
                self.tree1 = QTreeWidget()
                self.notes1 = QTextEdit()
                
                self.dock1 = QDockWidget("Objects")
                self.dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
                self.dock1.setWidget(self.tree1)
                self.addDockWidget(Qt.LeftDockWidgetArea, self.dock1)

                self.dock2 = QDockWidget("Notes")
                self.dock2.setAllowedAreas(Qt.RightDockWidgetArea | Qt.RightDockWidgetArea)
                self.dock2.setWidget(self.notes1)
                self.addDockWidget(Qt.RightDockWidgetArea, self.notes1)
                
                self.scene1 = QGraphicsScene()
                self.view1 = QGraphicsView(self.scene1)
                self.setCentralWidget(self.view1)
                self.resize(QSize(700,600))
                
                self.statusBar().showMessage("Ready")
       


if type(qApp.instance()) is type(None):
        app = QApplication([])
        
if __name__ == '__main__':
        label = Asteria()
        label.show()
        qApp.exec()
