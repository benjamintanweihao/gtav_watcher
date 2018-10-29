import numpy as np
import redis
from matplotlib import pyplot as plt
from matplotlib import animation

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

nx = 800
ny = 600

fig = plt.figure()
plt.axis('off')

cmap = 'Greys_r'

depth_raws = 'depth_raws'

for i in range(0, r.llen(depth_raws)):
    r.lpop(depth_raws)

prev_filename = None


def animate(foo):
    global prev_data

    filename = r.rpop(depth_raws)
    if filename is not None:
        try:
            A = np.fromfile(filename, dtype='int32', sep='')[4:]
            A = A.reshape([600, 800])
            plt.clf()
            plt.axis('off')
            im = plt.imshow(A, cmap=cmap)
            prev_data = A
        except:
            plt.clf()
            plt.axis('off')
            im = plt.imshow(prev_data, cmap=cmap)
    else:
        plt.axis('off')
        im = plt.imshow(prev_data, cmap=cmap)

    plt.pause(0.0001)

    return im,


def init():
    global im
    global prev_data
    prev_data = np.zeros([600, 800])
    im = plt.imshow(prev_data, cmap=cmap)
    return im,


ani = animation.FuncAnimation(fig, animate,
                              init_func=init,
                              frames=nx * ny,
                              interval=10,
                              blit=False)

plt.show()
