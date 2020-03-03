# dekla
Experiment builder

# notes:

The YAML file conforms to the Petri net graph layout 

N = (P,T,F) - places, transitions, F - arcs (flow relations)

the hybrid version with the time 

--

All the time objects are kept in a separate vector and updated
they produce interrupts when timed out and update the state as a discrete events

the watchdog is a process scrubbing the net after each discrete update
for example: after you reach certain keypoints you erase all the tokens left behind
and disable the ability to produce tokens there
we do not want to have suddenly two different parts of the timeline engaging at the same time - in this manner we are more prone to follow the Gantt graphs - after you finish an operation it implies you will never go back and relaunch the old ones - you just live on and deal with the consequences

the net within a net

first (most-inner) net is the experiment itself, it is actually a deployable net
it contains all the informations about the experiment, a set of variables with default values and acceptable ranges, all the time information (or placeholders for the experimentally established range values)

the second net is the trial structure
this is actually more like a simulink model, the inner net can be started using different initial state and variables 











The visualisation has been created that aims to look like more a flowchart than a Petri net, in order to be more readable by the end-user.




---


- tobii glasses
- audio
- keypresses
- triggers from anywhere
  ethernet, mouse, keyboard
    microphone over ethernet
    keypresses over ethernet
    joystick over ethernet
- [far future] python code with separate, persistent variables (scope)

Main engine should load a yaml file, prepare a chain
of events and then execute them - so pretty much
no actual computations once the experiment starts.

Not everything will be possible, some things will
be dynamic and with variable triggers.

Buffer all images, all audio. 

Send python commands in a separate thread, non-blocking. (exec commands are in another thread)

---

TODO:

- sanity check module - full diagnosis of the icub connection, of the yaml file,
  of the modules used in the yaml file
  
  


- multiple screen support 30%
- customizable key actions in yaml
- sounds
- encapsulate pyicub inside functions

- load from directory or a .zip file

---

info field:
  robot - can be icub, bioloid, wheeled
  screens - screens that will be used, for example: 0,1 (yes, comma separated)
 
  date - timestamp that you want to have in report files
  behaviour - time behaviour, what do you want to do with microdelays? by default
   the behaviour is to aggregate, but you can set 'strict' to work in absolute time

        
---

keyEvent:

https://doc.qt.io/qt-5/qt.html#Key-enum



https://doc.qt.io/qt-5/qtsvg-index.html
https://doc.qt.io/qt-5/qtsvg-svggenerator-example.html#
https://doc.qt.io/qt-5/qtsvg-svgviewer-example.html#



External trigger:
        1. make another socket with a custom port
        2. use 80 and wait for any message, grep to find a pattern



audio:
from PyQt5.QtMultimedia import *
https://doc.qt.io/qt-5/qaudiooutput.html#notify
Designer: see the waveform


just in case:
https://pythonprogramminglanguage.com/pyqt5-video-widget/







do NOT use QtCharts - in python it is external
and not easy enough to install



#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtCharts/QChartView>
#include <QtCharts/QStackedBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QLegend>
#include <QtCharts/QBarCategoryAxis>

QT_CHARTS_USE_NAMESPACE

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QBarSet *set0 = new QBarSet("Jane");
    QBarSet *set1 = new QBarSet("John");
    QBarSet *set2 = new QBarSet("Axel");
    QBarSet *set3 = new QBarSet("Mary");
    QBarSet *set4 = new QBarSet("Samantha");

    *set0 << 1 << 2 << 3 << 4 << 5 << 6;
    *set1 << 5 << 0 << 0 << 4 << 0 << 7;
    *set2 << 3 << 5 << 8 << 13 << 8 << 5;
    *set3 << 5 << 6 << 7 << 3 << 4 << 5;
    *set4 << 9 << 7 << 5 << 3 << 1 << 2;

    QStackedBarSeries *series = new QStackedBarSeries();
    series->append(set0);
    series->append(set1);
    series->append(set2);
    series->append(set3);
    series->append(set4);

    QChart *chart = new QChart();
    chart->addSeries(series);
    chart->setTitle("Simple stackedbarchart example");
    chart->setAnimationOptions(QChart::SeriesAnimations);

    QStringList categories;
    categories << "Jan" << "Feb" << "Mar" << "Apr" << "May" << "Jun";
    QBarCategoryAxis *axis = new QBarCategoryAxis();
    axis->append(categories);
    chart->createDefaultAxes();
    chart->setAxisX(axis, series);

    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);

    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);

    QMainWindow window;
    window.setCentralWidget(chartView);
    window.resize(420, 300);
    window.show();

    return a.exec();
}




------



Flask
        https://medium.com/@balramchavan/angular-python-flask-full-stack-demo-27192b8de1a3
        https://auth0.com/blog/using-python-flask-and-angular-to-build-modern-apps-part-1/
        https://github.com/pallets/flask/blob/master/examples/tutorial/flaskr/blog.py
        https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-facelift
        
        
        
        

Node.js
        has js-yaml
                https://www.npmjs.com/package/js-yaml
        https://thisdavej.com/getting-started-with-yaml-in-node-js-using-js-yaml/
        https://socket.io/get-started/chat
        https://nodejs.org/api/net.html

AngularJS
        https://angularjs.org/
        https://angular.io/tutorial/toh-pt0
        https://www.w3schools.com/angular/angular_forms.asp
        https://www.fullstackpython.com/angular.html
        
        
Meteor
        meteor.com
        uses either Blaze or Angular for UI
        https://www.meteor.com/tutorials/angular/templates

Coffeescript
QuickUI


Petal


Rust + Rocket
        https://rocket.rs/
        https://rocket.rs/v0.4/guide/responses/#templates
        
        
Ruby on Rails
        https://guides.rubyonrails.org/getting_started.html



        
WebAssembly
        C / C++ / Rust - as main proposals
  

Electron - desktop only?

java + spring



Django with Python3
        I would either way require yaml
        http://dev.splunk.com/view/webframework-djangobindings/SP-CAAAESP
        https://vsupalov.com/django-app-looks-bad/
        https://www.jamesstone.com/python-css-frameworks/
