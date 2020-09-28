#!/usr/bin/env python3
import time
import threading

from pykron.core import AsyncRequest

import yarp
from pyicub.api.iCubHelper import iCub, ROBOT_TYPE, ICUB_PARTS
from pyicub.api.classes.Logger import YarpLogger

class ROBOT_VISUAL_TARGETS:
        DOWN                = 'Down'
        SCREEN              = 'Screen Robot'
        SCREEN_LEFT         = 'Screen Left'
        SCREEN_RIGHT        = 'Screen Right'
        PPT                 = 'Participant'
        BUTTONS             = 'Buttons'

class Robot:
        LOOKAT_POSITIONS = {
                ROBOT_VISUAL_TARGETS.DOWN            : [0.0, -40.0, 3.0],
                ROBOT_VISUAL_TARGETS.SCREEN          : [0.0, -20.0, 3.0],
                ROBOT_VISUAL_TARGETS.SCREEN_LEFT     : [-20.0, -10.0, 3.0],
                ROBOT_VISUAL_TARGETS.SCREEN_RIGHT    : [20.0, -10.0, 3.0],
                ROBOT_VISUAL_TARGETS.PPT             : [0.0, -5.0, 3.0],
                ROBOT_VISUAL_TARGETS.BUTTONS         : [0.0, -40.0, 3.0]
        }

        TIMEOUT_LOOKAT = 2.0

        def __init__(self,simulation=True,face=False):

                if simulation == True:
                        self.robot_type = ROBOT_TYPE.ICUB_SIMULATOR
                else:
                        self.robot_type = ROBOT_TYPE.ICUB

                self.__icub__ = iCub(self.robot_type, logtype=YarpLogger.DEBUG)
                self.__lock__ = threading.Lock()

                self.__rightarm__ = self.__icub__.getPositionController(ICUB_PARTS.RIGHT_ARM)
                self.__leftarm__ = self.__icub__.getPositionController(ICUB_PARTS.LEFT_ARM)

                self.__icub__.gaze.reset()
                self.__icub__.gaze.setTrackingMode(True)
                # for the future:
                if face:
                        self.face = True
                        self.__icub__.emo.neutral()
                        self.__icub__.face.sendRaw("S48")
                else:
                        self.face = False

                self.robot_deciding = False

        def __lookat__(self, position):
                with self.__lock__:
                        p = yarp.Vector(3)
                        p.set(0, position[0]) # Azimuth
                        p.set(1, position[1]) # Elevation
                        p.set(2, position[2]) # Vergence
                        self.__icub__.gaze.getIGazeControl().lookAtAbsAnglesSync(p)
                        self.__icub__.gaze.getIGazeControl().waitMotionDone(timeout=self.TIMEOUT_LOOKAT)

        def __lookatrel__(self, position):
                with self.__lock__:
                        p = yarp.Vector(3)
                        p.set(0, position[0]) # Azimuth
                        p.set(1, position[1]) # Elevation
                        p.set(2, position[2]) # Vergence
                        self.__icub__.gaze.getIGazeControl().lookAtRelAnglesSync(p)
                        self.__icub__.gaze.getIGazeControl().waitMotionDone(timeout=self.TIMEOUT_LOOKAT)

        @AsyncRequest.decorator()
        def init_robot_pos(self):
                self.__lookat__(self.LOOKAT_POSITIONS[ROBOT_VISUAL_TARGETS.PPT])
                self.default_arms()

        @AsyncRequest.decorator()
        def default_arms(self):
                self.__rightarm__.move(target_joints=[-7.0, 21.20, 32.62, 53.91, 34.27, -23.17, 11.03, 59.77, 10.09, 42.77], req_time=3.0, joints_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
                self.__leftarm__.move(target_joints=[-7.0, 21.20, 32.62, 53.91, 34.27, -23.17, 11.03, 59.77, 10.09, 42.77], req_time=3.0, joints_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


        @AsyncRequest.decorator(timeout=TIMEOUT_LOOKAT)
        def look_at(self, target):
                self.__lookat__(self.LOOKAT_POSITIONS[target])

        @AsyncRequest.decorator()
        def press_left_button(self):
                self.__leftarm__.moveRefVel(target_joints=[-10.17], req_time=0.2, joints_list=[5], vel_list=[200], waitMotionDone=True)
                self.__leftarm__.moveRefVel(target_joints=[-23.17], req_time=0.2, joints_list=[5], vel_list=[100], waitMotionDone=True)

        @AsyncRequest.decorator()
        def press_right_button(self):
                self.__rightarm__.moveRefVel(target_joints=[-10.17], req_time=0.2, joints_list=[5], vel_list=[200], waitMotionDone=True)
                self.__rightarm__.moveRefVel(target_joints=[-23.17], req_time=0.2, joints_list=[5], vel_list=[100], waitMotionDone=True)
