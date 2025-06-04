#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
###############################################################################

import os
# import subprocess

### import the library with all specific functions that this code uses 
from lib import libMapping as maps
from lib import libParameters as para

###############################################################################
###############################################################################
### get current path ###
currentPath = os.path.abspath(os.path.dirname(__file__))+'/'
parameters  = para.parameters(currentPath)

###############################################################################
###############################################################################
### read json and create parameters for plotting and analisys ###

configFilePath  = currentPath+'config/'

configFileName  = "AMOR.json"

# configFileName  = "ESTIA.json"

# configFileName  = "ESTIA_sect0.json"
# configFileName  = "ESTIA_sect1.json"
# configFileName  = "ESTIA_sect2.json"
# configFileName  = "ESTIA_sect3.json"
# configFileName  = "ESTIA_sect4.json"
# configFileName  = "ESTIA_sect5.json"

# configFileName  = "ESTIA_sect0and1.json"
# configFileName  = "ESTIA_sect2and3.json"
# configFileName  = "ESTIA_sect4and5.json"

###############################################################################
###############################################################################
### read json and create parameters for plotting and analisys ###
config = maps.read_json_config(configFilePath+configFileName)
parameters.loadConfigAndSetParameters(config)
###############################################################################
###############################################################################
###############################################################################
###############################################################################
### edit parameters for plotting and analisys here ###
###############################################################################

### ACQ MODES:
#################################
### can only be only one of these 5 options: off, pcap-sync, pcap-local, pcap-local-overwrite or kafka

parameters.acqMode = 'pcap-sync'
# parameters.acqMode = 'pcap-local'
# parameters.acqMode = 'pcap-local-overwrite'
# parameters.acqMode = 'kafka'
parameters.acqMode = 'off'

###  then check parameters.fileManagement.openMode = 'window' for the open mode ...
###############################################################################
###############################################################################
### FILE MANAGMENT  PARAMETERS:
#################################

# relevant for acqMode =  pcap-local, pcap-local-overwrite and kafka 

parameters.dumpSettings.interface     = 'ens2'

parameters.dumpSettings.typeOfCapture = 'packets'
parameters.dumpSettings.quantity      =  100      #packets

# parameters.dumpSettings.typeOfCapture = 'duration'
# parameters.dumpSettings.quantity      = 1   #seconds

parameters.fileManagement.fileNameSave = 'test'

# NOTE
# for acqMode =  pcap-local saves files in parameters.fileManagement.filePath 

# relevant for acqMode =  kafka , num of packets to dump is in dumpSettings 
parameters.kafkaSettings.broker       = '127.0.0.1:9092'
parameters.kafkaSettings.topic        = 'freia_debug'
parameters.kafkaSettings.numOfPackets =  100      #packets

###############################################################################

# relevant for acqMode =  pcap-sync
### from ... to  ... rsync the data

parameters.fileManagement.sourcePath = 'essdaq@172.30.244.50:~/pcaps/'
# parameters.fileManagement.sourcePath = 'essdaq@172.30.244.233:~/pcaps/'
parameters.fileManagement.destPath   = '/Users/francescopiscitelli/Desktop/dataVMM/' 

###############

parameters.fileManagement.filePath = parameters.fileManagement.destPath 

# relevant for acqMode =  off, pcap-sync and pcap-local

parameters.fileManagement.filePath = currentPath+'data/'

# parameters.fileManagement.filePath = '/Users/francescopiscitelli/Documents/DOC/DATA/202311_PSI_AMOR_MBnewAMOR_VMM_neutrons/SamplesAndMasks/'

# parameters.fileManagement.filePath = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap_develDataFormatClustered/data/'
# parameters.fileManagement.fileName = [ 'sampleData_NormalMode.pcapng']
# parameters.fileManagement.fileName = [ 'sampleData_ClusteredMode.pcapng']

### folder and file to open (file can be a list of files)

# parameters.fileManagement.fileName = ['freia_1k_pkts_ng.pcapng']
# parameters.fileManagement.fileName = ['freiatest.pcapng']
# parameters.fileManagement.fileName = ['20231106_142811_duration_s_5_YESneutrons1240K1070Rth280_maskESS_00000.pcapng']
parameters.fileManagement.fileName = ['ESSmask2023.pcapng']

# parameters.fileManagement.fileName = ['DiagonaltestData.pcapng']


# parameters.fileManagement.fileSerials = np.arange(18,28,1)

### valid otions: 'window','fileName', 'latest', 'secondLast', 'wholeFolder', 'sequence' 
### window opens to selcet file, filename speficified  earlier, last or sencond last file crearted in folder, 
### entire  folder  opend  and analized and cumulated  all togheter 
### sequence opens all filens in     parameters.fileManagement.fileSerials and with fileName
parameters.fileManagement.openMode = 'window'
parameters.fileManagement.openMode = 'fileName'
# parameters.fileManagement.openMode = 'latest'
# parameters.fileManagement.openMode = 'secondLast'
# parameters.fileManagement.openMode = 'wholeFolder'
# parameters.fileManagement.openMode = 'sequence'

###############
### type of pcap file loading, prealloc of memeory with allocate or quick, allocate is more rigorous, quick estimates the memory and it is faster 
parameters.fileManagement.pcapLoadingMethod = 'allocate'
# parameters.fileManagement.pcapLoadingMethod = 'quick'

###############
### path to calibration file
parameters.fileManagement.calibFilePath = parameters.fileManagement.currentPath+'calib/'
parameters.fileManagement.calibFileName = 'AMOR_calib_20231111002842.json'

###############
### path to threshold  file
parameters.fileManagement.thresholdFilePath = parameters.fileManagement.currentPath+'config/'
parameters.fileManagement.thresholdFileName = 'MB300L_thresholds.xlsx'

###############
### path to  Tshark, in case you open a pcap  it gets converted into pcapng 
parameters.fileManagement.pathToTshark = '/Applications/Wireshark.app/Contents/MacOS/'
# parameters.fileManagement.pathToTshark = '/usr/sbin/'

###############
### save a hdf file with clusters (reduced file)

### ON/OFF
parameters.fileManagement.saveReducedFileONOFF = False   
parameters.fileManagement.saveReducedPath = '/Users/francescopiscitelli/Desktop/reducedFile/'

parameters.fileManagement.reducedNameMainFolder  = 'entry1'
parameters.fileManagement.reducedCompressionHDFT  = 'gzip'  
parameters.fileManagement.reducedCompressionHDFL  = 9    # gzip compression level 0 - 9

###############################################################################
### ANALISYS PARAMETERS:
#################################

### calibration VMM ADC
parameters.dataReduction.calibrateVMM_ADC_ONOFF = False

### sorting readouts by time stamp, if OFF they are as in RMM stream
parameters.VMMsettings.sortReadoutsByTimeStampsONOFF = False

### time stamp is time HI + time LO or if fine corrected with TDC 
parameters.VMMsettings.timeResolutionType = 'fine'
# parameters.VMMsettings.timeResolutionType = 'coarse'

### timeWindow to search for clusters, timeWindow is max time between events in candidate cluster 
### and timeWindow/2 is the recursive time distance between adjacent hits
parameters.dataReduction.timeWindow = 0.3e-6

### 'OFF', 'fromFile' = File With Threhsolds Loaded, 'userDefined' = User defines the Thresholds in an array softTh
parameters.dataReduction.softThresholdType = 'off' 
# parameters.dataReduction.softThresholdType = 'fromFile' 

if parameters.dataReduction.softThresholdType == 'userDefined':
    
    parameters.dataReduction.createThArrays(parameters.config.DETparameters.cassInConfig, parameters)    
    parameters.dataReduction.softThArray.ThW[:,0] = 15000
    parameters.dataReduction.softThArray.ThS[:,0] = 500   
          
###############################################################################
### WAVELENGTH PARAMETERS:
#################################

### distance in mm from chopper and wires 0 of detector
parameters.wavelength.distance = 8000

##ON/OFF
parameters.wavelength.calculateLambda = False

### ON/OFF plot X vs Lambda 2D plot
parameters.wavelength.plotXLambda     = False
### ON/OFF integrated over single cassettes
parameters.wavelength.plotLambdaDistr = False

parameters.wavelength.lambdaBins  = 128
parameters.wavelength.lambdaRange = [1, 16]   #A

parameters.wavelength.chopperPeriod = 0.12 #s (NOTE: only matters if multipleFramesPerRest > 1)

### if chopper has two openings or more per reset of ToF
parameters.wavelength.multipleFramePerReset = False  #ON/OFF (this only affects the lambda calculation)
parameters.wavelength.numOfBunchesPerPulse  = 2
parameters.wavelength.lambdaMIN             = 2.5     #A

### in seconds, time shift betweeen pickup and chopper edge 
parameters.wavelength.chopperPickUpDelay =  13.5/(2.*180.) * parameters.wavelength.chopperPeriod/parameters.wavelength.numOfBunchesPerPulse 

  
###############################################################################
### MONITOR PARAMETERS:
#################################

### ON/OFF
parameters.MONitor.MONOnOff = False   

### threshold on MON, th is OFF if 0, any other value is ON
parameters.MONitor.MONThreshold = 0   

### ON/OFF plotting (MON ToF and Pulse Height) 
parameters.MONitor.plotMONtofPHS = True  

### in mm, distance of MON from chopper if plotMONtofPH == 1 (needed for lambda calculation if ToF)
parameters.MONitor.MONDistance  = 6000   

###############################################################################
### PLOTTING PARAMETERS:
#################################

###############
# with True disables clustering and mapping for speed reasons, analisys stops at readouts 
parameters.plotting.bareReadoutsCalculation = False

###############     
### plotting in sections of cassettes to ease the visualization if True and in blocks of ...  
parameters.plottingInSections       = False 
parameters.plottingInSectionsBlocks = 5

###############     
### show stat during clustering, option  'globalStat'  stat for all cassettes together, 
### 'individualStat' stat per cassette or None for no stat
parameters.plotting.showStat = 'globalStat'
# parameters.plotting.showStat = 'individualStat'

###############     
### raw plots
parameters.plotting.plotRawReadouts         = True
parameters.plotting.plotReadoutsTimeStamps  = False
parameters.plotting.plotADCvsCh             = False 
parameters.plotting.plotADCvsChlog          = False 
parameters.plotting.plotChopperResets       = False 

parameters.plotting.plotRawHits             = False
parameters.plotting.plotHitsTimeStamps      = False
parameters.plotting.plotHitsTimeStampsVSChannels = False

###############
### Instantaneous Rate
parameters.plotting.plotInstRate    = False
parameters.plotting.instRateBin     = 100e-6  # s
 
###############
### ToF plot integrated over individual cassette, one per cassette
parameters.plotting.plotToFDistr    = False

parameters.plotting.ToFrange        = 0.15    # s
parameters.plotting.ToFbinning      = 100e-6 # s

parameters.plotting.ToFGate         = False
parameters.plotting.ToFGateRange    = [0.02,0.025]   # s
     
parameters.plotting.plotMultiplicity = False 

### 'W.max-S.max' is max max,  'W.cog-S.cog' is CoG CoG, 'W.max-S.cog' is wires max and strips CoG 
parameters.plotting.positionReconstruction = 'W.max-S.cog'
parameters.plotting.positionReconstruction = 'W.max-S.max'
# parameters.plotting.positionReconstruction = 'W.cog-S.cog'

### if True plot XY and XtoF plot in absolute unit (mm), if False plot in wire and strip ch no.
parameters.plotting.plotABSunits = False
 
### plot XY and XToF in log scale 
parameters.plotting.plotIMGlog   = False

### ON/OFF, if  Tof  and Lambdaplot needs to include only events with strip present (2D) is True otherwise all events also without strip set to False
parameters.plotting.coincidenceWS_ONOFF = True

### ON/OFF, if  invalid ToFs Tofare included in the plots or removed from events 
parameters.plotting.removeInvalidToFs   = True

### histogram outBounds param set as True as default (Events out of bounds stored in first and last bin)
parameters.plotting.hitogOutBounds = True

##############################      
### PHS

### ON/OFF PHS per channel and global
parameters.pulseHeigthSpect.plotPHS = True

### plot PHS in log scale 
parameters.pulseHeigthSpect.plotPHSlog = False

parameters.pulseHeigthSpect.energyBins = 128
parameters.pulseHeigthSpect.maxEnerg   = 1700

### plot the PHS correaltion wires vs strips
parameters.pulseHeigthSpect.plotPHScorrelation = False


###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################


    