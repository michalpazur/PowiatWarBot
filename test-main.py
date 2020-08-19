from select_turn_type import select_turn_type
from PIL import Image
from log import log_info, log_error
from datetime import datetime
import facebook as fb
from export import create_map
import json

powiaty_left = 9999
while powiaty_left > 1:
    post_message, powiaty_left, powiaty_ammount = select_turn_type()
    
    with open('map-data/names.json', encoding='utf-8') as f:
        powiaty_names = json.load(f)

    items_to_sort = [(v, k) for (k, v) in zip(powiaty_ammount.keys(), powiaty_ammount.values())]
    items_to_sort.sort(reverse = True)
    
    if (len(items_to_sort) > 10) :
        range_len = 10
    else:
        range_len = len(items_to_sort)
    
    message = 'Top {} powiaty by number of controlled territories:'.format(range_len)
    for j in range(range_len): 
        powiat_name = powiaty_names[items_to_sort[j][1]]
        message = '{}\n{}: {}'.format(message, powiat_name, items_to_sort[j][0])

    with open('count.csv', 'a') as f:
        f.write('{},{}\n'.format(items_to_sort[0][0], items_to_sort[1][0]))
    
    with open('map-data/status.txt', 'a') as f:
        f.write('{}'.format(items_to_sort[0][1]))
    print(message)
