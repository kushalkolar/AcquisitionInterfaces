#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 11:13:48 2018

@author: kushal
"""

import abc
import cv2
from threading import Thread
from queue import Queue
from time import time


class AbstractVideoGrabber(Thread):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, framerate: int, shape: tuple, exposure: float, duration: int = -1, preview=False, **kwargs):
        Thread.__init__(self)
        self._framerate = None
        self._shape = None
        self._exposure = None
        self._preview = preview
        self._duration = duration

    @abc.abstractmethod
    def run(self):
        pass
    
    @abc.abstractmethod
    def stop(self):
        pass

    @property
    @abc.abstractmethod
    def framerate(self):
        pass

    @framerate.setter
    @abc.abstractmethod
    def framerate(self, frate: int):
        pass

    @property
    @abc.abstractmethod
    def exposure(self):
        pass

    @exposure.setter
    @abc.abstractmethod
    def exposure(self, exp: float):
        pass

    @property
    @abc.abstractmethod
    def shape(self):
        pass

    @shape.setter
    @abc.abstractmethod
    def shape(self, width_height: tuple):
        pass


class OpenCVCameraGrabber(AbstractVideoGrabber):
    def __init__(self, framerate: int, shape: tuple, exposure: float, duration: int = -1, camera: int = 0, preview=False):
        super().__init__(framerate, shape, exposure, duration, preview)
        self.camera = camera
        self._cap = cv2.VideoCapture(self.camera)
        self.framerate = framerate
        self.shape = shape
        self.exposure = exposure
        self._brightness = None
        self._gain = None

        self.queue = Queue()

        self._alive = True

    def run(self):
        if self._duration == -1:
            while self._alive:
                self._grab_frame()
        else:
            end_time = time() + self._duration
            while time() < end_time:
                self._grab_frame()

        self.stop()

    def _grab_frame(self):
        rval, frame = self._cap.read()
        if rval:
            self.queue.put(frame)
        if self._preview:
            cv2.imshow('Frame Grabber Preview', frame)

    def stop(self):
        self._alive = False
        if self._preview:
            cv2.destroyWindow('Frame Grabber Preview')
        self._cap.release()
        self.queue.put('done')

    @property
    def framerate(self):
        return self._framerate

    @framerate.setter
    def framerate(self, frate: int):
        self._framerate = frate
        self._cap.set(cv2.CAP_PROP_FPS, frate)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value: float):
        self._brightness = value
        self._cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, dims: tuple):
        self._shape = dims
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, dims[0])
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, dims[1])

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value):
        self._gain = value
        self._cap.set(cv2.CAP_PROP_GAIN, value)

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, exp: float):
        self._exposure = exp
        self._cap.set(cv2.CAP_PROP_EXPOSURE, exp)

