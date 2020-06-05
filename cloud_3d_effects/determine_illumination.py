# GOAL: 2D dot product of sunbeam vector and the vector representint the motion of the 
#       satellite, the sign of which indicates which point (before or after the anomaly)
#       is closer to the sun

# Standard library imports.
import datetime
import os
import re
from typing import Union
import math

# Third party imports.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

# Local application imports.
from collocate import lambert

# Constant definitions.
ANOMALY_PATH  = "2007_over-water_worldview_anomalies_with_sea_ice.csv"

def dot_product_sign(phi_1   : float,
                     phi_2   : float,
                     theta_1 : float = 90,
                     theta_2 : float = 90) -> float:

    '''
    
    Computes the sign of a 2d or 3d dot product of two vectors using their
    spherical coordinates (phi = azimuthal angle, theta = zenith angle)
 
    Parameters:
    
        * phi_1 (float) : 
          - Azimuthal angle for vector 1 
    
        * phi_2 (float) :
          - Azimuthal angle for vector 2 

        * theta_1 (float) :
          - Zenith angle for vector 1
          - Optional (default is 0 assuming 2d vector)

        * theta_2 (float) :
          - Zenith angle for vector 2
          - Optional (default is 0 assuming 2d vector)
    
    Return values:
    
        * sign (int) :
          - Sign of the dot product
               o Negative: -1
               o Positive: 1
               o Zero: 0

    '''

    phi_1   = math.radians(phi_1)
    phi_2   = math.radians(phi_2)
    theta_1 = math.radians(theta_1)
    theta_2 = math.radians(theta_2)

    rel_bounds = 1e-5
    abs_bounds = 1e-8
    
    print(np.sin(theta_1) * np.sin(theta_2) * np.cos(phi_1 - phi_2) 
                   + np.cos(theta_1) * np.cos(theta_2))
    sign = np.sign(np.sin(theta_1) * np.sin(theta_2) * np.cos(phi_1 - phi_2) 
                   + np.cos(theta_1) * np.cos(theta_2))

    return sign


if __name__ == "__main__":
    
    # Loads anomalies.
    #anomalies = pd.read_csv(ANOMALY_PATH)

    print(dot_product_sign(14, 123, 72, 2))
    print(dot_product_sign(14, 123, 72, 101))
    

    for i, anomaly in tqdm(anomalies.iterrows(), total = anomalies.index.size):
        
        # Read in longitude for the anomaly and points before and after anomaly

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!! need to update csv file/figure out how to read in lat/long envelopes 

        #anomaly_longitude = 
        #prev_longitude    = 
        #next_longtidue    = 

        #anomaly_latitude = 
        #prev_latitude    = 
        #next_latitude    = 


        # Calculate 2D vector dot product

        
        longitude_difference = next_longitude - prev_longitude
        latitude_difference  = next_latitude - prev_latitude

        # Determine azimuthal angle based on whether latitude and longtitude decrease 
        # between the previous and next point for the anomaly
        
        if latitude_difference < 0:
            azimuthal_angle = 180 - longitude_difference

        elif longitude_difference < 0:
            azimuthal_angle = 360 + longitude_difference

        else:
            azimuthal_angle = longitude_difference
    
        # Read in solar azimuthal angle (SAA) at anomaly
        # !!!!!! NEED TO DO THIS STILL !!!!!!!!

        # Calculate sign of dot product of the 2d vectors
        2d_sign = dot_product_sign(azimuthal angle, SAA)

        if 2d_sign > 0:
            point_longitude = prev_longitude
            point_latitude  = prev_latitude 
            #read in cloud top height for the previous point
            #point_height   = 

        if 2d_sign < 0:
            point_longitude = next_longitude
            point_latitude  = next_latitude 
            #read in cloud top height for the next point
            #point_height   = 
  


        # Calculate 3D vector

        longitude_difference = point_longitude - anomaly_longitude
        latitude_difference  = point_latitude - anomaly_latitude

        # Determine azimuthal angle based on whether latitude and longtitude decrease
        # between the previous and next point for the anomaly

        if latitude_difference < 0:
            azimuthal_angle = 180 - longitude_difference

        elif longitude_difference < 0:
            azimuthal_angle = 360 + longitude_difference

        else:
            azimuthal_angle = longitude_difference


        # Read in cloud top height for the anomaly
        #anomaly_height = 
        
        # Read in solar zenith angle (SZA) at anomaly
        # SZA = 

        height_diff_bween_points = point_height - anomaly_height

        distance_bween_points = lambert((anomaly_latitude, anomaly_longitdue), (point_latitude, point_longitude))
        
        zenith_angle = np.arctan(distance_bween_points / height_diff_bween_points)


        3D_sign = dot_product_sign(azimuthal angle, SAA, zenith_angle, SZA)

        if 3D_sign > 0:
            illuminated = True

        else:
            illumintated = False
