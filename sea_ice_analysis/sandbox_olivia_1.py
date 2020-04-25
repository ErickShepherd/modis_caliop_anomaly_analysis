import pandas as pd
import netCDF4 as nc
import numpy as np

def editTimestamp(x):

    head, sep, tail = str(x).partition(' ')
    head = head.replace("-","")
    return head

def

def main():

    # read in anomalies csv as pandas dataframe
    df = pd.read_csv("../anomaly_locations.csv")

    # remove time
    df['timestamp'] = df['timestamp'].apply(editTimestamp)

    # go through each of the anomalies individually
    for index, row in df.iterrows():

        date = row['timestamp']
        anomalyLatitude = row['latitude']
        anomalyLongitude = row['longitude']

        if (date == "20070101"):
            # if its in the northern hemisphere
            if (anomalyLatitude >= 0):
                
                # only open sea ice file from same day
                filename = "NHData/asicd25e2_" + date + "_v01r02.nc"
                dataset  = nc.Dataset(filename, "r+", format = "NETCDF4_Classic")
                
                
                extents = dataset["sea_ice_cover"][:].data
                iceLatitudes = dataset["latitude"][:].data
                iceLongitudes = dataset["longitude"][:].data
                
                
                # find matching latitude 
                latMatch = np.where(np.around(iceLatitudes,decimals = 0) == round(anomalyLatitude,0))
                
                #iceLongitude = find_nearest(np.around(iceLongitudes, decimals = 2), 
                longMatch = np.where(np.around(iceLongitudes, decimals = 0) == round(anomalyLongitude, 0))
                
                
                if len(latMatch[0]) <= len(longMatch[0]):
                    
                    for i in range(len(latMatch[0])):
                        for j in range(len(latMatch[1])):
                            
                            if (latMatch[0][i] == longMatch[0][i]) and (latMatch[1][j] == longMatch[1][j]):
                                print(date)
                                
                                latIndex = latMatch[0][i]
                                longIndex = latMatch[1][j]
                                print(iceLatitudes[latIndex][longIndex])
                                print(iceLongitudes[latIndex][longIndex])
                                
                                print(anomalyLatitude)
                                print(anomalyLongitude)

                else:
                    
                    for i in range(len(longMatch[0])):
                        for j in range(len(longMatch[1])):
                            
                            if (latMatch[0][i] == longMatch[0][i]) and (latMatch[1][j] == longMatch[1][j]):
                                print(date)
                                
                                latIndex = latMatch[0][i]
                                longIndex = latMatch[1][j]
                                print(iceLatitudes[latIndex][longIndex])
                                print(iceLongitudes[latIndex][longIndex])
                                                                        
                                print(anomalyLatitude)
                                print(anomalyLongitude)
main()

