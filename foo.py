# "C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V\cap\2018_10_29_12_44_57\00058515_object_id.raw"
# "C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V\cap\2018_10_29_12_44_57\00058595_object_id.raw"
# "C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V\cap\2018_10_29_12_44_57\00058676_object_id.raw"
import numpy as np
import matplotlib.pyplot as plt

filename = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Grand Theft Auto V\\cap\\2018_10_29_13_02_51\\00104004_disparity.raw"

A = np.fromfile(filename, dtype='int32', sep='')[4:]

print(set([x for x in A.reshape(-1)]))

A = A.reshape([600, 800])
im = plt.imshow(A, cmap='Greys_r')
plt.show()