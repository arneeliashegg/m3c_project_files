import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
population_data = pd.read_csv("extrap_population.csv")
energy_consumption = pd.read_csv("domestic_energy_consumption20yrs.csv")

# These are variables used for iterating over the arrays.
# As they are different lengths it is important to know which datapoints
# correspond to which years and match them effectively.
energy_index = 0 # For the iterator
begin = False # For the iterator

# These are the output arrays that will be put into the DataFrame
energy_per_person = []  # Energy per person is domestic consumption / population
                        # for a given year.
relevant_years = []     # This array just takes a note of which years of 
                        # population_data & energy_consumption matched. Which years
                        # are being calculated for in the iterator below.
for n,i in enumerate(population_data["year"]):
    # If the current year in population_data matches the first year in energy_consumption
    # we can begin calculations. This ensures that we are using data for the same
    # year in both the dataframes.
    if i == energy_consumption["year"][0]:
        begin = True
        # Tells the user what year calculations begin
        print(f"{population_data['year'][n]} {energy_consumption['year'][0]}")

    # Once the arrays are synchronized
    if begin:
        current_year = energy_consumption['year'][energy_index]
        energy_pp = energy_consumption['domestic_consumption'][energy_index] / population_data['population'][n]
        energy_index += 1

        relevant_years.append(current_year)
        energy_per_person.append(energy_pp)

# Return the resulting DataFrame
energy_per_person = pd.DataFrame({
    'year': relevant_years,
    'energy_per_person': energy_per_person
})

# Saves the generated population data to energy_per_person.csv
# Contents of this file is our own generated data.
energy_per_person.to_csv("energy_per_person.csv")