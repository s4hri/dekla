import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import time
import re

import json

class PostHandler(BaseHTTPRequestHandler):
        def do_GET(self):
                if self.path.endswith('favicon.ico'):
                        return
                if self.path.endswith('index.html') or self.path=='/':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        with open('dekla_web.html') as htmlfile:
                                self.html = htmlfile.read()
                        self.wfile.write(self.html.encode('utf-8'))
                if None != re.search('/api/time', self.path):
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.send_header('Access-Control-Allow-Origin','*')
                        self.end_headers()
                        
                        self.wfile.write(str(time.time()).encode('utf-8'))
                        
                        return

        def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                self.send_response(200)
                self.end_headers()
                #response = BytesIO()
                #response.write(b'This is POST request. ')
                #response.write(b'Received: ')
                #response.write(body)
                print(body)
                #self.wfile.write(response.getvalue())
                
                print(type(json.loads(body.decode('utf-8'))))
if __name__ == '__main__':
    server = HTTPServer(('localhost', 8088), PostHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
