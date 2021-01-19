""" Create transition matrix """

from os import initgroups
import pandas as pd
import numpy as np
import re

# Import data

DATA_FOLDER = "./data/"

def import_data(file, data_folder):
    """Import data"""
    df = pd.read_csv(data_folder + file, sep = ";", parse_dates = True, index_col = 0)
    df["customer_no"] = re.findall(r"^\w+", file)[0] + df["customer_no"].astype("string")
    return(df)
    
monday = import_data("monday.csv", DATA_FOLDER)
tuesday = import_data("tuesday.csv", DATA_FOLDER)
wednesday = import_data("wednesday.csv", DATA_FOLDER)
thursday = import_data("thursday.csv", DATA_FOLDER)
friday = import_data("friday.csv", DATA_FOLDER)


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

prob_matrix = create_probability_matrix(monday)

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

nr_unique_customers = len(monday["customer_no"].unique())
opening_minutes_per_day = (monday.index.hour.max()-monday.index.hour.min()) * 60
customers_per_minute = nr_unique_customers / opening_minutes_per_day
entrance_probability_per_minute = customers_per_minute / nr_unique_customers


# Initial probability matrix on entrance

monday[monday["customer_no"].duplicated() == False][["location"]].value_counts(normalize = True)