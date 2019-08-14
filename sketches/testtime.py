from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time

app = QApplication([])

label = QLabel()
label.setMinimumSize(200,200)
label.show()

i=0
times = []
while i<1000000:
        t0 = time.perf_counter_ns()
        i = i+1
        times.append( time.perf_counter_ns() - t0 )
        if i%1000==0:
                text = f'{i},{sum(times)/len(times)}'
                print(text)

app.exec()
