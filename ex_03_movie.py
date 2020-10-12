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

        # add a movie under the name 'video1'
        self.stacks['main'].addVideo('video1','assets/movies/movie1.mp4')

        # afterwards it is accessible in widgets dictionary under the 'video1':
        self.widgets['video1'].player.play()

        # set the size manually, since the video is larger AND is inside a stack
        # you can drag it around
        self.windows['main'].setMinimumSize(640,480)

if __name__ == '__main__':
    mainwindow = Example1()
    mainwindow.show()
    qApp.exec()
