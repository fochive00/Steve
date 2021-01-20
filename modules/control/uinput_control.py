import numpy as np
import libevdev
from libevdev import InputEvent
import threading
import time
import queue
from modules.control.control_map import createControlMap

class Control(object):
    key_map = [
        libevdev.EV_KEY.BTN_LEFT,
        libevdev.EV_KEY.BTN_RIGHT,

        libevdev.EV_KEY.KEY_1,
        libevdev.EV_KEY.KEY_2,
        libevdev.EV_KEY.KEY_3,
        libevdev.EV_KEY.KEY_4,
        libevdev.EV_KEY.KEY_5,
        libevdev.EV_KEY.KEY_6,
        
        libevdev.EV_KEY.KEY_SPACE,
        libevdev.EV_KEY.KEY_LEFTSHIFT,
        libevdev.EV_KEY.KEY_LEFTCTRL,

        libevdev.EV_KEY.KEY_W,
        libevdev.EV_KEY.KEY_A,
        libevdev.EV_KEY.KEY_S,
        libevdev.EV_KEY.KEY_D,
    ]

    def __init__(self):
        self.queue = queue.Queue()
        
        self.evdev = libevdev.Device()
        self.evdev.name = "control"

        self.evdev.enable(libevdev.EV_REL.REL_X)
        self.evdev.enable(libevdev.EV_REL.REL_Y)
        for key in self.key_map:
            self.evdev.enable(key)

        self.mouse_move_events = [
            InputEvent(libevdev.EV_REL.REL_X, 0),
            InputEvent(libevdev.EV_REL.REL_Y, 0),
            InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
        ]

        self.control_map = createControlMap()

        self.uinput = self.evdev.create_uinput_device()
        print("New device at {} ({})".format(self.uinput.devnode, self.uinput.syspath))
    
        # Sleep for a bit so udev, libinput, Xorg, Wayland, ... all have had
        # a chance to see the device and initialize it. Otherwise the event
        # will be sent by the kernel but nothing is ready to listen to the
        # device yet.
        time.sleep(1)

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

            mouse_move_events, button_events = self.array2events(event_arr)
            self.uinput.send_events(button_events)

            # change the moving direction of the mouse
            self.mouse_move_thread_lock.acquire()
            self.mouse_move_events = mouse_move_events
            self.mouse_move_thread_lock.release()

    def mouse_worker(self) -> None:
        while True:
            self.mouse_move_thread_lock.acquire()
            self.uinput.send_events(self.mouse_move_events)
            self.mouse_move_thread_lock.release()
            time.sleep(0.005)
    def getControlMapRange(self) -> int:
        return self.control_map.shape[0]

    def stop(self) -> None:
        self.put(0)

    def array2events(self, arr: np.ndarray) -> (list, list):
        mouse_move_events = [
            InputEvent(libevdev.EV_REL.REL_X, arr[0]),
            InputEvent(libevdev.EV_REL.REL_Y, arr[1]),
            InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
        ]

        button_events = list(map(lambda key, val: InputEvent(key, val), self.key_map, arr[2:]))
        return (mouse_move_events, button_events)