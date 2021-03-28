import numpy as np
import cv2 as cv
import threading
import queue

class Capture(object):
    def __init__(self):
        self.__url__ = 'udp://localhost:2000'
        # TODO exception handle
        print('Make sure your video source is streaming to ' + self.__url__)
        self.__cap__ = cv.VideoCapture(self.__url__)

        # self.__cap__.set(cv.CAP_PROP_BUFFERSIZE, 3)
        print('start listen to ' + self.__url__)

        # capture thread
        self.last_frame = None
        self.queue = queue.Queue()
        self.last_frame_lock = threading.Lock()
        self.thread = threading.Thread(target=self.captureWorker)
        self.thread.start()

    def captureWorker(self):
        while True:
            ret = False
            while ret == False:
                ret, frame =self.__cap__.read()

            # store in 'last_frame'
            self.last_frame_lock.acquire()
            self.last_frame = frame
            self.last_frame_lock.release()

    def getGray(self):
        """ get a frame, and convert it to gray scale.
            and then return it
        """
        # get the frame from buffer
        self.last_frame_lock.acquire()
        frame = self.last_frame
        self.last_frame_lock.release()

        # convert the frame to gray scale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        return gray

    def __del__(self):
        self.__cap__.release()
        print('no longer listen ' + self.__url__ + ' anymore')