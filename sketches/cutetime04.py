#!/usr/bin/env python3

#
# nonlinear timeline for robotics/psychology experiments
#

# previous took 9ms extra after timer to actually finish showing
# an image
# VERSION WITH: buffering images
# this on average take extra 4ms after each timer

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5.QtChart import * # this is external pkg!
import yaml

import time
import socket

BLUE = '34m'
ORANGE = '33m'

class CuteTask(QTimer):
        def __init__(self,name,time,parent):
                super().__init__()
                self.name = name
                self.parent = parent
                self.setTimerType(Qt.PreciseTimer)
                #self.setSingleShot(True)
                self.start(time*1000)
                print(f"CuteTask: __init__ created: {name}, {time}")
                
                
        def timerEvent(self,event):
                print(f"CuteTask: timeout: {self.name}")
                self.parent.parse(self.name)
                self.stop()

class CuteView(QLabel):
        def __init__(self,db):
                super().__init__()
                self.setMinimumSize(640,480)
                self.setText("press S to start")
                self.currentPixmap = None
                self.timerlist = []
                self.imagelist = [ db[s]['show'] for s in db if 'show' in db[s].keys() if db[s]['show']!='None' ]
                self.images = {image: QPixmap.fromImage(QImage(image)) for image in self.imagelist}
                self.labelText = None
        def image(self,filename):
                #image = QImage(filename)
                #self.currentPixmap = QPixmap.fromImage(image)
                self.currentPixmap = self.images.get(filename)
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
                        app.quit()
                if event.key() == Qt.Key_S:
                        self.start()
                # if event.key() in frameKeys:
                        # self.parseKey()
        def resizeEvent(self,event):
                if self.currentPixmap != None:
                        self.setPixmap( self.currentPixmap.scaled(self.size()) )
        def start(self):
                evlist = [ s for s in db if db[s]['depends']=='None' ]
                print(evlist)
                self.parse(evlist)
                
        def paintEvent(self, event):
                super().paintEvent(event)
                qp = QPainter(self)
                br = QBrush(QColor(100, 10, 10, 40))
                qp.setBrush(br)
                if self.labelText != None:
                        pos = self.size()
                        qp.drawText(pos.width()/2,pos.height()/2, self.labelText)
                
        def parse(self,evlist):
                print(f"Parsing: {evlist}")
                if type(evlist) != type(list()):
                        evlist = [evlist]
                        print(evlist)
                for ev in evlist:
                        if 'show' in db[ev].keys():
                                if db[ev].get('show') != None:
                                        self.image(db[ev].get('show'))
                                        if sock1 != None:
                                                sock1.sendall(f'showing'.encode())
                        if 'time' in db[ev].keys():
                                if db[ev].get('time') != None:
                                        schedulelist = [ s for s in db if db[s]['depends']==ev ]
                                        for scheduleev in schedulelist:
                                                
                                                if db[scheduleev].get('delay'):
                                                        total = db[ev].get('time')+db[ev].get('delay')
                                                else:
                                                        total = db[ev].get('time')
                                                self.timerlist.append( CuteTask(scheduleev,total,self) )
                                                print(f"Scheduling {scheduleev} in {total} seconds")
                        if 'exec' in db[ev].keys():
                                if db[ev].get('exec') != None:
                                        t1 = time.perf_counter_ns()
                                        exec( db[ev].get('exec'),globals(), globals() )
                                        if sock1 != None:
                                                sock1.sendall(f"Exec took: {(time.perf_counter_ns()-t1)/1e6}ms".encode())
                        if 'text' in db[ev].keys():
                                if db[ev].get('text') != None:
                                        self.labelText = db[ev].get('text')


def colourfull(colour, text):
        coloured_text = f"\033[{colour}{text}\033[00m"
        return coloured_text


try:
	sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock1.connect(('127.0.0.1', 50009))
except OSError as msg:
	sock1 = None
	print(colourfull(ORANGE,"WARNING:"),"Please create a logger service if a time log is needed")



with open('test1.yaml','r') as file:
        db = yaml.load(file,Loader=yaml.Loader)
app = QApplication([])
mainWidget = CuteView(db)
mainWidget.show()

app.exec()
if sock1 != None:
        sock1.close()