# Description: Determine if the anomaly is on the illuminated side of a cloud
#              using the sign of the dot product of the slope vector and the 
#              sunbeam vector
#
#              Slope vector is calculated using the anomaly and one of the points
#              next to it, which point is determined using the sign of the 2D dot 
#              product of sunbeam vector and the vector representing the motion of 
#              the satellite

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
import netCDF4 as nc

# Local application imports.
from collocate import lambert

# Constant definitions.
FILENAME  = "cloud_top_heights/2007_over-water_water_cloud_anomalies_with_sea_ice_and_heights_and_illuminated.nc"
#"cloud_top_heights/2007_over-water_worldview_anomalies_with_sea_ice_and_heights.nc"

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

    phi_1, phi_2, theta_1, theta_2 = map(np.radians, [phi_1, phi_2, theta_1, theta_2])


    sign = np.sign(np.sin(theta_1) * np.sin(theta_2) * np.cos(phi_1 - phi_2) 
                   + np.cos(theta_1) * np.cos(theta_2))

    return sign


def calculate_azimuthal_angle(latitude_1  : float, 
                              longitude_1 : float, 
                              latitude_2  : float,
                              longitude_2 : float) -> float:

    '''
    Computes the azimuthal angle for a vector described by two points,
    going from point (latitude_1, longitude_1) to point (latitude_2, longitude_2)

    Parameters:

        * latitude_1 (float) :
          - Latiutde position for starting point of the vector

        * longitude_1 (float) :
          - Longitude position for starting point of the vector

        * latitude_2 (float) :
          - Latiutde position for end point of the vector

        * longitude_2 (float) :
          - Longitude position for end point of the vector

    Return values:

        * angle (float) :
          - Units: degrees
          - Azimuthal angle for the vector

    '''

    latitude_diff  = latitude_2 - latitude_1
    longitude_diff = longitude_2 - longitude_1 

    # if satellite is moving E or W along cadinal axes
    if latitude_diff == 0:

        # if satellite is moving E  
        if longitude_2 > longitude_1:
            angle = 90

        # if satellite is moving W
        else:
            angle = 270

        return angle


    # if satellite is moving N or S along cadinal axes
    if longitude_diff == 0:

        # if satellite is moving N  
        if latitude_2 > latitude_1:
            angle = 0

        # if satellite is moving S
        else:
            angle = 180

        return angle


    # if satellite is not moving along cardinal axes find the x and y component
    # of the displacement vector between these two points calculated along the 
    # cardinal axes

    point_start = np.array([(latitude_1, longitude_1)])
    point_mid   = np.array([(latitude_1, longitude_2)])
    point_end   = np.array([(latitude_2, longitude_2)])                    

    # Lambert formula calculates distance between first and second point given
    distance_x = lambert(point_start[0], point_mid[0])
    distance_y = lambert(point_mid[0], point_end[0])

    angle = np.degrees(np.arctan( distance_x / distance_y ))

    # Determine azimuthal angle based on whether latitude and longtitude decrease
    # between the previous and next point for the anomaly
    
    if latitude_diff < 0 and longitude_diff < 0:
        angle = 180 + angle
        
    elif longitude_diff < 0:
        angle = 360 - angle
        
    elif latitude_diff < 0:
        angle = 180 - angle

    return angle


def determine_cardinal_direction(latitude_1  : float,
                                 longitude_1 : float,
                                 latitude_2  : float,
                                 longitude_2 : float) -> float:

    '''
    Computes the cardinal direction (e.g. N, NW, SW, etc.) for a vector 
    described by two points going from point (latitude_1, longitude_1) to 
    point (latitude_2, longitude_2)

    Parameters:

        * latitude_1 (float) :
          - Latiutde position for starting point of the vector

        * longitude_1 (float) :
          - Longitude position for starting point of the vector

        * latitude_2 (float) :
          - Latiutde position for end point of the vector

        * longitude_2 (float) :
          - Longitude position for end point of the vector

    Return values:

        * cardinal_direction (string) :
          - Direction of a vector in reference to the cardinal points
    '''

    if latitude_1 < latitude_2 and longitude_1 < longitude_2:
        cardinal_direction = "NE"

    elif latitude_1 > latitude_2 and longitude_1 < longitude_2:
        cardinal_direction = "SE"

    elif latitude_1 > latitude_2 and longitude_1 > longitude_2:
        cardinal_direction = "SW"
        
    elif latitude_1 < latitude_2 and longitude_1 > longitude_2:
        cardinal_direction = "NW"

    elif latitude_1 < latitude_2:
        cardinal_direction = "N"

    elif latitude_1 > latitude_2:
        cardinal_direction = "S"

    elif longitude_1 < longitude_2:
        cardinal_direction = "E"

    elif longitude_1 > longitude_2:
        cardinal_direction = "W"

    return cardinal_direction


if __name__ == "__main__":
    
    # Loads anomalies.
    ncin = nc.Dataset(FILENAME, 'r+')

    # Added these variables to the existing nc file
    #ncin.createVariable("previous_point_used", 'i1',        ("time",))
    #ncin.createVariable("illuminated",         'i1',        ("time",))
    #ncin.createVariable("cardinal_direction",  np.unicode_, ("time",))
    #ncin.createVariable("missing_point",       'i1',        ("time",))

    numAnomalies = ncin["latitude"].size
    envelopeSize = ncin["latitude_envelope"][1][:].size

    prevIndex = int(envelopeSize/2 - 1)
    nextIndex = int(envelopeSize/2 + 1)
    anomalyIndex = int(envelopeSize/2)


    for i in tqdm(range(numAnomalies)):
        #print("Anomaly", i)

        #_____________________Read in data_____________________#

        # Read in longitude for the anomaly and points before and after anomaly
        anomaly_longitude = ncin["longitude"][i]
        prev_longitude    = ncin["longitude_envelope"][i][prevIndex]
        next_longitude    = ncin["longitude_envelope"][i][nextIndex]

        anomaly_latitude = ncin["latitude"][i]
        prev_latitude    = ncin["latitude_envelope"][i][prevIndex]
        next_latitude    = ncin["latitude_envelope"][i][nextIndex]

        cardinal_direction = determine_cardinal_direction(prev_latitude, prev_longitude, 
                                                          next_latitude, next_longitude)

        # Read in cloud top height for the anomaly
        anomaly_height = ncin["calipso_cloud_top_height"][i][anomalyIndex]

        # Read in solar azimuthal angle (SAA) at anomaly
        SAA = ncin["saa"][i]

        # Read in solar zenith angle (SZA) at anomaly
        SZA = ncin["sza"][i]


        #____________Determine point closest to the sun____________#

        # Calculate azimuthal angle for the satellite displacement vector
        displacement_azimuthal_angle = calculate_azimuthal_angle(prev_latitude, prev_longitude,
                                                                 next_latitude, next_longitude)
        #print("Disp Az: ", displacement_azimuthal_angle)

        # convert SAA so that vector is pointing away from the origin, with origin representing the sun
        SAA = 180 + SAA

        #print("SAA: ", SAA)
        
        # Calculate sign of dot product of the 2d vectors
        sign_2d = dot_product_sign(displacement_azimuthal_angle, SAA)
        #print("2D Sign: ", sign_2d)

        # Determine which point to use in the slope calculation based on the sign

        # If positive, use point before anomaly
        if sign_2d > 0:
            # Calculate azimuthal angle for the satellite displacement vector
            slope_azimuthal_angle = calculate_azimuthal_angle(prev_latitude, prev_longitude,
                                                          anomaly_latitude, anomaly_longitude)

            distance_bween_points = lambert((anomaly_latitude, anomaly_longitude), 
                                            (prev_latitude, prev_longitude))

            #read in cloud top height for the previous point
            point_height = ncin["calipso_cloud_top_height"][i][prevIndex]
            
            # find height in meters
            height_diff_bween_points = (anomaly_height - point_height) * 1000

            # Append 'True' to the prevPointUsed array, since the previous point was the one used to calculate slope
            prevPointUsed = 1


        # If negative, use point after anomaly
        if sign_2d < 0:

            # Calculate azimuthal angle for the satellite displacement vector
            slope_azimuthal_angle = calculate_azimuthal_angle(prev_latitude, prev_longitude,
                                                              anomaly_latitude, anomaly_longitude)
             
            distance_bween_points = lambert((anomaly_latitude, anomaly_longitude),
                                             (prev_latitude, prev_longitude))

            #read in cloud top height for the next point
            point_height    = ncin["calipso_cloud_top_height"][i][nextIndex]
  
            # find height in meters
            height_diff_bween_points = (point_height - anomaly_height) * 1000


            prevPointUsed = 0


        if np.isnan(point_height):
            missingPoint = 1
        else:
            missingPoint = 0

        #____________Determine if anomaly is on illuminated side of cloud____________#
        
        #print("Slope Az: ", slope_azimuthal_angle)
        
        # Change SZA vector to be greater than 90, since it is pointing down
        SZA = 180 - SZA
        #print("SZA: ", SZA)
        
        slope_zenith_angle = np.degrees(np.arctan(distance_bween_points / height_diff_bween_points))

        # if cloud top height decreases, then zenith angle is greater than 90
        if height_diff_bween_points < 0:
            slope_zenith_angle = 180 - abs(slope_zenith_angle)

        #print("Slope Zen: ", slope_zenith_angle)

        sign_3d = dot_product_sign(slope_azimuthal_angle, SAA, slope_zenith_angle, SZA)
        
        if height_diff_bween_points > 0:
            if sign_3d > 0:
                illuminated = 1
                
            else:
                illuminated = 0
        
        else:
            if sign_3d < 0:
                illuminated = 1

            else:
                illuminated = 0

        # Update nc file with new information for anomaly "i"
        ncin["previous_point_used"][i] = prevPointUsed
        ncin["illuminated"][i]         = illuminated
        ncin["cardinal_direction"][i]  = cardinal_direction
        ncin["missing_point"][i]       = missingPoint 
    
    ncin.close()

