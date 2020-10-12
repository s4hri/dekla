#!/usr/bin/env python3

from kuki import robot
from kuki.robot import ROBOT_VISUAL_TARGETS, Robot

import time
import argparse
import collections
import threading
import random

from statemachine import StateMachine, State

from pykron.core import PykronLogger, AsyncRequest

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class iCubStateMachine(StateMachine):

    home = State('Home', initial=True)
    main_screen = State('MainScreen')
    left_screen = State('LeftScreen')
    right_screen = State('RightScreen')

    start_trial = home.to(main_screen)
    follow_left = main_screen.to(right_screen)
    turnback_fromleft = right_screen.to(main_screen)
    turnback_fromright = left_screen.to(main_screen)
    follow_right = main_screen.to(left_screen)
    end_trial = main_screen.to(home) | right_screen.to(home) | left_screen.to(home)

    event_lock = threading.Lock()

    def on_start_trial(self, robot):
        with iCubStateMachine.event_lock:
            print("Main Screen")
            robot.look_at(ROBOT_VISUAL_TARGETS.SCREEN).wait_for_completed()

    def on_follow_left(self, robot):
        with iCubStateMachine.event_lock:
            print("PPT Left Screen")
            robot.look_at(ROBOT_VISUAL_TARGETS.SCREEN_RIGHT).wait_for_completed()

    def on_follow_right(self, robot):
        with iCubStateMachine.event_lock:
            print("PPT Right Screen")
            robot.look_at(ROBOT_VISUAL_TARGETS.SCREEN_LEFT).wait_for_completed()

    def on_turnback_fromleft(self, robot):
        with iCubStateMachine.event_lock:
            print("Main Screen")
            robot.look_at(ROBOT_VISUAL_TARGETS.SCREEN).wait_for_completed()

    def on_turnback_fromright(self, robot):
        with iCubStateMachine.event_lock:
            print("Main Screen")
            robot.look_at(ROBOT_VISUAL_TARGETS.SCREEN).wait_for_completed()

    def on_end_trial(self, robot):
        with iCubStateMachine.event_lock:
            print("End Trial")
            robot.look_at(ROBOT_VISUAL_TARGETS.PPT).wait_for_completed()

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class iCubTest:
    """ iCub Test
    tests XML-RPC with robot interface
    """

    def __init__(self, robot):
        self.robot = robot
        self.robot.init_robot_pos().wait_for_completed()

        self.logger = PykronLogger.getInstance()
        self.M = iCubStateMachine()

        self.yaw_threshold = 10
        self.gp_threshold = 5
        self.follow_threshold = 0.20 # follows for a between 0.0 and follow_threshold, max 1.0 for always

        self.log("init finished")

        # without allow_none the server will complain a lot about those functions not returning anything
        self.server = SimpleXMLRPCServer(('localhost', 8081), requestHandler=RequestHandler, allow_none=True)
        self.server.register_introspection_functions()

        # maybe forward the whole instance of the class?
        # TODO split it in half to allow that
        self.server.register_function(self.turnLeft,"turnLeft")
        self.server.register_function(self.turnRight,"turnRight")
        self.server.register_function(self.start_trial,"start_trial")
        self.server.register_function(self.end_trial,"end_trial")

    def turnLeft(self):
        self.log("leftStart")
        self.M.follow_left(self.robot)
        self.M.turnback_fromleft(self.robot)
        self.log("leftEnd")

    def turnRight(self):
        self.log("rightStart")
        self.M.follow_right(self.robot)
        self.M.turnback_fromright(self.robot)
        self.log("rightEnd")

    def start_trial(self):
        self.log('start trial')
        self.M.start_trial(self.robot)

    def end_trial(self):
        self.log('end trial')
        self.M.end_trial(self.robot)

    def log(self,message):
        # TODO add log type: error, debug
        self.logger.log.debug(message)

    def start(self):
        self.log("server starting")
        self.server.serve_forever()
        self.log("server ending")

if __name__ == '__main__':
    icub = Robot(simulation=True)
    app = iCubTest(icub)

    app.start()
