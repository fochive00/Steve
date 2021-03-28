import numpy as np
import cv2 as cv
import time
import platform
from modules.brains.move_on import Brain
from modules.capture.capture import Capture

if platform.system() == 'Windows':
    from modules.control.windll_control import Control
elif platform.system() == 'Linux':
    from modules.control.uinput_control import Control


def main():
    capture = Capture()
    control = Control()
    
    # control_map_range = control.getControlMapRange()

    print('start')
    for i in range(500000):
        # get a frame
        gray = capture.getGray()
        print('aaa')
        # if i == 10:
        #     ch = input('After confirm this, you have to switch to Minecraft window in 5 seconds. Are you ready? (y/n): ')
        #     if ch.upper() == 'N':
        #         print('exiting...')
        #         exit(0)
        #     elif ch.upper() == 'Y':
        #         time.sleep(5)
        
        time.sleep(0.3)

        # control_cmd = np.random.randint(control_map_range, size=1)[0]

        # control.put(control_cmd)
        cv.imshow("capture", gray)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
    cv.destroyAllWindows()
    control.stop()
    print('stop')
if __name__ == '__main__':
    main()