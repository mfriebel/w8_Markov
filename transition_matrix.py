import os
import pandas as pd
import numpy as np
from functools import reduce
import re


#def import_data(file):
  #  """Import data"""
   
    #monday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/monday.csv', sep = ";", parse_dates = True)
    #tuesday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/tuesday.csv', sep = ";", parse_dates = True)
    #wednesday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/wednesday.csv', sep = ";", parse_dates = True)
    #thursday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/thursday.csv', sep = ";", parse_dates = True)
    #friday = pd.read_csv('/mnt/c/users/noram/Documents/Coding/SpicedAcademy/week08/data/friday.csv', sep = ";", parse_dates = True)
    
    #day_of_week = 
   # df = monday.append(tuesday).append(wednesday).append(thursday).append(friday)
  #  df["customer_no"] = re.findall(r"^\w+", file)[0] + df["customer_no"].astype("string")
  #  return(df)

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
df["customer_no"] = df['day_of_week'] + df["customer_no"]#.astype("string")

# Create Probability matrix

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


prob_matrix = create_probability_matrix(df)

# Get initial state

def get_initial_state(prob_matrix, location):
    """Generate an initial state vector
    Args:
        prob_matrix (DataFrame): Probability matrix for supermarket customers
        location (str): Location in the supermarket to start with
    Returns:
        np.array: Initial state vector
    """
    
    out = np.zeros(len(prob_matrix.index))
    pos = [i for i, loc in enumerate(prob_matrix.index) if loc == location]
    out[pos] = 1
    
    return out

initial_state = get_initial_state(prob_matrix, "fruit")

# Propagate probabilities
    
def propagate(initial_state, prob_matrix, nr_steps):
    """Get probabilities for given initial state after a number of steps
    Args:
        initial_state (np.array): Initial state of a customer in the supermarket
        prob_matrix (DataFrame): Probability matrix for supermarket
        nr_steps (int): Nr of steps to calculate
    Returns:
        np.array: Probabilities for locations
    """
    
    result = initial_state
    for _ in range(nr_steps):
        result = result.dot(prob_matrix)
        
    return result
    
propagate(initial_state, prob_matrix, 200)

# Entrance probability of customers into the market per day
# Idea is to create the "outside" of the market as a reservoir (node) with a specific probability (per time) that people enter the market
# * This could also be calculated per hour (this likely differs over the day)
df.set_index('timestamp', inplace=True)
nr_unique_customers = len(df["customer_no"].unique())
opening_minutes_per_day = (df.index.hour.max()-df.index.hour.min()) * 60
customers_per_minute = nr_unique_customers / opening_minutes_per_day
entrance_probability_per_minute = customers_per_minute / nr_unique_customers


# Initial probability matrix on entrance

#df[df["customer_no"].duplicated() == False][["location"]].value_counts(normalize = True)