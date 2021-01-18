import numpy as np
import pandas as pd

PATH = "./data/"

# Data import
def get_data(path, file):
    df = pd.read_csv(path+file, sep=';', index_col=0, parse_dates=True)

    return df

monday = get_data(PATH, 'monday.csv')

# duplicates
duplicates = monday[monday.duplicated()]
no_duplicates = monday[monday.duplicated() == False]

# Calculate the total number of customers in the supermarket over time. - Matthias
# Reduce to only one section per customer

def total_number_over_time(df):

    customer_only = df[df['customer_no'].duplicated() == False]
    time_step = customer_only.index.hour
    return customer_only.groupby([time_step])[['customer_no']].count()

print(total_number_over_time(monday))
