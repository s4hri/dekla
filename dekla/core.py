"""
MIT License

Copyright (c) 2020 Davide De Tommaso, Adam Lukomski - Social Cognition in Human-Robot Interaction

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import threading
import collections
import socket
import logging



class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def runRPCServer(address, instance):
    with SimpleThreadedXMLRPCServer(address, requestHandler=RequestHandler, allow_none=True, logRequests=False) as server:
        server.register_introspection_functions()
        server.register_instance(instance)
        server.serve_forever()

class DeklaMaster:

    MODULE_REGISTRATION_TIMEOUT = 2000

    def __init__(self, address=('localhost', 9966), logging_level=logging.DEBUG, logging_format = '%(asctime)s %(levelname)-5s: %(message)s'):
        logging.basicConfig(level=logging_level, format=logging_format)
        self._address = address
        self._registered_modules = collections.OrderedDict()
        self._registered_modules[self._address] = self.__class__.__name__
        self._module_registration = threading.Lock()
        t = threading.Thread(target=runRPCServer, args=(self._address, self))
        try:
            t.start()
            logging.debug("DeklaMaster is running ...")
        except RuntimeError:
            logging.error("DeklaMaster encountered an error during its execution.")

    def getAvailablePort(self, hostname):
        self._module_registration.acquire(blocking=True, timeout=DeklaMaster.MODULE_REGISTRATION_TIMEOUT)
        host_registered_modules = list(filter( lambda x: x[0] == hostname, list(self._registered_modules.keys())))
        released_ports = list(filter( lambda k: self._registered_modules[k] == None, list(self._registered_modules.keys()) ))
        if len(host_registered_modules) > 0:
            if len(released_ports) > 0:
                port = released_ports[0][1]
            else:
                port = host_registered_modules[-1][1] + 1
        else:
            port = self._address[1]+1
        return port

    def register(self, name, hostname, port):
        address = (hostname, port)
        self._registered_modules[address] = name
        logging.debug("A Dekla Module named %s has been registered with address %s", name, address)
        self._module_registration.release()

    def unregister(self, name):
        addr = self.getModuleAddress(name)
        self._registered_modules[addr] = None
        logging.debug("A Dekla Module named %s has been unregistered. The address %s is free to use", name, addr)

    def getRegisteredModules(self):
        return self._registered_modules

    def getModuleAddress(self, name):
        return list(self._registered_modules.keys())[list(self._registered_modules.values()).index(name)]

class DeklaModule:

    def __init__(self, deklamaster_address=('localhost', 9966)):
        self._deklamaster = xmlrpc.client.ServerProxy("http://%s:%d" % (deklamaster_address[0], deklamaster_address[1]))
        port = self._deklamaster.getAvailablePort(socket.gethostname())
        self._address = (socket.gethostname(), port)
        self._deklamaster.register(self.__class__.__name__, self._address[0],  self._address[1])
        threading.Thread(target=runRPCServer, args=(self._address, self)).start()
        logging.debug("Dekla module %s has started!", self.__class__.__name__)

    def unregister(self):
        self._deklamaster.unregister(self.__class__.__name__)
