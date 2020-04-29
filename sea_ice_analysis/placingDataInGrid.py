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


grid=np.zeros((180,360))

if conc > 15:
    icePresent = True
else:
    icePresent = False

if grid[latPos[0][0] - 1][lonPos[0][0] - 1] == 0:
    count = 1
else:
    icePresent += grid[latPos[0][0] - 1][lonPos[0][0] - 1][0]
    count += grid[latPos[0][0] - 1][lonPos[0][0] - 1][1]

grid[latPos[0][0] - 1][lonPos[0][0] - 1] == (icePresent, count) 

print(grid)
