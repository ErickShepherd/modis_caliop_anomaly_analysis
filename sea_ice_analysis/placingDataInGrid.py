import numpy as np
import matplotlib.pyplot as plt

latArray = np.arange(-90,91)
lonArray = np.arange(0,360)

lat = [[-89.1, -87, -87, -89.3], [-89.1, -87, -87, -89.3]]
lon = [[3.2, 1.7, 3.1, 3.5],[3.2, 1.7, 3.1, 3.5]]
conc = [[4, 97, 45, 100],[4, 97, 45, 100]]

grid=np.zeros((4,4,2))

for i in range(len(lat)):
    for j in range(len(lat[i])):
        lat_array_temp = latArray
        lat_array_temp = np.append(lat_array_temp, lat[i][j])
        lat_array_temp.sort()
    
        lon_array_temp = lonArray
        lon_array_temp = np.append(lon_array_temp, lon[i][j])
        lon_array_temp.sort()
        
        latPos = np.where(lat_array_temp == lat[i][j])
        lonPos = np.where(lon_array_temp == lon[i][j])

        if conc[i][j] >= 15:
            icePresent = True
        else:
            icePresent = False

        grid[latPos[0][0] - 1][lonPos[0][0] - 1][0] += icePresent
        grid[latPos[0][0] - 1][lonPos[0][0] - 1][1] += 1


concProb = np.zeros((4,4))

for i in range(len(grid)):
    for j in range(len(grid[i])):
        concProb[j][i] = grid[i][j][0]/grid[i][j][1]
lat = np.arange(0, 5)
long = np.arange(0,5)
latv, longv = np.meshgrid(lat, long)

cmap = plt.get_cmap('PiYG')
fig, ax = plt.subplots()

im = ax.pcolormesh(longv, latv, concProb, cmap=cmap)

fig.colorbar(im, ax = ax)
plt.show()
 
print(grid)
print(concProb)
