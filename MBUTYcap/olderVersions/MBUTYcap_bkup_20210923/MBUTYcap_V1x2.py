#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
###############################################################################
########    V1.2 2021/09/17      francescopiscitelli     ######################
###############################################################################
###############################################################################

import numpy as np
import time
import os
import sys
import matplotlib.pyplot as plt

### import the library with all specific functions that this code uses 
from lib import libReadPcapngVMM as pcapr
from lib import libSampleData as sdat
from lib import libMapping as maps
from lib import libCluster as clu
from lib import libAbsUnitsAndLambda as absu
from lib import libHistograms as hh
from lib import libFileManagmentUtil as fd
from lib import libParameters as para
from lib import libTerminal as ta
from lib import libPlotting as plo
from lib import libEventsSoftThresholds as thre

###############################################################################
###############################################################################

# STILL TO IMPLEMENT:
#     - save reduced data
#     - monitor analisys and plots
#     - ignore extra threhsolds row in file if num of strips is 32  

###############################################################################
###############################################################################
profiling = para.profiling()
print('----------------------------------------------------------------------')
plt.close("all")
### check version ###
para.checkPythonVersion()
### get current path ###
currentPath = os.path.abspath(os.path.dirname(__file__))+'/'
parameters  = para.parameters(currentPath)
###############################################################################
###############################################################################
### read json and create parameters for plotting and analisys ###

configFilePath  = currentPath+'config/'
configFileName  = "MB300_AMOR_config.json"
# configFileName  = "MB300_FREIA_config.json"
# configFileName  = "MB300_FREIA_config_inverted.json"
# configFileName  = "Utgard_test.json"

###############################################################################
###############################################################################
### read json and create parameters for plotting and analisys ###
config = maps.read_json_config(configFilePath+configFileName)
parameters.loadConfigParameters(config)
###############################################################################
###############################################################################
###############################################################################
###############################################################################
### edit parameters for plotting and analisys here ###
###############################################################################
### FILE MANAGMENT  PARAMETERS:
#################################

### ON/OFF if you want to rsync the data     
parameters.fileManagement.sync = False  

### from ... to  ... rsync the data
parameters.fileManagement.sourcePath = 'essdaq@172.30.244.233:~/pcaps/'
parameters.fileManagement.destPath   = '/Users/francescopiscitelli/Desktop/dataPcapUtgard/'

###############

parameters.fileManagement.filePath = parameters.fileManagement.destPath 

### folder and file to open (file can be a list of files)
# parameters.fileManagement.filePath = parameters.fileManagement.destPath
parameters.fileManagement.fileName = ['freia_1k_pkts_ng.pcapng']
parameters.fileManagement.fileName = ['freiatest.pcapng']

### valid otions: 'window','fileName', 'latest', 'secondLast', 'wholeFolder'
### window opens tos elcet file, filename speficified  earlier, last or sencond last file crearted in folder, 
### entire  folder  opend  and analized and cumulated  all togheter 
parameters.fileManagement.openMode = 'window'
parameters.fileManagement.openMode = 'fileName'

###############
### path to threshold  file
parameters.fileManagement.thresholdFilePath = parameters.fileManagement.currentPath+'config/'
parameters.fileManagement.thresholdFileName = 'MB300L_thresholds.xlsx'

###############
### path to  Tshark, in case you open a pcap  it gets converted into pcapng 
parameters.fileManagement.pathToTshark = '/Applications/Wireshark.app/Contents/MacOS/'

###############
### save a hdf file with clusters (reduced file)

### ON/OFF
parameters.fileManagement.saveReducedFileONOFF = False   
parameters.fileManagement.saveReducedPath = ''

parameters.fileManagement.reducedNameMainFolder  = 'entry1'
parameters.fileManagement.reducedCompressionHDFT  = 'gzip'  
parameters.fileManagement.reducedCompressionHDFL  = 9    # gzip compression level 0 - 9

###############################################################################
### ANALISYS PARAMETERS:
#################################

### cassettes to clusterize and to plot, if empty the cassettes in the config file are taken as default
# parameters.cassettes.cassettes = [1,2,3,4,5,6]
# parameters.cassettes.cassettes = np.arange(32,0,-1)

### timeWindow to search for clusters, timeWindow is max time between events in candidate cluster 
### and timeWindow/2 is the recursive time distance between adjacent hits
parameters.dataReduction.timeWindow = 3e-6

### 'OFF', 'fromFile' = File With Threhsolds Loaded, 'userDefined' = User defines the Thresholds in an array softTh
parameters.dataReduction.softThresholdType = 'off' 

if parameters.dataReduction.softThresholdType == 'userDefined':
    
    parameters.dataReduction.createThArrays(parameters.cassettes.cassettes, parameters)    
    parameters.dataReduction.softThArray.ThW[:,0] = 15000
    parameters.dataReduction.softThArray.ThS[:,0] = 500   
          
###############################################################################
### WAVELENGTH PARAMETERS:
#################################

### distance in mm from chopper and wires 0 of detector
parameters.wavelength.distance = 8000

##ON/OFF
parameters.wavelength.calculateLambda = True

### ON/OFF plot X vs Lambda 2D plot
parameters.wavelength.plotXLambda   = True
### ON/OFF integrated over single cassettes
parameters.wavelength.plotLambdaDistr = True

parameters.wavelength.lambdaBins  = 128
parameters.wavelength.lambdaRange = [1, 16]   #A

parameters.wavelength.chopperPeriod = 0.06 #s

### if chopper has two openings or more per reset of ToF
parameters.wavelength.multipleFramePerReset = True  #ON/OFF (this only affects the lambda calculation)
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
parameters.MONitor.plotMONtofPHS = False  

### in mm, distance of MON from chopper if plotMONtofPH == 1 (needed for lambda calculation if ToF)
parameters.MONitor.MONDistance  = 0   

###############################################################################
### PLOTTING PARAMETERS:
#################################

###############     
### show stat during clustering, option  'globalStat'  stat for all cassettes together, 
### 'individualStat' stat per cassette or None for no stat
parameters.plotting.showStat = 'globalStat'
# parameters.plotting.showStat = 'individualStat'

###############     
### raw plots
parameters.plotting.plotRawReadouts         = False
parameters.plotting.plotReadoutsTimeStamps  = False
parameters.plotting.plotRawHits             = True
parameters.plotting.plotHitsTimeStamps      = False
parameters.plotting.plotHitsTimeStampsVSChannels = False


parameters.plotting.plotInstRate    = False
parameters.plotting.instRateBin     = 1e-6  # s
 
###############
### ToF plot integrated over individual cassette, one per cassette
parameters.plotting.plotToFDistr    = False

# parameters.plotting.ToFrange        = 0.1    # s
# parameters.plotting.ToFbinning      = 100e-6 # s

parameters.plotting.ToFrange        = 0.001   # s
parameters.plotting.ToFbinning      = 10e-6 # s
     
parameters.plotting.plotMultiplicity = False 

# parameters.configJsonFile.orientation = 'vertical'

### 'W.max-S.max' is max max,  'W.cog-S.cog' is CoG CoG, 'W.max-S.cog' is wires max and strips CoG 
parameters.plotting.positionReconstruction = 'W.max-S.cog'
parameters.plotting.positionReconstruction = 'W.max-S.max'

### if True plot XY and XtoF plot in absolute unit (mm), if False plot in wire and strip ch no.
parameters.plotting.plotABSunits = False
 
### plot XY and XToF in log scale 
parameters.plotting.plotIMGlog = False

### ON/OFF, if  Tof  and Lambdaplot needs to include only events with strip present (2D) is True otherwise all events  also without strip set to False
parameters.plotting.coincidenceWS_ONOFF = True

### histogram outBounds param set as True as default (Events out of bounds stored in first and last bin)
parameters.plotting.hitogOutBounds = True

### for absolute  units calculation in X, already loaded in config json file
# parameters.configJsonFile.offset1stWires = 10

###############     
### PHS

### ON/OFF PHS per channel and global
parameters.pulseHeigthSpect.plotPHS = True

### plot PHS in log scale 
parameters.pulseHeigthSpect.plotPHSlog = False

parameters.pulseHeigthSpect.energyBins = 128
parameters.pulseHeigthSpect.maxEnerg   = 70e3

### plot the PHS correaltion wires vs strips
parameters.pulseHeigthSpect.plotPHScorrelation = False

###############################################################################
###############################################################################
########    end of with all the settings you can choose   #####################
########        DO NOT EDIT BELOW THIS LINE!!!!           #####################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
### if you want to save reduced data, it must include lambda, 
### so lambda calculation is turned ON if not yet 
if parameters.fileManagement.saveReducedFileONOFF is True:       
    parameters.wavelength.calculateLambda = True
    print('\n \t Lambda calculation turned ON to save reduced DATA')
    
if parameters.wavelength.plotXLambda or parameters.wavelength.plotLambdaDistr is True:
    parameters.wavelength.calculateLambda = True
    print('\n \t Lambda calculation turned ON to plot Lambda')
###############################################################################
###############################################################################
parameters.update()
###############################################################################
###############################################################################
### create axes for plotting and histograms 

allAxis = hh.allAxis()
allAxis.createAllAxis(parameters)

### here eventually edit axes 
### then update axes with: allAxis.updateAllAxis()

###############################################################################
###############################################################################
### sync the data folder from remote computer to local folder 
if parameters.fileManagement.sync is True:
    transferData = ta.transferDataUtil()
    transferData.syncData(parameters.fileManagement.sourcePath, parameters.fileManagement.destPath)

###############################################################################
###############################################################################
### select data
fileDialogue = fd.fileDialogue(parameters)
fileDialogue.openFile()
###############################################################################
###############################################################################

### init readouts cumulated over file list
readouts = pcapr.readouts()

# hits = maps.hits()

# eve = clu.events()

for fileName in fileDialogue.fileName:
    
    ### check if a file is pcapng otherwise pcap is converted into pcapng
    conv = ta.pcapConverter(parameters)
    conv.checkExtensionAndConvertPcap(fileDialogue.filePath+fileName)
    if conv.flag is False:
        fileName = conv.fileName_OUT
        
    ### check which Ring, Fen and Hybrid is present in the selected File 
    # pcapr.checkWhich_RingFenHybrid_InFile(fileDialogue.filePath+fileName).check()
    
    ### load data  
    pcap = pcapr.pcapng_reader(fileDialogue.filePath+fileName,timeResolutionType='fine', sortByTimeStampsONOFF = True)
    readouts.append(pcap.readouts)
    
    # md  = maps.mapDetector(pcap.readouts, config)
    # md.mappAllCassAndChannelsGlob()
    # # hits = md.hits
    
    # # hits.append(md.hits)
    # cc = clu.clusterHits(md.hits,parameters.plotting.showStat)
    # cc.clusterizeManyCassettes(parameters.cassettes.cassettes, parameters.dataReduction.timeWindow)
    # eve.append(cc.events)
    
      
####################    
### for debug, generate sample readouts
# aa = sdat.sampleReadouts_1()
# aa.fill()
# readouts = aa.readouts
####################

####################
### for debug, readouts in single array
# readoutsArray = readouts.concatenateReadoutsInArrayForDebug()
####################

###############################################################################
### map data
md  = maps.mapDetector(readouts, config)
md.mappAllCassAndChannelsGlob()
hits = md.hits

####################
### getting the hits for the MONitor
if parameters.MONitor.MONOnOff is True:
    MON = maps.mapMonitor(readouts, config)
    hitsMON = MON.hits
 
####################    
### for debug, generate sample hits 
Nhits = 1e4
bb = sdat.sampleHitsMultipleCassettes()
bb.generateGlob(Nhits)
hits = bb.hits   

# bb = sdat.sampleHitsMultipleCassettes_2()
# bb.generateGlob()
# hits = bb.hits  
######################

####################    
### for debug, hits in single array 
hitsArray = hits.concatenateHitsInArrayForDebug()
####################

###############################################################################
### clusterize
cc = clu.clusterHits(hits,parameters.plotting.showStat)
cc.clusterizeManyCassettes(parameters.cassettes.cassettes, parameters.dataReduction.timeWindow)
events = cc.events

####################    
### for debug, events in single array 
eventsArray = events.concatenateEventsInArrayForDebug() 
####################
   
####################    
### for debug, generate sample events 2
# dd = sdat.sampleEventsMultipleCassettes(parameters.cassettes.cassettes,'./data/')
# dd.generateGlob(Nevents)
# events  = dd.events
# eventsArray = events.concatenateEventsInArrayForDebug()
# eventsArray = eventsArray[72:100,:]
#################### 
    

###############################################################################
### calculate abs units, ToF and lambda

ab = absu.calculateAbsUnits(events, parameters)
ab.calculatePositionAbsUnit()

ab.calculateToF()

if parameters.wavelength.calculateLambda is True:
    ab.calculateWavelength()

eventsBTh = ab.events 

eventsArray2 = eventsBTh.concatenateEventsInArrayForDebug() 

###############################################################################
###############################################################################
### software thresholds

asth = thre.applyThresholdsToEvents(eventsBTh, parameters.cassettes.cassettes, parameters, parameters.plotting.showStat)
asth.thresholdizeAllCassettes()
    
events  = asth.events 

###############################################################################
###############################################################################
### plot
parameters.HistNotification()

######################
### readouts
if (parameters.plotting.plotRawReadouts  or  parameters.plotting.plotReadoutsTimeStamps) is True:
    plread = plo.plottingReadouts(readouts, config)
    if parameters.plotting.plotRawReadouts is True:
        plread.plotChRaw(parameters.cassettes.cassettes)
    if parameters.plotting.plotReadoutsTimeStamps is True:
        plread.plotTimeStamps(parameters.cassettes.cassettes)
######################

######################
### hits
if (parameters.plotting.plotRawHits or parameters.plotting.plotHitsTimeStamps or parameters.plotting.plotHitsTimeStampsVSChannels) is True:
    plhits = plo.plottingHits(hits, parameters)
    if parameters.plotting.plotRawHits is True:
        plhits.plotChRaw(parameters.cassettes.cassettes)
    if parameters.plotting.plotHitsTimeStamps is True:
        plhits.plotTimeStamps(parameters.cassettes.cassettes)
    if parameters.plotting.plotHitsTimeStampsVSChannels is True:    
        plhits.plotTimeStampsVSCh(parameters.cassettes.cassettes)    
######################

######################
### events

### XY and XToF
plev = plo.plottingEvents(events,allAxis,parameters.plotting.coincidenceWS_ONOFF)
plev.plotXYToF(logScale = parameters.plotting.plotIMGlog, absUnits = parameters.plotting.plotABSunits, orientation = parameters.configJsonFile.orientation)

### ToF per cassette 
if parameters.plotting.plotToFDistr is True:
    plev.plotToF(parameters.cassettes.cassettes)

### lambda
if parameters.wavelength.plotXLambda is True:
    plev.plotXLambda(logScale = parameters.plotting.plotIMGlog, absUnits = parameters.plotting.plotABSunits)
### lambda per cassette
if parameters.wavelength.plotLambdaDistr is True:
    plev.plotLambda(parameters.cassettes.cassettes)
    
### multiplicity 
if parameters.plotting.plotMultiplicity is True:
    plev.plotMultiplicity(parameters.cassettes.cassettes)

### PHS
if parameters.pulseHeigthSpect.plotPHS is True:
    plev.plotPHS(parameters.cassettes.cassettes, parameters, logScale = parameters.pulseHeigthSpect.plotPHSlog)
if parameters.pulseHeigthSpect.plotPHScorrelation is True:
    plev.plotPHScorrelation(parameters.cassettes.cassettes, parameters.pulseHeigthSpect.plotPHSlog)

### instantaneous Rate per cassette
if parameters.plotting.plotInstRate is True:
    plev.plotInstantaneousRate(parameters.cassettes.cassettes)


######################
### monitor

#  to be implemented

###############################################################################
###############################################################################
plt.show()
profiling.stop()
print('----------------------------------------------------------------------')
###############################################################################
###############################################################################


