import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# Create the hour data
outdoor_temp = pd.read_csv('heatwave_temps.csv')
outdoor_temp = outdoor_temp["temperature"]
hours = np.arange(24)
t_fine = np.arange(0,24, 1/60)
T_out_interp = np.interp(t_fine, hours, outdoor_temp)
outdoor_temp = T_out_interp


# Simulation parameters
dt = 60 # Time step (s)
duration = 24 * 3600 #24 hours x 3600 seconds
n_steps = len(outdoor_temp)


# Building params
C = 5*10**5 # Thermal Capacitance
R = 0.002 # Thermal Resistance
T_out = outdoor_temp
Q_solar = 100
Q_internal = 300

# Initial conditions
T_in = np.zeros(n_steps)
T_in[0] = 22 # Initial indoor temperature

# Euler method to solve HBE 
for i in range(0, n_steps):

    dT_dt = (T_out[i] - T_in[i-1]) / R + Q_solar + Q_internal

    T_in[i] = T_in[i-1] + (dT_dt / C) * dt


# Plot results
plt.figure(figsize=(10, 5))
plt.plot(np.arange(n_steps) / 3600, T_in, label='Indoor Temperature', color='r')
plt.plot(np.arange(n_steps) / 3600, T_out, label='Outdoor Temperature', color='b', linestyle='dashed')
plt.xlabel('Time (hours)')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.title('Predicted Indoor Temperature over 24h')
plt.show()
