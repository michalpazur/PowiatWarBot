import folium, geopandas
import matplotlib.pyplot as plt

def get_color_str(value):
    cmap = plt.get_cmap('tab20')
    color = cmap(value)
    color_str = '#'
    for value in color[:-1]:
        value = int(value * 255)
        hex_str = hex(value)[2:]
        if (len(hex_str) == 1):
            hex_str = '0' + hex_str
        color_str += hex_str
    return color_str

def create_map():

    powiaty = geopandas.read_file('map-data/powiaty.shp', encoding = 'utf-8')
    powiaty = powiaty[powiaty.geometry.notnull()]
    powiaty = powiaty.to_crs('EPSG:4326')
    powiaty.geometry = powiaty.simplify(0.005)
    with open('map-data/powiaty.json', 'w', encoding = 'utf-8') as f:
        f.write(powiaty.to_json(na = 'null'))

    print('Saved powiaty.json!')
    m = folium.Map(location = [51.850984, 19.462806], zoom_start = 6.3, tiles = 'Stamen Terrain')

    highlight_style = lambda feature: dict(opacity = 1, weight = 4, color = 'limegreen')
    none_fill_style = lambda feature: dict(weight = 0, fillOpacity = 0)
    dashed_fill_style = lambda feature: dict(color = 'black', dashArray = '3 15', opacity = 1, fill = None, weight = 1)
    fill_style = lambda feature: dict(stroke = False, fillColor = get_color_str(feature['properties']['value']), fillOpacity = 1, weight = 1.5)

    powiaty_base = folium.GeoJson(
        'map-data/powiaty.json',
        name = 'powiaty_base',
        style_function = fill_style
    ).add_to(m)

    powiaty_borders = folium.GeoJson(
        'map-data/powiaty-shapes.json',
        name = 'powiaty_borders',
        style_function = dashed_fill_style
    ).add_to(m)

    powiaty_highlight = folium.GeoJson(
        'map-data/powiaty.json',
        name = 'powiaty_highlight',
        style_function = none_fill_style,
        highlight_function = highlight_style
    ).add_to(m)

    m.save('map.html')
    
create_map()