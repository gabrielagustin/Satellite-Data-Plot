# -*- coding: utf-8 -*-
#!/usr/bin/python

'''

Created on Tue Feb  5 10:58:49 2020
Author: Gabriel Agustín Garcia
Copyright (c) 2020 Your Company
'''

import geopandas as gpd
import matplotlib.pyplot as plt


plt.rcParams['figure.figsize'] = (10,5)

# path al geojson del pais
argentina_fp = "/media/ggarcia/data/Satellogic/Satellogic/Data/SIG_Argentina/provincia.json"
provincias = gpd.read_file(argentina_fp)

print(type(provincias))


###  La Pampa, Neuquén, Río Negro, Chubut, Santa Cruz y Tierra del Fuego, Antártida e Islas del Atlántico Sur
patagonia = ['La Pampa', 'Neuquén','Río Negro', 'Chubut', 'Santa Cruz', 'Tierra del Fuego']

litoral = ['Misiones', 'Corrientes', 'Entre Ríos','Formosa', 'Chaco', 'Santa Fe']

map_dep1 = provincias[provincias.nam.isin(litoral)]


ax = map_dep1.plot(alpha=0.5, edgecolor='k')
plt.show()

