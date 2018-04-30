# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 01:13:12 2018

@author: aspit
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_wemo_csv(days = 4):
    data_daily = pd.read_csv('Data/Wemo/Export for Miner.csv', skiprows = np.arange(5),nrows = days, usecols = np.arange(10))
    data_halfhour = pd.read_csv('Data/Wemo/Export for Miner.csv', skiprows = np.arange(5+days+3), usecols = np.arange(2))
#    time = rawtext_read['Time']

    return data_daily,data_halfhour

data_daily,data_halfhour= read_wemo_csv()

rate = data_daily.iloc[:,len(data_daily.columns)-1]
rate = rate[0]

time_halfhour = data_halfhour['Date & Time']
Power_halfhour = data_halfhour['Power Consumed for past 30 mins (kWh)']
Cost_halfhour = Power_halfhour*rate    
fig, ax = plt.subplots()

ax.plot(time_halfhour, Power_halfhour)