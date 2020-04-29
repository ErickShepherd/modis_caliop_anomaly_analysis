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

#Find element in nd array closest to the scalar value
def find_nearest(array, value):

    idx = np.abs(array - value).argmin()
    return array.flat[idx]


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
    
    # read in anomalies csv as pandas dataframe
    df = pd.read_csv("../../2007-01_water_anomalies.csv")

    # remove time
    df['timestamp'] = df['timestamp'].apply(editTimestamp)

    # to keep track of the previous row's date
    oldDate = 0

    # go through each of the anomalies individually
    for index, row in df.iterrows():

        date = row['timestamp']
        anomalyLatitude = row['latitude']
        anomalyLongitude = row['longitude']
        #anomalyLongitude += 180

        print(date)

        filename   = "data/AMSR_E_L3_SeaIce12km_V15_" + date + ".hdf"
        data_file  = SD(filename, SDC.READ)
        
        # https://nsidc.org/data/AE_SI12/versions/3
        
        NHconc = np.array(data_file.select("SI_12km_NH_ICECON_ASC")[:]).astype(np.float32)
        NHconc[(NHconc == 110) | (NHconc == 105) | (NHconc ==120) | (NHconc == 0)] = np.nan
    
        SHconc = np.array(data_file.select("SI_12km_SH_ICECON_ASC")[:]).astype(np.float32)
        SHconc[(SHconc == 110) | (SHconc == 105) | (SHconc == 120) | (SHconc == 0)] = np.nan

        # if this date isn't the same as the last one, then create new plot for new day
        if oldDate != date:

            plt.savefig(str(oldDate) + ".png")
            plt.close()
            
            fig = plt.figure()
            ax  = plt.axes(projection = ccrs.PlateCarree())
            ax.scatter(NHlon, NHlat, c = NHconc, alpha = 0.2, linewidth = 0, s = 1)
            ax.scatter(SHlon, SHlat, c = SHconc, alpha = 0.2, linewidth = 0, s = 1)
            ax.set_extent([-180, 180, -90, 90])
            ax.coastlines()

        
        if anomalyLatitude > 0:
            
            # find matching latitude
            latMatch = np.where(np.around(NHlat,decimals = 0) == round(anomalyLatitude,0))
            
            #iceLongitude = find_nearest(np.around(iceLongitudes, decimals = 2),
            longMatch = np.where(np.around(NHlon, decimals = 0) == round(anomalyLongitude + 180, 0))
            
            matchFound = False
            
            # want to loop through matches, use the array (lat or long) that is shortest
            if len(latMatch[0]) <= len(longMatch[0]):
                
                for i in range(len(latMatch[0])):
                    for j in range(len(latMatch[1])):
                        
                        # if position (index) of latitude and longitude match are equal
                        if (latMatch[0][i] == longMatch[0][i]) and (latMatch[1][j] == longMatch[1][j]):
                            
                            latIndex = latMatch[0][i]
                            longIndex = latMatch[1][j]
                            
                            if np.isnan(NHconc[latIndex][longIndex]):
                                m = 4
                            else:
                                matchFound = True
                                    
            else:
                for i in range(len(longMatch[0])):
                    for j in range(len(longMatch[1])):
                        
                        if (latMatch[0][i] == longMatch[0][i]) and (latMatch[1][j] == longMatch[1][j]):
                            
                            latIndex = latMatch[0][i]
                            longIndex = latMatch[1][j]
                            
                            if np.isnan(NHconc[latIndex][longIndex]):
                                m = 4
                            else:
                                matchFound = True
                                
        if matchFound == True:
            print("YES")
            print(anomalyLatitude, anomalyLongitude)
            print(NHconc[latIndex][longIndex])
            ax.scatter(anomalyLongitude, anomalyLatitude, c = "r",edgecolors = "k", zorder = 3)
        else:
            print("NO")
            print(anomalyLatitude, anomalyLongitude)
            ax.scatter(anomalyLongitude, anomalyLatitude, c = "b",edgecolors = "k", zorder = 3)

        oldDate = date
