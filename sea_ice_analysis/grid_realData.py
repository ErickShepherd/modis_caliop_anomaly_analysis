# Standard library imports.
from pprint import pprint

# Third party imports.
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from pyhdf.SD import SD
from pyhdf.SD import SDC
import my_lib as ml
import pandas as pd
import netCDF4 as nc

def editTimestamp(x):

    head, sep, tail = str(x).partition(' ')
    head = head.replace("-","")
    return head

if __name__ == "__main__":
        

    # num rows and cols in NH data
    rowsNH = 896
    colsNH = 608

    jNH = np.arange(1,colsNH)
    iNH = np.arange(1,rowsNH)

    # NH coordinates
    NHlat = np.zeros((rowsNH, colsNH))
    NHlon = np.zeros((rowsNH, colsNH))

    # convert each i, j position in grid into lat, long
    for i in iNH:
        for j in jNH:

            # Call the fortran routine.
            # gtype (1 = 12.5km, 2 = 25km)
            # ihem (1 = NH, 2 = SH)
            # itrans(1 = i,j to lat, lon, 2 = lat,lon to i,j)
            lat, lon = ml.locate(gtype = 1, ihem = 1, itrans = 1, i = i, j = j)
            
            NHlat[i][j] = lat
            NHlon[i][j] = lon

    # num rows and cols in SH data
    rowsSH = 664
    colsSH = 632

    jSH = np.arange(1,colsSH)
    iSH = np.arange(1,rowsSH)

    # SH coordinates
    SHlat = np.zeros((rowsSH, colsSH))
    SHlon = np.zeros((rowsSH, colsSH))

    # convert each i, j position in grid into lat, long
    for i in iSH:
        for j in jSH:

            # Call the fortran routine.
            lat, lon = ml.locate(gtype = 1, ihem = 2, itrans = 1, i = i, j = j)
            
            SHlat[i][j] = lat
            SHlon[i][j] = lon
    print(np.amax(SHlon))
    print(np.amin(SHlon))
    
    filename   = "data/AMSR_E_L3_SeaIce12km_V15_20070106.hdf"
    data_file  = SD(filename, SDC.READ)
    
    # https://nsidc.org/data/AE_SI12/versions/3
    
    NHconc = np.array(data_file.select("SI_12km_NH_ICECON_ASC")[:]).astype(np.float32)
    NHconc[(NHconc == 110) | (NHconc == 105) | (NHconc ==120)] = np.nan

    latArray = np.arange(-90,91)
    lonArray = np.arange(0,360)


    grid=np.zeros((180,360,2))

    for i in range(len(NHlat)):
        for j in range(len(NHlat[i])):
            latTemp = latArray
            latTemp = np.append(latTemp, NHlat[i][j])
            latTemp.sort()
            
            lonTemp = lonArray
            lonTemp = np.append(lonTemp, NHlon[i][j])
            lonTemp.sort()
            
            latPos = np.where(latTemp == NHlat[i][j])
            lonPos = np.where(lonTemp == NHlon[i][j])
        
        
        if NHconc[i][j] >= 15:
            icePresent = True
        else:
            icePresent = False
            
        grid[latPos[0][0] - 1][lonPos[0][0] - 1][0] = icePresent
        grid[latPos[0][0] - 1][lonPos[0][0] - 1][1] = count
    
    concProb = np.zeros((180,360))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            concProb[i][j] = grid[i][j][0]/grid[i][j][1]
            
            
    lat = np.arange(-90, 91)
    lon = np.arange(0,361)
    longv, latv = np.meshgrid(lon, lat)
            
    cmap = plt.get_cmap('PiYG')
    fig, ax = plt.subplots()
    
    im = ax.pcolormesh(longv, latv,  concProb, cmap=cmap)
    
    fig.colorbar(im, ax = ax)
    plt.savefig("test.png")

