#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import * # sound support

app = QApplication([])

class petriPlace(QGraphicsRectItem):
        labelText = None
        def paint(self, painter,option,widget):
                super().paint(painter,option,widget)
                #qp = QPainter(self)
                br = QBrush(QColor(100, 10, 10, 40))
                painter.setBrush(br)
                if self.labelText != None:
                        pos = self.rect()
                        #painter.drawText(round(pos.width()),round(pos.height()), self.labelText)
                        painter.drawText(round(pos.x()),round(pos.y()+pos.height()/2), self.labelText)
                        #painter.drawText(0,0, self.labelText)
                        #print( round(pos.width()),round(pos.height()) )
        def mouseDoubleClickEvent(self,event):
                self.labelText,_ = QInputDialog.getText(QWidget(), "Name the place", "Name for the place block:", QLineEdit.Normal,"")
                super().update()



scene = QGraphicsScene()
el1 = petriPlace(10,10,60,40)
el1.setFlag(QGraphicsItem.ItemIsMovable)
el1.labelText = "hi"
el2 = petriPlace(50,20,60,40)
el2.setFlag(QGraphicsItem.ItemIsMovable)
scene.addItem(el1)
scene.addItem(el2)
scene.addText('hello')

view = QGraphicsView(scene)
view.setDragMode( QGraphicsView.DragMode.ScrollHandDrag )
view.setMinimumSize( 400,700 )
view.show();




app.exec()