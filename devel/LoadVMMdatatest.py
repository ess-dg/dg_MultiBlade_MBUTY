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
