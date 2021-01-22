"""
This module defines the Supermarket class, which creates customers.
It writes a csv with customer_id and the time.
"""

import numpy as np
import pandas as pd
from transition_matrix import create_probability_matrix, get_initial_state
from CustomerClass import Customer
import os
import csv

monday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/monday.csv', sep = ";", parse_dates = True)
tuesday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/tuesday.csv', sep = ";", parse_dates = True)
wednesday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/wednesday.csv', sep = ";", parse_dates = True)
thursday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/thursday.csv', sep = ";", parse_dates = True)
friday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/friday.csv', sep = ";", parse_dates = True)
print(friday)
df = monday.append(tuesday).append(wednesday).append(thursday).append(friday)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['day_of_week'] = df['timestamp'].dt.weekday
print(df)
df["customer_no"] = df['day_of_week'] + df["customer_no"]




class Supermarket:
    """manages multiple Customers that are currently in the supermarket."""

    def __init__(self,customer_list):        
        """ a list of Customer objects"""
        self.customers = customer_list
        self.minute = 0
        self.last_id = 0 
        self.history = []
        self.time = 0
      

    def __repr__(self):
        pass

    def get_time(self):
        """current time in HH:MM format"""
        hour = 7 + self.minute // 60
        minute = self.minute % 60
        if minute < 10:
            time = f'{hour:02}:{minute:02}'
        print(f' The current time is{self.time}') 
        return time

    def print_customers():
        """print all customers with the current time and id in CSV format."""
        data_list = ['Timestamp', 'Customer_id']
        with open('customers_at_supermarket.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter= ';')
            writer.writerows(data_list)
        

    def next_minute(self):
        """propagates all customers to the next state."""
        time = self.get_time()
        for customer in self.customers:
            if time =="21:00":
                customer.state = "checkout"
            else:
                customer.next_state
            #self.remove_exitsting_customers(Customer)
        self.minute + 1


    def add_new_customers(self):
        """randomly creates new customers.""" 
        if len(self.customers) < 5:
            self.customers.append(Customer())
            self.last_id += 1   
        print(f'a new customer has arrived')    

    def remove_existing_customers(self, customer):
        """removes every customer that is not active any more."""
        if customer.is_active() == False:
            self.customers.remove(customer)
            self.add_new_customers()
        print(f'a customer has left the Supermarket')


transition_mat = create_probability_matrix(df)

intial_state_vector = monday[monday["customer_no"].duplicated() == False][["location"]]
intial_state_vector = intial_state_vector['location'].value_counts(normalize=True)
intial_state_vector_index = [element[0] for element in intial_state_vector.index] # how to change this

customer_list = []


#customers_states(1)
for n in range(10):
    intial_state = np.random.choice(intial_state_vector_index, p=intial_state_vector)
    c = Customer('id','state','transition_mat')
    customer_list.append(c)

print(customer_list)
s = Supermarket(customer_list)
print(s.customers)
s.get_time()
s.next_minute()
s.add_new_customers()
s.remove_existing_customers(c)
