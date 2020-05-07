# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.haversine_distances.html

# Third party imports.
import numpy as np

# Constant definitions.
#   - Planet radii values in meters.
EQUATORIAL_RADIUS = 6_378_137.0
POLAR_RADIUS      = 6_356_752.3142
MEAN_RADIUS       = (2 * EQUATORIAL_RADIUS + POLAR_RADIUS) / 3


def haversine(latitude_1, longitude_1, latitude_2, longitude_2):
    
    # Aliasing for brevity.
    R     = MEAN_RADIUS
    lat_1 = latitude_1
    lon_1 = longitude_1
    lat_2 = latitude_2
    lon_2 = longitude_2
    
    lon_1, lat_1, lon_2, lat_2 = map(np.radians, [lon_1, lat_1, lon_2, lat_2])
    
    dlon = lon_2 - lon_1
    dlat = lat_2 - lat_1
    
    d = 2 * R * np.asin(np.sin(dlat / 2) ** 2 +
                        np.sin(dlon / 2) ** 2 *
                        np.cos(lat_1) *
                        np.cos(lat_2))
    
    return d
    

def lambert(latitude_1, longitude_1, latitude_2, longitude_2):
    
    # Aliasing for brevity.
    a     = EQUATORIAL_RADIUS
    b     = POLAR_RADIUS
    R     = MEAN_RADIUS
    lat_1 = latitude_1
    lon_1 = longitude_1
    lat_2 = latitude_2
    lon_2 = longitude_2
    
    # Flattening.
    f = (a - b) / a
    
    # Reduced latitudes.
    beta_1 = np.atan((1 - f) * np.tan(lat_1))
    beta_2 = np.atan((1 - f) * np.tan(lat_2))
    
    P = (beta_2 + beta_1) / 2
    Q = (beta_2 - beta_1) / 2
    
    D = haversine(lat_1, lon_1, lat_2, lon_2)
    
    sigma = D / R
    
    X = (sigma - np.sin(sigma)) * (np.sin(P) ** 2 * np.cos(Q) ** 2) / np.cos(sigma / 2) ** 2
    Y = (sigma + np.sin(sigma)) * (np.sin(Q) ** 2 * np.cos(P) ** 2) / np.sin(sigma / 2) ** 2
    
    d = a * (sigma - f / 2 * (X + Y))
    
    return d
