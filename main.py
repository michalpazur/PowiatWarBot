import json, geopandas, pandas, random, contextily, re
import matplotlib.pyplot as plt

powiaty = geopandas.read_file('map-data/powiaty.shp', encoding = 'utf-8')
with open('map-data/neighbours.json', 'r') as neighbours_file:
    neighbours = json.load(neighbours_file)

for i in range(1000):
    can_poceed = False

    while not can_poceed:
        random_powiat_row = powiaty.loc[[random.choice(powiaty.index)]]
        random_powiat_code = random_powiat_row['code'].iloc[0]
        random_powiat_belongs_to = random_powiat_row['belongs_to'].iloc[0]
        conquering_powiat_row = powiaty[powiaty['code'] == random_powiat_belongs_to]
        conquering_powiat_code = conquering_powiat_row['code'].iloc[0]
        conquering_powiat_value = conquering_powiat_row['value'].iloc[0]
        conquering_powiat_name = conquering_powiat_row['name'].iloc[0]

        powiat_to_conquer_code = random.choice(neighbours[random_powiat_code])
        powiat_to_conquer_row = powiaty[powiaty['code'] == powiat_to_conquer_code]
        powiat_to_conquer_name = powiat_to_conquer_row['name'].iloc[0]
        powiat_to_conquer_belongs_to = powiat_to_conquer_row['belongs_to'].iloc[0]
        can_poceed = (powiat_to_conquer_belongs_to != conquering_powiat_code)
        
    powiaty['belongs_to'][powiaty['code'] == powiat_to_conquer_code] = random_powiat_belongs_to
    powiaty['value'][powiaty['code'] == powiat_to_conquer_code] = conquering_powiat_value
    print('{} podbija {}'.format(conquering_powiat_name, powiat_to_conquer_name))

cmap = plt.get_cmap('tab20')
fig, ax = plt.subplots(figsize = (8,8))
ax.set_axis_off()
ax.set_aspect('equal')

for i in range(len(powiaty)):
    row = powiaty.loc[[i],]
    row.plot(ax = ax, color = cmap(row['value']), edgecolor = 'k', linewidth = 0.3)
    
contextily.add_basemap(ax, source = contextily.sources.ST_TERRAIN_BACKGROUND, zoom = 9)
plt.show(ax)