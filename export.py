import geopandas, pandas, json
import matplotlib.pyplot as plt

def get_color_str(value):
    cmap = plt.get_cmap('tab20')
    value = (value - 1)/20
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

    with open('map-data/names.json', 'r', encoding = 'utf-8') as f:
        names = json.load(f)
    powiaty = geopandas.read_file('map-data/powiaty.shp', encoding = 'utf-8')
    powiaty_shapes = geopandas.read_file('map-data/powiaty-shapes.shp', encoding = 'utf-8')
    powiaty = powiaty.merge(powiaty_shapes, how = 'left', left_index = True, right_index = True)
    powiaty = powiaty.drop(columns = 'code_y')
    powiaty = powiaty.rename(columns = {'code_x': 'code', 'geometry_x': 'geometry', 'geometry_y': 'powiat_shape'})
    powiaty = powiaty.set_geometry('powiat_shape')
    powiaty = powiaty.assign(belongs_to_name = ['']*len(powiaty.index))

    for i, row in powiaty.iterrows():
        row_code = row['code']
        row_owner_code = row['belongs_to']
        row_owner_name = names[row_owner_code]
        row_color = get_color_str(row['value'])
        powiaty['belongs_to_name'][powiaty['code'] == row_code] = row_owner_name
        powiaty['value'][powiaty['code'] == row_code] = row_color
    
    powiaty = powiaty.drop(columns = ['geometry', 'powiat_shape'])
    powiaty = pandas.DataFrame(powiaty)
    powiaty = powiaty.set_index('code')
    with open('map-data/powiaty.json', 'w', encoding = 'utf-8') as f:
        f.write(powiaty.to_json(orient = 'index'))