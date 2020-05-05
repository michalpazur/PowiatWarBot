from main import play_turn

try:
    for i in range(100):
        play_turn()
finally:
    with open('map-data/status.txt', 'w') as f:
        f.write('{}\n'.format(334))
        f.write('0')