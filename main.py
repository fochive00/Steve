import numpy as np
import cv2 as cv
import time
import platform
from modules.input.capture import Capture

if platform.system() == 'Windows':
    from modules.control.windll_control import Control
elif platform.system() == 'Linux':
    from modules.control.uinput_control import Control


def main():
    capture = Capture()
    control = Control()
    
    control_map_range = control.getControlMapRange()
    time.sleep(5)

    print('start grabing images')
    for i in range(50):
    # get a frame
        # gray = capture.getGray()

        time.sleep(1)
        control_cmd = np.random.randint(control_map_range, size=1)[0]

        control.put(control_cmd)

        # cv.imshow("capture", gray)
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     break

    # cv.destroyAllWindows()
    control.stop()
    print('stop')
if __name__ == '__main__':
    main()