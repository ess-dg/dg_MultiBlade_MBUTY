#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:59:56 2020

@author: francescopiscitelli
"""

import numpy as np
import pandas as pd


datapathinput  = '/Users/francescopiscitelli/Documents/DOC/DATA/2020_02/VMM_testData/'

filename = 'AmBeSource1526gdgem-readouts-20190819-152708_00000.h5'

Clockd = 1e-9  # clock is 1ns

DATA = np.array(pd.read_hdf((datapathinput+filename),'srs_hits'))

TIME = (DATA[:,2]+DATA[:,8])*Clockd   # in s

# check ch num has to start from 0 

FEC = DATA[:,0]

ChipID = DATA[:,1]

CH  = DATA[:,3]
ADC = DATA[:,6]



# MyDict =	{
#   "cassette": 33,
#   "wires_fec": 2,
#   "wires_chip": 3,
#   "strips_fec": 2,
#   "strips_chip": 5,
  
#   "cassette": 33,
#   "wires_fec": 2,
#   "wires_chip": 3,
#   "strips_fec": 2,
#   "strips_chip": 5,
# }

fec2cass = np.zeros((6,5))

fec2cass[0,0] = 33
fec2cass[0,1] = 2
fec2cass[0,2] = 3
fec2cass[0,3] = 2
fec2cass[0,4] = 5

fec2cass[1,0] = 34
fec2cass[1,1] = 2
fec2cass[1,2] = 4
fec2cass[1,3] = 2
fec2cass[1,4] = 3

digitID = [33]

indexcass = np.argwhere(fec2cass[:,0] == digitID)

selectionw = np.logical_and( DATA[:,0] == fec2cass[indexcass,1] , DATA[:,1] == fec2cass[indexcass,2] )

data_w = DATA[selectionw[0,:],:]

# TIME = (data_w[:,2]+data_w[:,8])*Clockd   # in s

# etc....

selections = np.logical_and( DATA[:,0] == fec2cass[indexcass,3] , DATA[:,1] == fec2cass[indexcass,4] )

data_s = DATA[selections[0,:],:]











