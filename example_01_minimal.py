#!/usr/bin/env python3

from dekla import *

from PyQt5.QtWidgets import *


class Main(CuteMain):
        def __init__(self):
                super().__init__({})
                pass
        def keyPressEvent(self,event):
                super().keyPressEvent(event)
                print( event.key() )
        def startExperiment(self):
                pass
        def pauseExperiment(self):
                pass
        def trialsLeft(self):
                return 0

if __name__ == '__main__':
        label = Main()
        label.finishedExperiment.connect(qApp.quit)
        label.show()
        qApp.exec()
