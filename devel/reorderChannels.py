#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 09:46:46 2019

@author: francescopiscitelli
"""
import numpy  as np
#this is the equivalent of the MATALB function 
#data = flipSwapChOrder(data,flipOrderCh,switchOddEven)

# # ch from 1
# def flipSwapChOrder (data,flipOrderCh,switchOddEven):
#     # switch odd and even channels  
#     if switchOddEven == 1:
#         odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
#         data[odd,1]  = data[odd,1]+1   #ch 1 becomes 2, etc.
#         data[~odd,1] = data[~odd,1]-1  #ch 2 becomes 1, etc.
#     elif switchOddEven == 2: # swaps only wires, ch 1-32 or 0-31
#         odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
#          wch = data[:,1] < 33  #if ch from 1
#         data[odd & wch,1]  = data[odd & wch,1]+1
#         data[~odd & wch,1] = data[~odd & wch,1]-1
#     elif switchOddEven == 3: # swaps only strips, ch 33-64 or 32-63
#         odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
#         sch = data[:,1] > 32 #if ch from 1
#         data[odd & sch,1]   = data[odd & sch,1]+1
#         data[~odd & sch,1]  = data[~odd & sch,1]-1
  
      
# ch from 0
def flipSwapChOrder (data,flipOrderCh,switchOddEven):
    # switch odd and even channels  
    if switchOddEven == 1:
        odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
        data[odd,1]  = data[odd,1]-1   #ch 0 becomes 1, etc.
        data[~odd,1] = data[~odd,1]+1  #ch 1 becomes 0, etc.
    elif switchOddEven == 2: # swaps only wires, ch 0-31
        odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
        wch = data[:,1] < 32    #if ch from 0
        data[odd & wch,1]  = data[odd & wch,1]-1
        data[~odd & wch,1] = data[~odd & wch,1]+1
    elif switchOddEven == 3: # swaps only strips, ch 32-63
        odd = np.array((data[:,1]%2), dtype=bool) #gives 0 if even and 1 if odd
        sch = data[:,1] > 31 #if ch from 0
        data[odd & sch,1]   = data[odd & sch,1]-1
        data[~odd & sch,1]  = data[~odd & sch,1]+1
        
    # # flip 1 - 32 and 33 - 64  if ch from 1
    # if flipOrderCh == 1: # w and s both flipped
    #    wch = data[:,1] < 33
    #    sch = data[:,1] > 32
    #    data[wch,1] = 33 - data[wch,1]
    #    data[sch,1] = 33 + (64-data[sch,1])
    # elif flipOrderCh == 2:   # w only flipped
    #    wch = data[:,1] < 33
    #    data[wch,1] = 33 - data[wch,1]
    # elif flipOrderCh == 3:  # s only flipped
    #    sch = data[:,1] > 32
    #    data[sch,1] = 33 + (64-data[sch,1])
       
        # flip 0 - 31 and 32 - 63  if ch from 0
    if flipOrderCh == 1: # w and s both flipped
       wch = data[:,1] < 32
       sch = data[:,1] > 31
       data[wch,1] = 31 - data[wch,1]
       data[sch,1] = 32 + (63-data[sch,1])
    elif flipOrderCh == 2:   # w only flipped
       wch = data[:,1] < 32
       data[wch,1] = 31 - data[wch,1]
    elif flipOrderCh == 3:  # s only flipped
       sch = data[:,1] > 31
       data[sch,1] = 32 + (63-data[sch,1])
       
    return data