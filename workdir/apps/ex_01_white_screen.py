#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from dekla import *

class Example1(Dekla):
    """ Basic example of using Dekla

    basic keyboard shortcuts are hard coded into Dekla,
    so q will quit the current example
    """
    def __init__(self):
        super().__init__()

        # add a basic window that supports multiple widgets that can be switched
        self.addScrollStack('main')

        # add a basic image from the assets folder
        self.stacks['main'].addImage('image1','assets/images/white.png')


if __name__ == '__main__':
    mainwindow = Example1()
    mainwindow.show()
    qApp.exec()
