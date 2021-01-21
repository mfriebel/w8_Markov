import numpy as np
import pandas as pd
from data_exploration import load_data


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

data = load_data()
transition_mat = create_probability_matrix(data)

class Customer:
    """
    Class representing a customer
    """
    def __init__(self, id, state, transition_mat):
        self.id = id
        self.state = state
        self.transition_mat = transition_mat

    def __repr__(self):
        """
        Returns a csv string for that customer.
        """
        return f"--Customer {self.id} is in {self.state}"

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

def customers_states(customer):
    initial_state = np.random.choice(transition_mat.index)
    c = Customer(customer, initial_state, transition_mat)
    print(f"customer {customer} initial state: {initial_state}")
    while c.is_active() is True:
        c.next_state()
        print(c)
    print("The customer left the supermarket")