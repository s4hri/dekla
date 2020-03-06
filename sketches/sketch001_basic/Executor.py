#!/usr/bin/env python3
import PyQt5.QtCore


class Executor(PyQt5.QtCore.QThread):
        enviro = globals()
        command = None
        def run(self):
                exec(self.command,self.enviro,self.enviro)
        def exec(self,commands):
                self.command = commands
                self.start()

#exe = Executor()
#exe.exec('a=5')
#exe.exec('print(dir())')
#print(dir())