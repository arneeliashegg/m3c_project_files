import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression

def addyears(noyears: int, years):
    """
    This function creates a nice list of years, e.g. [2020,2021,2023,etc...] based on a list of
    numbers which are the amount of years from 2012.
    It takes the years from the original data and adds on a certain amount of years (parameter=noyears)
    and returns them in a Pandas.pandas.series.series object.
    """
    year_i = years.index[::-1]
    years.index = year_i

    startyear = years.iloc[-1]

    new_years = []
    
    for i in range(years[10], years[10]+noyears):
        if i == 2022:
            continue

        new_years.append(i)

    return np.concatenate((years.iloc[::-1], new_years))


def energy_model(nayears: int):
    """ 
    Main function of the file. Predicts the domestic energy consumption of Birmingham
    1) Loads data from q2/bh_elec_consum.csv (Birmingham Electrical Consumption)
    2) Parse and format the data in order to make it work with the code
    3) Train a linear regression model in order to predict what the domestic energy 
    consumption of Birmingham will be after n years after 2012.

        <-- Justification for a linear model --> 
        The population of Birmingham has been 
    steadily increasing since ~2002, and the domestic power consumption has at 
    the same time decreased in an approximately linear fashion.
    Assuming that the change in population for the next couple of years
    is approximately linear, the change in domestic electricity consumption
    can also be assumed to be changing approximately linearly.

    4) Generate data in order to extrapolate
    5) Extrapolate
    6) Return a DataFrame object

    """

    # Firstly we want to create a prediction for the domestic energy consumption
    ## Load the data
    energydata = pd.read_csv('q2/bh_elec_consum.csv')
    years = energydata['year']

    ## Make a list of the amount of years after 2012. i.e., [0,1,2] corresponds to [2012,2013,2014]
    ### newaxis required because the model needs a 2D array
    nyears = np.array(list(range(len(years))))[:, np.newaxis]

    ## Reverse the order of energy data so that the data begins in the past, instead of the present
    energy = energydata['domestic_consumption'].iloc[::-1]

    ## Make Model
    model = LinearRegression()
    ## Train Model
    model.fit(nyears, energy)

    ### Print characteristics of model (Coefficient + Intercept)
    print(f"Model intercept: {model.intercept_} Model Coefficient: {model.coef_}")

    ### Generate predictions
    x_pred = np.array(list(range(len(years), len(years) + int(nayears))))[:,np.newaxis]
    y_pred = model.predict(x_pred)

    ## This makes the real years (Human readable, i.e, [2030,2031,2032, etc.])
    true_years = addyears(nayears+1, years)

    ## Create a new dataframe with predictions
    return pd.DataFrame({
        'year': true_years, # Years like 2012, 2013
        'nyear': np.concatenate((nyears.ravel(), x_pred.ravel())), # Number of years since 2012
        'domestic_consumption': np.concatenate((energy, y_pred)) # Predicted domestic consumption of birmingham
    })

# The generated DataFrame object
mdf = energy_model(23)

# Saves the DataFrame in .csv format as domestic_energy_consumption20yrs.csv
# Contents of this file is a concatenation of the original data 
# from M3C and our own generated data.
mdf.to_csv("domestic_energy_consumption20yrs.csv")

# Plotting is optional
"""
plt.scatter("year", "domestic_consumption", color='blue', data=mdf)
plt.plot("year", "domestic_consumption", color='red', data=mdf)
plt.show()
"""