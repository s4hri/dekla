#!/usr/bin/env python3

#
# Lemmings - main loop for parsing the petri net, in a thread
#               no timers, everything is flat with manual
#               time calculation
#               1e-6 delay included, about 30% cpu load
#
#
#
# TODO:
#   - in this version the images are not buffered yet, do it (saves 4ms)
#   - buffer pdf pages
#   - sounds
#
#
#

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import * # sound support


import popplerqt5             # this is external pkg!


# from PyQt5.QtChart import *   # this is external pkg!
import yaml

import time
import socket
import Executor


class Lemmings(QThread):
        evlist = None
        transitions = []
        keys = []
        quitConditions = {'external': 0, 'internal': 0}
        t0 = None
        
        def print(self,text):
                if sock1 != None:
                        sock1.sendall(text.encode())
        
        def time(self):
                return time.perf_counter_ns()-self.t0
        
        def run(self):
                if self.t0 == None:
                        self.t0 = time.perf_counter_ns()
                if self.evlist is None:
                        # default place to start, set manually for now:
                        # TODO fetch it from places structure
                        self.evlist = [db['info'].get('_start')]
                        #print(self.evlist)
                        
                while True not in self.quitConditions.values():
                        if type(self.evlist) != type(list()):
                                self.evlist = [self.evlist]
                        for ev in self.evlist:
                                if type(ev) == type([]):
                                        ev = ev[0]
                                cute.parse(ev)
                                if db['places'][ev].get('arc'):
                                        for arc in db['places'][ev].get('arc'):
                                                self.transitions.append((arc,self.time()))
                                        self.print(f"{self.time()}, added transition to {db['places'][ev].get('arc')}")
                        self.evlist = []
                        #self.print(f"{self.time()},scrapped all events")
                        #print(self.transitions)
                        for transition in self.transitions:
                                if db['transitions'][transition[0]].get('maxtime'):
                                        if self.time() > transition[1]+db['transitions'][transition[0]].get('maxtime')*1e9:
                                                self.evlist.append( db['transitions'][transition[0]].get('arc') )
                                                self.print( f"{self.time()}, added place: {db['transitions'][transition[0]].get('arc')}" )
                                                while transition in self.transitions:
                                                        self.transitions.remove(transition)
                                #if 'keyboard' in db['transitions'][transition[0]].keys():
                                        #db['transitions'][transition[0]].get('keyboard')
                                        
                        if len(self.evlist)==0 and len(self.transitions)==0:
                                self.quitConditions['internal'] = 1
                                print("internal quit condition triggered")
                        #time.sleep(1e-6)
                print('quitting')
        def load(self,db):
                pass

class CuteView(QLabel):
        def __init__(self,db):
                super().__init__()
                self.setMinimumSize(640,480)
                self.setText("press S to start")
                self.currentPixmap = None
                self.timerlist = []
                self.imagelist = [ db['places'][s]['show'] for s in db['places'] if 'show' in db['places'][s].keys() if db['places'][s]['show']!='None' ]
                self.images = {image: QPixmap.fromImage(QImage(image)) for image in self.imagelist}
                self.labelText = None
                self.executor = Executor.Executor()
        def image(self,filename):
                #image = QImage(filename)
                #self.currentPixmap = QPixmap.fromImage(image)
                if '.png' in filename:
                        self.currentPixmap = self.images.get(filename)
                if '.pdf' in filename:
                        d = popplerqt5.Poppler.Document.load( filename )
                        d.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
                        d.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
                        d.setRenderHint(popplerqt5.Poppler.Document.TextHinting)
                        d.setRenderHint(popplerqt5.Poppler.Document.ThinLineSolid)
#                        d.setRenderHint(popplerqt5.Poppler.Document.ThinLineShape)
                        page1 = d.page(0)
                        self.currentPixmap = QPixmap.fromImage(page1.renderToImage( 600,600,-1,-1,-1,-1 ) )
                self.setPixmap( self.currentPixmap.scaled(self.size()) )
                self.update()
        def full(self):
                if not self.windowState() == Qt.WindowFullScreen:
                        self.setWindowState(Qt.WindowFullScreen)
                else:
                        self.setWindowState(Qt.WindowNoState)
        def keyPressEvent(self,event):
                print( event.key() )
                if event.key() == Qt.Key_F:
                        self.full()
                if event.key() == Qt.Key_Q:
                        lemmings.quitConditions['external'] = 1
                        time.sleep(1e-3)
                        lemmings.quit()
                        self.executor.quit()
                        app.quit()
                if event.key() == Qt.Key_S:
                        if lemmings.isRunning():
                                lemmings.quitConditions['external'] = 1
                        else:
                                lemmings.quitConditions['external'] = 0
                                lemmings.start()
                # if event.key() in frameKeys:
                        # self.parseKey()
        def closeEvent(self,event):
                lemmings.quit()
                self.executor.quit()
                super().closeEvent(event)
        def resizeEvent(self,event):
                if self.currentPixmap != None:
                        self.setPixmap( self.currentPixmap.scaled(self.size()) )
        def paintEvent(self, event):
                super().paintEvent(event)
                qp = QPainter(self)
                br = QBrush(QColor(100, 10, 10, 40))
                qp.setBrush(br)
                if self.labelText != None:
                        pos = self.size()
                        qp.drawText(pos.width()/2,pos.height()/2, self.labelText)
        def playsound(self, filename):
                effect = QSoundEffect()
                effect.setSource(QUrl.fromLocalFile("untitled.wav"))
                #effect.setLoopCount(QSoundEffect.Infinite)
                effect.setVolume(0.25)
                effect.play()
        def parse(self,ev):
                if 'show' in db['places'][ev].keys():
                        if db['places'][ev].get('show') != None:
                                self.image(db['places'][ev].get('show'))
                                if sock1 != None:
                                        sock1.sendall(f'showing'.encode())
                if 'exec' in db['places'][ev].keys():
                        if db['places'][ev].get('exec') != None:
                                t1 = time.perf_counter_ns()
                                self.executor.exec( db['places'][ev].get('exec') )
                                if sock1 != None:
                                        sock1.sendall(f"Exec took: {(time.perf_counter_ns()-t1)/1e6}ms".encode())
                if 'text' in db['places'][ev].keys():
                        if db['places'][ev].get('text') != None:
                                self.labelText = db['places'][ev].get('text')
                if 'pdf' in db['places'][ev].keys():
                        if db['places'][ev].get('pdf') != None:
                                self.image( db['places'][ev].get('pdf') )



BLUE = '34m'
ORANGE = '33m'
def colourfull(colour, text):
        coloured_text = f"\033[{colour}{text}\033[00m"
        return coloured_text






try:
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(('127.0.0.1', 50010))
except OSError as msg:
        sock1 = None
        print(colourfull(ORANGE,"WARNING:"),"Please create a logger service if a time log is needed")

with open('petri1.yaml','r') as file:
        db = yaml.load(file,Loader=yaml.Loader)

app = QApplication([])

lemmings = Lemmings()
lemmings.load(db)


cute = CuteView(db)
cute.show()

#mainWidget = CuteView(db)
#mainWidget.show()
app.exec()
if sock1 != None:
        sock1.close()