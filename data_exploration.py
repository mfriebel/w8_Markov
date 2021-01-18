import pandas as pd
import numpy as np
import os


# Load the data

try:
    path = './data'
    data = pd.DataFrame()
    for file in os.listdir(path):
        data = pd.read_csv(os.path.join(path, file), sep=';')
        data['timestamp'] = pd.to_datetime(data['timestamp'], format="%Y-%m-%d %H:%M:%S")
except:
    pass


# Calculate the total number of customers in each section
def customer_section(data):
    df_section = data.sort_values(by=['location'])
    df_section = data.groupby(['location']).mean()
    return df_section

print(customer_section(data))

# Calculate the total number of customers in each section over time


# Display the number of customers at checkout over time


# Calculate the time each customer spent in the market


# Calculate the total number of customers in the supermarket over time.

