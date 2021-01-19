""" EDA """

import pandas as pd
import numpy as np
import re

# Import data

DATA_FOLDER = "./data/"
TIMESTEP = "1T"

def import_data(file, data_folder):
    df = pd.read_csv(data_folder + file, sep = ";", parse_dates = True, index_col = 0)
    df["customer_no"] = re.findall(r"^\w+", file)[0] + df["customer_no"].astype("string")
    return(df)

def unique_customers(df):
    mask = df["customer_no"].duplicated() == False
    return(df[mask][["customer_no"]])
    
monday = import_data("monday.csv", DATA_FOLDER)
tuesday = import_data("tuesday.csv", DATA_FOLDER)
wednesday = import_data("wednesday.csv", DATA_FOLDER)
thursday = import_data("thursday.csv", DATA_FOLDER)
friday = import_data("friday.csv", DATA_FOLDER)

data = monday.append(tuesday).append(wednesday).append(thursday).append(friday)

# Make pivot data frame

data_customer_centric = data.pivot(columns = "customer_no")

data_customer_centric = data_customer_centric.fillna(method = 'ffill', axis = 0) + (data_customer_centric.fillna(method = 'bfill', axis = 0) * 0) # from https://stackoverflow.com/questions/28136663/using-pandas-to-fill-gaps-only-and-not-nans-on-the-ends


# Some basic data understanding
data.shape
data.info()
data.head()
data.index.weekday.value_counts()


# Calculate the total number of customers in each section

monday.groupby(["location"]).size() # not unique customers
monday[monday.duplicated() == False].groupby("location").size() # unique customers


# Calculate the total number of customers in each section over time

data.groupby([data.index, "location"]).size()
# Do it over hour and remove duplicates


# Display the number of customers at checkout over time

monday[monday["location"] == "checkout"]["customer_no"].resample(TIMESTEP).size()


# Calculate the time each customer spent in the market

data_customer_centric.notna().sum(axis = 0)

data.index.max()
def minmax(df):
    return df.index.max() - df.index.min()

data.groupby("customer_no").agg(minmax)


# Calculate the total number of customers in the supermarket over time

data_customer_centric.notna().sum(axis = 1)

unique_customers(monday).resample(TIMESTEP).size()

    
# Our business managers think that the first section customers visit follows a different pattern than the following ones. Plot the distribution of customers of their first visited section versus following sections (treat all sections visited after the first as “following”).

# ! missing


# Estimate the total revenue for a customer using the following table:
    # fruit: 4€
    # spices: 3€
    # dairy: 5€
    # drinks: 6€
    
table_locations = pd.crosstab(data["customer_no"], data["location"])
table_locations["dairy"] = table_locations["dairy"].apply(lambda x: x * 5)
table_locations["spices"] = table_locations["spices"].apply(lambda x: x * 3)
table_locations["fruit"] = table_locations["fruit"].apply(lambda x: x * 4)
table_locations["drinks"] = table_locations["drinks"].apply(lambda x: x * 6)