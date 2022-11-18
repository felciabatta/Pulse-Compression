# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:53:50 2022

@author: matth
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statistics as st

data = pd.read_csv("SNR_True_Reformatted.csv")**2
x1 = np.array(data)
# y=[pow(10, i) for i in range(10)]

# x=np.array([1,2,3,4,5])
# x=(1,2,3,4,5)

# =============================================================================
# P_in directly proportional to SNR
# Consider 1st point input and final point output
# Use a low pass filter to filter undetectables
# =============================================================================
P_in = 1
P_out = 1
y = []
i = 0
Atn = []
Atn_pairs = []


while i != 28:
    # if st.mean(x1[i])>2:
    y = x1[i]
    Atn.append(10*np.log(y[0]/y[4]))

    i += 1
    # else:
    #     i+=1

Atn = np.array(Atn)
Atn = Atn.reshape(7, 4)
np.savetxt('Results/AttenuationResults.csv', Atn, delimiter=',')

x = np.linspace(1, 28, 28)
plt.scatter(x, Atn)


# a_list=[]
# b_list=[]

# i=0
# while i!=28:
#     if st.mean(x1[i])>2:

#         y=x1[i]
#         a,b=np.polyfit(x,y,1)
#         a_list.append(a)
#         b_list.append(b)
#         plt.scatter(x,y)
#         plt.plot(x,(a*x+b))
#         i+=1
#     else:
#         i+=1

# i=0
# while i!=28:
#     if st.mean(y[i])<1:

# plt.yscale("log")
plt.show()

# =============================================================================
# How can I show how penetration depth can be quantified
# change first to last-if it starts low and declines less it will have good PD
# not good
# Final value-good but could be more refined
# logscale irrelevant
# normalise by ratio?
# =============================================================================


# =============================================================================
# If it declines quickly it has a high accuracy low penetration depth
# If it declines slowly but has a low starting point high acc low pen
# =============================================================================
