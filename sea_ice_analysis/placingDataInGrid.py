import numpy as np


latArray = np.arange(-90,91)
lonArray = np.arange(0,360)

lat = -89.1
lon = 3.2
conc = 4
lat_array_temp = latArray
lat_array_temp = np.append(lat_array_temp, lat)
lat_array_temp.sort()

lon_array_temp = lonArray
lon_array_temp = np.append(lon_array_temp, lon)
lon_array_temp.sort()

latPos = np.where(lat_array_temp == lat)
lonPos = np.where(lon_array_temp == lon)


grid=np.zeros((4,4))

if conc > 15:
    icePresent = True
else:
    icePresent = False

# want to append the concentration to a list at the index of the grid below:
grid[latPos[0][0] - 1][lonPos[0][0] - 1].append(???)
print(grid)
