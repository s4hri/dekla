#
# Copyright (C) 2020  Davide De Tommaso
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>

from tobiiglassesctrl.controller import TobiiGlassesController
from eyetracking.asyn import AsyncRequest

class TobiiGlassesHelper:

    def __init__(self, address):
        self.__address__ = address
        self.__device__ = None

    @property
    def device(self):
        return self.__device__

    @AsyncRequest.decorator
    def connect(self):
        try:
            self.__device__ = TobiiGlassesController(self.__address__)
            return True
        except ConnectionError:
            return False

    @AsyncRequest.decorator
    def prepare(self, project_name, participant_name):
        try:
            project_id = self.__device__.create_project(project_name)
            participant_id = self.__device__.create_participant(project_id, participant_name)
            self.__calibration_id__ = self.__device__.create_calibration(project_id, participant_id)
            self.__recording_id__ = self.__device__.create_recording(participant_id)
            return True
        except:
            return False

    @AsyncRequest.decorator
    def start_calibration(self):
        res = False
        try:
            self.__device__.start_calibration(self.__calibration_id__)
            res = self.__device__.wait_until_calibration_is_done(self.__calibration_id__)
        except:
            res = False
        return res

    @AsyncRequest.decorator
    def start_recording(self):
        try:
            self.__device__.start_recording(self.__recording_id__)
            return True
        except:
            return False

    @AsyncRequest.decorator
    def stop_recording(self):
        res = False
        try:
            if self.__device__.is_recording():
                rec_id = self.__device__.get_current_recording_id()
                self.__device__.stop_recording(rec_id)
                res = True
        except:
            res = False
        return res

    @AsyncRequest.decorator
    def identify(self):
        raise NotImplementedError("This has to be implemented")

    @AsyncRequest.decorator
    def send_event(self, etype, evalue):
        try:
            self.__device__.send_custom_event(etype, evalue)
            return True
        except:
            return False
