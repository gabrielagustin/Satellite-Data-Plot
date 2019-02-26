# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:16:04 2018

@author: gag

Script that graphs satellite image coming from the SMAP mission of level L1B file .H5 
using basemap library

"""



import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

import functions


if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    hdfFile = '/.../SMAP_L1B/SMAP_L1B_TB_20137_A_20181108T101842_R16020_001.h5'
    try:
        hdfFile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass
    ##### lee el archivo HDF, se extrae la variable y se genera el objeto geopandas
    nameVariable = ['/Brightness_Temperature/tb_h']
    # pdHDF = functions.readHDF(hdfFile, nameVariable)
    box_lat = [-85, -65]
    box_lon = [120, 180]
    df = functions.read_SMAP_L1B_HDF_box(hdfFile, box_lat, box_lon, nameVariable)

    print(list(df))
    print(df)

    #### plot using basemap
    m = Basemap(projection='cyl', resolution='l',
            llcrnrlat= -85, urcrnrlat=-65,
            llcrnrlon=120, urcrnrlon=180)


    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90, 91, 10),labels=[True,False,False,True])
    m.drawmeridians(np.arange(-180, 180, 15), labels=[True,False,False,True])
    name = "/Brightness_Temperature/tb_h"
    m.scatter(df.Longitude, df.Latitude, c=df[name], s=1, cmap=plt.cm.jet,
            edgecolors=None, linewidth=0)
    cb = m.colorbar(location="bottom", pad=0.7)    
    cb.set_label('[°K]')
    plt.title(name)

    plt.show()

