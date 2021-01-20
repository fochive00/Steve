import numpy as np

def join(v1, v2):
    res = np.array([np.hstack((i, j)) for i in v1 for j in v2])

    return res

def createControlMap() -> np.ndarray:
    v = np.array([0, 2, 3, -2, -3])
    direction = join(v, v)

    mousebutton = np.array(
        [[0, 0],
         [1, 0],
         [0, 1]]
    )

    tools = np.array(
        [[0, 0, 0, 0,0, 0],
         [1, 0, 0, 0,0, 0],
         [0, 1, 0, 0,0, 0],
         [0, 0, 1, 0,0, 0],
         [0, 0, 0, 1,0, 0],
         [0, 0, 0, 0,1, 0],
         [0, 0, 0, 0,0, 1]]
    )

    ctl_shift_space = np.array(
        [[0, 0, 0],
         [1, 0, 0],
         [1, 0, 1],
         [0, 1, 0]]
   )

    wasd = np.array(
        [[0, 0, 0, 0], # none
         [1, 0, 0, 0], # w
         [0, 1, 0, 0], # a
         [0, 0, 1, 0], # d
         [0, 0, 0, 1], # s
         [1, 1, 0, 0], # w-a
         [1, 0, 1, 0], # w-d
         [0, 1, 0, 1], # s-a
         [0, 0, 1, 1]] # s-d
    )

    res = join(direction, mousebutton)
    res = join(res, tools)
    res = join(res, ctl_shift_space)
    res = join(res, wasd)

    return res