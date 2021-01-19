import pandas as pd
import numpy as np
import os


# Load the data

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


# Calculate the total number of customers in each section

data = load_data(path = './data')

def customer_section(data):
    df_section = data.sort_values(by=['location'])
    df_section = data.groupby(['location']).mean()
    return df_section

# Calculate the total number of customers in each section over time

# by Day
def customer_section_by_day(data):
    df_section_by_day = data.sort_values(by=['location', 'timestamp'])
    df_section_by_day['day'] = df_section_by_day['timestamp'].dt.dayofweek
    df_section_by_day = df_section_by_day [['day','location','customer_no']]
    df_section_by_day = df_section_by_day.groupby(['day', 'location']).count()
    return df_section_by_day


# Calculate the total number of customers in each section over time

# by Hour
def customer_section_by_hour(data):
    df_section_by_hour = data.sort_values(by=['location', 'timestamp'])
    df_section_by_hour['hour'] = df_section_by_hour['timestamp'].dt.hour
    df_section_by_hour = df_section_by_hour [['hour','location','customer_no']]
    df_section_by_hour = df_section_by_hour.groupby(['hour', 'location']).count()
    return df_section_by_hour


# Display the number of customers at checkout over time

def customer_checkout_by_hour(data):
    df_checkout_by_hour = data.sort_values(by=['location', 'timestamp'])
    df_checkout_by_hour['hour'] = df_checkout_by_hour['timestamp'].dt.hour
    df_checkout_by_hour = df_checkout_by_hour [['hour','location','customer_no']]
    mask = df_checkout_by_hour['location'] == 'checkout'
    df_checkout_by_hour = df_checkout_by_hour[mask].groupby(['hour', 'location']).count()
    return df_checkout_by_hour


# Calculate the time each customer spent in the market


# Calculate the total number of customers in the supermarket over time.

