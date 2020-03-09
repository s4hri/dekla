#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AnimatedLabel(QObject):
        def __init__(self,image):
                super().__init__()
                self.label = QLabel()
                self.pixmap = QPixmap.fromImage(QImage(image))
                self.label.setPixmap( self.pixmap )
        
        def _set_angle(self, angle):
                transformation = QTransform()
                transformation.rotate(angle)
                self.pixmapRotated = self.pixmap.transformed( transformation )
                self.label.setPixmap( self.pixmapRotated )

        angle = pyqtProperty(float, fset=_set_angle)



# make sure there exists a Qt5 application
if type(qApp.instance()) is type(None):
        app = QApplication([])

if __name__ == '__main__':
        widget = QWidget()

        animatedLabel = AnimatedLabel("red.png")
        
        anim = QPropertyAnimation(animatedLabel, b"angle")
        anim.setDuration(1000)
        anim.setEasingCurve(QEasingCurve.Linear)
        anim.setKeyValueAt(0.0, float(0))                   
        anim.setKeyValueAt(1.0, float(180))
        
        button = QPushButton()
        button.clicked.connect( anim.start )
        
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(animatedLabel.label)
        
        widget.setLayout(layout)
        widget.show()
        
        app.exec()
