#!/usr/bin/env python3

import socket
import time
import io

class CuteLog:
        def __init__(self):
                self.initTime = self.time()
                try:
                        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.sock1.connect(('127.0.0.1', 50010))
                except OSError as msg:
                        self.sock1 = None
                        print("Please create a logger service if a time log is needed")
        
        def time(self):
                return time.time()
                # time.time_ns()
        
        def print(self,*args): #,**kwargs):
                # workaround to get nice print results
                out = io.StringIO()
                print( '{:8.2f}:'.format(self.time()-self.initTime), *args, file=out) #, **kwargs )
                content = out.getvalue()
                out.close()
                
                print(content)
                if self.sock1 != None:
                        self.sock1.sendall(content.encode('utf-8'))



# server part:
# TODO make a thread out of it, classic python threading


#HOST = ''                 # Symbolic name meaning all available interfaces
#PORT = 50010              # Arbitrary non-privileged port

#t0 = None
#while True:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                #s.bind((HOST, PORT))
                #s.listen(1)
                #conn, addr = s.accept()
                #with conn:
                        #while True:
                                #data = conn.recv(1024)
                                #if data==None or data==b'':
                                        #break
                                #if t0==None or data[0]=='a':
                                        #t0 = time.perf_counter_ns()
                                #print(f"Bump: {(time.perf_counter_ns()-t0)/1e9}: {data}")
                                #data = None



#cuteLog = CuteLog()
