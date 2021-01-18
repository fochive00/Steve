import numpy as np
import cv2 as cv
from modules.input.eyes import Eyes
from modules.control.wayland_control import Body
import time

def main():
    eyes = Eyes()
    body = Body()
    
    control_map_range = body.getControlMapRange()
    time.sleep(5)

    print('start grab images')
    for i in range(50):
    # get a frame
        gray = eyes.getGray()

        time.sleep(1)
        control_cmd = np.random.randint(control_map_range, size=1)[0]

        body.put(control_cmd)

        # cv.imshow("capture", gray)
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #      break

    # cv.destroyAllWindows()
    body.stop()
    print('stop')
if __name__ == '__main__':
    main()