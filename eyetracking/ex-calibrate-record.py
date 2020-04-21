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

from TobiiGlassesHelper import TobiiGlassesHelper
from asyn import RequestManager

def connected(args):
    print("connected: ", args)

def main():
    tobiiglasses = TobiiGlassesHelper("192.168.71.50")
    tobiiglasses.connect().wait_for_completed(callback=connected)
    tobiiglasses.stop_recording().wait_for_completed()
    project_name = input("Please insert the project's name: ")
    participant_name = input("Please insert the participant's name: ")
    res = tobiiglasses.prepare(project_name, participant_name).wait_for_completed()
    if res is False:
        print("Preparation failed!")
        exit(1)
    input("Put the calibration marker in front of the user, then press enter to calibrate")
    res = tobiiglasses.start_calibration().wait_for_completed()
    if res is False:
        print("Calibration failed!")
        exit(1)
    input("Press enter to start recording")
    tobiiglasses.start_recording().wait_for_completed()
    tobiiglasses.send_event("start_recording", "Start of the recording")
    input("Press enter to stop recording")
    tobiiglasses.send_event("stop_recording", "Stop of the recording ")
    res = tobiiglasses.stop_recording().wait_for_completed()

    if res is False:
        print("Recording failed!")
        exit(1)


if __name__ == '__main__':
    main()
    RequestManager().quit()
