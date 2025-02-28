import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

tempdata = pd.read_csv('q2/max_annual_temp_bh.csv')

# Scatterplots
sns.pairplot(tempdata, diag_kind='hist', corner=False)

# Show the linear correlations
#sns.heatmap(tempdata.corr(), linecolor = 'white', linewidths = 1, annot = True ) 

plt.show()