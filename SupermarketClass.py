"""
Start with this to implement the supermarket simulator.
"""

import numpy as np
import pandas as pd
from transition_matrix import create_probability_matrix
import os
import csv




# Load the data


#monday = pd.read_csv ('C:\\Users\\noram\\Documents\\Coding\\SpicedAcademy\\week08\\data\\monday.csv', sep=';', parse_dates=True, index_col=0)
#tuesday = pd.read_csv ('C:\\Users\\noram\\Documents\\Coding\\SpicedAcademy\\week08\\data\\tuesday.csv', sep=';', parse_dates=True, index_col=0)
#wednesday = pd.read_csv ('C:\\Users\\noram\\Documents\\Coding\\SpicedAcademy\\week08\\data\\wednesday.csv', sep=';', parse_dates=True, index_col=0)
#thursday = pd.read_csv ('C:\\Users\\noram\\Documents\\Coding\\SpicedAcademy\\week08\\data\\thursday.csv', sep=';', parse_dates=True, index_col=0)
#friday = pd.read_csv ('C:\\Users\\noram\\Documents\\Coding\\SpicedAcademy\\week08\\data\\friday.csv', sep=';', parse_dates=True, index_col=0)

transition_mat = create_probability_matrix
p = transition_mat

class Customer:
    """
    Class representing a customer
    """
    def __init__(self, id, state, transition_mat):
        self.id = id
        self.state = state
        self.transition_mat = p

    def __repr__(self):
        """
        Returns a csv string for that customer.
        """
        return f"The customer with number {self.id} is in {self.state}"

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
        self.state = np.random.choice(transition_mat.index, p)


class Supermarket:
    """manages multiple Customers that are currently in the supermarket.
    """

    def __init__(self,customer, minutes, last_id, history, time):        
        # a list of Customer objects
        self.customers = []
        self.minutes = 0
        self.last_id = 0
        self.history = []
        self.time = 1

    def __repr__(self):
        pass

    def get_time():
        """current time in HH:MM format,
        """
        if self.time == 21:00
            return False
        else:
            return True
        print(f' The current time is{time}) 

    def print_customers():
        """print all customers with the current time and id in CSV format.
        """
        datalist = ['Timestamp', 'Customer_id']
        with open('customers_at_supermarket.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter= ';')
            writer.writerows(data_list)
        

    def next_minute(self):
        """propagates all customers to the next state.
        """
        self.current_location = np.random.choice(\['spices','fruit','drinks','dairy'], transition_mat.index, p)
        self.history
    
    def add_new_customers(self):
        """randomly creates new customers.
        """
        self.new_customer = np.random.choice(transition_mat.index ,p)

    def remove_exitsting_customers(self):
        """removes every customer that is not active any more."""
        c = Customers
        if self.state == 'checkout'

for c in customers(50):
    if current_location == 'checkout'
        return False
    else:
        print(c.add_new_customer)

