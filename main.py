import json, geopandas, pandas, random, contextily, re
import matplotlib.pyplot as plt

pandas.set_option('mode.chained_assignment', None)

powiaty = geopandas.read_file('map-data/powiaty.shp', encoding = 'utf-8')
with open('map-data/neighbours.json', 'r') as neighbours_file:
    neighbours = json.load(neighbours_file)

for i in range(500):
    can_proceed = False

    while not can_proceed:
        if i == 0 or random.random() < 0.6:
            random_powiat_row = powiaty.loc[[random.choice(powiaty.index)]]
        else:
            random_powiat_row = all_rows_for_conquering_powiat.loc[[random.choice(all_rows_for_conquering_powiat.index)]]

        #get a random powiat and its owner
        random_powiat_code = random_powiat_row['code'].iloc[0]
        random_powiat_belongs_to = random_powiat_row['belongs_to'].iloc[0]
        conquering_powiat_row = powiaty[powiaty['code'] == random_powiat_belongs_to]
        conquering_powiat_code = conquering_powiat_row['code'].iloc[0]
        conquering_powiat_value = conquering_powiat_row['value'].iloc[0]

        #get a powiat to conquer from the list of neighbors
        powiat_to_conquer_code = random.choice(neighbours[random_powiat_code])
        powiat_to_conquer_row = powiaty[powiaty['code'] == powiat_to_conquer_code]
        powiat_to_conquer_belongs_to_code = powiat_to_conquer_row['belongs_to'].iloc[0]
    
        #powiat can only be conquered if it doesn't belong to conquering powiat
        can_proceed = (powiat_to_conquer_belongs_to_code != conquering_powiat_code)
    
    conquering_powiat_name = conquering_powiat_row['name'].iloc[0]
    powiat_to_conquer_name = powiat_to_conquer_row['name'].iloc[0]

    #merge geometry for conquering powiat
    all_rows_for_conquering_powiat = powiaty[powiaty['belongs_to'] == conquering_powiat_code]
    conquering_powiat_geometry = all_rows_for_conquering_powiat['geometry'].unary_union
    conquering_powiat_row['geometry'].iloc[0] = conquering_powiat_geometry

    #find row for conquered powiat owner
    powiat_to_conquer_owner_row = powiaty[powiaty['code'] == powiat_to_conquer_belongs_to_code]
    powiat_to_conquer_owner_name = powiat_to_conquer_owner_row['name'].iloc[0]
    powiat_to_conquer_owner_value = powiat_to_conquer_owner_row['value'].iloc[0]

    #update values for conquered powiat
    powiaty['belongs_to'][powiaty['code'] == powiat_to_conquer_code] = conquering_powiat_code
    powiaty['value'][powiaty['code'] == powiat_to_conquer_code] = conquering_powiat_value

    print('{} podbija {} należący do {}'.format(conquering_powiat_name, powiat_to_conquer_name, powiat_to_conquer_owner_name))

    #find all rows for conquered powiat owner and merge geometry
    all_rows_for_powiat_to_conquer_owner = powiaty[powiaty['belongs_to'] == powiat_to_conquer_belongs_to_code]
    powiat_to_conquer_owner_geometry = all_rows_for_powiat_to_conquer_owner['geometry'].unary_union
    powiat_to_conquer_owner_row['geometry'].iloc[0] = powiat_to_conquer_owner_geometry

    if (all_rows_for_powiat_to_conquer_owner.empty):
        print('🦀 {} is gone 🦀'.format(powiat_to_conquer_owner_name))

cmap = plt.get_cmap('tab20')
fig, ax = plt.subplots(figsize = (8,8))
ax.set_axis_off()
ax.set_aspect('equal')

for i in range(len(powiaty)):
    row = powiaty.loc[[i],]
    row.plot(ax = ax, color = cmap(row['value']), edgecolor = 'k', linewidth = 0.3)
    
conquering_powiat_row.plot(ax = ax, color = cmap(conquering_powiat_value), edgecolor = 'green', linewidth = 2)
powiat_to_conquer_row.plot(ax = ax, color = cmap(powiat_to_conquer_owner_value), edgecolor = 'red', hatch = '///', linewidth = 2)
powiat_to_conquer_owner_row.plot(ax = ax, color = cmap(powiat_to_conquer_owner_value), edgecolor = 'blue', linewidth = 2)

contextily.add_basemap(ax, source = contextily.sources.ST_TERRAIN_BACKGROUND, zoom = 9)
plt.show(ax)