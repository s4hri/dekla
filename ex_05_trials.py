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

        self.participant, status = QInputDialog.getInt(QWidget(), "Participant id", "Participant id", 0, 0, 300000, 1);
        self.filenameResults = self.savefile+'id_'+str(self.participant)+'_date_'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.csv'

    def startExperiment(self):
        self.petri['current'] = 'place_initial'

        self.trialsFileName = 'ex_05_trials.csv'
        self.loadTrials()

        super().startExperiment()

    def stepExperiment(self):
        if self.petri['current'] == 'place_initial':
            first = self.trial['firstcolour']
            self.stacks['main'].setCurrentWidget( self.widgets[first] )
            # change the variable 'current' inside petri to 'showblue' after 1000ms
            self.petriTimer( 1000, 'current', 'showsecond' )
            self.petri['current'] = 'nothing'

        elif self.petri['current'] == 'showsecond':
            second = self.trial['secondcolour']
            self.stacks['main'].setCurrentWidget( self.widgets[second] )
            self.petriTimer( 1000, 'current', 'showthird' )
            self.petri['current'] = 'nothing'

        elif self.petri['current'] == 'showred':
            third = self.trial['thirdcolour']
            self.stacks['main'].setCurrentWidget( self.widgets[third] )

            if len(self.trials) > 0:
                self.sliceTrial()
                self.petriTimer( 1000, 'current', 'place_initial' )
            else:
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
