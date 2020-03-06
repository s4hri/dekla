#!/usr/bin/env python3

# TODO check pkg requirements for poppler


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5.QtSvg import *

import popplerqt5

class CuteTime( QLabel ):
        def __init__(self,image=None):
                super().__init__()
                # if type(image) is not type(None):
                #   self.setImage(image)
                
        currentPixmap = None
        def setImage(self,filename):
                d = popplerqt5.Poppler.Document.load(filename)
                d.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
                page1 = d.page(0)
                image = page1.renderToImage( 300,300,-1,-1,-1,-1 )
                self.currentPixmap = QPixmap.fromImage(image)
                self.resizeEvent(None)
                
