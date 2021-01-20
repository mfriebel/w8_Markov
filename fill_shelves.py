from PIL import Image
import numpy as np
import random

# Load sample image Supermarket
im_1 = Image.open('supermarket.png')
market = np.array(im_1)
# Load image with all possible tiles
im_2 = Image.open('tiles.png')
tiles = np.array(im_2)


def item(tuple):
    """Selects an item from tiles based on tuple (x, y) """
    x = tuple[0]
    y = tuple[1]
    return tiles[y:y+32, x:x+32]

def place_in_market(x, y, product, market_img):
    """Replaces the tile in the supermarket array with an product item"""
    tx = x * 32
    ty = y * 32
    market_img[ty:ty+32, tx:tx+32] = product

def populate_supermarket(section_list, items_list, market):
    """Replaces tiles beside our isles(in section_list) 
        with products of an item_list"""
    coordinates = list()
    for column in section_list[0]:
        for x in range(section_list[1][0], section_list[1][1]+1):
            coordinates.append((column, x))

    for tuple in coordinates:
        product = random.choice(items_list)
        place_in_market(tuple[0], tuple[1], product, market)

# Map all tiles into a dictionary, e.g. dict[row_column] = (x, y) 
tiles_dict = {}

for row in range(8):
    for column in range(15):
        y = row * 32
        x = column * 32 
        name = str(row)+'_'+str(column)
        tiles_dict[name] = item((x, y))

## Cutting out the products
#fruits
apple = tiles_dict['1_4']
strawberry = tiles_dict['1_5']
ananas = tiles_dict['5_4']
banana = tiles_dict['0_4']
cherry = tiles_dict['7_4']
# vegetables
aubergine = tiles_dict['1_11']
carrots = tiles_dict['2_11']
tomato = tiles_dict['3_5']
corn = tiles_dict['6_5']
peas = tiles_dict['1_4']
# dairy
eggs = tiles_dict['7_11']
icecream = tiles_dict['6_12']
cake = tiles_dict['5_6']
meat = tiles_dict['4_13']
# drinks
beer = tiles_dict['6_13']
wine = tiles_dict['4_9']
liquer = tiles_dict['3_13']
soft_drinks = tiles_dict['0_10']
# spices
salt = tiles_dict['7_13']
pepper = tiles_dict['6_9']
herbs = tiles_dict['5_9']
secret_spice = tiles_dict['3_9']

## Creating the isles and according product lists
# [Columns], [Start Row, End Row]
fruits_section = [[13, 16], [2, 6]]
fruits = [apple, carrots, strawberry, ananas, banana, cherry, aubergine, tomato, corn, peas]
drinks_section = [[1, 4], [2, 6]]
drinks = [beer, wine, liquer, soft_drinks]
spices_section = [[12, 9], [2, 6]]
spices = [salt, pepper, herbs, secret_spice]
dairy_section = [[5, 8], [2, 6]]
dairy = [eggs, icecream, cake, meat]

## Placing all the products into the market
populate_supermarket(fruits_section, fruits, market)
populate_supermarket(drinks_section, drinks, market)
populate_supermarket(spices_section, spices, market)
populate_supermarket(dairy_section, dairy, market)

# drawing the image
im_filled = Image.fromarray(market)
# Save as an png file
im_filled.save('supermarket_filled.png')