import numpy as np
import sys
import matplotlib.pyplot as plt

nrows = 3
ncols = 12
nact = 4

nepisodes = 100000
epsilon = 0.1
alpha = 0.1
gamma = 0.95

reward_normal = -1
reward_cliff = -100
reward_destination = 1

Q = np.zeros((nrows, ncols, nact), dtype=np.float)


def go_to_start():
    y = nrows
    x = 0
    return x, y


def random_action():
    a = np.random.randint(nact)
    return a


def move(x, y, a):
    state = 0

    if x == 0 and y == nrows and a == 0:
        x1 = x
        y1 = y - 1
        return x1, y1, state
    elif x == ncols - 1 and y == nrows - 1 and a == 2:
        x1 = x
        y1 = y + 1
        state = 1
        return x1, y1, state
    else:
        if a == 0:
            x1 = x
            y1 = y - 1
        elif a == 1:
            x1 = x + 1
            y1 = y
        elif a == 2:
            x1 = x
            y1 = y + 1
        elif a == 3:
            x1 = x - 1
            y1 = y

        if x1 < 0:
            x1 = 0
        if x1 > ncols - 1:
            x1 = ncols - 1
        if y1 < 0:
            y1 = 0
        if y1 > nrows - 1:
            state = 2

        return x1, y1, state


def exploit(x, y, Q):
    if x == 0 and y == nrows:
        a = 0
        return a
    if x == ncols - 1 and y == nrows - 1:
        a = 2
        return a
    if x == ncols - 1 and y == nrows:
        print("exploit at destination not possible")
        sys.exit()
    if x < 0 or x > ncols - 1 or y < 0 or y > nrows - 1:
        print("error ", x, y)
        sys.exit()

    a = np.argmax(Q[y, x, :])
    return a

def bellman(x, y, a, reward, Qs1a1, Q):
    if y == nrows and x == 0:
