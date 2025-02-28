import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression

"""
Will generate extrapolated data of non-domestic 
power consumption in Birmingham based on previous years.
"""

def generate_nice_years(nyears, startyear):
    """
    Returns a list of 'nice' years, i.e. years like 2002, 2003 instead of the 
    amount of years (nyears) since a given pivot. In this case it is 2012
    """
    niceyears = []
    for y in nyears:
        niceyears.append(startyear+y[0])

    return niceyears

# 
def flip_series_index(series):
    """
    Flips the indexes of a Pandas.pandas.series.series object.
    Useful in order to use data how we want it to behave.
    """
    series_i = series.index[::-1]
    series.index = series_i

    return series

# nondom_consum means non-domestic consumption
def nondom_consum(nayears: int):
    """
    main function of this file.
    1) loads and selects needed data
    2) manipulates data, indexes, etc. in order to make it nice to work with
    3) 
    """

    # Load dataset
    ed = pd.read_csv("q2/bh_elec_consum.csv") # This is the original dataset from M3C on Birminghams electrical consumption statistics

    ## Select needed data
    undom_elec = ed['non-domestic_consumption'].iloc[::-1] # We are only dealing with non-domestic consumption in this case

    # Gets and flips the indexes of years. 
    # This way, 2022 is the last datapoint in the set instead of the first.
    years = flip_series_index(ed['year'])
    
    # Create a number of years (since 2012) list
    nyears = np.array(list(range(len(years))))[:, np.newaxis]

    # Create a linear model
    model = LinearRegression()
    # Fit the model to the data
    model.fit(nyears, undom_elec)
    ## Describe model coefficient and intercept
    print(f"Coefficient: {model.coef_} Intercept: {model.intercept_}")

    # Generate extrapolations for the model
    x_pred = np.array(list(range(len(years), len(years) + int(nayears))))[:,np.newaxis] # newaxis added because the model needs a 2D array for x.
    y_pred = model.predict(x_pred)

    # Combine the new power data with the original data
    all_non_domestic_consumption = np.concatenate((undom_elec, y_pred))
    # Add the new years since 2012 with the old years since 2012 in one big series
    all_nyears = np.concatenate((nyears, x_pred))

    ## Make some nice years i.e. 2002, 2003, etc. from the number of years since 2012
    niceyears = generate_nice_years(all_nyears, years.iloc[-1])

    # Return the final DataFrame
    return pd.DataFrame({
        'year': niceyears, # 'human readable' years
        'nyear': all_nyears.ravel(), # years since 2012. .ravel() in order to remove 2-dimensionality from the array.
        'non-domestic_consumption': all_non_domestic_consumption.ravel() # Original and generated non-domestic electrical consumption data. .ravel() in order to remove 2-dimensionality from the array.
    })

# Make the dataframe
df = nondom_consum(23)

# Saves the generated population data to non-domestic_power_consumption.csv
# Contents of this file is a concatenation of the original data 
# from M3C and our own generated data.
df.to_csv('non-domestic_power_consumption.csv')