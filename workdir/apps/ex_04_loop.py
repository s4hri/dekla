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
        self.stacks['main'].addImage('white','assets/images/white.png')
        self.stacks['main'].addImage('blue','assets/images/blue.png')
        self.stacks['main'].addImage('red','assets/images/red.png')

    def startExperiment(self):
        self.petri['current'] = 'place_initial'

        # prepare a list of trials
        self.trials = list()
        # add first trial (no variables, but the length of trials is now 1)
        self.trials.append( dict() )

        super().startExperiment()

    def stepExperiment(self):
        if self.petri['current'] == 'place_initial':
            self.stacks['main'].setCurrentWidget( self.widgets['white'] )
            # change the variable 'current' inside petri to 'showblue' after 1000ms
            self.petriTimer( 1000, 'current', 'showblue' )
            self.petri['current'] = 'nothing'

        elif self.petri['current'] == 'showblue':
            self.stacks['main'].setCurrentWidget( self.widgets['blue'] )
            self.petriTimer( 1000, 'current', 'showred' )
            self.petri['current'] = 'nothing'

        elif self.petri['current'] == 'showred':
            self.stacks['main'].setCurrentWidget( self.widgets['red'] )
            self.petriTimer( 1000, 'current', 'stop' )
            self.petri['current'] = 'nothing'

        elif self.petri['current'] == 'stop':
            self.stopExperiment()

        elif self.petri['current'] == 'nothing':
            pass # this is just to show that 'nothing' means nothing
                 # using time.sleep() is not an option, GUI must be responsive


if __name__ == '__main__':
    mainwindow = Example1()
    mainwindow.show()
    qApp.exec()
