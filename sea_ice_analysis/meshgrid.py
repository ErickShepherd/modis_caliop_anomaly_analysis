import numpy as np


nx, ny = (361, 180)
x = np.linspace(0, 360, nx)
y = np.linspace(-90, 90, ny)
xv, yv = np.meshgrid(x, y)
print(xv)
print(yv)


