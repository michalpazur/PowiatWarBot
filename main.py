from turn import play_turn
from PIL import Image
from log import log_info, log_error
from datetime import datetime
import facebook as fb
from export import create_map
import discord_bot as discord

i = 0
log_info('\n')
while i < 5:
    try:
        post_message, powiaty_left, powiaty_ammount, powiaty_names = play_turn()
        i = 10
    except Exception as e:
        i += 1
        log_error('An error {} occured, trying again [{}/{}].'.format(e, i, 5))
        if (i == 5):
            quit()

i = 0
while i < 5:
    try:
        was_posted = False

        if (not was_posted):
            image = Image.open('overall-map.png')
            bbox = image.convert('RGBa').getbbox()
            image = image.crop(bbox)
            image.save('overall-map.png')
            image = Image.open('detail-map.png')
            bbox = image.convert('RGBa').getbbox()
            image = image.crop(bbox)
            image.save('detail-map.png')

            with open('api-key.txt', 'r') as f:
                api_key = f.readline()

            facebook = fb.GraphAPI(access_token = api_key)
            post_response = facebook.put_photo(image = open('overall-map.png', 'rb'), message = post_message)
            discord.SendMessageToAll(post_message, open('overall-map.png', 'rb'))

        was_posted = True
        post_id = post_response['post_id']
        log_info('Post was created at {} with id {}'.format(datetime.now(), post_id))
        image_response = facebook.put_photo(image = open('detail-map.png', 'rb'), no_story = True, published = False)
        photo_id = image_response['id']

        items_to_sort = [(v, k) for (k, v) in zip(powiaty_ammount.keys(), powiaty_ammount.values())]
        items_to_sort.sort(reverse = True)
        message = 'Top 10 powiaty by number of controlled territories:'
        for j in range(10):
            powiat_name = powiaty_names[items_to_sort[j][1]]
            message = '{}\n{}: {}'.format(message, powiat_name, items_to_sort[j][0])

        comment_response = facebook.put_object(parent_object = post_id, message = message, connection_name = 'comments', attachment_id = photo_id)
        comment_id = comment_response['id']
        facebook.put_comment(comment_id, 'prawmapopodobnie')

        i = 10
    except Exception as e:
        i += 1
        log_error('An error {} occured, trying again [{}/{}].'.format(e, i, 5))
        if (i == 5):
            quit()

create_map()