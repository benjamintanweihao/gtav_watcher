import numpy as np
import redis
from matplotlib import pyplot as plt
from matplotlib import animation

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

nx = 800
ny = 600

fig = plt.figure()
plt.axis('off')

vals = np.linspace(0, 1, 256)
np.random.seed(42424242)
np.random.shuffle(vals)
cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))

object_id_raws_2 = 'object_id_raws_2'

for i in range(0, r.llen(object_id_raws_2)):
    r.lpop(object_id_raws_2)

prev_filename = None


def animate(foo):
    global prev_data

    filename = r.rpop(object_id_raws_2)
    if filename is not None:
        try:
            print(filename)
            A = np.fromfile(filename, dtype='int32', sep='')[4:]
            A = A.reshape([600, 800])
            # shifting the bits to differentiate the segments
            B = ((A >> 28) & 0xf)
            print(set([x for x in B.reshape(-1)]))
            plt.clf()
            plt.axis('off')
            im = plt.imshow(B, cmap=cmap)
            prev_data = B
        except:
            plt.clf()
            plt.axis('off')
            im = plt.imshow(prev_data, cmap=cmap)
    else:
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
