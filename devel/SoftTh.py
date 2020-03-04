#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:17:16 2020

@author: francescopiscitelli
"""

import numpy as np
import pandas as pd
import math as mt
import matplotlib.pyplot as plt
import os
   
    # path_mapping = os.path.join(dir_name, '../Tables/new_THE_MG_to_VMM_Mapping.xlsx')
    # mapping_matrix = pd.read_excel(path_mapping).values
    # # Store in convenient format
    # VMM_ch_to_MG24_ch = np.empty((6, 80), dtype='object')
    # for row in mapping_matrix:
    #     VMM_ch_to_MG24_ch[row[1]][row[2]] = row[5]
    # return VMM_ch_to_MG24_ch


digitID = [33,142,143,137]

sthpath =  '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/'
sthfile = 'ThresholdsMB182.xlsx'

softthreshold = 1

# 

if softthreshold == 1:

    sthfullpath = sthpath+sthfile
    
    if os.path.exists(sthfullpath) == False:
        print('\n ---> WARNING ... File: '+sthfullpath+' NOT FOUND')
        print("\t ... software thresholds switched OFF ... ")
        softthreshold = 0
    else:
        digit = pd.read_excel(sthfullpath).columns
        temp  = pd.read_excel(sthfullpath).values
        temp  = np.matrix.transpose(temp)
             
    sth = np.ones((np.size(digitID,axis=0),64))
        
    for k in range(len(digitID)):
       
         if not(digitID[k] in digit):
            print('\n ---> WARNING ... Threshold File does NOT contain all the digitser IDs')
            print("\t ... software thresholds switched OFF for digitiser ",+(digitID[k]))
            sth[k,:] = 0
         else:
            index = np.where(digitID[k] == digit)
            sth[k,:] = temp[index,:]
         