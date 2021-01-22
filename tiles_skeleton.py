import time
import os
import pandas as pd
import numpy as np
import cv2

TILE_SIZE = 32
OFS = 50
supermarket_aisles = {"fruit" : {'xpos' : [14, 15], 'ypos' : [2, 3, 4, 5, 6]},
                        "spices" : {'xpos' : [11, 12], 'ypos' : [2, 3, 4, 5, 6]},
                        "dairy" : {'xpos' : [6, 7], 'ypos' : [2, 3, 4, 5, 6]},
                        "drinks" : {'xpos' : [2, 3], 'ypos' : [2, 3, 4, 5, 6]},
                        "checkout" : {'xpos' : [2, 3, 6, 7, 10, 11], 'ypos' : [8, 9]},
                        "entrance" : {'xpos' : [14, 15], 'ypos' : [7, 8,9,10]} 
                    }

MARKET = """
##################
##..............##
##..##..##..##..##
##..##..##..#b..b#
##..##..##..##..##
##..##..##..##..##
##..##..##..#b..##
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
#############MGGM#
""".strip()


# Data load from Wail
def load_data(path):
    data = pd.DataFrame()
    try:
        for file in os.listdir(path):
            df = pd.read_csv(os.path.join(path, file), sep=';')
            df['timestamp'] = pd.to_datetime(df['timestamp'],format="%Y-%m-%d %H:%M:%S")
            data = pd.concat([data, df])
    except:
        pass
    data = data.sort_values(by=['timestamp']).reset_index(drop=True)
    return data


# probability matrix implemented by Daniel..
def create_probability_matrix(df):
    """Create a probability matrix for the supermarket example
    Args:
        df (DataFrame): DataFrame containing the customer positions over time
    Returns:
        DataFrame: Probability matrix
    """
    
    df["go_to_next"] = df.groupby("customer_no")["location"].shift(-1)
    prob_matrix = pd.crosstab(df["location"], df["go_to_next"], normalize = 0)
    prob_matrix.loc["checkout"] = [1,0,0,0,0]
    
    return prob_matrix


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tile   : a numpy array containing the tile image
        """
        self.tiles = tiles
        self.contents = [list(row) for row in layout.split("\n")]
        self.xsize = len(self.contents[0])
        self.ysize = len(self.contents)
        self.image = np.zeros(
            (self.ysize * TILE_SIZE, self.xsize * TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.tiles[0:32, 0:32]
        elif char == "G":
            return self.tiles[7 * 32 : 8 * 32, 3 * 32 : 4 * 32]
        elif char == "C":
            return self.tiles[2 * 32 : 3 * 32, 8 * 32 : 9 * 32]
        elif char == "b":
            return self.tiles[0 * 32 : 1 * 32, 4 * 32 : 5 * 32]
        elif char == "M":
            return self.tiles[7 * 32 : 8 * 32, 2 * 32 : 3 * 32]
        else:
            return self.tiles[32:64, 64:96]

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                bm = self.get_tile(tile)
                self.image[
                    y * TILE_SIZE : (y + 1) * TILE_SIZE,
                    x * TILE_SIZE : (x + 1) * TILE_SIZE,
                ] = bm

    def draw(self, frame, offset=OFS):
        """
        draws the image into a frame
        offset pixels from the top left corner
        """
        frame[
            OFS : OFS + self.image.shape[0], OFS : OFS + self.image.shape[1]
        ] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)

# Customer Class from Wail merged with Matthias Customer Class from Vis
class Customer:
    """Draws an customer on the supermarket background"""
    def __init__(self, id, transition_mat, terrain_map, aisles, image):
        """
        terrain_map : SupermarketMap object
        image   : a numpy array containing the tile image of customer
        x : initial x position of the customer
        y : initial y position of the customer
        """
        self.id = id
        self.state = 'entrance'
        self.transition_mat = transition_mat
        self.terrain_map = terrain_map
        self.aisles = aisles
        self.image = image
        self.x = 15
        self.y = 10
        self.x_target = np.random.choice(self.aisles[self.state]['xpos'])
        self.y_target = np.random.choice(self.aisles[self.state]['ypos'])

    def __repr__(self):
        """
        Returns a csv string for that customer.
        """
        return f'{self.id}, {self.state}'

    def is_active(self):
        """
        Return the customer's active
        """
        if self.state == "checkout":
            return False
        else:
            return True
    
    def next_state(self):
        """
        randomly selects the customer's next location from self.transition_mat
        """
        self.state = np.random.choice(transition_mat.index, p=self.transition_mat.loc[self.state])
        self.x_target = np.random.choice(self.aisles[self.state]['xpos'])
        self.y_target = np.random.choice(self.aisles[self.state]['ypos'])

    def draw(self, frame):
        """Places customer image onto the background frame """
        xpos = OFS + self.x * TILE_SIZE
        ypos = OFS + self.y * TILE_SIZE
        frame[ypos: ypos+TILE_SIZE, xpos: xpos+TILE_SIZE] = self.image
        # overlay the Customer image / sprite onto the frame

    def move(self, direction):
        """Moves the customer by one tile to a given direction"""
        newx = self.x
        newy = self.y
        if direction == 'up':
            newy -= 1
        elif direction == 'down':
            newy += 1
        elif direction == 'left':
            newx -= 1
        elif direction == 'right':
            newx += 1
        else:
            raise KeyError

        if self.terrain_map.contents[newy][newx] == '.':
            # Customer can only move on '.' sections of the map
            self.x = newx
            self.y = newy

    def move_to_next_state(self):
        """Looks where the customer is and excutes 
        move until it is in the right aisle"""

        x_pos = self.x 
        y_pos = self.y
        target_x_pos = self.x_target
        target_y_pos = self.y_target
        next_aisle = self.aisles[self.state]
        print(x_pos, target_x_pos)
        print(y_pos, target_y_pos)
        
        #move vertically into aisle
        if self.state == 'entrance':
            if y_pos > 7:
                self.move('up')
            else:
                self.state = np.random.choice(intial_state_vector_index, p=intial_state_vector)
                self.x_target = np.random.choice(self.aisles[self.state]['xpos'])
                self.y_target = np.random.choice(self.aisles[self.state]['ypos'])
        elif (y_pos == target_y_pos) and (x_pos == target_x_pos):
            self.next_state()
        elif self.state == 'checkout':  #and x_pos < target_x_pos
            if y_pos == 10 and x_pos != 14:
                self.move('right')
            else:
                self.move('down') 
        elif (y_pos not in [1, 7]) and (x_pos != target_x_pos):
            # Customer not in lane and wrong aisle
            if y_pos > target_y_pos:
                self.move('up')
            else:
                self.move('down')
        elif (y_pos in [1, 7]) and (x_pos != target_x_pos):
            # Customer in lane, but not on aisle position
            if x_pos > target_x_pos:
                self.move('left')
            else:
                self.move('right')
        elif (y_pos in [1, 7]) and (x_pos == target_x_pos):
            # Customer in lane and on aisle position
            if y_pos > target_y_pos:
                self.move('up')
            else:
                self.move('down')
        else:
            # Customer not in lane and right aisle
            if y_pos > target_y_pos:
                self.move('up')
            else:
                self.move('down')
  
        
        
# Supermarket Class from Nora not pulled in yet
class Supermarket:
    ...

if __name__ == "__main__":

    data = load_data('./data/')
    transition_mat = create_probability_matrix(data)

    intial_state_vector = data[data["customer_no"].duplicated() == False][["location"]].value_counts(normalize = True)
    intial_state_vector_index = [element[0] for element in intial_state_vector.index]



    background = np.zeros((700, 1000, 3), np.uint8)
    tiles = cv2.imread("tiles.png")

    market = SupermarketMap(MARKET, tiles)
    
    # Select ghost tile from tiles
    image_customer = tiles[8 * 32 : 9 * 32, 1 * 32 : 2 * 32]
    # Initial x and y positions
    # Instantiate customer
    c = Customer(1, transition_mat, market, supermarket_aisles, image_customer)

    while True:
        # Creates the frame of the visualisation
        frame = background.copy()
        # Draws the market on the background frame
        market.draw(frame)
        # Draws the customer on the market
        c.draw(frame)
        
        cv2.imshow("frame", frame)

        c.move_to_next_state()
        
        time.sleep(0.5)
        print(c)
        key = chr(cv2.waitKey(1) & 0xFF)
        
        # Lets customer move by key
        if key == 'w':
            c.move('up')
        if key == 's':
            c.move('down')
        if key == 'a':
            c.move('left')
        if key == 'd':
            c.move('right')
        if key == "q":
            break

    cv2.destroyAllWindows()

    market.write_image("supermarket.png")
