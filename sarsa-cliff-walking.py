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
        return Q

    if y == nrows and x == ncols - 1:
        return Q

    Q[y, x, a] = Q[y, x, a] + alpha * (reward + gamma * Qs1a1 - Q[y, x, a])


def explore_exploit(x, y, Q):
    if x == 0 and y == nrows:
        a = 0
        return a

    r = np.random.uniform()

    if r < epsilon:
        a = random_action()
    else:
        a = exploit(x, y, Q)
    return a


for n in range(nepisodes + 1):
    if n % 1000 == 0:
        print("episodes #: ", n)

    x, y = go_to_start()

    a = explore_exploit(x, y, Q)

    while True:
        x1, y1, state = move(x, y, Q)

        if state == 1:
            reward = reward_destination
            Qs1a1 = 0.0
            Q = bellman(x, y, a, reward, Qs1a1, Q)
            break
        elif state == 2:
            reward = reward_cliff
            Qs1a1 = 0.0
            Q = bellman(x, y, a, reward, Qs1a1, Q)
            break
        elif state == 0:
            reward = reward_normal

            a1 = explore_exploit(x, y, Q)
            if x1 == 0 and y1 == nrows:
                Qs1a1 = 0.0
            else:
                Qs1a1 = Q[y1, x1, a1]

            Q = bellman(x, y, a, reward, Qs1a1, Q)
            x = x1
            y = y1
            a = a1

for i in range(nact):
    plt.subplot(nact, 1, i + 1)
    plt.imshow(Q[:, :, i])
    plt.axis('off')
    plt.colorbar()
    if i == 0:
        plt.title('Q-north')
    elif i == 1:
        plt.title('Q-east')
    elif i == 2:
        plt.title('Q-south')
    elif i == 3:
        plt.title('Q-west')
    plt.savefig('Q_sarsa.png')
    plt.clf()
    plt.close()

path = np.zeros((nrows, ncols, nact), dtype=np.float)
x, y = go_to_start()
while True:
    a = exploit(x, y, Q)
    print(x, y, a)
    x1, y1, state = move(x, y, a)
    if state == 1 or state == 1:
        print("breaking ", state)
        break
    elif state == 0:
        x = x1
        y = y1
        if x >= 0 and x <= ncols - 1 and y > -0 and y < nrows - 1:
            path[x, y] = 100.0
    plt.imshow(path)
    plt.savefig('path_sarsa.png')
