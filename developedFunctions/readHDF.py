#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 10:19:11 2019

@author: francescopiscitelli
"""

import pandas as pd
import numpy  as np
import time
import os
#this is the equivalent of the MATALB function 
#[DATA,Ntoffi,GTime] = readHDFEFUfile(datapathinput,filename,digitID,ordertime)
# output data 4 columns, col 0 time stamp, col 1 ch num from 0 to 63, col 2 ADC value, col 3 reset of ToF in ms
tProfilingStart = time.time()
# def readHDFefu (datapathinput,filename,digitID,ordertime):

digitID = [34]

ordertime = 1

Clockd = 16e-9

datapathinput = os.path.abspath('../.')+'/data/' 

filename = '13827-C-ESSmask-20181116-120805_00000.h5'
    
# def readHDFefu (datapathinput,filename,digitID,Clockd,ordertime):


    
DATA = np.array(pd.read_hdf((datapathinput+filename),'mbcaen_readouts'))
   
if not(digitID in DATA[:,1]): #if the digitID does not exist in the file 
    
    Bdata  = np.ones([2,4], dtype='float64' )*np.inf
    Ntoffi = np.array([1], dtype='float64' )*np.inf
    GTime  = np.array([1], dtype='float64' )*np.inf
    flag   = -1
    presentdigit = np.unique(DATA[:,1])
    print('\n \t No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
    for digit in presentdigit:
        print(digit,end=' ')
           
else:
    
    flag   = 0
    
    selectdigi = DATA[:,1] == digitID

    Adata = DATA[selectdigi,:]
    
    ## CH NUMBER FROM 0 NOT FROM 1 AS MATLAB !!!!! OTHERVIWISE ADD A LINE HERE TO ADD +1
#        uncomment for ch from 1 to 64
    # Adata[:,3] = Adata[:,3]+np.float64(1) ## ch is from 1 to 64
    
    GTime  = np.unique(Adata[:,0]) 
    Ntoffi = len(GTime)
    
    #plt.plot(GTime)
    
    tofChange = np.diff(Adata[:,0])
    tofChange = np.append([np.float64(1)], tofChange)
    ###tofChange[tofChange != 0] = 1
    index = np.flatnonzero(tofChange)
    index = np.append(index,[np.int64(len(tofChange))])
    
    Bdata = Adata[:,2:5] 
    Bdata =  np.concatenate((Bdata,tofChange[:,None]),axis=1)
    # col 1 time stamp, col 2 channel, col 3 ADC, col 4 global time reset delta in ms
    
    #Bdata[2:10,0] = range(444008,444000,-1)
    
    if ordertime == 1:
        for k in range(0,Ntoffi,1):
        #    print(index[k])
            temp = Bdata[index[k]:index[k+1],:]
            temp = temp[temp[:,0].argsort(),]
            Bdata[index[k]:index[k+1]] = temp
            
    Bdata[:,0] = Bdata[:,0]*Clockd       # time in s 
            
    # return Bdata, Ntoffi, GTime, flag
    
# DATA = np.array(pd.read_hdf((datapathinput+filename),'mbcaen_readouts'))
   
# if not(digitID in DATA[:,1]): #if the digitID does not exist in the file 
    
#     Bdata  = np.ones([2,4], dtype='float64' )*np.inf
#     Ntoffi = np.array([1], dtype='float64' )*np.inf
#     GTime  = np.array([1], dtype='float64' )*np.inf
#     flag   = -1
#     presentdigit = np.unique(DATA[:,1])
#     print('\n \t No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
#     for digit in presentdigit:
#         print(digit,end=' ')
           
# else:
    
#     flag   = 0
    
#     selectdigi = DATA[:,1] == digitID

#     Adata = DATA[selectdigi,:]
    
#     ## CH NUMBER FROM 0 NOT FROM 1 AS MATLAB !!!!! OTHERVIWISE ADD A LINE HERE TO ADD +1
# #        uncomment for ch from 1 to 64
#     # Adata[:,3] = Adata[:,3]+np.float64(1) ## ch is from 1 to 64
    
#     GTime  = np.unique(Adata[:,0]) 
#     Ntoffi = len(GTime)
    
#     #plt.plot(GTime)
    
#     tofChange = np.diff(Adata[:,0])
#     tofChange = np.append([np.float64(1)], tofChange)
#     ###tofChange[tofChange != 0] = 1
#     index = np.flatnonzero(tofChange)
#     index = np.append(index,[np.int64(len(tofChange))])
    
#     Bdata = Adata[:,2:5] 
#     Bdata =  np.concatenate((Bdata,tofChange[:,None]),axis=1)
#     # col 1 time stamp, col 2 channel, col 3 ADC, col 4 global time reset delta in ms
    
#     #Bdata[2:10,0] = range(444008,444000,-1)
    
#     if ordertime == 1:
#         for k in range(0,Ntoffi,1):
#         #    print(index[k])
#             temp = Bdata[index[k]:index[k+1],:]
#             temp = temp[temp[:,0].argsort(),]
#             Bdata[index[k]:index[k+1]] = temp
            
#     Bdata[:,0] = Bdata[:,0]*Clockd       # time in s 
        
# return Bdata, Ntoffi, GTime, flag

# DATA = np.array(pd.read_hdf((datapathinput+filename),'mbcaen_readouts'))

# if not(digitID in DATA[:,1]): #if the digitID does not exist in the file 
    
#     Bdata  = np.ones([2,4], dtype='float64' )*np.inf
#     Ntoffi = np.array([1], dtype='float64' )*np.inf
#     GTime  = np.array([1], dtype='float64' )*np.inf
#     presentdigit = np.unique(DATA[:,1])
#     print('\n No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
#     for digit in presentdigit:
#         print(digit,end=' ')

# else:
    
#     selectdigi = DATA[:,1] == digitID

#     Adata = DATA[selectdigi,:]
    
#     ## CH NUMBER FROM 0 NOT FROM 1 AS MATLAB !!!!! OTHERVIWISE ADD A LINE HERE TO ADD +1
# #        uncomment for ch from 1 to 64
#     # Adata[:,3] = Adata[:,3]+np.float64(1) ## ch is from 1 to 64
    
#     GTime  = np.unique(Adata[:,0]) 
#     Ntoffi = len(GTime)
    
#     #plt.plot(GTime)
    
#     tofChange = np.diff(Adata[:,0])
#     tofChange = np.append([np.float64(1)], tofChange)
#     ###tofChange[tofChange != 0] = 1
#     index = np.flatnonzero(tofChange)
#     index = np.append(index,[np.int64(len(tofChange))])
    
#     Bdata = Adata[:,2:5] 
#     Bdata =  np.concatenate((Bdata,tofChange[:,None]),axis=1)
#     # col 1 time stamp, col 2 channel, col 3 ADC, col 4 global time reset delta in ms
    
#     #Bdata[2:10,0] = range(444008,444000,-1)
    
#     if ordertime == 1:
#         for k in range(0,Ntoffi,1):
#         #    print(index[k])
#             temp = Bdata[index[k]:index[k+1],:]
#             temp = temp[temp[:,0].argsort(),]
#             Bdata[index[k]:index[k+1]] = temp
            
     
        
    # return Bdata, Ntoffi, GTime
            
tElapsedProfiling = time.time() - tProfilingStart            
print('\n Completed --> time elapsed: %.2f s' % tElapsedProfiling)

####################################
#
#DATA = pd.read_hdf((path+filename),'mbcaen_readouts')
#
#DD = DATA.digitizer
#selectdigi = DD == digitID
#
#if sum(selectdigi) == 0:  #if the digitID does not exist in the file 
#        data   = []
#        Ntoffi = []
#        GTime  = []
#        presentdigit = np.unique(DD)
#        print('\n No Digit ',str(digitID),' found! This file only contains Digitizers:', end=' ')
#        for digit in presentdigit:
#            print(digit,end=' ')
##        print('\n')
#        pass
#
#Ddata = DATA[selectdigi]
#
## CH NUMBER FROM 0 NOT FROM 1 AS MATALB !!!!! OTHERVIWQSE ADD A LINE HERE TO ADD +1
#
#data  = Ddata.drop(['global_time','digitizer'], axis=1)
#
##data = Ddata[['local_time', 'channel', 'adc']].copy()
#
#data = data.reset_index(drop=True)
# 
#GTime  = np.unique(Ddata.global_time) 
#Ntoffi = len(GTime)
#
###plt.plot(GTime)
#
#tofChange = np.diff(Ddata.global_time)
#
#tofChange = np.append([np.uint64(1)], tofChange)
###tofChange[tofChange != 0] = 1
#
###index = np.nonzero(tofChange)
#
#data['reset'] = tofChange
#
#####################################

   

