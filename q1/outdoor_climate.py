import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. load the data
heatwave_data = pd.read_csv("heatwave_temps.csv")

# 2. Specify which columns to use
columns = ["time","temperature", "dew point", "humidity", "wind speed"]

# 3. Create the pairplot
#sns.pairplot(heatwave_data[columns], diag_kind='hist', corner=False)

# Create a heatmap showing correlation
sns.heatmap(heatwave_data.corr(), linecolor = 'white', linewidths = 1, annot = True ) 


plt.show()