#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 10:44:55 2020

@author: francescopiscitelli
"""

import os

def syncData (pathsource,desitnationpath):

# pathsource = '/Users/francescopiscitelli/Desktop/aa/*'
# desitnationpath = '/Users/francescopiscitelli/Desktop/bb'


    command = 'rsync -av --progress'

    # command = 'cp'
    
    comm = command + ' ' + pathsource + ' ' + desitnationpath
    
    # print(comm)
    
    print('\n ... syncing data ...');
    
    status = os.system(comm);
    
    # NOTE: it will ask for password 
    
     # disp(cmdout)
    
    if status == 0: 
          print('\n data sync completed')
    else:
          print('\n ERROR ... \n')
    
    # print(status)
          
    print('\n-----')

