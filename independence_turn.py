import json, geopandas, pandas, random, contextily, os, re
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import matplotlib as matplotlib
from adjustText import adjust_text
from log import log_info, log_error

powiaty_names = {}
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
matplotlib.rcParams['hatch.linewidth'] = 3
pandas.set_option('mode.chained_assignment', None)

def load_values():

    powiaty = geopandas.read_file('map-data/powiaty.shp', encoding = 'utf-8')
    powiaty_shapes = geopandas.read_file('map-data/powiaty-shapes.shp', encoding = 'utf-8')
    powiaty = powiaty.merge(powiaty_shapes, how = 'left', left_index = True, right_index = True)
    powiaty = powiaty.drop(columns = 'code_y')
    powiaty = powiaty.rename(columns = {'code_x': 'code', 'geometry_x': 'geometry', 'geometry_y': 'powiat_shape'})
    powiaty = powiaty.set_geometry('geometry')

    for index, row in powiaty.iterrows():
        all_rows_for_powiat = powiaty[powiaty['belongs_to'] == row['code']]
        powiaty_names[row['code']] = row['name'].lstrip('miasto ')
        if (all_rows_for_powiat.empty):
            powiaty['geometry'][powiaty['code'] == row['code']] = None
        else:
            all_rows_for_powiat = all_rows_for_powiat.set_geometry('powiat_shape')
            row_geometry = all_rows_for_powiat.unary_union
            powiaty['geometry'][powiaty['code'] == row['code']] = row_geometry
    
    mapbox = ""
    with open("api-key.txt", "r") as f:
        for i in range(6):
            line = f.readline()
            if i != 5:
                continue
            mapbox = line.strip()

    return powiaty, mapbox

def play_independence_turn():
    powiaty, mapbox = load_values()

    with open('map-data/status.txt', 'r') as f:
        powiaty_left = int(f.readline())
        last_powiat = f.readline().rstrip()
        date = int(f.readline())
        biggest_powiat = f.readline().rstrip()
    
    month = months[date % 12]
    year = 1999 + date // 12
    message = '{} {}'.format(month, year)

    #find a powiat with empty geometry - it can regain independence
    all_rows_with_null_geometry = powiaty[powiaty['geometry'].isna()]
    random_powiat_row = all_rows_with_null_geometry.loc[[random.choice(all_rows_with_null_geometry.index)]]

    random_powiat_code = random_powiat_row['code'].iloc[0]
    conquering_powiat_row = powiaty[powiaty['code'] == random_powiat_code]
    conquering_powiat_code = conquering_powiat_row['code'].iloc[0]
    conquering_powiat_value = conquering_powiat_row['value'].iloc[0]
    conquering_powiat_geometry = conquering_powiat_row['powiat_shape'].iloc[0]
    conquering_powiat_name = conquering_powiat_row['name'].iloc[0].lstrip('miasto ')

    conquering_powiat_owner_code = conquering_powiat_row['belongs_to'].iloc[0]

    #find row for powiat gaining idependence powiat owner
    conquering_powiat_owner_row = powiaty[powiaty['code'] == conquering_powiat_owner_code]
    conquering_powiat_owner_name = conquering_powiat_owner_row['name'].iloc[0]
    conquering_powiat_owner_value = conquering_powiat_owner_row['value'].iloc[0]

    #update value for conquered powiat
    powiaty['belongs_to'][powiaty['code'] == conquering_powiat_code] = conquering_powiat_code

    message = '{}, {} has gained independence from {}.'.format(message, conquering_powiat_name, conquering_powiat_owner_name)
    log_info(message)
        
    #find all rows for conquered powiat owner and change geometry
    all_rows_for_conquering_powiat_owner = powiaty[powiaty['belongs_to'] == conquering_powiat_owner_code]
    conquering_powiat_owner_geometry = conquering_powiat_owner_row['geometry'].iloc[0]
    conquering_powiat_owner_geometry = conquering_powiat_owner_geometry.difference(conquering_powiat_geometry)
    conquering_powiat_row['geometry'].iloc[0] = conquering_powiat_geometry
    conquering_powiat_owner_row['geometry'].iloc[0] = conquering_powiat_owner_geometry
    powiaty['geometry'][powiaty['code'] == conquering_powiat_owner_code] = conquering_powiat_owner_geometry

    if (all_rows_for_conquering_powiat_owner.empty):
        info = '🦀 {} is gone 🦀'.format(conquering_powiat_owner_name)
        message = '{}\n{}'.format(message, info)
        log_info(info)
    else:
        powiaty_left += 1

    if (powiaty_left > 1):
        info = '{} powiaty left.'.format(powiaty_left)
    else:
        capitalized_name = conquering_powiat_name[0].capitalize() + conquering_powiat_name[1:]
        info = '{} now rules over Poland. Niech żyje {}!'.format(capitalized_name, conquering_powiat_name)

    message = '{}\n{}\nCheck the full map at: http://powiatwarbot.xyz/.'.format(message, info)
    log_info(info)

    #=== Plotting both maps ===

    cmap = plt.get_cmap('tab20')
    font_dict = {"fontfamily": "ARIAL" if os.name == "posix" else "arial", 'fontsize': 24, "fontweight": "bold"}
    path_effects = [patheffects.Stroke(linewidth=3, foreground='black'), patheffects.Normal()]
    texts = []
    fig, ax = plt.subplots(figsize = (20,20))
    conquering_powiat_owner_row = conquering_powiat_owner_row.set_geometry('geometry')
    conquering_powiat_row = conquering_powiat_row.set_geometry('geometry')

    #get bbox for the detailed map
    conquering_powiat_centroid = conquering_powiat_row['powiat_shape'].iloc[0].centroid
    x_limit = (conquering_powiat_centroid.x - 70000, conquering_powiat_centroid.x + 70000)
    y_limit = (conquering_powiat_centroid.y - 70000, conquering_powiat_centroid.y + 70000)
    ax.clear()
    ax.set_axis_off()
    ax.set_aspect('equal')
    powiaty_ammount = {}

    #every powiat has to be plotted separately, otherwise it would have a color from a normalized color map
    for i in range(len(powiaty)):
        row = powiaty.loc[[i],]
        row_code = row['code'].iloc[0]
        row_belongs_to = row['belongs_to'].iloc[0]

        powiaty_ammount[row_belongs_to] = powiaty_ammount.setdefault(row_belongs_to, 0) + 1

        if (not powiaty[powiaty['belongs_to'] == row_code].empty):
            row.plot(ax = ax, color = cmap((row['value'] - 1)/20), edgecolor = 'k', linewidth = 0.4)

    powiaty = powiaty.set_geometry('powiat_shape')
    powiaty.plot(ax = ax, color = 'none', dashes = ':', edgecolor = 'k', linewidth = 0.3)

    if (not all_rows_for_conquering_powiat_owner.empty):
        conquering_powiat_owner_row.plot(ax = ax, color = cmap((conquering_powiat_owner_value - 1)/20), edgecolor='#4a4a4a', hatch='///')
        conquering_powiat_owner_row.plot(ax = ax, color = 'none', edgecolor = '#262626', linewidth = 3)
        to_conquer_owner_text = plt.text(s = conquering_powiat_owner_name, x = conquering_powiat_owner_row['geometry'].iloc[0].centroid.x, y = conquering_powiat_owner_row['geometry'].iloc[0].centroid.y, fontdict = font_dict, clip_on=True)
        to_conquer_owner_text.set_color('#7a7a7a')
        texts.append(to_conquer_owner_text)

    conquering_powiat_row.plot(ax = ax, color = cmap((conquering_powiat_value - 1)/20), edgecolor = '#73e600', linewidth = 3)
    conquering_text = plt.text(s = conquering_powiat_name, x = conquering_powiat_row['geometry'].iloc[0].centroid.x, y = conquering_powiat_row['geometry'].iloc[0].centroid.y, fontdict = font_dict, clip_on=True)
    conquering_text.set_color('#9DFF9C')
    texts.append(conquering_text)

    for text in texts:
        text.set_path_effects(path_effects)

    adjust_text(texts, only_move = {'points': 'y', 'texts': 'y'}, va = 'center', autoalign = 'y')
    plt.savefig('maps/{}.png'.format(date), transparent = True)
    plt.savefig('overall-map.png', transparent = True)
    
    conquering_text.set_position((conquering_powiat_row['geometry'].iloc[0].centroid.x, conquering_powiat_row['geometry'].iloc[0].centroid.y))

    if (not all_rows_for_conquering_powiat_owner.empty):
        to_conquer_owner_text.set_position((conquering_powiat_owner_row['geometry'].iloc[0].centroid.x, conquering_powiat_owner_row['geometry'].iloc[0].centroid.y))

    #set bbox for detailed map
    ax.set_xlim(x_limit)
    ax.set_ylim(y_limit)

    contextily.add_basemap(ax, zoom=10, source="https://api.mapbox.com/styles/v1/kolorowytoster/ckn0rhk6b1er317pe7kg5jkgl/tiles/256/{z}/{x}/{y}@2x?access_token=" + mapbox)
    plt.savefig('detail-map.png', transparent = True)
    
    #finally, update geometry for conquering conquered powiat
    powiaty = powiaty.set_geometry('geometry')
    powiaty = powiaty.drop(columns = 'powiat_shape')
    powiaty.to_file('map-data/powiaty.shp', encoding = 'utf-8')
    
    with open('map-data/status.txt', 'w') as f:
        f.write('{}\n'.format(powiaty_left))
        f.write('{}\n'.format(conquering_powiat_code))
        f.write('{}\n'.format(date + 1))

    return message, powiaty_left, powiaty_ammount