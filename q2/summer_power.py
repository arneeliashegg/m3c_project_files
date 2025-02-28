import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def summer_consum_f():
    # The percentage (22.373%) of annual power which is used in the months June-August
    summer_consumption = 0.22373

    ### LOAD ALL DATA! ###
    nondom_power_data = pd.read_csv('non-domestic_power_consumption.csv')
    population_data = pd.read_csv('extrap_population.csv')
    energy_per_person_data = pd.read_csv('energy_per_person.csv')

    # Then we need to get the total power every year until 2045
    ## Non domestic power:
    nondom_power = nondom_power_data['non-domestic_consumption']

    ## Domestic power: (energy per person * population)
    ### Load data to do calculations with
    energy_per_person = energy_per_person_data['energy_per_person']
    population = population_data['population']

    # These two arrays are being used in the Dataframe
    domestic_power_consumption = []
    relevant_years = []

    # These two variables are simply there to make the iterator function.
    begin = False
    index = 0
    for i,n in enumerate(population_data["year"]):
        # Checks if the lists are at the same year / point in time. 
        # So that data from 1967 is not accidentally combined with data from 2018.
        if n == energy_per_person_data['year'][0]:
            begin = True
        
        # Does the calculations
        if begin:
            domestic_power_consumption.append(population_data['population'][i] * energy_per_person[index])
            relevant_years.append(energy_per_person_data['year'][index])
            index += 1
    
    ## Now we must add it all up!
    # Takes domestic power + non-domestic power
    all_power = []
    for i,n in enumerate(nondom_power):
        all_power.append(summer_consumption * (n + domestic_power_consumption[i]))
    
    # Returns a Dataframe
    return pd.DataFrame({
        'year': relevant_years, # This dataframe only has 'nice' years like 2002, 2003, etc.
        'summer_power_consumption': all_power # The kWh consumed in summer
    })

# Generate the dataframe
summer_df = summer_consum_f()

# Plotting is optional
"""
plt.scatter('year', 'summer_power_consumption', data=summer_df)
plt.show()
"""

# Saves the data frame to summer_power_consumption.csv
## All data in this file is our own.
summer_df.to_csv("summer_power_consumption.csv")