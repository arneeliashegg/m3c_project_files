import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

"""
This file takes population data sourced from https://worldpopulationreview.com/cities/united-kingdom/birmingham
and uses a model made in GeoGebra with regression, cubic polynomial.
It then uses said model to extrapolate population data until 2045.
The data is then saved into a .csv file called extrap_population.csv
"""

def addyears(noyears: int, years):
    """
    This function creates a nice list of years, e.g. [2020,2021,2023,etc...] based on a list of
    numbers which are the amount of years from 1950. 
    It takes the years from the original data and adds on a certain amount of years (parameter=noyears)
    and returns them in a Pandas.pandas.series.series object.
    """
    year_i = years.index[::-1]
    years.index = year_i

    startyear = years.iloc[-1]

    new_years = []
    
    for i in range(years[74], years[74]+noyears):
        if i == 2024:
            continue

        new_years.append(i)

    return np.concatenate((years.iloc[::-1], new_years))

# Create a model
def model(x):
    """ 
    This cubic polynomial is used to extrapolate population data for Birmingham 
    It was found using GeoGebra's polynomial regression tool. The data used for that is the original
    sample data for birminghams population found at https://worldpopulationreview.com/cities/united-kingdom/birmingham
    """
    return int(7.1*x**3 - 673.57*x**2 + 17942.6*x+2157920.2)

def population_f(nayears: int):
    """
    The main function of this file.
    Takes in population data from https://worldpopulationreview.com/cities/united-kingdom/birmingham
    Returns a pandas DataFrame object with original + extrapolated population numbers
    """
    # Load population data
    df = pd.read_csv("q2/pop.csv")
    years = df["year"]

    # This series has the years from the original data + the years which are extrapolated.abs
    # The reason we do this is to be able to tell not only what year since 1950 it has been,
    # but also which year it actually was.
    niceyears = addyears(nayears+1, years)

    og_years = years

    # Reverse the population list
    pop = df["population"].iloc[::-1]

    # Reversed list of index of years // Years since 1950
    years_n = list(range(len(years)))

    new_df = pd.DataFrame({
        "year": years_n,
        "population": pop
    })

    # Extrapolate
    ## Create a list of the new next years
    new_years = [new_df["year"][0]]
    for n,i in enumerate(range(1,nayears+1)):
        if n == 0:
            continue 

        new_years.append(new_years[0]+i)

    # Combine the lists of years since 1950
    years = np.concatenate((new_df["year"], new_years))

    # Generate the extrapolated population data
    newpop = []
    for y in years:
        newpop = np.append(newpop, model(y))
    
    # Returns a DataFrame with three variables
    return pd.DataFrame({
        'year': niceyears,      # The actual years (2002, 2003, etc.)
        "nyear": years,         # number of years since 1950. Used for the model
        "population": newpop    # Estimated population
    })

# NewDataFrame - simply, where the generated population data ends up.
ndf = population_f(nayears=21)

# Plotting is optional
"""
plt.plot('nyear', 'population', data=ndf)

plt.show()
"""

# Saves the generated population data to extrap_population.csv
# Contents of this file is a concatenation of the original data 
# from M3C and our own generated data.
ndf.to_csv('extrap_population.csv')