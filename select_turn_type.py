import random
from turn import play_turn
from independence_turn import play_independence_turn

def load_values():
    with open('map-data/status.txt', 'r') as f:
        powiaty_left = int(f.readline())
        last_powiat = f.readline().rstrip()

    return powiaty_left, last_powiat

def get_last_powiat_value(powiaty_left):
    x = 337 - powiaty_left
    return ((3.5 * 10**-6) * x**2) + 0.125

def get_biggest_powiat_value(powiaty_left):
    x = 337 - powiaty_left
    return 0.0075 * x - 1.9275

def select_turn_type():
    powiaty_left, last_powiat = load_values()

    if (last_powiat == '0'):
        return play_turn('regular')

    if (random.random() < 1/150):
        print('[INFO] Playing independence round.')
        return play_independence_turn()

    random_val = random.random()
    if (random_val < get_last_powiat_value(powiaty_left)):
        print('[INFO] Powiat conquering previously will be conquering.')
        return play_turn('last')

    return play_turn('regular')
