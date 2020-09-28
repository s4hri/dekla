#!/usr/bin/env python3

import xmlrpc.client
import time

test1 = xmlrpc.client.ServerProxy('http://localhost:8081')

print(test1.system.listMethods())

test1.start_trial()
test1.turnLeft()
test1.turnRight()
test1.end_trial()

