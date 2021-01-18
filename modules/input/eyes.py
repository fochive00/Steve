import numpy as np
import cv2 as cv

class Eyes(object):
    def __init__(self):
        self.__url__ = 'udp://localhost:9999'
        # TODO exception handle
        self.__cap__ = cv.VideoCapture(self.__url__)
        print('start listen to ' + self.__url__)

    def getGray(self):
        """ get a frame, and convert it to gray scale.
            and then return it
        """
        ret = False
        while ret is not True:
            ret, frame = self.__cap__.read()

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return gray

    def __del__(self):
        self.__cap__.release()
        print('no longer listen ' + self.__url__ + ' anymore')