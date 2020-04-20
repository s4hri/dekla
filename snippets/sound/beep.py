#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *




app = QApplication([])
effect = QSoundEffect()
effect.setSource(QUrl.fromLocalFile('beep_CC_zero.wav'))
effect.setVolume(1.00)

button = QPushButton("Press me to play a beep sound")
button.pressed.connect(effect.play)
button.setMinimumSize(600,400)
button.show()
app.exec()
