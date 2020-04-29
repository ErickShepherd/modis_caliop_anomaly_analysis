import numpy as np


nlat, nlong = (361, 180)
lat = np.linspace(0, 360, nlat)
long = np.linspace(-90, 90, nlong)
latv, longv = np.meshgrid(lat, long)
#print(latv)
#print(longv)

coordinate_grid = np.array([lat, long])
print(coordinate_grid)