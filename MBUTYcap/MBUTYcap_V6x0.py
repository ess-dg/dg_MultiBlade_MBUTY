#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
###############################################################################
########    V6.0 2025/06/04      francescopiscitelli     ######################
###############################################################################
###############################################################################
#  includes streaming from kafka 

import numpy as np
import time
import os
import sys
import matplotlib.pyplot as plt

# import matplotlib
# # matplotlib.use(‘Qt5Agg’)
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QGridLayout, QLabel, QLineEdit
app = QApplication(sys.argv)

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
from lib import libReducedFileH5 as saveH5
from lib import libVMMcalibration as cal 

# from lib import libKafkaReader as kaf

###############################################################################
###############################################################################

# STILL TO IMPLEMENT:
#     - monitor lambda
#     - TDC calibration 
#     - now the mon events stay in the events array,they need  to be taken out 

# NOTES:
    # in some sytems the command plt.show(block=False) at the end does not work for showing plots 
    # so try using plt.show() instead 
    
###############################################################################
###############################################################################
# parameters come from GUI or set them via the file MBUTYcap_setParameters

if len(sys.argv) > 1:
    print('running with GUI')
    
    # add import GUI param 
    
else:
    print('running w/o GUI')
    from MBUTYcap_setParameters import parameters, config


###############################################################################
###############################################################################
########    PARAMETERS COME FROM  MBUTYcap_setParameters  #####################
########    OR FROM GUI                                   #####################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
profiling = para.profiling()
print('----------------------------------------------------------------------')
print('\033[1;32mCiao '+os.environ['USER']+'! Welcome to MBUTY 6.0\033[1;37m')
print('----------------------------------------------------------------------')
plt.close("all")
### check version ###
para.checkPythonVersion()
# check packages installation 
check = para.checkPackageInstallation()
check.checkPackagePcap()

if parameters.acqMode == 'kafka':
    flag = check.checkPackageKafka()
    if flag is True:  
        from lib import libKafkaReader as kaf

###############################################################################
###############################################################################
### if you want to save reduced data, it must include lambda, 
### so lambda calculation is turned ON if not yet 
if parameters.fileManagement.saveReducedFileONOFF is True:       
    if parameters.wavelength.calculateLambda == False:
        parameters.wavelength.calculateLambda = True
        print('\n \t Lambda calculation turned ON to save reduced DATA')
    
if parameters.wavelength.plotXLambda or parameters.wavelength.plotLambdaDistr is True:
    if parameters.wavelength.calculateLambda == False:
        parameters.wavelength.calculateLambda = True
        print('\n \t Lambda calculation turned ON to plot Lambda')
        
###############################################################################
###############################################################################
parameters.set_acqMode(parameters.acqMode)
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
if parameters.acqMode  == 'pcap-local-overwrite'  or parameters.acqMode  == 'pcap-local':
    
    rec = ta.dumpToPcapngUtil(parameters.fileManagement.pathToTshark, parameters.dumpSettings.interface, \
    parameters.dumpSettings.destTestData, parameters.dumpSettings.fileName)

    # sta = ta.acquisitionStatus(parameters.dumpSettings.destTestData)  
    # sta.set_RecStatus()
    
    status = rec.dump(parameters.dumpSettings.typeOfCapture,parameters.dumpSettings.quantity,parameters.dumpSettings.numOfFiles,\
    parameters.dumpSettings.delay,parameters.dumpSettings.fileNameOnly)
    # if status == 0: 
    #      sta.set_FinStatus()
    # else:
    #      sta.set_RecStatus()

### sync the data folder from remote computer to local folder 
elif parameters.acqMode == 'pcap-sync':
    transferData = ta.transferDataUtil()
    transferData.syncData(parameters.fileManagement.sourcePath, parameters.fileManagement.destPath)   

###############################################################################
###############################################################################
### select data
fileDialogue = fd.fileDialogue(parameters)
fileDialogue.openFile()
###############################################################################
###############################################################################

### initialize readouts cumulated over file list
readouts = pcapr.readouts()
# hits   = maps.hits()
# events = clu.events()

for cont, fileName in enumerate(fileDialogue.fileName):

    if parameters.acqMode == 'pcap-sync' or parameters.acqMode == 'pcap-local' or parameters.acqMode == 'pcap-local-overwrite' or parameters.acqMode == 'off':
        
        print('\033[1;32m-> reading file {} of {}\033[1;37m'.format(cont+1,len(fileDialogue.fileName)))
        
        ### check if a file is pcapng otherwise pcap is converted into pcapng
        conv = ta.pcapConverter(parameters)
        conv.checkExtensionAndConvertPcap(fileDialogue.filePath+fileName)
        if conv.flag is False:
            fileName = conv.fileName_OUT
            
        ### check which Ring, Fen and Hybrid is present in the selected File 
        # pcapr.checkWhich_RingFenHybrid_InFile(fileDialogue.filePath+fileName,parameters.clockTicks.NSperClockTick).check()
        ### load data  
        pcap = pcapr.pcapng_reader(fileDialogue.filePath+fileName, parameters.clockTicks.NSperClockTick, MONTTLtype = config.MONmap.TTLtype, MONring = config.MONmap.RingID, \
        timeResolutionType = parameters.VMMsettings.timeResolutionType, sortByTimeStampsONOFF = parameters.VMMsettings.sortReadoutsByTimeStampsONOFF, \
        operationMode = config.DETparameters.operationMode, pcapLoadingMethod=parameters.fileManagement.pcapLoadingMethod)

    elif parameters.acqMode == 'kafka':
            
        testing = False 
        pcap = kaf.kafka_reader(parameters.clockTicks.NSperClockTick, nOfPackets = parameters.kafkaSettings.numOfPackets, \
        broker = parameters.kafkaSettings.broker, topic = parameters.kafkaSettings.topic, MONTTLtype = config.MONmap.TTLtype , MONring = config.MONmap.RingID, \
        timeResolutionType =parameters.VMMsettings.timeResolutionType, sortByTimeStampsONOFF=parameters.VMMsettings.sortReadoutsByTimeStampsONOFF, \
        operationMode=config.DETparameters.operationMode, testing=testing)
  
    readouts.append(pcap.readouts)
    # rrarr = rr.concatenateReadoutsInArrayForDebug()
    
    # md  = maps.mapDetector(pcap.readouts, config)
    # md.mappAllCassAndChannelsGlob()
    # hits.append(md.hits)
     
    # cc = clu.clusterHits(md.hits,parameters.plotting.showStat)
    # cc.clusterizeManyCassettes(parameters.config.DETparameters.cassInConfig, parameters.dataReduction.timeWindow)
    # eve.append(cc.events)
    
# 

heartbeats1 = readouts.heartbeats
heartbeats2 = readouts.removeNonESSpacketsHeartbeats(readouts.heartbeats)

readouts.checkChopperFreq()

readouts.checkInvalidToFsInReadouts()

####################    
### for debug, generate sample readouts
# aa = sdat.sampleReadouts_2()
# aa.fill()
# readouts = aa.readouts
####################

####################
### for debug, readouts in single array
readoutsArray = readouts.concatenateReadoutsInArrayForDebug()
####################

if parameters.plotting.bareReadoutsCalculation is False:
    
    ###########################################################################
    ### calibration ADC
    if parameters.dataReduction.calibrateVMM_ADC_ONOFF is True:
        calib = cal.read_json_calib(parameters.fileManagement.calibFilePath+parameters.fileManagement.calibFileName,config)
    
        if calib.calibFlag is True:
            ca = cal.calibrate(readouts,config,calib)
            ca.calibrateADC()
            readouts = ca.readouts
        
            # readouts_array = readoutsOut.concatenateReadoutsInArrayForDebug()

    ########################################################################### 
    
    md  = maps.mapDetector(readouts, config)
    md.mappAllCassAndChannelsGlob()
    hits = md.hits
    hitsArray  = hits.concatenateHitsInArrayForDebug()


    ####################
    ### getting the hits for the MONitor
    if parameters.MONitor.MONOnOff is True:
        MON = maps.mapMonitor(readouts, config)
        if MON.flagMONfound is True:
            hitsMON = MON.hits
            
            MONe = clu.hitsMON2events(hitsMON)
            eventsMON = MONe.events
            
            abMON = absu.calculateAbsUnits(eventsMON, parameters, 'MON')
            abMON.calculateToF(parameters.plotting.removeInvalidToFs)
            
            print('\033[1;32m\t MON events: {}\033[1;37m'.format(len(eventsMON.timeStamp)))
            
            
            if parameters.wavelength.calculateLambda is True:
                
                abMON.calculateWavelengthMON()

            eventsMON = abMON.events
            eventsMONarray = eventsMON.concatenateEventsInArrayForDebug()

    
    ###############################################################################
    ### map data
    # md  = maps.mapDetector(readouts, config)
    # md.mappAllCassAndChannelsGlob()
    # hits = md.hits
    
    # for debug force all hits in a single cassetteno.1 even if from different hybrids
    # hits.Cassette = np.ones(len((hits.Cassette)),dtype='int64')
    
     
    ####################    
    ### for debug, generate sample hits 
    # Nhits = 5e4
    # bb = sdat.sampleHitsMultipleCassettes()
    # bb.generateGlob(Nhits)
    # hits = bb.hits   
    
    # bb = sdat.sampleHitsMultipleCassettes_2()
    # bb.generateGlob()
    # hits = bb.hits  
    ######################
    
    ####################    
    ### for debug, hits in single array 
    # hitsArray = hits.concatenateHitsInArrayForDebug()
    ####################
    
    
    if config.DETparameters.operationMode == 'normal':
        ###############################################################################
        ### clusterize
        cc = clu.clusterHits(hits,parameters.plotting.showStat)
        cc.clusterizeManyCassettes(parameters.config.DETparameters.cassInConfig, parameters.dataReduction.timeWindow)
        events = cc.events
        deltaTimeWS = cc.deltaTimeClusterWSall
        
        # deltaTimeWSc = deltaTimeWS[ np.logical_and(deltaTimeWS[:,0]==7,deltaTimeWS[:,2]==2) , :]
        
        # xax = np.arange(-300,300,1)
        
        # hitows = hh.histog().hist1D(xax, deltaTimeWSc[:,1])

        
        # fig334, ax335 = plt.subplots(num=101445,figsize=(12,6), nrows=1, ncols=1)   
        # ax335.step(xax,hitows,'r')
        # ax335.set_yscale('log')
        
    elif  config.DETparameters.operationMode == 'clustered':  
        ### do not clusterize
        events = clu.events()
        events.importClusteredHits(hits,config)
    
    ####################    
    ### for debug, events in single array 
    eventsArray = events.concatenateEventsInArrayForDebug() 
    ####################
       
    ####################    
    ### for debug, generate sample events 2
    # dd = sdat.sampleEventsMultipleCassettes(parameters.config.DETparameters.cassInConfig,'./data/')
    # dd.generateGlob(Nevents)
    # events  = dd.events
    # eventsArray = events.concatenateEventsInArrayForDebug()
    # eventsArray = eventsArray[72:100,:]
    #################### 
        
    
    ###############################################################################
    ### calculate abs units, ToF and lambda
    
    ab = absu.calculateAbsUnits(events, parameters)
    ab.calculatePositionAbsUnit()
    
    ab.calculateToF(parameters.plotting.removeInvalidToFs)
    
    if parameters.wavelength.calculateLambda is True:
        ab.calculateWavelength()
    
    # eventsBTh = ab.events 
    
    events = ab.events 
    
    ####################    
    ### for debug, events in single array 
    # eventsArrayBTh = eventsBTh.concatenateEventsInArrayForDebug() 
    # eventsArrayBTh = events.concatenateEventsInArrayForDebug() 
    ####################    
    
    ###############################################################################
    ###############################################################################
    ### software thresholds
    
    # asth = thre.applyThresholdsToEvents(eventsBTh, parameters.config.DETparameters.cassInConfig, parameters, parameters.plotting.showStat)
    # asth.thresholdizeAllCassettes()
        
    # events  = asth.events 
    
    # eventsArrayAT = events.concatenateEventsInArrayForDebug()
    
    ###############################################################################
    ###############################################################################
    ### save reduced data to hdf5
      
    if parameters.fileManagement.saveReducedFileONOFF is True: 
        
        fileNameSave  = os.path.splitext(fileDialogue.fileName[0])[0]+'_reduced'
        
        sav = saveH5.saveReducedDataToHDF(parameters,parameters.fileManagement.saveReducedPath,fileNameSave)
        
        if (parameters.MONitor.MONOnOff is True) and (MON.flagMONfound is True):
            sav.save(events,eventsMON)
        else:
            sav.save(events)
            
###############################################################################
###############################################################################            
            
#  like this all ToFs get into reduced file, the gate is only in plotting 
    if parameters.plotting.ToFGate is True:
        abb = absu.gateToF(events,parameters.plotting.ToFGateRange)
        events = abb.events 

###############################################################################
###############################################################################
### plot
parameters.HistNotification()

######################
if parameters.plottingInSections is False:
    parameters.plottingInSectionsBlocks = parameters.config.DETparameters.numOfCassettes
else:
    print('\n\033[1;36m \t Plotting Cassettes in blocks of {} \033[1;37m\n'.format(parameters.plottingInSectionsBlocks)) 
    fullConfig = config
    
numOfLoops = int(np.ceil(parameters.config.DETparameters.numOfCassettes/parameters.plottingInSectionsBlocks))
    
for loop in range(numOfLoops):
    
    plt.close("all")
       
    start = loop*parameters.plottingInSectionsBlocks
    stop  = (loop+1)*parameters.plottingInSectionsBlocks
    
    if parameters.plottingInSections is True:
        config  = maps.extractPartialConfig.extract(fullConfig,start,stop)
        print('\033[1;36m \t Plotting Cassettes from {} to {} \033[1;37m'.format(start,stop-1))
        
    parameters.loadConfig(config)
    allAxis.createAllAxis(parameters)
        
    ######################
    ### readouts
    
    if (parameters.plotting.plotRawReadouts  or  parameters.plotting.plotReadoutsTimeStamps or parameters.plotting.plotChopperResets or parameters.plotting.plotADCvsCh) is True:
        plread = plo.plottingReadouts(readouts, config)
        if parameters.plotting.plotRawReadouts is True:
            plread.plotChRaw(parameters.config.DETparameters.cassInConfig)
        if parameters.plotting.plotReadoutsTimeStamps is True:
            plread.plotTimeStamps(parameters.config.DETparameters.cassInConfig)
        if parameters.plotting.plotADCvsCh is True:
            plread.plotADCvsCh(parameters.config.DETparameters.cassInConfig, allAxis , parameters.plotting.plotADCvsChlog)          
        if parameters.plotting.plotChopperResets is True:
            plread.plotChoppResets()
            
    ######################
    
    ######################
    if parameters.plotting.bareReadoutsCalculation is False:
        ### hits
        if (parameters.plotting.plotRawHits or parameters.plotting.plotHitsTimeStamps or parameters.plotting.plotHitsTimeStampsVSChannels) is True:
            plhits = plo.plottingHits(hits, parameters)
            if parameters.plotting.plotRawHits is True:
                plhits.plotChRaw(parameters.config.DETparameters.cassInConfig)
            if parameters.plotting.plotHitsTimeStamps is True:
                plhits.plotTimeStamps(parameters.config.DETparameters.cassInConfig)
            if parameters.plotting.plotHitsTimeStampsVSChannels is True:    
                plhits.plotTimeStampsVSCh(parameters.config.DETparameters.cassInConfig)    
    ######################
    
    ######################
    ### events
    
    if parameters.plotting.bareReadoutsCalculation is False:
        ### XY and XToF
        plev = plo.plottingEvents(events,allAxis,parameters.plotting.coincidenceWS_ONOFF)
        plev.plotXYToF(logScale = parameters.plotting.plotIMGlog, absUnits = parameters.plotting.plotABSunits, orientation = parameters.config.DETparameters.orientation)
        
        # ### ToF per cassette 
        if parameters.plotting.plotToFDistr is True:
            plev.plotToF(parameters.config.DETparameters.cassInConfig)
    
        ### lambda
        if parameters.wavelength.plotXLambda is True:
            plev.plotXLambda(logScale = parameters.plotting.plotIMGlog, absUnits = parameters.plotting.plotABSunits)
        ### lambda per cassette
        if parameters.wavelength.plotLambdaDistr is True:
            plev.plotLambda(parameters.config.DETparameters.cassInConfig)
            
        ### multiplicity 
        if parameters.plotting.plotMultiplicity is True:
            plev.plotMultiplicity(parameters.config.DETparameters.cassInConfig)
    
        # ### PHS
        if parameters.pulseHeigthSpect.plotPHS is True:
            plev.plotPHS(parameters.config.DETparameters.cassInConfig, parameters, logScale = parameters.pulseHeigthSpect.plotPHSlog)
        if parameters.pulseHeigthSpect.plotPHScorrelation is True:
            plev.plotPHScorrelation(parameters.config.DETparameters.cassInConfig, parameters.pulseHeigthSpect.plotPHSlog)
        
        ### instantaneous Rate per cassette
        if parameters.plotting.plotInstRate is True:
            plev.plotInstantaneousRate(parameters.config.DETparameters.cassInConfig)
    
        ############
        # MON plots
        if parameters.MONitor.MONOnOff is True and parameters.MONitor.plotMONtofPHS is True and MON.flagMONfound is True:
            
            plMON = plo.plottingMON(eventsMON,allAxis)
            plMON.plot_ToF_PHS_MON()
            
            if parameters.wavelength.calculateLambda is True: 
                plMON.plotLambda_MON()
                
    #########################################################          
    plt.show(block=False)    
    #########################################################           
    if parameters.plottingInSections is True:    
    
        plt.pause(0.5)
        
        inp = input('\033[1;32m--> press (enter) to continue to the next block or (q + enter) to quit \033[1;37m')
        
        if inp == 'q':
            plt.close()
            profiling.stop()
            print('----------------------------------------------------------------------')
            sys.exit()        

###############################################################################
###############################################################################
#  any other plot that the user wants...

# # sel = np.logical_or(hits.WiresStrips == 31,  hits.WiresStrips == 2)
# sel = np.logical_or(hits.WiresStrips == 0,  hits.WiresStrips == 8)

# diffe       = np.diff(hits.timeStamp[sel])

# # print('\n',np.sum(~sel))

# # sortedDiffe = diffe[diffe.argsort()]

# # # print('freq injected in 1 ch '+str(1/(sortedDiffe[-1]*1e-9))+' Hz')

# TD = np.arange(-2000,2000,1)

# hist  = hh.histog().hist1D(TD,diffe) 
# figl, ax = plt.subplots(num=567,figsize=(6,6), nrows=1, ncols=1) 
# ax.step(TD,hist,'b',where='mid')   
# ax.set_yscale('log')
# ax.set_xlabel('delta time (ns)')
# ax.set_ylabel('counts') 
# ax.grid()
# ax.set_xlim((-200,200))
# # figl.suptitle('2FEN_2Hy')
      
# ToF     = readouts.timeStamp - readouts.PulseT

# # ToFprev = readouts.timeStamp - readouts.PrevPT

# # delta =  readouts.PulseT -  readouts.PrevPT

# # patth = 'ToFs.txt'


# TofAxis  = np.linspace(0,5e7,1024)
        


# histo = hh.histog().hist1D(TofAxis,ToF)


# figl5666, ax5666 = plt.subplots(num=567655,figsize=(6,6), nrows=1, ncols=1)
           
# # global PHS plot
# # ax5666.step(allAxis.axEnergy.axis,PHSGw,'r',where='mid',label='w')
# ax5666.step(TofAxis,histo,'k',where='mid',label='w/s')
# # ax5666.set_xlabel('pulse height (a.u.)')
# # ax5666.set_ylabel('counts')
# # ax5666.set_xlim([0,1200])
# ax5666.grid()
# ax5666.set_yscale('log')


# chaxis = np.linspace(0,63,64)


# selHYB = readouts.hybrid  == 3

# selVMM = readouts.VMM     == 6

# selall = np.logical_and(selHYB,selVMM)



# histo2D = hh.histog().hist2D( TofAxis, ToF[selall], chaxis, readouts.Channel[selall] ) 

# from matplotlib.colors import LogNorm

# figl5667, ax5667 = plt.subplots(num=567657,figsize=(6,6), nrows=1, ncols=1)
           
# # global PHS plot
# # ax5666.step(allAxis.axEnergy.axis,PHSGw,'r',where='mid',label='w')
# pos1  = ax5667.imshow(histo2D,aspect='auto',norm=LogNorm(),interpolation='none',extent=[TofAxis[0],TofAxis[-1],chaxis[-1],chaxis[0]], origin='upper',cmap='viridis')
 
# ax5667.grid()

# aa = np.concatenate((ToF[:,None],ToFprev[:,None]),axis=1)


# # bb = np.round(aa/100000)   
  
# dataTemp = np.savetxt(patth,aa,delimiter='\t')


###############################################################################
###############################################################################
plt.show(block=False)
profiling.stop()
print('----------------------------------------------------------------------')
###############################################################################
###############################################################################

