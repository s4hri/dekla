#!/usr/bin/env python3

# TODO check pkg requirements for poppler


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *


class CuteSVG(QLabel):
        def __init__(self,svgfile):
                # buffer the svg file?
                self.filename = svgfile
        def paintEvent(self,event):
                super().paintEvent(event)
                painter = QPainter(self)
                renderer =  QSvgRenderer(self.filename)
                #widget.resize(renderer.defaultSize())
                renderer.render(painter)
        def resizeEvent(self,event):
                super().resizeEvent(event)
                

# or:


#svgWidget = QSvgWidget()
#svgWidget.renderer().load('testsvg1.svg')
#svgWidget.setGeometry(100,100,300,300)
#svgWidget.show()