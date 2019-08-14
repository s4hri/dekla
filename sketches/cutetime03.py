#!/usr/bin/env python3

#
# nonlinear timeline for robotics/psychology experiments
#


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5.QtChart import * # this is external pkg!
import yaml

import time
import socket

class CuteTask(QTimer):
        def __init__(self,name,time,parent):
                super().__init__()
                self.name = name
                self.parent = parent
                #self.setSingleShot(True)
                self.start(time*1000)
                print(f"CuteTask: __init__ created: {name}, {time}")
        def timerEvent(self,event):
                print(f"CuteTask: timeout: {self.name}")
                self.parent.parse(self.name)
                self.stop()

class CuteView(QLabel):
        def __init__(self):
                super().__init__()
                self.setMinimumSize(640,480)
                self.setText("press S to start")
                self.currentPixmap = None
                self.timerlist = []
        def image(self,filename):
                image = QImage(filename)
                self.currentPixmap = QPixmap.fromImage(image)
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
        def resizeEvent(self,event):
                if self.currentPixmap != None:
                        self.setPixmap( self.currentPixmap.scaled(self.size()) )
        def start(self):
                evlist = [ s for s in db if db[s]['depends']=='None' ]
                print(evlist)
                self.parse(evlist)
        def parse(self,evlist):
                print(f"Parsing: {evlist}")
                if type(evlist) != type(list()):
                        evlist = [evlist]
                        print(evlist)
                for ev in evlist:
                        if 'show' in db[ev].keys():
                                if db[ev].get('show') != None:
                                        self.image(db[ev].get('show'))
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
                                        print(f"Exec took: {(time.perf_counter_ns()-t1)/1e6}ms")

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1.connect(('127.0.0.1', 50008))
#s.sendall('test'.encode())

app = QApplication([])
mainWidget = CuteView()
with open('test1.yaml','r') as file:
        db = yaml.load(file,Loader=yaml.Loader)
mainWidget.show()

app.exec()
sock1.close()