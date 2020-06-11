import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from tqdm import tqdm

ncin = nc.Dataset("cloud_top_heights/test.nc", "r")
#"2007_over-water_water_cloud_anomalies_with_sea_ice_and_heights.csv", nrows = 20)

t = ncin["timestamp"][:]
d = ncin["distances"][:]
modis = ncin["modis_cloud_top_height"][:]
cal = ncin["calipso_cloud_top_height"][:]
direction = ncin["cardinal_direction"][:]
sza = ncin["sza"][:]
saa = ncin["saa"][:]
illuminated = ncin["illuminated"][:]
prevPointUsed = ncin["previous_point_used"][:]

# determine index of the anomaly
anomaly_pos = int((len(modis[0]) - 1) / 2)

for i in tqdm(range(len(t))):

    # Convert MODIS cloud top height to km
    modis[i] = [x / 1000 for x in modis[i]]
    
    
    if illuminated[i]:
        color = "purple"
        label = "Illuminted"
    else:
        color = "green"
        label = "Not illuminated"

    plt.figure()
    plt.title(t[i] + "\nSatellite: " +  direction[i] + " direction\nSZA: " + str(sza[i]) +  "; SAA: " + str(saa[i]))
    plt.plot(d[i], modis[i], c = "b", marker = 'o', label = "MODIS")
    plt.plot(d[i], cal[i], c = "orange", marker = 'o', label = "CALIOP")
    plt.axvline(d[i][anomaly_pos], c = "r", ls = "--")
    plt.xlim(d[i].min(), d[i].max())
    
    # add in plot of point used to determine illumination
    if prevPointUsed[i]:
        plt.plot(d[i][anomaly_pos - 1: anomaly_pos + 1], cal[i][anomaly_pos - 1: anomaly_pos + 1], c = color, marker = 'o', label = label)
    else:
        plt.plot(d[i][anomaly_pos: anomaly_pos + 2], cal[i][anomaly_pos: anomaly_pos + 2], c = color, marker = 'o', label = label)
        
    plt.xlabel("Displacement from Anomaly Along Track (m)")
    plt.ylabel("Cloud Top Height (km)")
    plt.legend()
    plt.savefig(f"test_{i:02d}.png")
    plt.close()
