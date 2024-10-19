# -*- coding: utf-8 -*-
"""
Created on Thu May  9 17:10:48 2024

@author: eh64643
"""

#Assignment #9
# Question 2

import pandas as pd
import numpy as np

# Constants

Ω = (2 * np.pi) / 86164 #rad/s
g = 9.81  # Acceleration due to gravity
λ = 700000 #[m]
H =  4000 #[m] average depth of oceans
d = 14500000 #[m] the average width of Pacific Ocean_distance from west to east
# Create DataFrame for initial lattitudes
df0 = pd.DataFrame({'φ_deg': [0, -30,  60]})
df0['φ_rad'] = np.radians(df0['φ_deg'])
df0['y_m'] = df0['φ_deg'] *60* 1.852 * 1000  # converting degree to nautical mile and then meter
df0['f0'] = 2 * Ω* np.sin(df0['φ_rad'])

# Create DataFrame for 
df1 = pd.DataFrame({'φ_deg': [-0.1, -30.1,  60.1]})
df1['φ_rad'] = np.radians(df1['φ_deg'])
df1['y_m'] = df1['φ_deg'] *60* 1.852 * 1000  # [m] converting degree to nautical mile and then meter
df1['f0'] = 2 * Ω* np.sin(df1['φ_rad'])

Δf = df0['f0'] - df1['f0']
Δy = df0['y_m'] - df1['y_m']
β = Δf/Δy
k =  (2 * np.pi) / λ #[m**-1]
c_b = (np.sqrt(g * H))

ω = (-β*k)/(k**2) + ((df0['f0']**2)/c_b**2)
C = ω/k   # [m/s] all of these Rosby waves move in negative u direction Or Westward
C_abs = abs(C)  # Calculate the absolute value of C to avoid negative time values
t = d / C_abs #[s]
t_days = (t/3600)/24
t_years = t_days/365

#######################################################
 

# Question 3-b

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67e-11 # [Nm**2/kg**2]
R = 6378000 # [m] Earth radius in meter
m_M = 7.34e22 #[kg] mass of Moon
m_S = 1.99e30 #[kg] mass of Sun
r_EM = 3.84e8 # [m] distance between Earth and Moon
r_ES = 1.50e11 # [m] distance between Earth and Sun

# Define latitudes from 90 to -90 with 5-degree steps
latitudes_deg = range(90, -91, -5)

# Create DataFrame for latitudes
df3 = pd.DataFrame({'φ_deg': latitudes_deg})
df3['φ_rad'] = np.radians(df3['φ_deg'])

# Calculate a_z and a_y between Earth and Moon
a_z_M = ((G * m_M * R) / (r_EM ** 3)) * ((3 * (np.cos(df3['φ_rad']) ** 2)) - 1)
a_y_M = -1.5 * ((G * m_M * R) / (r_EM ** 3)) * np.sin(2 * df3['φ_rad'])

# Calculate a_z and a_y between Earth and Sun
a_z_S = ((G * m_S * R) / (r_ES ** 3)) * ((3 * (np.cos(df3['φ_rad']) ** 2)) - 1)
a_y_S = -1.5 * ((G * m_S * R) / (r_ES ** 3)) * np.sin(2 * df3['φ_rad'])

# Plot Earth-Moon and Earth-Sun tangential tide acceleration components against latitude
plt.figure(figsize=(10, 5))
plt.plot(a_y_M, df3['φ_deg'], marker='o', linestyle='-', label='Earth-Moon')
plt.plot(a_y_S, df3['φ_deg'], marker='o', linestyle='-', label='Earth-Sun')
plt.xlabel('Tangential tide acceleration component $a_y$ [m/s$^2$]', fontsize=12)
plt.ylabel('Latitude $φ$ [deg]', fontsize=12)
plt.title('Latitudinal Change of $a_y$ for Earth-Moon/Sun', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.tick_params(axis='both', which='major', labelsize=10)
# Save the plot
plt.savefig('tangential_tide_acceleration.png', dpi=300)
plt.show()

# Plot Earth-Moon and Earth-Sun vertical tide acceleration components against latitude
plt.figure(figsize=(10, 5))
plt.plot(a_z_M, df3['φ_deg'], marker='o', linestyle='-', label='Earth-Moon')
plt.plot(a_z_S, df3['φ_deg'], marker='o', linestyle='-', label='Earth-Sun')
plt.xlabel('Vertical tide acceleration component $a_z$ [m/s$^2$]', fontsize=12)
plt.ylabel('Latitude $φ$ [deg]', fontsize=12)
plt.title('Latitudinal Change of $a_z$ for Earth- Moon/Sun', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.tick_params(axis='both', which='major', labelsize=10)
# Save the plot
plt.savefig('vertical_tide_acceleration.png', dpi=300)
plt.show()

#############################################
# Question 3-c

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants
A = 1 #[m]
B = 0.4 #[m]

# Generate the time variable 't' from 0 to 45 days
t_days = np.linspace(0, 45, 902)

# # Create DataFrame for latitudes
df4 = pd.DataFrame({'t_45days': t_days})

df4['t_s'] = (df4['t_45days']) * 86400  # [s] to convert small fractions of days[t_days] into seconds
df4['ω_M2'] = (2 * np.pi) / ((12 * 3600) + (25*60))  # [s-1] for 12 hours and 25 min for lunar M2 tide
df4['η_M2'] = A * np.cos(df4['ω_M2'] * df4['t_s']) # The amplitude of M2 tide

df4['ω_S2'] = (2 * np.pi) / (12 * 3600)  # [s-1] for 12 hours for solar S2 tide 
df4['η_S2'] = B * np.cos((df4['ω_S2'] * df4['t_s']) + (np.pi/3)) # The amplitude of S2 tide 
df4['η_M2+S2'] = df4['η_M2'] + df4['η_S2']


# Superimposition of M2 and S2 tides amplitude over the period of 45 days 
plt.figure(figsize=(10, 5))
plt.plot(df4['t_45days'], df4['η_M2+S2'], linestyle='-')
plt.xlabel('Time [days]', fontsize=12)
plt.ylabel('Amplitude [m]', fontsize=12)
plt.title('M2 & S2 superimposition (M2+S2) tides ', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.tick_params(axis='both', which='major', labelsize=10)

# Save the figure as a high-quality PNG file
plt.savefig('M2+S2_tide_45days.png', dpi=300)
plt.show()

