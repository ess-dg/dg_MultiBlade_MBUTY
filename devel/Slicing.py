#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 10:52:00 2020

@author: francescopiscitelli
"""

import numpy  as np

 # selMON  = data[:,1] == MONch
 #           temp    = data[:,[0,2]] #selct only col with time stamp and charge
 #           MONdata = temp[selMON,:]
 #           MONdata[:,0] = np.around((MONdata[:,0]*Clockd),decimals=6)     #  time stamp in s and round at 1us
 #           data    = data[np.logical_not(selMON),:] # remove MON data from data 



aa = np.random.rand(100,5)


sel = aa[:,0] >= 0.6



temp = aa[:,[0,2]]

bb1 = temp[sel,:]




bb2 = aa[sel,:][:,[0,2]]