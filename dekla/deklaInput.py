#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

'''
        Usage:
                keys = { 'player1':0, 'player2':0 }
                inputWidget = DeklaInput(keys)
                inputWidget.captureFinished.connect(assignKeys)
                inputWidget.show()
                ...

                def assignKeys(self,keys):
                        self.keys = keys

                        if self.keys['player1'] == Qt.Key_Up:
                                ...
 
'''

class DeklaInput(QWidget):
        # default key dict, you can provide your own
        capturedKeys = { 'player1z': Qt.Key_Z, 
                         'player1m': Qt.Key_M,
                         'player2z': Qt.Key_A,
                         'player2m': Qt.Key_K }
        
        cycle = None
        capturingKeys = False
        
        labels = dict()
        labelVerification = dict()
        
        ''' init takes one optional argument:
                dict with names for keys to be captured
        '''
        def __init__(self,*args):
                super().__init__()
                #self.setText("waiting for key event")
                if args:
                        for arg in args:
                                if type(arg) is type(dict()):
                                        print('got custom key list')
                                        self.capturedKeys = arg
                else:
                        print('using default key list')
                        
                
                startbutton = QPushButton("Begin capture/verification")
                startbutton.pressed.connect(self.startCapture)
                
                #grid = QGridLayout()
                #grid.addWidget(startbutton,0,0)
                layout = QVBoxLayout()
                layout.addWidget(startbutton)
                for key in self.capturedKeys:
                        self.labels[key] = QLabel("...            ..")
                        self.labelVerification[key] = QLabel("...        ..")
                        layout.addWidget(self.labels[key])
                        layout.addWidget(self.labelVerification[key])
                
                self.order = list(self.capturedKeys.keys())
                self.setLayout(layout)
        
        def keyPressEvent(self,event):
                super().keyPressEvent(event)
                
                if self.capturingKeys:
                        if not self.verification:
                                self.capturedKeys[self.order[self.cycle]] = event.key()
                                self.labels[ self.order[self.cycle] ].setText("got a key")
                                self.labelVerification[ self.order[self.cycle] ].setText("waiting for verification")
                                self.verification = True
                        else:
                                if event.key() == self.capturedKeys[self.order[self.cycle]]:
                                        self.labelVerification[ self.order[self.cycle] ].setText("waiting for verification")
                                        self.verification = False
                                        self.cycle += 1
                                        if self.cycle < len(self.order):
                                                self.labels[ self.order[self.cycle] ].setText("waiting for key: "+str(self.order[self.cycle]))
                                        else:
                                                self.capturingKeys = False
                                                self.captureFinished.emit(self.capturedKeys)
                                                for order in self.order:
                                                        self.labels[ order ].setText("...            ..")
                                                        self.labelVerification[ order ].setText("...            ..")
                                                print( self.capturedKeys )

        def startCapture(self):
                if len(self.capturedKeys)>0:
                        self.capturingKeys = True
                        self.cycle = 0
                        self.verification = False
                        # self.label.setText("waiting for player 1 key left")
                        self.labels[ self.order[self.cycle] ].setText("waiting for key: "+str(self.order[self.cycle]))

        captureFinished = pyqtSignal(dict)

if __name__ == '__main__':
        app = QApplication([])
        # label = DeklaInput({'a':0,'b':0}) # use custom dict
        label = DeklaInput() # use default
        label.show()
        qApp.exec()
