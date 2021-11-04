from turn import play_turn
from PIL import Image
from log import log_info, log_error
from datetime import datetime
import facebook as fb
from export import create_map
from select_turn_type import select_turn_type
import json
import twitter

i = 0
while i < 5:
    try:
        post_message, powiaty_left, powiaty_ammount = select_turn_type()
        i = 10
    except Exception as e:
        i += 1
        log_error('An error {} occured, trying again [{}/{}].'.format(e, i, 5))
        if (i == 5):
            quit()

basemap = Image.open("basemap.png")
shadow = Image.open("shadow.png")
poland = Image.open("overall-map.png")
basemap = Image.alpha_composite(basemap, shadow)
basemap = Image.alpha_composite(basemap, poland)
basemap = basemap.crop(basemap.convert("RGBa").getbbox())
basemap.save("map.png")

image = Image.open('detail-map.png')
bbox = image.convert('RGBa').getbbox()
image = image.crop(bbox)
image.save('detail-map.png')

i = 0
while i < 5:
    try:
        was_posted = False

        if (not was_posted):
            with open('api-key.txt', 'r') as f:
                api_key = f.readline().rstrip()
                consumer_key = f.readline().rstrip()
                consumer_secret = f.readline().rstrip()
                access_token = f.readline().rstrip()
                access_token_secret = f.readline().rstrip()

            facebook = fb.GraphAPI(access_token = api_key)
            twitter_api = twitter.Api(consumer_key, consumer_secret, access_token, access_token_secret)
            post_response = facebook.put_photo(image = open('map.png', 'rb'), message = post_message)
            twitter_post_respone = twitter_api.PostUpdate(post_message, media=open('map.png', 'rb'))

        was_posted = True
        post_id = post_response['post_id']
        log_info('Post was created at {} with id {}'.format(datetime.now(), post_id))
        image_response = facebook.put_photo(image = open('detail-map.png', 'rb'), no_story = True, published = False)
        photo_id = image_response['id']

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

        comment_response = facebook.put_object(parent_object = post_id, message = message, connection_name = 'comments', attachment_id = photo_id)
        comment_id = comment_response['id']
        facebook.put_comment(comment_id, 'prawmapopodobnie')
        facebook.put_comment(post_id, "Also check out the Twitter version of the bot: https://twitter.com/powiatwarbot")

        with open('map-data/status.txt', 'a') as f:
            f.write('{}'.format(items_to_sort[0][1]))
            
        i = 10
    except Exception as e:
        i += 1
        log_error('An error {} occured, trying again [{}/{}].'.format(e, i, 5))
        if (i == 5):
            quit()

create_map()