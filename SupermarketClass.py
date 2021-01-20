"""
Start with this to implement the supermarket simulator.
"""

import numpy as np
import pandas as pd


class Supermarket:
    """manages multiple Customers that are currently in the supermarket.
    """

    transition_probabilities = [#to be filled in]

    def __init__(self):        
        # a list of Customer objects
        self.customers = []
        self.minutes = 0
        self.last_id = 0

    def __repr__(self):
        pass

    def get_time():
        """current time in HH:MM format,
        """
        get_time = 

    def print_customers():
        """print all customers with the current time and id in CSV format.
        """
        self.total_customers
        print(f' At {datetime.now()} are {total_customers()} in the Supermarket')

        print(f'The time is {datetime.now()} and the amount of Customers currently in the Supermarket is{count(customers')

    def next_minute():
        """propagates all customers to the next state.
        """
        self.current_location = np.random.choice(\['spices','fruit','drinks','dairy'], transition_probabilities)

    
    def add_new_customers():
        """randomly creates new customers.
        """
        self.new_customer = np.random.choice(\['customers'])

    def remove_exitsting_customers():
        """removes every customer that is not active any more.
        """