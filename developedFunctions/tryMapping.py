#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:13:29 2020

@author: francescopiscitelli
"""

import os
import sys
import numpy as np
import pandas as pd

import MBUTYLIB as mb 

###############################################################################

datapath     = '/Users/francescopiscitelli/Documents/DOC/DATA/2018_11/DATA_PSI/DATAraw/C_Masks/'

filename = '13827-C-ESSmask-20181116-120805_00000.h5'

[data, Ntoffi, GTime, flag] = mb.readHDFefu(datapath,filename,33,16e-9,1)

mappath = '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/'
mapfile = 'MB18_mapping.xlsx'

MAPPING = 1

###############################################################################

if MAPPING == 0:
    print(' ---> Mapping OFF ...')
    
elif MAPPING == 1:

    mapfullpath = mappath+mapfile
            
    if os.path.exists(mapfullpath) == False:
       print('\n ---> WARNING ... File: '+mapfullpath+' NOT FOUND')
       print(' ---> Exiting ... \n')
       print('------------------------------------------------------------- \n')
       sys.exit()
    
    else:
       mappe = pd.read_excel(mapfullpath).values
       
       dataorig = np.copy(data) 
       
       for k in range(np.shape(mappe)[0]):
           position = dataorig[:,1] == mappe[k,1] 
           data[position,1] = mappe[k,0]
           
           
       
    #    def flipSwapChOrder (data,flipOrderCh,switchOddEven):
    # # switch odd and even channels  
    # if switchOddEven == 1:
    #     odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
    #     data[odd,1]  = data[odd,1]-1   #ch 0 becomes 1, etc.
    #     data[~odd,1] = data[~odd,1]+1  #ch 1 becomes 0, etc.
    # elif switchOddEven == 2: # swaps only wires, ch 0-31
    #     odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
    #     wch = data[:,1] < 32    #if ch from 0
    #     data[odd & wch,1]  = data[odd & wch,1]-1
    #     data[~odd & wch,1] = data[~odd & wch,1]+1
    # elif switchOddEven == 3: # swaps only strips, ch 32-63
    #     odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
    #     sch = data[:,1] > 31 #if ch from 0
    #     data[odd & sch,1]   = data[odd & sch,1]-1
    #     data[~odd & sch,1]  = data[~odd & sch,1]+1
               
    #     # flip 0 - 31 and 32 - 63  if ch from 0
    # if flipOrderCh == 1: # w and s both flipped
    #    wch = data[:,1] < 32
    #    sch = data[:,1] > 31
    #    data[wch,1] = 31 - data[wch,1]
    #    data[sch,1] = 32 + (63-data[sch,1])
    # elif flipOrderCh == 2:   # w only flipped
    #    wch = data[:,1] < 32
    #    data[wch,1] = 31 - data[wch,1]
    # elif flipOrderCh == 3:  # s only flipped
    #    sch = data[:,1] > 31
    #    data[sch,1] = 32 + (63-data[sch,1])
       
    # return data
                    
       