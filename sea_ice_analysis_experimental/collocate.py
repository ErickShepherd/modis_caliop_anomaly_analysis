# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.haversine_distances.html

# Third party imports.
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Constant definitions.
#   - Planet radii values in meters.
EQUATORIAL_RADIUS = 6_378_137.0
POLAR_RADIUS      = 6_356_752.3142
MEAN_RADIUS       = (2 * EQUATORIAL_RADIUS + POLAR_RADIUS) / 3
NEIGHBORS_CHECKED = 4


def haversine(point_1, point_2):
    
    latitude_1, longitude_1 = point_1
    latitude_2, longitude_2 = point_2
    
    # Aliasing for brevity.
    R     = MEAN_RADIUS
    lat_1 = latitude_1
    lon_1 = longitude_1
    lat_2 = latitude_2
    lon_2 = longitude_2
    
    lon_1, lat_1, lon_2, lat_2 = map(np.radians, [lon_1, lat_1, lon_2, lat_2])
    
    dlon = lon_2 - lon_1
    dlat = lat_2 - lat_1
    
    d = 2 * R * np.arcsin(np.sqrt(np.sin(dlat / 2) ** 2 +
                                  np.sin(dlon / 2) ** 2 *
                                  np.cos(lat_1) *
                                  np.cos(lat_2)))
    
    return d
    

def lambert(point_1, point_2):
    
    latitude_1, longitude_1 = point_1
    latitude_2, longitude_2 = point_2
    
    # Aliasing for brevity.
    a     = EQUATORIAL_RADIUS
    b     = POLAR_RADIUS
    R     = MEAN_RADIUS
    lat_1 = latitude_1
    lon_1 = longitude_1
    lat_2 = latitude_2
    lon_2 = longitude_2
    
    lon_1, lat_1, lon_2, lat_2 = map(np.radians, [lon_1, lat_1, lon_2, lat_2])
    
    # Flattening.
    f = (a - b) / a
    
    # Reduced latitudes.
    beta_1 = np.arctan((1 - f) * np.tan(lat_1))
    beta_2 = np.arctan((1 - f) * np.tan(lat_2))
    
    P = (beta_2 + beta_1) / 2
    Q = (beta_2 - beta_1) / 2
    
    D = haversine(point_1, point_2)
        
    sigma = D / R
    
    X = (sigma - np.sin(sigma)) * (np.sin(P) ** 2 * np.cos(Q) ** 2) / np.cos(sigma / 2) ** 2
    Y = (sigma + np.sin(sigma)) * (np.cos(P) ** 2 * np.sin(Q) ** 2) / np.sin(sigma / 2) ** 2
    
    d = a * (sigma - f / 2 * (X + Y))
    
    return d


def nearest(latitude, longitude, latitudes, longitudes):
    
    point = np.array([(latitude, longitude)])
    
    latitude_grid, longitude_grid = np.meshgrid(latitudes, longitudes)
    
    coordinates = np.array([latitude_grid.ravel(), longitude_grid.ravel()]).T
    
    neighbors = NearestNeighbors(n_neighbors = NEIGHBORS_CHECKED,
                                 metric      = haversine)
    neighbors = neighbors.fit(coordinates)
    
    haversine_distances, indices = nbrs.kneighbors(point)
    lambert_distances = np.empty(NEIGHBORS_CHECKED)


if __name__ == "__main__":
    
    latitudes  = np.arange(-90, 91, 1)
    longitudes = np.arange(-180, 181, 1)
    
    LAT, LON = np.meshgrid(latitudes, longitudes)
    
    data = np.array([LAT.ravel(), LON.ravel()]).T

    nbrs = NearestNeighbors(n_neighbors = NEIGHBORS_CHECKED, metric = haversine).fit(data)
    
    p1 = np.array([(0.5, 0.5)])
    distance, index = nbrs.kneighbors(p1)
    p2 = data[index[0]]
    
    distance2 = lambert(p1[0], p2[0])
    
    print("Given point:   ", tuple(p1[0]))
    print("Closest point: ", tuple(p2[0]))
    print("Haversine:     ", distance[0][0])
    print("Lambert:       ", distance2)
