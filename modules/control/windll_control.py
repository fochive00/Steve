import numpy as np
import ctypes
import threading
import time
import queue
from modules.control.control_map import createControlMap

# types
LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

class Control(object):
    direct_key  = 0x0008
    key_press   = 0x0000
    key_release = 0x0002

    mouse_move       = 0x0001
    mouse_lb_press   = 0x0002
    mouse_lb_release = 0x0004
    mouse_rb_press   = 0x0008
    mouse_rb_release = 0x0010

    direct_key_map = [
        0x02, # 1
        0x03, # 2
        0x04, # 3
        0x05, # 4
        0x06, # 5
        0x07, # 6

        0x39, # SPACE
        0x2A, # LSHIFT
        0x1D, # LCTRL

        0x11, # W
        0x1E, # A
        0x1F, # S
        0x20, # D
    ]

    def __init__(self):
        self.queue = queue.Queue()
        
        self.control_map = createControlMap()
        # mouse move flag 0x0001
        self.mouse_move_inputs = (self.createMouseInput(0, 0, 0x0001),)

        self.mouse_move_thread_lock = threading.Lock()
        self.mouse_move_thread = threading.Thread(target=self.mouse_worker)
        self.mouse_move_thread.start()

        self.thread = threading.Thread(target=self.keybd_worker)
        self.thread.start()

    def put(self, cmd_arr:np.ndarray) -> None:
        self.queue.put(cmd_arr)

    def keybd_worker(self) -> None:
        while True:
            control_code = self.queue.get()
            event_arr = self.control_map[control_code]

            mouse_move_inputs, button_inputs = self.array2inputs(event_arr)
            self.SendInputs(button_inputs)

            # change the moving direction of the mouse
            self.mouse_move_thread_lock.acquire()
            self.mouse_move_inputs = mouse_move_inputs
            self.mouse_move_thread_lock.release()

    def mouse_worker(self) -> None:
        while True:
            self.mouse_move_thread_lock.acquire()
            self.SendInputs(self.mouse_move_inputs)
            self.mouse_move_thread_lock.release()
            time.sleep(0.005)
    def getControlMapRange(self) -> int:
        return self.control_map.shape[0]

    def stop(self) -> None:
        self.put(0)

    # input generator
    def createMouseInput(self, x, y, flag):
        return INPUT(0, _INPUTunion(mi=MOUSEINPUT(x, y, 0, flag, 0, None)))

    def createKeybdInput(self, key_code, flag):
        return INPUT(1, _INPUTunion(ki=KEYBDINPUT(key_code, key_code, flag, 0, None)))

    # send inputs
    def SendInputs(self, inputs):
        nInputs = len(inputs)
        LPINPUT = INPUT * nInputs
        pInputs = LPINPUT(*inputs)
        cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
        return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

    def array2inputs(self, arr: np.ndarray) -> (list, list):

        mouse_move_inputs = self.createMouseInput(arr[0], arr[1], self.mouse_move)
        mouse_lb_input = self.createMouseInput(0, 0, self.mouse_lb_press if arr[2] == 1 else self.mouse_lb_release)
        mouse_rb_input = self.createMouseInput(0, 0, self.mouse_rb_press if arr[3] == 1 else self.mouse_rb_release)

        flags = list(map(lambda val: self.key_press|self.direct_key if val == 1 else self.key_release|self.direct_key, arr[4:]))
        keybd_inputs = list(map(lambda key, flag: self.createKeybdInput(key, flag), self.direct_key_map, flags))

        button_inputs = [mouse_lb_input, mouse_rb_input]
        button_inputs.extend(keybd_inputs)
        return ((mouse_move_inputs,), tuple(button_inputs))