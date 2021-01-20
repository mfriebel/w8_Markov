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
        np.all(state.index.isin(transition_mat.index))
        self.id = id
        self.state = state
        self.transition_mat = transition_mat
        self.__set_initial_state__()
        self.current_location = self.__get_initial_state__()

    def __repr__(self):
        """
        Returns a csv string for that customer.
        """
        return f"The customer with number {self.id} is in {self.state}"
  
    def __set_initial_state__(self):
        """
        randomly selects an initial state from self.state
        """
        self.initial_state = np.random.choice(self.state.index,1,p=self.state)

    def __get_initial_state__(self):
        """
        Return the customer's initial state
        """
        return self.initial_state
    
    def is_active(self):
        """
        Return the customer's acti
        """
        if self.current_location == ("checkout"):
            return False
        else:
            return True

    def next_state(self):
        """
        randomly selects the customer's next location from self.transition_mat
        """
        self.state = np.random.choice(self.transition_mat.index, 1, p=self.transition_mat)   