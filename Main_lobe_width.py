# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:26:21 2022

@author: matth
"""

import numpy as np
import  matplotlib.pyplot as plt

t=np.linspace(0.5*np.pi,2.5*np.pi, 10000)
y=-np.sin(t)


# =============================================================================
# Here is code that isolates the main lobe
# =============================================================================

main_lobe=[]


i=0
while i !=len(t):
    if y[i]>=0:
        main_lobe.append(t[i])
    i+=1
# for i in y:
#     if i

main_lobe_width=main_lobe[len(main_lobe)-1]-main_lobe[0]
