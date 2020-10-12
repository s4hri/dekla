#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from dekla import *

class Example1(Dekla):
    """ Using multiple windows with Dekla

    basic keyboard shortcuts are hard coded into Dekla,
    so q will quit the current example
    """
    def __init__(self,simulation=True, modeRobot='social1'):
        super().__init__()

        self.addScrollStack('main')
        self.stacks['main'].addImage('image1','assets/images/white.png')

        self.addScrollStack('left')
        self.stacks['main'].addImage('image2','assets/images/white.png')

        self.addScrollStack('right')
        self.stacks['main'].addImage('image3','assets/images/white.png')


if __name__ == '__main__':
    mainwindow = Example1()
    mainwindow.show()
    qApp.exec()
