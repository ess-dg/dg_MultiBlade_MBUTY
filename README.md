MBUTY is a code to read the hdf5 files created by the EFU that collects data from the CAEN V1740D digitisers and the Multi-Blade detector

V8.22 2020/02/01      
Author: francesco piscitelli 
Mail: francesco.piscitelli@ess.eu   

(this version is equivalent of version MATLAB MBUTI v8.22)  

A file 13827-C-ESSmask-20181116-120805_00000.h5 is in this folder as an example.

###############################################################################

This code needs the following imports:

	import numpy as np
	import pandas as pd
	import math as mt
	import matplotlib.pyplot as plt
	import os
	import sys
	from PyQt5.QtWidgets import *
	from PyQt5.QtCore import *
	from PyQt5.QtGui import *
	from PyQt5 import uic
	import time
	import h5py

And to load specific functions in the file MBUTYLIB.py, this file contains functions like the clustering function and the h5 file reader, etc. 

	import MBUTYLIB as mb 


At the top of the code there is a section where you can edit some variables to select options.
When #ON/OFF is indicated you cans elect 0 for OFF and 1 for ON.

List of variables a user can edit: 

###############################################################################

If ON you rsync the data from pathsource (on remote computer) to desitnationpath, if you already have the data this must be OFF

	sync = 0   #ON/OFF if you want to rsync the data 

###############################################################################

Folders and open file options.

Folder where the data is saved on remote computer, generally: efu@192.168.0.58:/home/efu/data/

	pathsource          = ''

Folder on your computer where to put the data from pathsource

	desitnationpath     = ''

Folder on your computer where to find the data to open
	
	datapath            = desitnationpath 

Filename of the file to open		

	filename = '13827-C-ESSmask-20181116-120805_00000.h5'

Filenames are created with a serial _00000.h5, several serials can be loaded at the same time
	 
	acqnum   = [0]    #do not need to be senquential

3 options are available, also if you want to click with the mouse on the file to open, in this case filename is ignored.
-  0 = filename and acqnum is loaded, no window opens
-  1 = (does nothing for the moment)
-  2 = filename and acqnum are both ignored, window opens and serial is the only one selected 
-  3 = filename is ignored, window opens and serial is acqnum  
	 
	openWindowToSelectFiles = 0
     
If you know that a file has to last 60 sec, you pre-enter this info to check that everything is alright 

	SingleFileDuration       = 60   #s to check if h5 file has all the resets that are foreseen 

###############################################################################

The variable POPH will be saved in a new h5 file containing the clustered data 

	saveReducedData = 0 #ON/OFF 

path where to save the clustered data in h5

	savereducedpath = '/Users/francescopiscitelli/Desktop/dest/'

In h5 file all data is under a main folder	

	nameMainFolder  = 'entry1'

	 

	compressionHDFT  = 'gzip'  
	compressionHDFL  = 9     # gzip compression level 0 - 9 of your h5 file 

###############################################################################

indicate the order the digitisers has to be read, reflecting the order of the cassette of the Multi-Blade, you can also load only one digitiser

	digitID = [34,33,31,142,143,137] or # digitID = [137]

###############################################################################

Keep all this settings as they are, they only depend on the specific detector and electronics you are using, switchOddEven and flipOrderCh are because in MB18 the channels are physically swapped and this function renders them as a standard config, wire 1 at front, strip 1 at top. 
overflowcorr and zerosuppression remove saturated and just above threshold events from the data 
Clockd is the clock of the digitisers, and Timewindow is the time window to build the clusters and depends also on the front-end electronics used. 

# switch odd and even channels  
	switchOddEven  = 1   # 0 = OFF, 1 = swaps both w and s,  2 = swaps only w, 3 = swaps only s

# reverse ch number 
	flipOrderCh    = 2   # 0 = OFF, 1 = flips both w and s,  2 = flips only w, 3 = flips only s (Note: wire 1 must be at front!)
                      # 1 becomes 32 and 33 becomes 64
                    
	overflowcorr      = 1   #ON/OFF (does not affect the MONITOR)
	zerosuppression   = 1   #ON/OFF (does not affect the MONITOR)


	Clockd            = 16e-9;  #s CAEN V1740D clock steps
	Timewindow        = 2e-6;   #s to create clusters 

###############################################################################

	plotChRaw         = 0;      #ON/OFF plot of raw ch in the file (not flipped, not swapped) no thresholds (only for 1st serial)

	plottimestamp     = 0   #ON/OFF for debugging, plot the events VS time stamp (after thresholds)

	plottimeTofs      = 0   #ON/OFF for debugging, plot the time duration of ToFs (after thresholds)

	ToFduration       = 0.06;    #s duration of a ToF for AMOR 
	ToFbinning        = 100e-6   #s

	plotMultiplicity  = 0   #ON/OFF if you want to plot the multiplicity of the events 

###############################################################################

software thresholds
NOTE: they are applied to the flipped or swpadded odd/even order of ch! Standard orientation wire 1 at front, strip 1 at top.
th on ch number: 32 w and 32 s, one row per cassette 

The threshold have to be indicated in QDC levels (as value for energy in the file) and there is one row per digitisers loaded in digitID, one row per digitiser, in the same order as digitID, and 64 columns. 0-31 are wires, 32-63 are strips. 

NOTE: the number of digitisers in digitID have to match the number of rows of sth

	softthreshold = 1   # 0 = OFF, 1 = File With Threhsolds Loaded, 2 = USer defines the Thresholds in an array sth 
	
	sth = np.ones((np.size(digitID,axis=0),64))
	
file ThresholdsMB18.xlsx contains the calibrated th for the MB18 

###############################################################################

ToF gate, remove events with ToF outside the indicated range (it is applied globally to all images and PH and multiplicity)

	ToFgate      = 0               # ON/OFF
	ToFgaterange = [0.035, 0.04]   # s  

###############################################################################

ToF per digitizer, plot the ToF hist per digitiser
	plotToFhist  = 0    #ON/OFF
                                                   
###############################################################################

PHS image of all wires and strips for all digitizers             
	EnerHistIMG   = 0              # ON/OFF

	energybins    = 128
	maxenerg      = 65.6e3 

###############################################################################

Position reconstruction, calculating the reconstructed position of the clusters with a Max amplitude algorithm or a CoG (Center of Gravity)

	ChW = [0,31]  # wire channels NOTE: if ch from 1 many things do not work on indexes, keep ch num from 0
	ChS = [0,31]  # strip channels

	positionRecon = 2

	if positionRecon == 0:
  	   posBins = [32,32]     # w x s max max
	elif positionRecon == 1:
  	   posBins = [65,65]     # w x s CoG CoG
	elif positionRecon == 2:
   	   posBins = [32,65]     # w x s max CoG
   
###############################################################################

LAMBDA: calculates lambda and plot hist 
	calculateLambda  = 1              # ON/OFF  
   
	inclination     = 5       #deg
	wirepitch       = 4e-3    #m 
	DistanceWindow1stWire = (36+2)*1e-3    #m distance between vessel window and first wire
	DistanceAtWindow      = 9.288          #m
	Distance        = DistanceWindow1stWire + DistanceAtWindow    #m  flight path from chopper at 1st wire
	lambdaBins      = 191   
	lambdaRange     = [1,18]    #A

if chopper has two openings or more per reset of ToF
	MultipleFramePerReset = 1  #ON/OFF (this only affects the lambda calculation)
	NumOfBunchesPerPulse  = 2
	lambdaMIN             = 2.5     #A

###############################################################################

MONITOR (if present)
NOTE: if the MON does not have any ToF, lambda and ToF spectra can be still calculated but perhaps meaningless

	MONOnOff = 1       #ON/OFF

	MONdigit = 137     #digitiser of the Monitor
	MONch    = 63      #ch after reorganization of channels (from 0 to 63)

	MONThreshold = 0   #threshold on MON, th is OFF if 0, any other value is ON
 
	plotMONtofPH = 0   #ON/OFF plotting (MON ToF and Pulse Height) 

	MONDistance  = 3   #m distance of MON from chopper if plotMONtofPH == 1 (needed for lambda calculation if ToF)