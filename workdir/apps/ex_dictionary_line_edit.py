#!/usr/bin/env python3

'''
        usage:

        label = DictionaryLineEdit(dict1, 'hello', 'Just a test')

        after pressing 'enter' syncs the values to the dictionary


'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from dekla.widgets import DictionaryLineEdit

if __name__ == '__main__':
        app = QApplication([])
        dict1 = dict()
        dict1['hello'] = 'general kenobi'
        label = DictionaryLineEdit(dict1, 'hello', 'Just a test')
        #label.finishedExperiment.connect(qApp.quit)
        label.show()
        app.exec()
