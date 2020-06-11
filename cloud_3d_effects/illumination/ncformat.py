import pandas as pd
import netCDF4 as nc
import numpy as np

# CONSTANTS
NUM_POINTS_AROUND_ANOMALY = 11

if __name__ == "__main__":

    csv_filename   = "2007_over-water_water_cloud_anomalies_with_sea_ice_and_heights.csv"
    ncout_filename = "2007_over-water_water_cloud_anomalies_with_sea_ice_and_heights.nc"

    df   = pd.read_csv(csv_filename)
    numAnomalies = df.timestamp.size

    ncout = nc.Dataset(ncout_filename, "w")

    # size refers to number of points around anomaly plus anomaly that were retrieved from data files
    ncout.createDimension("envelope", NUM_POINTS_AROUND_ANOMALY)
    
    ncout.createDimension("time", numAnomalies)


    # np.unicode_ type generates incorrect timestamp? Use np.datetime64?
    ncout.createVariable("timestamp",                np.unicode_, ("time",))
    ncout.createVariable("daylight",                 'i1',        ("time",))
    ncout.createVariable("latitude",                 np.float64,  ("time",))
    ncout.createVariable("longitude",                np.float64,  ("time",))
    ncout.createVariable("over_water",               'i1',        ("time",))
    ncout.createVariable("cloud",                    'i1',        ("time",))
    ncout.createVariable("single_layer",             'i1',        ("time",))
    ncout.createVariable("transparent",              'i1',        ("time",))
    ncout.createVariable("cod",                      np.float64,  ("time",))
    ncout.createVariable("sza",                      np.float64,  ("time",))
    ncout.createVariable("saa",                      np.float64,  ("time",))
    ncout.createVariable("sea_ice_concentration",    np.float64,  ("time",))
    ncout.createVariable("latitude_envelope",        np.float64,  ("time", "envelope"))
    ncout.createVariable("longitude_envelope",       np.float64,  ("time", "envelope"))
    ncout.createVariable("distances",                np.float64,  ("time", "envelope"))
    ncout.createVariable("modis_cloud_top_height",   np.float64,  ("time", "envelope"))
    ncout.createVariable("calipso_cloud_top_height", np.float64,  ("time", "envelope"))
  
    lat_env = df.latitude_envelope
    lat_env = list(map(lambda x: np.array(lat_env[x][1:-1].split()).astype(np.float32), range(numAnomalies)))

    lon_env = df.longitude_envelope
    lon_env = list(map(lambda x: np.array(lon_env[x][1:-1].split()).astype(np.float32), range(numAnomalies)))

    dist = df.distance
    dist = list(map(lambda x: np.array(dist[x][1:-1].split()).astype(np.float32), range(numAnomalies)))

    cal_heights = df.cal_cloud_top_height
    cal_heights = list(map(lambda x: np.array(cal_heights[x][1:-1].split()).astype(np.float32), range(numAnomalies)))

    mod_heights = df.modis_cloud_top_height
    mod_heights = list(map(lambda x: np.array(mod_heights[x][1:-1].split()).astype(np.float32), range(numAnomalies)))

    ncout["timestamp"][:]                = df.timestamp.values
    ncout["daylight"][:]                 = df.daylight.values
    ncout["latitude"][:]                 = df.latitude.values
    ncout["longitude"][:]                = df.longitude.values
    ncout["over_water"][:]               = df.over_water.values
    ncout["cloud"][:]                    = df.cloud.values
    ncout["single_layer"][:]             = df.single_layer.values
    ncout["transparent"][:]              = df.transparent.values
    ncout["cod"][:]                      = df.cod.values
    ncout["sza"][:]                      = df.sza.values
    ncout["saa"][:]                      = df.saa.values
    ncout["sea_ice_concentration"][:]    = df.sea_ice_concentration.values
    ncout["latitude_envelope"][:]        = lat_env
    ncout["longitude_envelope"][:]       = lon_env
    ncout["distances"][:]                = dist
    ncout["calipso_cloud_top_height"][:] = cal_heights
    ncout["modis_cloud_top_height"][:]   = mod_heights

    ncout.close()
