#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:36:41 2020

@author: francescopiscitelli
"""

# from PyPl import progressbar
from time import sleep

# bar = progressbar.ProgressBar(maxval=20, \
#     widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
# bar.start()
# for i in range(20):
#     bar.update(i+1)
#     sleep(0.1)
    
# bar.finish()

import sys
import numpy as np
# for i in range(21):
#     sys.stdout.write('\r')
#     # the exact output you're looking for:
#     sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
#     sys.stdout.flush()
#     sleep(0.25)

NumClusters = 3459
n_bar = 10 #size of progress bar
postText = 'clustering ...'

# for kk in np.arange(NumClusters):
#     j = kk/(NumClusters-1)
#     # sys.stdout.write('\r')
#     sys.stdout.write(f"{postText} [{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%")
#     sys.stdout.flush()

# def progress(count, total, status=''):
status = 'cdfvf'
total = NumClusters
bar_len = 60
count = 56

for kk in np.arange(NumClusters):
    count = kk
    filled_len = int(round(bar_len * count / float(total)))
    
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 

        
        