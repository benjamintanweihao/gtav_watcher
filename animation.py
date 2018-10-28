import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

nx = 800
ny = 600

fig = plt.figure()

vals = np.linspace(0, 1, 256)
np.random.shuffle(vals)
cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))

index = 0

images = [
    'D:\\Program Files\\Rockstar Games\\Grand Theft Auto V\\cap\\00015579_object_id.raw',
    'D:\\Program Files\\Rockstar Games\\Grand Theft Auto V\\cap\\00015681_object_id.raw',
]


def animate(foo):
    global index
    print('animate')

    filename = images[index]
    index += 1

    # TODO: Remove this when done
    if index == 2:
        index = 0

    print('GOT: ' + filename)
    A = np.fromfile(filename, dtype='int32', sep='')[4:]
    A = A.reshape([600, 800])
    # shifting the bits to differentiate the segments
    B = A & ((1 << 28) - 1)
    im = plt.imshow(B, cmap=cmap)
    return im,


def init():
    global im
    im = plt.imshow(np.zeros([600, 800]), cmap=cmap)
    return im,


ani = animation.FuncAnimation(fig, animate,
                              init_func=init,
                              frames=nx * ny,
                              interval=1000,
                              blit=True)

plt.show()
