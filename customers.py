import numpy as np
from data_exploration import load_data
from transition_matrix import create_probability_matrix

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
        self.state = np.random.choice(transition_mat.index, p=self.transition_mat)