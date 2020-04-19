import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['figure.figsize'] = (10,5)

# path al geojson del pais
argentina_fp = "/media/ggarcia/data/Satellogic/Satellogic/Data/SIG_Argentina/provincia.json"
provincias = gpd.read_file(argentina_fp)

print(type(provincias))


###  La Pampa, Neuquén, Río Negro, Chubut, Santa Cruz y Tierra del Fuego, Antártida e Islas del Atlántico Sur
# patagonia = ['La Pampa', 'Neuquén','Río Negro', 'Chubut', 'Santa Cruz', 'Tierra del Fuego']

patagonia = ['Neuquén']

map_dep1 = provincias[provincias.nam.isin(patagonia)]
# outputFile = "/home/ggarcia/Documents/Satellogic/Tests/Neuquen_Metano/Neuquen.shp"
# map_dep1.to_file(driver = 'ESRI Shapefile', filename = outputFile)



ax = map_dep1.plot(alpha=0.5, edgecolor='k')
plt.show()

