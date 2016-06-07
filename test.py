import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig2 = plt.figure()

x = np.arange(-9, 10)
y = np.arange(-9, 10).reshape(-1, 1)
base = np.hypot(x, y)

ims = []
for add in np.arange(15):
    ims.append((plt.pcolor(base + add, norm=plt.Normalize(0, 30)),))

im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,)
#im_ani.save('im.mp4', metadata={'artist':'Guido'})

plt.show()