#!/usr/bin/env python3
import time
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50010              # Arbitrary non-privileged port

t0 = None
while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                        while True:
                                data = conn.recv(1024)
                                if data==None or data==b'':
                                        break
                                if t0==None or data[0]=='a':
                                        t0 = time.perf_counter_ns()
                                print(f"Bump: {(time.perf_counter_ns()-t0)/1e9}: {data}")
                                data = None
