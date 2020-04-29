# Standard library imports.
from pprint import pprint

# Third party imports.
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from pyhdf.SD import SD
from pyhdf.SD import SDC
import my_lib as ml

    
if __name__ == "__main__":
    
    filename   = "data/AMSR_E_L3_SeaIce12km_V15_20070108.hdf"
    data_file  = SD(filename, SDC.READ)
    attributes = data_file.attributes()
    datasets   = data_file.datasets()
    
    #pprint(attributes)
    #pprint(datasets)
    

    # https://nsidc.org/data/AE_SI12/versions/3
        
    NHconc = np.array(data_file.select("SI_12km_NH_ICECON_ASC")[:]).astype(np.float32)
    
    NHconc[(NHconc == 110) | (NHconc == 105) | (NHconc ==120) | (NHconc == 0)] = np.nan

    SHconc = np.array(data_file.select("SI_12km_SH_ICECON_ASC")[:]).astype(np.float32)
    
    SHconc[(SHconc == 110) | (SHconc == 105) | (SHconc == 120) | (SHconc == 0)] = np.nan
    
    plt.figure()
    plt.title("Concentration")
    img  = plt.contourf(NHconc)
    cbar = plt.colorbar()    
    plt.savefig("NH_CONC")
    plt.close()

    plt.figure()
    plt.title("Concentration")
    img  = plt.contourf(SHconc)
    cbar = plt.colorbar()
    
    plt.savefig("SH_CONC")
    plt.close()

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
    
    fig = plt.figure()
    ax  = plt.axes(projection = ccrs.PlateCarree())
    ax.coastlines()
    im = ax.contourf(NHlon, NHlat, NHconc, 50)
    cbar = plt.colorbar(im)
    plt.savefig("NHtest.png")
    plt.close()
    
    fig = plt.figure()
    ax  = plt.axes(projection = ccrs.PlateCarree())
    ax.coastlines()
    im = ax.contourf(SHlon, SHlat, SHconc, 50)
    cbar = plt.colorbar(im)
    plt.savefig("SHtest.png")
    plt.close()
    
    #vmin = 0
    #vmax = max([SHconc.max(), NHconc.max()])
    
    fig = plt.figure()
    ax  = plt.axes(projection = ccrs.PlateCarree())
    ax.set_extent([-180, 180, -90, 90])
    ax.coastlines()
    ax.scatter(NHlon, NHlat, c = NHconc, alpha = 0.2, linewidth = 0, s = 1)
    ax.scatter(SHlon, SHlat, c = SHconc, alpha = 0.2, linewidth = 0, s = 1)
    plt.savefig("map.png")
    plt.close()
    
    
