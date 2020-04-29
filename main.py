import geopandas, random, contextily
import matplotlib.pyplot as plt

powiaty = geopandas.read_file('map-data/powiaty.shp', encoding = 'utf-8')
print(powiaty.head())

cmap = plt.get_cmap('tab20')
fig, ax = plt.subplots(figsize = (8,8))
ax.set_axis_off()
ax.set_aspect('equal')

for i in range(len(powiaty)):
    row = powiaty.loc[[i],]
    row.plot(ax = ax, color = cmap(row['density']), edgecolor = 'k', linewidth = 0.3)
    
contextily.add_basemap(ax, source = contextily.sources.ST_TERRAIN_BACKGROUND, zoom = 9)
plt.show(ax)