import numpy as np


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

        if grid[latPos[0][0] - 1][lonPos[0][0] - 1][1] == 0:

            count = 1
            grid[latPos[0][0] - 1][lonPos[0][0] - 1][0] = icePresent
            grid[latPos[0][0] - 1][lonPos[0][0] - 1][1] = count
        
        else:

            grid[latPos[0][0] - 1][lonPos[0][0] - 1][0] += icePresent
            grid[latPos[0][0] - 1][lonPos[0][0] - 1][1] += 1


concProb = np.zeros((4,4))

for i in range(len(grid)):
    for j in range(len(grid[i])):
        concProb[i][j] = grid[i][j][0]/grid[i][j][1]
            
print(grid)
print(concProb)
