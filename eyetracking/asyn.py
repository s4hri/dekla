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


from threading import Thread
import asyncio
import threading

class RequestManager:

    class __RequestManager:
        def __init__(self):
            self.__closing_event__ = threading.Event()
            self.__request__ = threading.Event()
            self.__requests__ = []
            Thread(target=asyncio.run, args=(self.__main__(),)).start()

        async def __main__(self):
            while not (self.__closing_event__.is_set() and len(self.__requests__) == 0):
                self.__request__.wait()
                req = self.__requests__.pop()
                task = asyncio.create_task(req.run())
                self.__request__.clear()
                await asyncio.sleep(0.01)

    instance = None
    def __init__(self):
        if not RequestManager.instance:
            RequestManager.instance = RequestManager.__RequestManager()

    def request(self, req):
        RequestManager.instance.__requests__.append(req)
        RequestManager.instance.__request__.set()

        return req

    def quit(self):
        RequestManager.instance.__closing_event__.set()

    def __getattr__(self, name):
        return getattr(self.instance, name)

class AsyncRequest:

    @staticmethod
    def decorator(foo):

        def f(self, *args, **kwargs):
            args = (self,) + args
            req = AsyncRequest(foo, args=args)
            RequestManager().request(req)
            return req

        return f


    def __init__(self, f, args):
        self.__target__ = f
        self.__completed__ = threading.Event()
        self.__retval__ = None
        self.__callback__ = None
        self.__args__ = args

    @property
    def manager(self):
        return manager

    def wait_for_completed(self, callback=None):
        if not callback is None:
            self.on_completed(callback)
        self.__completed__.wait()
        return self.__retval__

    def on_completed(self, callback):
        self.__callback__ = callback

    async def run(self):
        try:
            t = self.__target__(*self.__args__)
            self.__retval__ = t
        except:
            self.__retval__ = None
        self.__completed__.set()
        if self.__callback__ is None:
            return self.__retval__
        else:
            self.__callback__(self.__retval__)
