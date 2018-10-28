import numpy as np
import redis
from matplotlib import pyplot as plt
from matplotlib import animation

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


nx = 800
ny = 600

fig = plt.figure()

vals = np.linspace(0, 1, 256)
np.random.shuffle(vals)
cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))

object_id_raws = 'object_id_raws'

for i in range(0, r.llen(object_id_raws)):
    r.lpop(object_id_raws)

prev_filename = None

def animate(foo):
    global prev_data

    filename = r.rpop(object_id_raws)
    if filename is not None:
        print('GOT: ' + filename)
        try:
            A = np.fromfile(filename, dtype='int32', sep='')[4:]
            A = A.reshape([600, 800])
            # shifting the bits to differentiate the segments
            # B = A & ((1 << 28) - 1)
            B = A
            im = plt.imshow(B, cmap=cmap)
            prev_data = B
        except:
            im = plt.imshow(prev_data, cmap=cmap)
    else:
        im = plt.imshow(prev_data, cmap=cmap)

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
