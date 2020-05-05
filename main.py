from turn import play_turn
from PIL import Image
import facebook

i = 0
while i < 5:
    try:
        post_message, powiaty_left = play_turn()
        i = 10
    except Exception as e:
        i += 1
        print('An error {} occured, trying again [{}/{}].'.format(e, i, 5))
        if (i == 5):
            quit()

i = 0
while i < 5:
    try:
        was_posted = False

        if (not was_posted):
            image = Image.open('overall-map.png')
            bbox = image.getbbox()
            image = image.crop(bbox)
            image.save('overall-map.png')
            image = Image.open('detail-map.png')
            bbox = image.getbbox()
            image = image.crop(bbox)
            image.save('detail-map.png')

            with open('api-key.txt', 'r') as f:
                api_key = f.readline()

            facebook = facebook.GraphAPI(access_token = api_key)
            post_response = facebook.put_photo(image = open('overall-map.png', 'rb'), message = post_message)

        was_posted = True
        post_id = post_response['post_id']
        image_response = facebook.put_photo(image = open('detailed-map.png', 'rb'), no_story = True, published = False)
        photo_id = image_response['id']
        facebook.put_object(parent_object = post_id, connection_name = 'comments', attachment_id = photo_id)

        i = 10
    except Exception as e:
        i += 1
        print('An error {} occured, trying again [{}/{}].'.format(e, i, 5))
        if (i == 5):
            quit()
