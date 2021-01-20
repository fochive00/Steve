# sending key events in this way didn't work
# not use
import numpy as np
import win32con
import win32api
# import win32gui
import threading
import time
import queue
from modules.control.create_map import createMap

def mouse_move(rel_x, rel_y):
    # not working
    # cur_x, cur_y = win32gui.GetCursorPos()
    # win32api.SetCursorPos((cur_x + rel_x,cur_y + rel_y))

    # work nicely
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, rel_x, rel_y, 0, 0)

# not work
def key_event(events):
    # win32 virtual key code
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    key_map = [
        0x01, # left_mouse_button
        0x02, # right_mouse_button

        0x31, # 1
        0x32, # 2
        0x33, # 3
        0x34, # 4
        0x35, # 5
        0x36, # 6

        0x20, # space
        0x10, # shift
        0x11, # ctrl

        0x57, # w
        0x41, # a
        0x53, # s
        0x44, # d    
    ]

    map(lambda key_code, event: win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code), event, 0), key_map, events)

def array2events(arr: np.ndarray) -> (list, list):
    direction = (arr[0], arr[1])

    button_events = list(map(lambda val: 0 if val == 1 else win32con.KEYEVENTF_KEYUP, arr[2:]))
    return (direction, button_events)

class Body(object):
    def __init__(self):
        self.queue = queue.Queue()
        
        self.control_map = createMap()
        self.direction = (0, 0)

        self.direction_thread_lock = threading.Lock()
        self.direction_thread = threading.Thread(target=self.direct)
        self.direction_thread.start()

        self.thread = threading.Thread(target=self.serve)
        self.thread.start()

    def put(self, cmd_arr:np.ndarray) -> None:
        self.queue.put(cmd_arr)

    def serve(self) -> None:
        while True:
            control_code = self.queue.get()
            event_arr = self.control_map[control_code]

            direction, button_events = array2events(event_arr)
            key_event(button_events)
            # change the moving direction of the mouse
            self.direction_thread_lock.acquire()
            self.direction = (direction[0], direction[1])
            self.direction_thread_lock.release()

    def direct(self) -> None:
        while True:
            self.direction_thread_lock.acquire()
            mouse_move(self.direction[0], self.direction[1])
            self.direction_thread_lock.release()
            time.sleep(0.005)
    def getControlMapRange(self) -> int:
        return self.control_map.shape[0]

    def stop(self) -> None:
        self.put(0)