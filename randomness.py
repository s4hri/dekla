#!/usr/bin/env python3

""" Randomness task


"""

from dekla import *

class Cir(QObject):
        def __init__(self):
                super().__init__()
                self.circle1 = QGraphicsEllipseItem(100-25,-25,50,50)
                self.circle2 = QGraphicsEllipseItem(100-25,-25,50,50)
                self.circle3 = QGraphicsEllipseItem(100-25,-25,50,50)
                self.circle4 = QGraphicsEllipseItem(-50,-50,100,100)
                self.circle5 = QGraphicsEllipseItem(-150,-150,300,300)
                
                self.circle1.setBrush(Qt.red)
                self.circle2.setBrush(Qt.green)
                self.circle3.setBrush(Qt.blue)
                self.circle2.setRotation(120)
                self.circle3.setRotation(240)
        def _set_pos(self, pos):
                self.circle1.setRotation(pos.x())
                self.circle2.setRotation(pos.x()+120)
                self.circle3.setRotation(pos.x()+240)
        pos = pyqtProperty(QPointF, fset=_set_pos)    

class CuteAnim(QGraphicsView):
        def __init__(self):
                super().__init__()
                self.setMinimumSize(640,480)
                self.item1 = Cir()
                
                self.scene1 = QGraphicsScene()
                self.scene1.addItem(self.item1.circle1)
                self.scene1.addItem(self.item1.circle2)
                self.scene1.addItem(self.item1.circle3)
                self.scene1.addItem(self.item1.circle4)
                self.scene1.addItem(self.item1.circle5)
                self.currentAngle = 0
                # anim has to exist for Pause checking:
                self.anim = QPropertyAnimation(self.item1, b"pos")
                self.anim.setDuration(1000)
                self.anim.setEasingCurve(QEasingCurve.Linear)
                self.anim.finished.connect(self.finishedAnim)
                
                self.label1Item = QGraphicsSimpleTextItem("+1")
                self.label1Item.setFont(QFont( "Arial", 40, QFont.Bold))
                self.scene1.addItem(self.label1Item)
                #self.label1Item.adjustSize()
                self.label1Item.setPos( -self.label1Item.boundingRect().x()/2,-self.label1Item.boundingRect().y()/2, )
                self.label1Item.hide()
                self.label1rotation = 0

                #self.label1 = QLabel("+1")
                #self.label1.setAlignment(Qt.AlignCenter)
                #self.label1item = self.scene1.addWidget(self.label1)
                
                
                
                        
                self.setScene(self.scene1)
        def rotateObjects(self,angle):
                self.anim.setKeyValueAt(0.0, QPointF(self.currentAngle,         0))                   
                self.anim.setKeyValueAt(1.0, QPointF(self.currentAngle + angle, 0))
                
                self.anim.start()
                self.currentAngle += angle

        def showReward(self,inverted):
                if inverted:
                        self.label1Item.setRotation(180)
                else:
                        self.label1Item.setRotation(0)
                self.label1Item.show()
        def finishedAnim(self):
                # hide everything:
                self.label1Item.hide()


class RandMain(CuteMain):
        def __init__(self):
                db = dict()
                super().__init__(db)
                self.cuteAnim = CuteAnim()
                self.layoutStack['main'].addWidget(self.cuteAnim)
                pass
        def keyPressEvent(self,event):
                super().keyPressEvent(event)
                print( event.key() )
                if event.key() == Qt.Key_Left:
                        if self.cuteAnim.anim.state() == QAbstractAnimation.Stopped:
                                self.stepExperiment(120)
                if event.key() == Qt.Key_Right:
                        if self.cuteAnim.anim.state() == QAbstractAnimation.Stopped:
                                self.stepExperiment(-120)
        def full(self):
                if not self.windowState() == Qt.WindowFullScreen:
                        self.setWindowState(Qt.WindowFullScreen)
                else:
                        self.setWindowState(Qt.WindowNoState)
        def startExperiment(self):
                self.layoutStack['main'].setCurrentIndex(1)
                
        def stepExperiment(self,choice):
                if choice == 120: #left
                        self.cuteAnim.rotateObjects(120)

                if choice == -120: #right
                        self.cuteAnim.rotateObjects(-120)
                        
                        
                randomreward = random.randint(1,3)
                if randomreward == 1:
                        self.cuteAnim.showReward(inverted=False)
                if randomreward == 2:
                        self.cuteAnim.showReward(inverted=True)
                        
        def pauseExperiment(self):
                pass
        def trialsLeft(self):
                return 0

if __name__ == '__main__':
        label = RandMain()
        label.finishedExperiment.connect(qApp.quit)
        label.show()
        app.exec()
