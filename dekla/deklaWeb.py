from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
import re
import json
import time
import io


# <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

website1 = """
<!doctype html>
<html lang="en">
<head>
        <meta charset="UTF-8">
        <title>Dekla interface</title>
        <script src="//code.angularjs.org/snapshot/angular.min.js"></script>
        
        <script src="https://raw.githubusercontent.com/angular-ui/bootstrap/gh-pages/ui-bootstrap-tpls-2.5.0.js"></script>
        <link href="//netdna.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
</head>
<body ng-app="hekateSketch">
        <script>
        angular.module('hekateSketch', [])
        .controller('HekateController', ['$scope', '$interval', '$http', '$templateCache',
        function($scope, $interval, $http, $templateCache)
        {
                var stop;
                var imageBaseUrl = 'http://localhost:8088/api/image'
                $scope.doStuff = function()
                {
                        if ( angular.isDefined(stop) ) return;
                        stop = $interval(function()
                        {
                                $http({method: 'GET', url: 'http://localhost:8088/api/time'}).
                                then(function(response)
                                {
//                                         var current = document.getElementById("logger").value; 
                                        $scope.status = response.status;
//                                         $scope.data = current + "\\n" + response.data;
//                                         document.getElementById("logger").value = = current + "\\n" + response.data;
                                        $scope.logger += "\\n"
                                        $scope.logger += response.data;
                                        
                                        
                                        // update the image preview:
                                        $scope.imageUrl = imageBaseUrl + '?' + new Date().getTime();
                                });
                        }, 100);
                };

// //         autostart:
         $scope.doStuff();
        
                $scope.stopFight = function()
                {
                        if (angular.isDefined(stop))
                        {
                                $interval.cancel(stop);
                                stop = undefined;
                        }
                };

                $scope.resetFight = function()
                {
                        var url = 'posturl', data = '{"a":"B"}',config='application/json ';
                        $http.post(url, data, config).then(function (response)
                        {
                                // This function handles success
                        }, function (response) {
                                // this function handles error
                        });
                };
                $scope.$on('$destroy', function()
                {
                        $scope.stopFight();
                });
                
               
                
        }]);
</script>

<div>
  <div ng-controller="HekateController">
    <table>
    <tbody>
    <tr>
        <td><button type="button" data-ng-click="doStuff()">Do stuff</button></td>
        <td>http response data: {{data}}</td>
    </tr>
    <tr>
        <td><button type="button" data-ng-click="stopFight()">StopFight</button></td>
        <td>http response data: {{data}}</td>
    </tr>
    <tr>
        <td><button type="button" data-ng-click="resetFight()">resetFight</button></td>
        <td>http response data: {{data}}</td>
    </tr>
    <tr>
        <td>
        <textarea id="textArea" rows="30" cols="50" ng-model="logger">
        Logging trial
        </textarea>
        </td>
    </tr>
    <tr>
        <td>
        <img ng-src={{imageUrl}} width=192 height=108></img>
        </td>
    </tr>
    </tbody>
    </table>
  </div>
</div>



</body>
</html>
"""

uglyHackImage = None

class CuteServer(QThread):
        def __init__(self):
                super().__init__()
                print('Starting server')
                self.server = HTTPServer(('localhost', 8088), PostHandler)
        def run(self):
                self.server.serve_forever()
        def setImageWidget(self,widget):
                global uglyHackImage
                uglyHackImage = widget

class PostHandler(BaseHTTPRequestHandler):
        imageWidget = None
        
        def do_GET(self):
                # check what is requested:
                if self.path.endswith('favicon.ico'):
                        # TODO implement icon for the web interface
                        return
                # this will grab ANY index.html, not necessarily the main one
                if self.path.endswith('index.html') or self.path=='/':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()

                        ## send the file
                        #with open('.deklaWeb.html') as htmlfile:
                                #self.html = htmlfile.read()
                        ## encoding is added the the Contect-Type, check it later
                        #self.wfile.write(self.html.encode('utf-8'))
                        
                        #html = website1
                        #html.replace("\n", "\\\n")
                        self.wfile.write(website1.encode('utf-8'))
                
                if None != re.search('/api/time', self.path):
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.send_header('Access-Control-Allow-Origin','*')
                        self.end_headers()
                        self.wfile.write(str(time.time()).encode('utf-8'))
                        return
                if None != re.search('/api/image', self.path):
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.send_header('Access-Control-Allow-Origin','*')
                        self.end_headers()
                        
                        #if type(self.imageWidget) is not type(None):
                        #self.imageWidget.grab().toImage().save('test.jpg')
                        global uglyHackImage
                        aaa = uglyHackImage.grabImage()
                        print("Image saved")
                        self.wfile.write(aaa)
                        #else:
                                #print("Not saving image")
                        return
                #if None != re.search('/api/status', self.path):
                        #self.send_response(200)
                        #self.send_header('Content-type','text/html')
                        #self.send_header('Access-Control-Allow-Origin','*')
                        #self.end_headers()
                        #self.wfile.write(str(time.time()).encode('utf-8'))
                        #return

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

