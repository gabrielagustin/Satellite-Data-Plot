# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:16:04 2018

@author: gag


"""


from pykml import parser
from os import path
import pandas as pd
import numpy as np
import math
from shapely.geometry import Point
import h5py


def readKML(filename):
    """ Read KML file extracts the coordinates (Lat, Lon) and generates a pandas object that then returns

    Parameters:
    -----------
    data : String instances that contain file path

    Returns: 
    --------
    Pandas DataFrame: coordinates (Lat, Lon)
    """

    kml_file = path.join(filename)

    #### se leen los elementos del KML
    with open(kml_file) as f:
        folder = parser.parse(f).getroot().Document.Folder

    #### se separan los elementos, nombres de los puntos y las coordenadas
    plnm=[]
    cordi=[]
    for pm in folder.Placemark:
        plnm1 = pm.name
        plcs1 = pm.Point.coordinates
        plnm.append(plnm1.text)
        cordi.append(plcs1.text)
    # print(cordi)
    # print(plnm)   

    #### se genera el objeto pandas
    db=pd.DataFrame()
    db['point_name']=plnm
    db['cordinates']=cordi

    db['Longitude'], db['Latitude'], db['value'] = zip(*db['cordinates'].apply(lambda x: x.split(',', 2)))
    db["Longitude"] = pd.to_numeric(db["Longitude"])
    db["Latitude"] = pd.to_numeric(db["Latitude"])
    del db['cordinates']
    del db['value']

    db['Coordinates'] = list(zip(db.Longitude, db.Latitude))
    db['Coordinates'] = db['Coordinates'].apply(Point)

    # print(db)

    return db

####------------------------------------------------------------------------------------------------------------


def read_SMAP_L1B_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray):
    """ Read a SMAP L1B satellite image in .H5 format

    Parameters:
    -----------
    FILE_NAME : complete path of the image 
    
    box_lat, box_lon: latitude and longitude of the specific study area

    nameVariableArray: vector of the variables to be read

    Returns: 
    --------
    Pandas DataFrame: it has as columns the coordinates (Lat, Lon) and the variables 
                      read for each pixel.
    """

    db=pd.DataFrame()
    pd.options.mode.chained_assignment = None
    with h5py.File(FILE_NAME, mode='r') as f:
        for i in range(0, len(nameVariableArray)):
            nameVariable = nameVariableArray[i]
            # print('Variable a extraer:' +str(nameVariable))
            data = f[nameVariable][:]
            units = f[nameVariable].attrs['units']
            longname = f[nameVariable].attrs['long_name']
            _FillValue = f[nameVariable].attrs['_FillValue']
            valid_max = f[nameVariable].attrs['valid_max']
            valid_min = f[nameVariable].attrs['valid_min']        
            invalid = np.logical_or(data > valid_max,
                                data < valid_min)
            invalid = np.logical_or(invalid, data == _FillValue)
            data[invalid] = np.nan
            data = np.ma.masked_where(np.isnan(data), data)
            data = data.flatten('F')
            
            # Get the geolocation data
            latitude = f['/Brightness_Temperature/tb_lat'][:]
            longitude = f['/Brightness_Temperature/tb_lon'][:]
            lat_index = np.logical_and(latitude > box_lat[0], latitude < box_lat[1])
            lon_index = np.logical_and(longitude > box_lon[0], longitude < box_lon[1])
            box_index = np.logical_and(lat_index, lon_index)
            data = f[nameVariable][box_index]
            #### se genera el objeto pandas
            db[nameVariable] = data
            latitude = f['/Brightness_Temperature/tb_lat'][box_index]
            longitude = f['/Brightness_Temperature/tb_lon'][box_index]


    # Latitude = Latitude.flatten('F')
    # Longitude = Longitude.flatten('F')

    db["Longitude"] = pd.to_numeric(longitude)
    db["Latitude"] = pd.to_numeric(latitude)    

    db['Coordinates'] = list(zip(db.Longitude, db.Latitude))
    db['Coordinates'] = db['Coordinates'].apply(Point)

    db = db.dropna()
    return db


