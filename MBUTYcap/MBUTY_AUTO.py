#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:44:24 2021

@author: francescopiscitelli
"""

from lib import libTerminal as ta

import sys
import time

############################################################################### 
###############################################################################

sourcePath = 'essdaq@172.30.244.233:~/pcaps/'
destPath   = '/Users/francescopiscitelli/Desktop/dataPcapUtgard/'


#  mode = 'poll' -> polling contineously and open new plot atomatically at every new closed file
#  mode = 'single' -> polling and new plot atomatically as soon as last finle is finished, then exit

mode = 'single'

# NOTE:
#  needs fix on auto polling mode, single works

############################################################################### 
###############################################################################

status = ta.acquisitionStatus(destPath)  

transferData = ta.transferDataUtil()

# status.set_FinStatus()
status.set_RecStatus()

startTime = time.time()

acqOverPlot = True

while True:
    
    transferData.syncData(sourcePath, destPath, verbose=False)
    acqOver = status.checkStatus()
    
    if acqOver is True:

        
        print('\033[1;36m ACQUISITION IS OVER \033[1;37m\n',end='')
        # print('\033[1;36m ACQUISITION IS OVER --> launching MBUTY \033[1;37m\n',end='')
 
        if acqOverPlot is True:
            exec(open("./MBUTYcap_V2x0.py").read())
       
        
        if mode == 'single':
            sys.exit()
        elif mode == 'poll':
            acqOverPlot = False
            time.sleep(5)
        
    else:
        
        timeElaps =  time.time() - startTime 
        
        print('\033[1;33m\nRECORDING ... elapsed time '+str('%.0f' % timeElaps)+' s \033[1;37m',end=' ')
        
        for tt in range(5):
            print('%',end=' ')
            time.sleep(1)
        