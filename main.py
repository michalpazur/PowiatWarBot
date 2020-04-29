import geopandas, random, matplotlib as plt

powiaty = geopandas.read_file('map-data/powiaty.shp', encoding = 'utf-8')
print(powiaty.head())