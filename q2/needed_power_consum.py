import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

"""
All we need to do here is to load in the summer_power consumption and
divide it by efficiency in order to know how much power is needed!
"""

# Justification can be found in main document
efficiency = 0.637

# Load the data
# Data generated previously
summer_data = pd.read_csv("summer_power_consumption.csv")

years = summer_data["year"]
power_values = summer_data["summer_power_consumption"]

# Calculate everything
needed_summer_power = []
for i,n in enumerate(power_values): # Enumerate is technically redundant 
                                    # in this case, but could be handy 
                                    # in case additions were to be made 
                                    # to the code.
    needed_summer_power.append(n/efficiency)

# create the final dataframe
needed_power_df = pd.DataFrame({
    'year': years,
    'needed-power': needed_summer_power
})

# Saves the generated DataFrame object as needed_power.csv
# Contents of this file is only our own generated data.
needed_power_df.to_csv('needed_power.csv')

# Plotting is optional
"""
plt.scatter('year', 'needed-power', data=needed_power_df)
plt.show()
"""