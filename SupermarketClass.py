"""
This module defines the Supermarket class, which creates customers.
It writes a csv with customer_id and the time.
"""

import numpy as np
import pandas as pd
from transition_matrix import create_probability_matrix
from CustomerClass import Customer
import os
import csv



transition_mat = create_probability_matrix
p = transition_mat



class Supermarket:
    """manages multiple Customers that are currently in the supermarket."""

    def __init__(self,customer, minutes, last_id, history, time):        
        """ a list of Customer objects"""
        self.customers = []
        self.minutes = 0
        self.last_id = 0
        self.history = []
        self.time = 1

    def __repr__(self):
        pass

    def get_time(self):
        """current time in HH:MM format"""
        if self.time == 21:
            return False
        else:
            return True
        print(f' The current time is{self.time}') 

    def print_customers():
        """print all customers with the current time and id in CSV format."""
        data_list = ['Timestamp', 'Customer_id']
        with open('customers_at_supermarket.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter= ';')
            writer.writerows(data_list)
        

    def next_minute(self):
        """propagates all customers to the next state."""
        self.current_location = np.random.choice(transition_mat.index, p=transition_mat)
        self.history
    
    def add_new_customers(self):
        """randomly creates new customers."""
        self.customers.append(Customer())

    def remove_exitsting_customers(self):
        """removes every customer that is not active any more."""
        c = Customers
        if self.state == 'checkout':
            return False

customer_list = []

for i in range(5):
    c = Customer('id', 'state', 'transition_mat')
    customer_list.append(c)

for c in customer_list:
    c.next_state
    while c.is_active() is True:
        c.next_state
        if c.next_state == 'checkout':
            c.remove_existing_customers
    print(c.add_new_customer)

