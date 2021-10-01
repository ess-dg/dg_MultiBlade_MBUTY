#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:44:24 2021

@author: francescopiscitelli
"""

from lib import libAcqStatus as st
from lib import libTerminal as ta

import MBUTYcap_V2x0 as MBUTY

import sys
import time




sourcePath = 'essdaq@172.30.244.233:~/pcaps/'
destPath   = '/Users/francescopiscitelli/Desktop/dataPcapUtgard/'

status = st.acquisitionStatus(destPath)  

transferData = ta.transferDataUtil()

# transferData.syncData(sourcePath, destPath, verbose=False)

# status.setFinStatus()

while True:
    
    
    transferData.syncData(sourcePath, destPath, verbose=False)
    acqOver = status.checkStatus()
    
    time.sleep(5)

    if acqOver is True:
        
        print('\033[1;31m ACQ IS OVER \033[1;37m\n')
        # sys.exit()
        
        MBUTY()
        
        time.sleep(10)
        
    else:
        
        
        print('\033[1;31m STILL recording \033[1;37m\n')
        time.sleep(5)