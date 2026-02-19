#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
###############################################################################
########    V1.4 2021/08/25     francescopiscitelli      ######################
########    script to read the pcapng file from VMM readout
###############################################################################
###############################################################################

# import argparse
import numpy as np
import pcapng as pg
import os
import time
import sys
import ipaddress
# from lib import libPlotting as plo


###############################################################################
###############################################################################

            
class readouts():            
    def __init__(self): 
        
        datype = 'int64'
        
        self.Ring    = -1*np.ones((0), dtype = datype)
        self.Fen     = -1*np.ones((0), dtype = datype)
        self.VMM     = -1*np.ones((0), dtype = datype)
        self.hybrid  = -1*np.ones((0), dtype = datype)
        self.ASIC    = -1*np.ones((0), dtype = datype)
        self.Channel = -1*np.ones((0), dtype = datype)
        self.ADC     = -1*np.ones((0), dtype = datype)
        self.Channel1 = -1*np.ones((0), dtype = datype)
        self.ADC1     = -1*np.ones((0), dtype = datype)     
        self.timeStamp   = np.zeros((0), dtype = datype)
        self.timeCoarse  = np.zeros((0), dtype = datype)
        self.BC      = -1*np.ones((0), dtype = datype)
        self.OTh     = -1*np.ones((0), dtype = datype)
        self.TDC     = -1*np.ones((0), dtype = datype)
        self.GEO     = -1*np.ones((0), dtype = datype)
        self.G0      = -1*np.ones((0), dtype = datype)
        self.PulseT    = np.zeros((0), dtype = datype)
        self.PrevPT    = np.zeros((0), dtype = datype)
        self.Durations = np.zeros((0), dtype = datype)
        self.mult0     = np.zeros((0), dtype = datype)
        self.mult1     = np.zeros((0), dtype = datype)
        self.heartbeats = np.zeros((0), dtype = datype)
               
    def transformInReadouts(self, data):
        self.Ring       = data[:,0]
        self.Fen        = data[:,1]
        self.VMM        = data[:,2]
        self.hybrid     = data[:,3]
        self.ASIC       = data[:,4]
        self.Channel    = data[:,5]
        self.ADC        = data[:,6]
        self.BC         = data[:,7]
        self.OTh        = data[:,8]
        self.TDC        = data[:,9]
        self.GEO        = data[:,10]
        self.timeCoarse = data[:,11]
        self.PulseT     = data[:,12]
        self.PrevPT     = data[:,13]
        self.G0         = data[:,14]
        self.Channel1   = data[:,15]
        self.ADC1       = data[:,16]
        self.mult0      = data[:,17]
        self.mult1      = data[:,18]

    # def list(self):
    #     print("Rings {}".format(self.Ring))
    #     print("Fens {}".format(self.Fen))
    
    def append(self, reado):
        
        self.Ring     = np.concatenate((self.Ring, reado.Ring), axis=0)
        self.Fen      = np.concatenate((self.Fen, reado.Fen), axis=0)
        self.VMM      = np.concatenate((self.VMM, reado.VMM), axis=0)
        self.hybrid   = np.concatenate((self.hybrid, reado.hybrid), axis=0)
        self.ASIC     = np.concatenate((self.ASIC, reado.ASIC), axis=0)
        self.Channel  = np.concatenate((self.Channel, reado.Channel), axis=0)
        self.ADC      = np.concatenate((self.ADC, reado.ADC), axis=0)
        self.Channel1 = np.concatenate((self.Channel1, reado.Channel1), axis=0)
        self.ADC1     = np.concatenate((self.ADC1, reado.ADC1), axis=0)
        self.timeStamp  = np.concatenate((self.timeStamp, reado.timeStamp), axis=0)
        self.BC      = np.concatenate((self.BC, reado.BC), axis=0)
        self.OTh     = np.concatenate((self.OTh, reado.OTh), axis=0)
        self.TDC     = np.concatenate((self.TDC, reado.TDC), axis=0)
        self.GEO     = np.concatenate((self.GEO, reado.GEO), axis=0)
        self.G0      = np.concatenate((self.G0, reado.G0), axis=0)
        self.PulseT  = np.concatenate((self.PulseT, reado.PulseT), axis=0)
        self.PrevPT  = np.concatenate((self.PrevPT, reado.PrevPT), axis=0)
        self.timeCoarse = np.concatenate((self.timeCoarse, reado.timeCoarse), axis=0)
        self.Durations  = np.append(self.Durations, reado.Durations)
        self.mult0     = np.concatenate((self.mult0, reado.mult0), axis=0)
        self.mult1     = np.concatenate((self.mult1, reado.mult1), axis=0)
        self.heartbeats= np.concatenate((self.heartbeats, reado.heartbeats), axis=0)
       
              
    def concatenateReadoutsInArrayForDebug(self):
        
        leng = len(self.timeStamp)
        
        readoutsArray = np.zeros((leng,19),dtype = 'int64')
        
        readoutsArray[:,0] = self.Ring
        readoutsArray[:,1] = self.Fen
        readoutsArray[:,2] = self.hybrid
        readoutsArray[:,3] = self.ASIC
        readoutsArray[:,4] = self.Channel
        readoutsArray[:,5] = self.ADC
        readoutsArray[:,6] = self.PulseT
        readoutsArray[:,7] = self.PrevPT
        readoutsArray[:,8] = self.timeStamp
        readoutsArray[:,9] = self.timeCoarse
        readoutsArray[:,10] = self.TDC
        readoutsArray[:,11] = self.G0      # G0 also for MON
        readoutsArray[:,12] = self.BC      # POS X for MON
        readoutsArray[:,13] = self.OTh     # POS Y for MON
        readoutsArray[:,14] = self.GEO     # type for MON
        readoutsArray[:,15] = self.Channel1 # for clustered mode 
        readoutsArray[:,16] = self.ADC1     # for clustered mode 
        readoutsArray[:,17] = self.mult0    # for clustered mode 
        readoutsArray[:,18] = self.mult1    # for clustered mode 
        
        return readoutsArray
    
    def sortByTimeStamps(self):
        
        indexes = self.timeStamp.argsort(kind='quicksort')
        
        self.timeStamp =  self.timeStamp[indexes]
        self.Ring      =  self.Ring[indexes]
        self.Fen       =  self.Fen[indexes]
        self.VMM       =  self.VMM[indexes]
        self.hybrid    =  self.hybrid[indexes]
        self.ASIC      =  self.ASIC[indexes]
        self.Channel   =  self.Channel[indexes]
        self.ADC       =  self.ADC[indexes]
        self.Channel1  =  self.Channel1[indexes]
        self.ADC1      =  self.ADC1[indexes]
        self.BC        =  self.BC[indexes]
        self.OTh       =  self.OTh[indexes]
        self.TDC       =  self.TDC[indexes]
        self.GEO       =  self.GEO[indexes]
        self.PulseT    =  self.PulseT[indexes]
        self.PrevPT    =  self.PrevPT[indexes]
        self.timeCoarse = self.timeCoarse[indexes]
        self.G0        =  self.G0[indexes]
        self.mult0     =  self.mult0[indexes]
        self.mult1     =  self.mult1[indexes]
        
    def calculateDuration(self):
         
         # Tstart = np.min(self.timeStamp)
         # Tstop  = np.max(self.timeStamp)
         try:
             Tstart = self.timeStamp[0]
             Tstop  = self.timeStamp[-1]
         except: 
             Tstart = 0
             Tstop  = 0
             print('\t \033[1;33mWARNING: Not able to calculate duration! (File might be empty)\033[1;37m')
             time.sleep(2)
         
         self.Durations = np.round(Tstop-Tstart, decimals = 3)
         
    def calculateTimeStampWithTDC(self,NSperClockTick,time_offset=0,time_slope=1):
        
         self.timeStamp = self.timeCoarse + VMM3A_convertCalibrate_TDC_ns(self.TDC,NSperClockTick,time_offset,time_slope).TDC_ns

    ###############

    def checkIfCalibrationMode(self):
        
        flag = False
        
        if np.any(self.G0 == 1) :
            
              flag = True
              
              qty = np.sum(self.G0 == 1)
              
              total = np.shape(self.G0)[0]
            
              print('\n\t\033[1;33mWARNING: {} calibration latency mode data found in READOUTS {}.\033[1;37m'.format(qty,total),end='')
              time.sleep(1)
             
        return flag     
    
    def checkIfClusteredMode(self):
        
        flag = False
        
        if np.any(self.G0 == 2) :
            
              flag = True
              
              qty = np.sum(self.G0 == 2)
              
              total = np.shape(self.G0)[0]
            
              print('\n\t\033[1;33mWARNING: {} clustered mode data found in READOUTS {}, whereas you selected normal hit mode!\033[1;37m'.format(qty,total),end='') 
              time.sleep(1)
             
        return flag     
    
    def checkIfNormalHitMode(self):
        
        flag = False
        
        if np.any(self.G0 == 0) :
            
              flag = True
              
              qty = np.sum(self.G0 == 0)
              
              total = np.shape(self.G0)[0]
            
              print('\n\t\033[1;33mWARNING: {} normal hit mode data found in READOUTS {}, whereas you selected clustered mode!\033[1;37m'.format(qty,total),end='')
              time.sleep(1)
             
        return flag     
    
     ###############        
            
    def removeCalibrationData(self):
        print('--> removing latency calib data from readouts ...')
        CalibData = self.G0 == 1
        self.removeData(CalibData)
        removedNum = np.sum(CalibData)
        return removedNum 
         
    def removeClusteredData(self):
        print('--> removing clustered data from readouts ...')
        ClusterData = self.G0 == 2
        self.removeData(ClusterData)
        removedNum = np.sum(ClusterData)
        return removedNum 
        
    def removeNormalHitData(self):
        print('--> removing normal hit data from readouts ...')
        NormalHitData = self.G0 == 0
        self.removeData(NormalHitData)     
        removedNum = np.sum(NormalHitData)
        return removedNum 
    
    def removeData(self, toBeRemoved):
        
        self.Ring    = self.Ring[~toBeRemoved]
        self.Fen     = self.Fen[~toBeRemoved]
        self.VMM     = self.VMM[~toBeRemoved]
        self.hybrid  = self.hybrid[~toBeRemoved]
        self.ASIC    = self.ASIC[~toBeRemoved]
        self.Channel = self.Channel[~toBeRemoved]
        self.ADC     = self.ADC[~toBeRemoved]
        self.Channel1 = self.Channel1[~toBeRemoved]
        self.ADC1     = self.ADC1[~toBeRemoved]
        self.timeStamp   = self.timeStamp[~toBeRemoved]
        self.timeCoarse  = self.timeCoarse[~toBeRemoved]
        self.BC      = self.BC[~toBeRemoved]
        self.OTh     = self.OTh[~toBeRemoved]
        self.TDC     = self.TDC[~toBeRemoved]
        self.GEO     = self.GEO[~toBeRemoved]
        self.G0      = self.G0[~toBeRemoved]
        self.PulseT  = self.PulseT[~toBeRemoved]
        self.PrevPT  = self.PrevPT[~toBeRemoved]
        self.mult0   = self.mult0[~toBeRemoved]
        self.mult1   = self.mult1[~toBeRemoved]
        
    ###############
    
    def checkChopperFreq(self):  
        
        try:
            # this extract timing from non-empty packets 
            deltaTime         = np.diff(self.PulseT - self.PulseT[0])
            indexesIsNotZero  = np.argwhere(deltaTime>0)
            deltaTimeNoTZero  = deltaTime[indexesIsNotZero]
            meanDelta         = np.mean(deltaTimeNoTZero)/1e9
            varianceDelta     = np.var(deltaTimeNoTZero)/1e9
            meanFreq          = 1/meanDelta
                
            # this extracts timing from all packets, also empty -> heartbeats 
            indexesIsNotZero2  = np.argwhere(self.heartbeats>0)
            heartbeats2        = self.heartbeats[indexesIsNotZero2]
            heartbeatsUnique   = np.unique(heartbeats2)
            
            deltaTime2         = np.diff(heartbeatsUnique - heartbeatsUnique[0])
            indexesIsNotZero3  = np.argwhere(deltaTime2>0)
            deltaTimeNoTZero3  = deltaTime2[indexesIsNotZero3]
            meanDelta2         = np.mean(deltaTimeNoTZero3)/1e9
            varianceDelta2     = np.var(deltaTimeNoTZero3)/1e9
            meanFreq2          = 1/meanDelta2
            
            if np.isnan(meanDelta):
                print('\nNo Chopper found or all data is in one single Pulse Time')
            else:
                print('\nHeartbeats Period     (all unique packets: %d)       is %.6f s (variance %.6f s) --> frequency %.3f Hz' % ((len(deltaTimeNoTZero3)+1,meanDelta2,varianceDelta2,meanFreq2)))
                print('Timing/Chopper Period (not empty unique packets: %d) is %.6f s (variance %.6f s) --> frequency %.3f Hz' % ((len(deltaTimeNoTZero)+1,meanDelta,varianceDelta,meanFreq)))
                       
        except:
    
            print('\t \033[1;33mWARNING: Unable to calculate timing/chopper frequency! \033[1;37m')
            time.sleep(2)
    
    def removeNonESSpacketsHeartbeats(self,heartbeats):
        indexesIsNotZero  = np.argwhere(heartbeats>0)
        heartbeats        = heartbeats[indexesIsNotZero[:,0]]
        return heartbeats
     
    # def removeNonESSpacketsHeartbeats(self):
    #     indexesIsNotZero = np.argwhere(self.heartbeats>0)
    #     self.heartbeats  = self.heartbeats[indexesIsNotZero[:,0]]

   
    def checkInvalidToFsInReadouts(self):
        
        NumReadouts = np.shape(self.timeStamp)[0]
        
        tempToF = self.timeStamp - self.PulseT
        
        invalidToFs = tempToF < 0
        
        invalidToFsCounter1 = np.sum(invalidToFs)
        
        invalidToFsCounter2 = 0
                  
        if invalidToFsCounter1 > 0:
            
            tempToF2 = self.timeStamp[invalidToFs] - self.PrevPT[invalidToFs]
            
            invalidToFsAgain = tempToF2 < 0
            
            invalidToFsCounter2 = np.sum(invalidToFsAgain)
            
        validToFs  = NumReadouts - invalidToFsCounter2
        validValid = NumReadouts - invalidToFsCounter1 
        validPrevP = invalidToFsCounter1 - invalidToFsCounter2 
           
        print('\n \033[1;33m\t Readouts %d: %d ToFs valid (%d valid, %d PrevPulse corrected) - invalid %d \033[1;37m' % (NumReadouts,validToFs,validValid,validPrevP,invalidToFsCounter2))
 
    
###############################################################################
###############################################################################

class checkInstrumentID():
    def __init__(self):
        
        self.FREIAID   = 72     #0x48
        self.ESTIAID   = 76     #0x4c
        self.AMORID    = 78     #0x4e
        self.TBLVMMID  = 73     #0x49
        
        self.LOKIID      = 48
        self.BMID        = 16
        self.BIFROSTID   = 52
        self.NMXID       = 68
        self.MAGICID     = 100
        self.TREXID      = 64
        self.CSPECID     = 60
        self.MIRACLESID  = 56
        self.DREAMID     = 96  #0x48
        
    def setBytesPerReadout(self,ID):
        
        # BM always 20 bytes 
   
        if ID in (self.FREIAID, self.ESTIAID, self.AMORID, self.TBLVMMID, self.NMXID, self.TREXID):
            self.bytesPerReadout = 20
            self.InstrType = 'VMM'
        elif ID == self.LOKIID:
            self.bytesPerReadout = 24
            self.InstrType = 'R5560bis'
        elif ID in (self.BIFROSTID, self.CSPECID, self.MIRACLESID):
            self.bytesPerReadout = 24
            self.InstrType = 'R5560'
        elif ID == self.BMID:
            self.bytesPerReadout = 20
            self.InstrType = 'BM'
        else:
            self.bytesPerReadout = 20
            self.InstrType = None
        
        return self.bytesPerReadout, self.InstrType
      
    def printInfoDataStream(self,ID):
        
        if ID == self.FREIAID:
             print('found FREIA data stream - VMM',end='')
        elif ID == self.ESTIAID:
             print('found ESTIA data stream - VMM',end='')
        elif ID == self.AMORID:
             print('found AMOR data stream - VMM',end='')
        elif ID == self.TBLVMMID:
             print('found TBL data stream - VMM',end='')        
        elif ID == self.TREXID:
             print('found TREX data stream - VMM',end='')
             
        elif ID == self.MIRACLESID:
             print('found MIRACLES data stream - R5560')
             print('\033[1;33m --> WARNING: only reader is supported for this data format, no plotting either analysis\033[1;37m',end='')
        elif ID == self.CSPECID:
             print('found CSPEC data stream - R5560')
             print('\033[1;33m --> WARNING: only reader is supported for this data format, no plotting either analysis\033[1;37m',end='')
        elif ID == self.BIFROSTID:
             print('found BIFROST data stream - R5560')
             print('\033[1;33m --> WARNING: only reader is supported for this data format, no plotting either analysis\033[1;37m',end='')
        elif ID == self.LOKIID:
             print('found LOKI data stream - R5560')   
             print('\033[1;33m --> WARNING: only reader is supported for this data format, no plotting either analysis, NOT SUPPORTED FOR NOW \033[1;37m',end='')
             
        elif ID == self.BMID:
                  print('found BM data stream',end='') 
            
        elif (ID == self.DREAMID) or (ID == self.MAGICID): 
             print('\033[1;33mWARNING: found DREAM or MAGIC or HEIMDAL data stream - CPIX -> not supported\033[1;37m',end='')
             time.sleep(2)
        else:
             print('found some other data stream',end='')
             
        
#################################################  

class  checkWhich_RingFenHybrid_InFile():
    def __init__(self, filePathAndFileName, NSperClockTick):
                
        pcap = pcapng_reader(filePathAndFileName, NSperClockTick, timeResolutionType = 'coarse', sortByTimeStampsONOFF = False)
        self.readouts = pcap.readouts
        
        temp = os.path.split(filePathAndFileName)
        # filePath = temp[0]+'/'
        self.fileName = temp[1]

    def check(self):
        
        print("\nRings, Fens and Hybrids in file: {}".format(self.fileName))
        
        RingsInFile = np.unique(self.readouts.Ring)
        
        cont = 0 
        
        for RR in RingsInFile:
            
            # self.RFH['Ring'] = RR
            
            selectRING = self.readouts.Ring == RR
            
            Fens4Ring    = self.readouts.Fen[selectRING]
            Hybrids4Ring = self.readouts.hybrid[selectRING]
            
            FensInRing = np.unique(Fens4Ring)
            
            for FF in FensInRing:
                
                selectFEN = Fens4Ring == FF
                
                Hybrids4Fen = Hybrids4Ring[selectFEN]
                
                HybridsInFen = np.unique(Hybrids4Fen)
                
                for HH in HybridsInFen:
                    
                    cont += 1
                
                    print("\tNo. {}:     Ring {}, Fen {}, Hybrid {}".format(cont,int(RR),int(FF),int(HH)))

           
        
#################################################   
class R5560():
    def __init__(self, buffer, NSperClockTick):
        
        # valid for MIRACLES, BIFROST and  CSPEC -- NOT LOKI!  
         
        # decode into little endian integers
        PhysicalRing = int.from_bytes(buffer[0:1], byteorder='little')
        self.Fen     = int.from_bytes(buffer[1:2], byteorder='little')
        self.Length  = int.from_bytes(buffer[2:4], byteorder='little')
        timeHI       = int.from_bytes(buffer[4:8], byteorder='little')
        timeLO       = int.from_bytes(buffer[8:12], byteorder='little')
        
        tube         = int.from_bytes(buffer[13:14], byteorder='little')
        counter1     = int.from_bytes(buffer[14:16], byteorder='little')
        ampA         = int.from_bytes(buffer[16:18], byteorder='little')
        ampB         = int.from_bytes(buffer[18:20], byteorder='little')
        counter2     = int.from_bytes(buffer[20:24], byteorder='little')
        
        
        self.BC      = 0
        self.TDC     = 0
        self.VMM     = 0
        self.Channel = 0
        
        
        self.ADC      = ampA
        
        self.Channel1 = 0
        self.ADC1     = ampB
        
        
        self.mult0    = -1
        self.mult1    = -1
        
        #######################
        #  IMPORTANT NOTE: phys ring is 0 and 1 for logical ring 0 etc. Always 12 logical rings 
        self.Ring = int(np.floor(PhysicalRing/2))
        # self.Ring = PhysicalRing
        #######################

        self.OTh      = 1

        # self.G0       = G0GEO >> 7
        modes         = VMM3A_modes(buffer)
        self.G0       = 0
        
        self.GEO      = 0
        
        self.ASIC     = 1        #extract only LSB
        self.hybrid   = tube     #extract only 1110 and shift right by one 

        
        timeHIns = int(round(timeHI * 1000000000))
        timeLOns = int(round(timeLO * NSperClockTick))
        
        self.timeCoarse  = timeHIns + timeLOns
        
#################################################

class MONdata():
    def __init__(self, buffer, NSperClockTick):
          
       # decode into little endian integers
       PhysicalRing = int.from_bytes(buffer[0:1], byteorder='little')
       self.Fen     = int.from_bytes(buffer[1:2], byteorder='little')
       self.Length  = int.from_bytes(buffer[2:4], byteorder='little')
       timeHI       = int.from_bytes(buffer[4:8], byteorder='little')
       timeLO       = int.from_bytes(buffer[8:12], byteorder='little')
       self.Type    = int.from_bytes(buffer[12:13], byteorder='little')
       self.Channel = int.from_bytes(buffer[13:14], byteorder='little')
       self.ADC     = int.from_bytes(buffer[14:16], byteorder='little')
       self.posX    = int.from_bytes(buffer[16:18], byteorder='little')
       self.posY    = int.from_bytes(buffer[18:20], byteorder='little')
       
       #######################
       #  IMPORTANT NOTE: phys ring is 0 and 1 for logical ring 0 etc. Always 12 logical rings 
       self.Ring = int(np.floor(PhysicalRing/2))
       # self.Ring = PhysicalRing
       #######################

       timeHIns = int(round(timeHI * 1000000000))
       timeLOns = int(round(timeLO * NSperClockTick))
       
       self.timeCoarse  = timeHIns + timeLOns 
 
#################################################

class VMM3A_modes():
    def __init__(self, buffer):
        
        self.G0 = -1
        
        # hybrid   = int.from_bytes(buffer[17:18], byteorder='little')
        
        G0GEO   = int.from_bytes(buffer[16:17], byteorder='little')
    
        temp  = (G0GEO & 0xC0) >> 6     #extract only first two MSB and shift right by 6
        
        geoBit6 = (temp & 0x1)          #bit 6 - if 0 either calib or normal mode, if 1 clustered mode 
        geoBit7 = (temp & 0x2) >> 1     #bit 7 - if 1 calib or 0 normal mode, if bit 6 is 0
        
        if geoBit6 == 1:
            # print('clustered mode')
            self.G0 = 2
        elif geoBit6 == 0:
            if geoBit7 == 1: 
                # print('calibration mode')
                self.G0 = 1
            elif geoBit7 == 0: 
                # print('normal hit mode')
                self.G0 = 0
                
        # self.G0 =  geoBit7      


class VMM3Aclustered():
    def __init__(self, buffer, NSperClockTick):
                 
        # decode into little endian integers
        PhysicalRing = int.from_bytes(buffer[0:1], byteorder='little')
        self.Fen     = int.from_bytes(buffer[1:2], byteorder='little')
        self.Length  = int.from_bytes(buffer[2:4], byteorder='little')
        timeHI       = int.from_bytes(buffer[4:8], byteorder='little')
        timeLO       = int.from_bytes(buffer[8:12], byteorder='little')
        
        ADC0temp    = int.from_bytes(buffer[12:14], byteorder='little')
        ADC1temp    = int.from_bytes(buffer[14:16], byteorder='little')
        
        # self.ADC      = int.from_bytes(buffer[12:14], byteorder='little')
        # self.ADC1     = int.from_bytes(buffer[14:16], byteorder='little')
        G0GEO         = int.from_bytes(buffer[16:17], byteorder='little')
        self.hybrid   = int.from_bytes(buffer[17:18], byteorder='little')
        self.Channel  = int.from_bytes(buffer[18:19], byteorder='little')
        self.Channel1 = int.from_bytes(buffer[19:20], byteorder='little')
        
        #######################
        #  IMPORTANT NOTE: phys ring is 0 and 1 for logical ring 0 etc. Always 12 logical rings 
        self.Ring = int(np.floor(PhysicalRing/2))
        # self.Ring = PhysicalRing
        #######################

        self.ADC      = ADC0temp & 0x1FFF  #extract only 13 LSB
        self.ADC1     = ADC1temp & 0x1FFF  #extract only 13 LSB
        
        self.mult0    = (ADC0temp & 0xE000) >> 13 #extract only 3 MSB
        self.mult1    = (ADC1temp & 0xE000) >> 13 #extract only 3 MSB
        
        modes         = VMM3A_modes(buffer)
        self.G0       = modes.G0

        self.GEO      = G0GEO & 0x3F
        
        timeHIns = int(round(timeHI * 1000000000))
        timeLOns = int(round(timeLO * NSperClockTick))

        self.timeCoarse  = timeHIns + timeLOns
        
        self.VMM  = -1
        self.ASIC = -1
        self.BC   = -1
        self.OTh  = 1
        self.TDC  = 0
        
   
class VMM3A():
    def __init__(self, buffer, NSperClockTick):
                 
        # decode into little endian integers
        PhysicalRing = int.from_bytes(buffer[0:1], byteorder='little')
        self.Fen     = int.from_bytes(buffer[1:2], byteorder='little')
        self.Length  = int.from_bytes(buffer[2:4], byteorder='little')
        timeHI       = int.from_bytes(buffer[4:8], byteorder='little')
        timeLO       = int.from_bytes(buffer[8:12], byteorder='little')
        self.BC      = int.from_bytes(buffer[12:14], byteorder='little')
        OTADC        = int.from_bytes(buffer[14:16], byteorder='little')
        G0GEO        = int.from_bytes(buffer[16:17], byteorder='little')
        self.TDC     = int.from_bytes(buffer[17:18], byteorder='little')
        self.VMM     = int.from_bytes(buffer[18:19], byteorder='little')
        self.Channel = int.from_bytes(buffer[19:20], byteorder='little')
        
        self.Channel1 = -1
        self.ADC1     = -1
        self.mult0    = -1
        self.mult1    = -1
        
        #######################
        #  IMPORTANT NOTE: phys ring is 0 and 1 for logical ring 0 etc. Always 12 logical rings 
        self.Ring = int(np.floor(PhysicalRing/2))
        # self.Ring = PhysicalRing
        #######################

        self.ADC      = OTADC & 0x3FF  #extract only 10 LSB
        self.OTh      = OTADC >> 15    #extract only 1 MSB

        # self.G0       = G0GEO >> 7
        modes         = VMM3A_modes(buffer)
        self.G0       = modes.G0
        
        self.GEO      = G0GEO & 0x3F
        
        self.ASIC     =  self.VMM & 0x1           #extract only LSB
        self.hybrid   = (self.VMM & 0xE) >> 1     #extract only 1110 and shift right by one 
        
        timeHIns = int(round(timeHI * 1000000000))
        timeLOns = int(round(timeLO * NSperClockTick))
        
        self.timeCoarse  = timeHIns + timeLOns
       

class VMM3A_convertCalibrate_TDC_ns(): 
    def __init__(self,TDC,NSperClockTick,time_offset=0,time_slope=1):
                
        # self.TDC = TDC
        # self.NSperClockTick = NSperClockTick
   
        self.pTAC = 60    #  in ns
        
    # def convert_ns(self):
        
    #     self.calibrate(time_offset=0, time_slope=1)
        
    # def calibrate(self,time_offset,time_slope):
        
         # time_offset in ns, time_slope adimensional
        
        aboveLimit = TDC > 255
        belowLimit = TDC < 0 
        
        if np.any(aboveLimit == True):
            TDC[aboveLimit] = 255
        elif np.any(belowLimit == True):
            TDC[belowLimit] = 0
        
        TDC_ns = np.around( ( (NSperClockTick*2*1.5 - TDC*self.pTAC/255 - time_offset) * time_slope ) )

        self.TDC_ns = TDC_ns.astype('int64')
        
        
class VMM3A_calibrate_ADC():  
    def __init__(self,ADC,ADC_offset=0,ADC_slope=1):      
            
        # accepts either arrays or single scalars as ADC 
        
        ADC_calibrated = np.around(( ADC - ADC_offset ) * ADC_slope)
        
        aboveLimit = ADC_calibrated > 1023
        belowLimit = ADC_calibrated < 0
        
        if type(ADC) is int:
            
            if aboveLimit == True:
                ADC_calibrated = 1023
            elif belowLimit == True:
                ADC_calibrated = 0
           
            self.ADC_calibrated  = int(ADC_calibrated)
                
        else:            
            if np.any(aboveLimit == True):
                ADC_calibrated[aboveLimit] = 1023
            elif np.any(belowLimit == True):
                ADC_calibrated[belowLimit] = 0
                
            self.ADC_calibrated  = ADC_calibrated.astype('int64')
            
        
 
        
        
###############################################################################
###############################################################################
        

class checkIfFileExistInFolder():
     def __init__(self, filePathAndFileName):
         
          if os.path.exists(filePathAndFileName) is False:
            temp2 = os.path.split(filePathAndFileName)
            filePath = temp2[0]+'/'
            fileName = temp2[1]
            print('\n \033[1;31m---> File: '+fileName+' DOES NOT EXIST \033[1;37m')
            print('\n ---> in folder: '+filePath+' \n')
            print('\n NOTE: file name must contain extension, e.g. *.pcapng\n')
            print(' ---> Exiting ... \n')
            print('------------------------------------------------------------- \n')
            sys.exit()
            
################################################## 

class pcapng_reader():
    def __init__(self, filePathAndFileName, NSperClockTick, MONtype = 'RING' , MONring = 11, timeResolutionType = 'fine', sortByTimeStampsONOFF = True, operationMode = 'normal', pcapLoadingMethod='allocate'):
        
        # try:
            # print('PRE-ALLOC method to load data ...')
        pcapng = pcapng_reader_PreAlloc(NSperClockTick,MONtype,MONring,filePathAndFileName,timeResolutionType,operationMode, kafkaStream = False)
        pcapng.allocateMemory(pcapLoadingMethod)
        pcapng.read()
        self.readouts = pcapng.readouts

        # except:
        #     # print('\n... PRE-ALLOC method failed, trying APPEND method to load data ...')
        #     print('\n\033[1;31m... PRE-ALLOC method failed, exiting ...\033[1;37m')
            
        #     sys.exit()
            
            #  HERE IS FUTURE DEVEL IF NEEDED 
            # self.pcapng = pcapng_reader_slowAppend(filePathAndFileName)
            # self.pcapng.read(timeResolutionType)
            # self.readouts = self.pcapng.readouts    
            
        # finally:
             
        if sortByTimeStampsONOFF is True:

                  print('Readouts are sorted by TimeStamp')
                 
                  self.readouts.sortByTimeStamps()
                 
            
        else:
                
                 print('Readouts are NOT sorted by TimeStamp')
                
        self.readouts.calculateDuration()     
                        
##################################################  

class pcapng_reader_PreAlloc():
    def __init__(self, NSperClockTick, MONtype, MONring, filePathAndFileName = '', timeResolutionType = 'fine', operationMode = 'normal', kafkaStream = False):
        
        # self.timeResolution = 11.25e-9  #s per tick for 88.888888 MHz
        # self.timeResolution = 11.356860963629653e-9  #s per tick ESS for 88.0525 MHz
        
        self.NSperClockTick      = NSperClockTick 
        self.MONtype             = MONtype
        self.MONring             = MONring
        self.timeResolutionType  = timeResolutionType
        self.kafkaStream         = kafkaStream

        # print('----->>>'+(self.timeResolutionType))
        
        # operation mode is either normal hit or clustered mode
        # in normal hit G0 is 0 and 1 for calib mode, or G0 is 2 for clustered mode 
        self.operationMode       = operationMode
        
        ##########################################################
        
        self.debug = False
        
        self.removeremoveOtherDataTypesONOFF = True
 
        self.readouts = readouts()
        
        ##########################################################
        
        if self.kafkaStream is False:
            self.filePathAndFileName = filePathAndFileName
            
            checkIfFileExistInFolder(self.filePathAndFileName)
            
            temp2 = os.path.split(filePathAndFileName)
            fileName = temp2[1]
            
            self.fileSize   = os.path.getsize(self.filePathAndFileName) #bytes
            print('{} is {} kbytes'.format(fileName,self.fileSize/1000))
            
            self.mainHeaderSize  = 42  #bytes only if pcap file otherise from kafka this is 0 
            
        else:    
            
            self.stepsForProgress = 1
            self.mainHeaderSize   = 0
    
        ##########################################################
        
        self.readoutsPerPacket   = 446 #packets NOT USED here and dinamically recalcualted in extractfrombytes but used as a default to init kafka 
        self.ESSheaderSize       = None  # 30 bytes if version is 0  or 32 bytes if version is 1   
        self.headerSize          = None  # self.mainHeaderSize+self.ESSheaderSize #bytes  (72 if mainHeaderSize = 42)
        self.singleReadoutSize   = 20  # bytes, dinamically recalcualted in extractfrombytes but used as a default to init kafka 
 
        self.InstrType = None
    
       ##########################################################
        
        self.counterPackets           = 0
        self.counterCandidatePackets  = 0
        self.counterValidESSpackets   = 0
        self.counterNonESSpackets     = 0
        self.counterEmptyESSpackets   = 0
        self.totalReadoutCount        = 0  
        self.overallDataIndex         = 0 
        self.preallocLength           = 0   
        
        self.data = np.zeros((self.preallocLength,19), dtype='int64')
        
        ##########################################################
        
        if self.MONtype == "LEMO" :
            if self.MONring < 11:
                print('\n\t\033[1;31mERROR: MON mode {} selected with RING < 11 (can be any ring 11 - inf, but not < 11)-> check config file! ---> Exiting ... \n\033[1;37m'.format(self.MONtype),end='') 
                sys.exit()
        
        if self.MONtype == "RING" : 
            if self.MONring != 11:
                print('\n\t\033[1;31mERROR: MON mode {} selected with RING != 11 (must be ring 11) -> check config file! ---> Exiting ... \n\033[1;37m'.format(self.MONtype),end='') 
                sys.exit()

        if self.MONtype == "LEMO" or self.MONtype == "RING" : 
            pass
        else:
            print('\n\t\033[1;31mERROR: MON mode (found {}) can only be either LEMO or RING  -> check config file! ---> Exiting ... \n\033[1;37m'.format(self.MONtype),end='') 
            sys.exit()
        ##########################################################
        
    def calculateHeaderSize(self):
        self.headerSize  = self.mainHeaderSize+self.ESSheaderSize #bytes  (72 if mainHeaderSize = 42 and 74 if version 1)
        
    def extractFWversion(self,packetData,indexESS):
        version = int.from_bytes(packetData[indexESS-1:indexESS], byteorder='little') # bytes 
        return version

    def extractInstrID(self,packetData,indexESS):
        ID = int.from_bytes(packetData[indexESS+3:indexESS+4], byteorder='little') # 
        return ID
    
    def checkFWversionSetHeaders(self,packetsFWversion):
        
        print('\nchecking RMM firmware version ',end='')
        try:
            if np.any(packetsFWversion != packetsFWversion[0]):
                print('\n \033[1;31mWARNING ---> found different Firmware Versions in packets, use version 0 as default, data might be corrupted for other versions\033[1;37m')
                time.sleep(1)
            else:
                print('--> version: {}'.format(packetsFWversion[0]))   
        except: 
             print('--> unable to verify version.')   
             pass
        
        self.ESSheaderSize = 30  # 30 bytes if version is 0  or 32 bytes if version is 1   
        self.calculateHeaderSize()
        
        # packetsFWversion = np.atleast_1d(packetsFWversion)
        try:
            if packetsFWversion[0] == 0:
                    self.ESSheaderSize = 30  # 30 bytes if version is 0  or 32 bytes if version is 1   
                    self.calculateHeaderSize()  
                    
            elif packetsFWversion[0] >= 1:
                    self.ESSheaderSize = 32  # 30 bytes if version is 0  or 32 bytes if version is >= 1    
                    self.calculateHeaderSize()
        except:
            pass
     
    def checkInstrIDsetReadoutSize(self,packetsInstrIDs):    
        
        packetsInstrIDs = np.atleast_1d(packetsInstrIDs)
        print('checking intrument ID ... ',end='')
        
        # print(packetsInstrIDs)
        try:
                
            packetsInstrIDsunique = np.unique(packetsInstrIDs)
            
            is_single_stream     = (len(packetsInstrIDsunique) == 1)
            is_valid_dual_stream = (len(packetsInstrIDsunique) == 2 and (checkInstrumentID().BMID in packetsInstrIDsunique))
            
            #  there must be only 2 data streams, intrum and BM, if there is more then Warning! 
            
            if len(packetsInstrIDsunique) == 0:
                print('\n---> no instr ID', end='')
            
            elif is_single_stream or is_valid_dual_stream:
 
                for ids in packetsInstrIDsunique:
                    print('\n---> ', end='')
                    checkInstrumentID().printInfoDataStream(ids)
                
                # Dynamically update readout size (using first packet as reference)
                self.singleReadoutSize, _ = checkInstrumentID().setBytesPerReadout(packetsInstrIDs[0])
            
            else:
                # Handle all Warning cases (3+ IDs, or 2 IDs without BM)
                print('\n\033[1;31mWARNING ---> unexpected instrument ID versions found. Data might be corrupted - check RMM output queue config!\033[1;37m',end='')
                
                for ids in packetsInstrIDsunique:
                    print('\n---> ', end='')
                    checkInstrumentID().printInfoDataStream(ids)
                    
                self.singleReadoutSize, _ = checkInstrumentID().setBytesPerReadout(packetsInstrIDs[0])
 
        except: 
             print('--> unable to verify data format version.')   
             pass

        
    def checkTimeSrc(self, timeSourceBytes):
 
            # NOTE for now upper 4 bits unused 
            
            # print('timeSrc: {} {} {}'.format(timeSourceBytes,hex(timeSourceBytes),bin(timeSourceBytes)  ))
          
            # timeSourceBytes = int.from_bytes(timeSourceBytes, byteorder='little') # bytes 
          
          bit0 = (timeSourceBytes & 0x1) 
          bit1 = (timeSourceBytes & 0x2) >> 1
          bit2 = (timeSourceBytes & 0x4) >> 2
          bit3 = (timeSourceBytes & 0x8) >> 3

          if bit0 == 0:
              src = 'MRF timestamp'
          elif bit0 == 1:
              src = 'local timestamp'
          
          if bit1 == 0:
              iss = 'MRF sync'
          elif bit1 == 1:
              iss = 'local sync'
          
          if bit2 == 0:
              sm = 'internal'
          elif bit2 == 1:
              sm = 'external (TTL)'
              
          if bit3 == 0:
              status = 'OK'
          elif bit3 == 1:
              status = 'Error'

          print("checking time source --> source: {}, internal sync source: {}, sync method: {}, status: {}".format(src,iss,sm,status))
          # return tsrc
      
        
    def checkIP(self, IPBytes):

                IPlen   = 20
                # portLen = 8
                
                indexIPstart = IPlen-8

                IPSourcebytes  = int.from_bytes(IPBytes[indexIPstart:indexIPstart+4], byteorder='big') 
                IPDestbytes    = int.from_bytes(IPBytes[indexIPstart+4:indexIPstart+8], byteorder='big') 
                
                
                IPSource = ipaddress.IPv4Address(IPSourcebytes)
                IPDest   = ipaddress.IPv4Address(IPDestbytes)
                
                indexUDPstart = IPlen
                   
                portSource  = int.from_bytes(IPBytes[indexUDPstart:indexUDPstart+2], byteorder='big') 
                portDest    = int.from_bytes(IPBytes[indexUDPstart+2:indexUDPstart+4], byteorder='big') 
                
           
                print("checking IP (ports)  --> source: {} ({}), dest: {} ({})".format(IPSource,portSource,IPDest,portDest))    

    def dprint(self, msg):
        if self.debug:
            print("{}".format(msg))

    def allocateMemory(self, pcapLoadingMethod='allocate'):  
        
        # NOTE IMPORTANT: when load method is quick the check of FW version and data format 
        # is done only on the first packet and not all of them !!!! 
        
        self.pcapLoadingMethod = pcapLoadingMethod
        
        if (self.pcapLoadingMethod != 'allocate') and (self.pcapLoadingMethod != 'quick') :
            print('\033[1;33mWARNING: Wrong data loading option: select either quick or allocate --> setting it to allocate method!\033[1;37m')
            self.pcapLoadingMethod = 'allocate'
            
        if self.pcapLoadingMethod == 'allocate':
            endCounter = np.inf
            print('pcap loading method: allocate')
        elif self.pcapLoadingMethod == 'quick':
            endCounter = 2
            print('pcap loading method: quick \033[1;33m---> WARNING: when load method is quick the check of FW version and data format is done only on the first packet and not all of them.\033[1;37m')    

        
        print('allocating memory...',end='')
        
        ff = open(self.filePathAndFileName, 'rb')
        scanner = pg.FileScanner(ff)
        
        packetsSizes       = np.zeros((0),dtype='int64')
        packetsFWversion   = np.zeros((0),dtype='int64')
        packetsInstrID     = np.zeros((0),dtype='int64')
        
        counter = 0
        
        for block in scanner:
            
            if counter <= endCounter:
            
                counter+=1
    
                if counter == 4 or np.mod(counter,5000) == 0:
                    print('.',end='')
        
                self.counterPackets += 1
                self.dprint("packet {}".format(self.counterPackets))
        
                try:
                    packetSize = block.packet_len
                    self.dprint("packetSize {} bytes".format(packetSize))
                    
                    packetData = block.packet_data
                    
                    indexESS   = packetData.find(b'ESS')
 
                    if indexESS != -1:
                        
                       FWversionTemp = self.extractFWversion(packetData, indexESS)
                       instrIDtemp   = self.extractInstrID(packetData, indexESS)

                except:
                    self.dprint('--> other packet found No. {}'.format(self.counterPackets-self.counterCandidatePackets))
                else:
                    self.counterCandidatePackets += 1

                    packetsSizes     = np.append(packetsSizes,packetSize)
                    try:
                        packetsFWversion  = np.append(packetsFWversion,FWversionTemp)
                        packetsInstrID    = np.append(packetsInstrID,instrIDtemp)
                    except:
                        # print('this data does not contain FW version')
                        pass
      
        self.dprint('counterPackets {}, counterCandidatePackets {}'.format(self.counterPackets,self.counterCandidatePackets))    
        
        # self.checkIfUniformFWversion(packetsFWversion)
        self.checkFWversionSetHeaders(packetsFWversion)

        self.checkTimeSrc(packetData[indexESS+7])
        
        if self.kafkaStream is False:
             self.checkIP(packetData[indexESS-2-8-20:indexESS-2])

        self.checkInstrIDsetReadoutSize(packetsInstrID)

        if self.debug:
            overallSize = np.sum(packetsSizes)
            self.dprint('overallSize {} bytes'.format(overallSize))

        numOfReadoutsInPackets = (packetsSizes - self.headerSize)/self.singleReadoutSize  #in principle this is 446 for every packet
        
        
        if self.pcapLoadingMethod == 'allocate':
            # #  if negative there was a non ESS packetso length < 72bytes 
            # #  and if much bigger wee anyhowallocate morethan needed and remove zeros aftyerwards at the end 
            numOfReadoutsTotal = np.sum(numOfReadoutsInPackets[ numOfReadoutsInPackets >= 0])
        
        elif self.pcapLoadingMethod == 'quick':
            numOfReadoutsTotal  = self.fileSize/self.singleReadoutSize
            # need to initialize the counters even if the are quite off, but it gives an upper limit then will be overwritten after read  
            self.counterCandidatePackets = int(round(numOfReadoutsTotal))
            self.counterPackets          = self.counterCandidatePackets
     
        self.preallocLength = int(round(numOfReadoutsTotal))
        self.dprint('preallocLength {}'.format(self.preallocLength))
        
        ff.close()
                
        
    def read(self):   
        
        print('\n',end='')
        
        self.data = np.zeros((self.preallocLength,19), dtype='int64') 
        
        self.readouts.heartbeats = np.zeros((self.counterCandidatePackets), dtype='int64') 
        
        ff = open(self.filePathAndFileName, 'rb')
        scanner = pg.FileScanner(ff)
        
        self.overallDataIndex = 0 
        
        self.stepsForProgress = int(self.counterCandidatePackets/5)+1  # 4 means 25%, 50%, 75% and 100%
        
        indexPackets = 0 
        
        for block in scanner:
            
            try:
                
                packetLength = block.packet_len
                packetData   = block.packet_data
                   
                
                # ### to write file from pcapr 
                # cont =+1 
                
                # if cont == 1 :
                #     # print(packetData)
                #     with open('/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/lib/outputBin2', 'wb') as f: 
                #         f.write(packetData)
                        
                # else:
                #     with open('/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/lib/outputBin2', 'ab') as f: 
                #         f.write(packetData) 
                
                
            except:
                self.dprint('--> other packet found')
                
            else:
                self.extractFromBytes(packetData,packetLength,indexPackets,debugMode = self.debug)
                indexPackets += 1
         
        print('[100%]',end=' ') 

        self.dprint('\n All Packets {}, Candidates for Data {} --> Valid ESS {} (empty {}), NonESS  {} '.format(self.counterPackets , self.counterCandidatePackets,self.counterValidESSpackets ,self.counterEmptyESSpackets,self.counterNonESSpackets))
             
        #######################################################       
             
        # here I remove  the rows that have been preallocated but no filled in case there were some packets big but no ESS
        if self.preallocLength > self.totalReadoutCount:
            
            datanew = np.delete(self.data,np.arange(self.totalReadoutCount,self.preallocLength),axis=0)
            print('removing extra allocated length not used ...',end='') 
            
        elif self.preallocLength < self.totalReadoutCount:
            print('something wrong with the preallocation: allocated length {}, total readouts {}'.format(self.preallocLength,self.totalReadoutCount))
            sys.exit()
       
        elif self.preallocLength == self.totalReadoutCount:
            
            datanew = self.data
        
        cz = checkIfDataHasZeros(datanew)
        datanew = cz.dataOUT
        
        self.readouts.transformInReadouts(datanew)
        
        # self.readouts.heartbeats = self.heartbeats
        # print(self.readouts.heartbeats)
        
        # self.readouts.removeNonESSpacketsHeartbeats()
        
        # print(self.readouts.heartbeats)
        
        ############
        
        self.checkTimeSettings()
          
        self.timeAdjustedWithResolution()
        
        ############

        
        # we overwrite the excess estimate of packets by the right amount 
        if self.pcapLoadingMethod == 'quick':
           self.counterCandidatePackets = self.counterValidESSpackets  +  self.counterNonESSpackets  
           self.counterPackets          = self.counterCandidatePackets 
                
        
        # print('\ndata loaded - found {} readouts - Packets: all {} (candidates {}) --> valid ESS {} (of which empty {}), nonESS {}'.format(self.totalReadoutCount, self.counterPackets,self.counterCandidatePackets,self.counterValidESSpackets ,self.counterEmptyESSpackets,self.counterNonESSpackets))    

        print('\ndata loaded - found {} readouts - Packets: all {} --> valid ESS {} (of which empty {}), nonESS {}'.format(self.totalReadoutCount, self.counterCandidatePackets,self.counterValidESSpackets ,self.counterEmptyESSpackets,self.counterNonESSpackets))    

        ############
        
        self.removeOtherDataTypes(removeONOFF=self.removeremoveOtherDataTypesONOFF)
        
        ff.close()
        
    def checkTimeSettings(self):
        
        if self.operationMode == 'normal' or self.operationMode == 'clustered':
            
            pass

        else:
            
            print('\n\t\033[1;31mERROR: Operation mode (found {}) not set either to normal or clustered ---> Exiting ... \n\033[1;37m'.format(self.operationMode),end='') 
            sys.exit()  
            
        if self.timeResolutionType == 'fine' or self.timeResolutionType == 'coarse':
                
            pass

        else:
                
            print('\n\t\033[1;31mERROR: Time resolution (found {}) not set either to fine or coarse ---> Exiting ... \n\033[1;37m'.format(self.operationMode),end='') 
            sys.exit()      
        
    def timeAdjustedWithResolution(self):
        
        # self.readouts.calculateTimeStamp(self.NSperClockTick)
        if self.operationMode == 'normal':
            if self.timeResolutionType == 'fine':
                self.readouts.calculateTimeStampWithTDC(self.NSperClockTick)
            elif self.timeResolutionType == 'coarse':
                self.readouts.timeStamp = self.readouts.timeCoarse       
        elif self.operationMode == 'clustered': 
            # tere is no time fine in clustered mode is already one sigle time 
                    self.readouts.timeStamp = self.readouts.timeCoarse

    def removeOtherDataTypes(self,removeONOFF=True):
        
        flag = self.readouts.checkIfCalibrationMode() 
        if flag is True: 
           if removeONOFF == True:
              removedNum = self.readouts.removeCalibrationData()
              print('removed {} calibration readouts --> readouts left {}'.format(removedNum,self.totalReadoutCount-removedNum)) 
              self.totalReadoutCount = self.totalReadoutCount-removedNum
                  
                  
        if self.operationMode == 'normal':
 
            flag = self.readouts.checkIfClusteredMode()
            if flag is True: 
               if removeONOFF == True:
                  removedNum = self.readouts.removeClusteredData()
                  print('removed {} normal readouts --> readouts left {}'.format(removedNum,self.totalReadoutCount-removedNum))
                  self.totalReadoutCount = self.totalReadoutCount-removedNum
                
        elif self.operationMode == 'clustered': 
                 
              flag = self.readouts.checkIfNormalHitMode()
              if flag is True: 
                 if removeONOFF == True:
                    removedNum = self.readouts.removeNormalHitData()
                    print('removed {} clustered readouts --> readouts left {}'.format(removedNum,self.totalReadoutCount-removedNum))
                    self.totalReadoutCount = self.totalReadoutCount-removedNum
      
        
    def extractPulseTime(self,packetData,indexESS):
        
        ESSlength  = int.from_bytes(packetData[indexESS+4:indexESS+6], byteorder='little') # bytes 
        
        PulseThigh = int.from_bytes(packetData[indexESS+8:indexESS+12], byteorder='little')*1000000000
        PulseTlow  = int.from_bytes(packetData[indexESS+12:indexESS+16], byteorder='little')*self.NSperClockTick 
        PrevPThigh = int.from_bytes(packetData[indexESS+16:indexESS+20], byteorder='little')*1000000000
        PrevPTlow  = int.from_bytes(packetData[indexESS+20:indexESS+24], byteorder='little')*self.NSperClockTick 
        
        #  IMPORTANT if you do int round after sum is off, needs to be done before then sum hi and low
        PulseThighR = int(round(PulseThigh))
        PulseTlowR  = int(round(PulseTlow))
        PrevPThighR = int(round(PrevPThigh))
        PrevPTlowR  = int(round(PrevPTlow))
        
        PulseT = PulseThighR + PulseTlowR
        PrevPT = PrevPThighR + PrevPTlowR
        
        return PulseT, PrevPT, ESSlength
        
        
    def extractFromBytes(self,packetData,packetLength,indexPackets,debugMode=False):
        
        # ICMP packet has ESS data in it but must be discarded 
        # the ICMP protocal adds 28 bytes 
        ICMPbyteExtraLength = 28 
        ICMPflag            = False 
  
        indexESS = packetData.find(b'ESS') # index of(cookie) ESS = 0x 45 53 53 it is always 44 with pcap 
        
        self.dprint('index where ESS word starts {}'.format(indexESS))
        #  it should be always 44 = 42+2
     
        if indexESS == -1:
           # this happens if it not an ESS packet 
           self.counterNonESSpackets += 1
           
        else: 
            # there is an ESS packet but i can still be empty, i.e. 72 bytes only
           self.counterValidESSpackets += 1
           
           if self.counterValidESSpackets == 1:
                   
               print('loading ... [0%]',end=' ')    
         
               
           # print('---')
           # print('indexESS '+str(indexESS))    
           # print('header '+str(self.ESSheaderSize))
           # print('full header '+str(self.headerSize))
    
           indexDataStart = self.ESSheaderSize +( indexESS - 2 )   # index after (cookie) ESS = 0x 45 53 53 where data starts (eg 44+30-2=72 or 44+32-2=74 )

           # print('data starts at: '+str(indexDataStart))

           #   give a warning if not 72 or 74,  check that ESS cookie is always in the same place
           if indexDataStart != self.headerSize:
               print('\n \033[1;33mWARNING ---> ESS cookie is not in position! Data does not start at byte 72 or 74 or 42 or 44! ... \033[1;37m')
               
               if (indexDataStart == self.headerSize + ICMPbyteExtraLength):
                   # this is the case where the packet is sent instead of UDP but as a ping from RMM ICMP message -> need to skip this package 
                   print(' \033[1;33m    ... ---> ICMP packet found in data -> skipping packet. \033[1;37m')
                   ICMPflag = True
               else:
                   print(' \033[1;31m    ... ---> this packet is not a ICMP packet that can be skipped, DATA MIGHT BE CORRUPTED. \033[1;37m')
                   time.sleep(2)
           
           # if the packet is a good packet then...
           if ICMPflag == False:
               # dinamically change readoutsize 20 or 24 bytes 
               self.singleReadoutSize, self.InstrType = checkInstrumentID().setBytesPerReadout(self.extractInstrID(packetData,indexESS))             
               
               readoutsInPacket = (packetLength - indexDataStart) / self.singleReadoutSize
               # or alternatively
               # readoutsInPacket = (ESSlength - self.ESSheaderSize) / self.singleReadoutSize
               
               if (packetLength - indexDataStart) == 0: #empty packet 72 bytes 
                   
                   self.counterEmptyESSpackets += 1
                   self.dprint('empty packet No. {}'.format(self.counterEmptyESSpackets))
                   
                   PulseT, _, _  = self.extractPulseTime(packetData,indexESS)
    
               else:
                   
                   if readoutsInPacket.is_integer() is not True:
                       print('\n \033[1;31mWARNING ---> something wrong with data bytes dimensions \033[1;37m')
                       time.sleep(2)
                   else:
                       
                       # only read header if there is no emplty packet
                       PulseT, PrevPT, ESSlength  = self.extractPulseTime(packetData,indexESS)
                     
                       # ESSlength is only 30 if the packet is an ESS packet but empty= 72-42 =30
                       self.dprint('ESS packet length {} bytes, packetLength {} bytes, readouts in packet {}'.format(ESSlength, packetLength,readoutsInPacket))  
                   
                       readoutsInPacket = int(readoutsInPacket)
                       self.totalReadoutCount += readoutsInPacket
                       
                       for currentReadout in range(readoutsInPacket):
                           
                       # for currentReadout in range(1):
                           
                           self.overallDataIndex += 1 
                       
                           indexStart = indexDataStart + self.singleReadoutSize * currentReadout
                           indexStop  = indexDataStart + self.singleReadoutSize * (currentReadout + 1)
               
                           if self.operationMode == 'normal':  # expected G0 is 0 or 1 
                               vmm3 = VMM3A(packetData[indexStart:indexStop], self.NSperClockTick)
                               # vmm3.G0 = 2
                           elif self.operationMode == 'clustered':  # expected G0 is 2
                               vmm3 = VMM3Aclustered(packetData[indexStart:indexStop], self.NSperClockTick)
                               # vmm3.G0 = 2
                           else:
                               print('\n\t\033[1;31mERROR: Operation mode ({} found) is not one of these: normal or clustered mode! --> Exiting!\033[1;37m'.format(self.operationMode),end='') 
                               sys.exit()
                           
                           index = self.overallDataIndex-1   
   
                           # ring 11 reserved for MON
                           if vmm3.Ring < 11:
                               
                               if self.InstrType == 'VMM':
                               
                                    self.data[index, 0] = vmm3.Ring
                                    self.data[index, 1] = vmm3.Fen
                                    self.data[index, 2] = vmm3.VMM
                                    self.data[index, 3] = vmm3.hybrid
                                    self.data[index, 4] = vmm3.ASIC
                                    self.data[index, 5] = vmm3.Channel
                                    self.data[index, 6] = vmm3.ADC
                                    self.data[index, 7] = vmm3.BC
                                    self.data[index, 8] = vmm3.OTh
                                    self.data[index, 9] = vmm3.TDC
                                    self.data[index, 10] = vmm3.GEO
                                    self.data[index, 11] = vmm3.timeCoarse
                                    self.data[index, 12] = PulseT
                                    self.data[index, 13] = PrevPT
                                    self.data[index, 14] = vmm3.G0  # if 1 is calibration
                                    self.data[index, 15] = vmm3.Channel1
                                    self.data[index, 16] = vmm3.ADC1
                                    self.data[index, 17] = vmm3.mult0
                                    self.data[index, 18] = vmm3.mult1
                                    
                               elif  self.InstrType == 'R5560':
                                   
                                    R5560data = R5560(packetData[indexStart:indexStop], self.NSperClockTick)
                                      
                                    self.data[index, 0] = R5560data.Ring
                                    self.data[index, 1] = R5560data.Fen
                                    self.data[index, 2] = R5560data.VMM
                                    self.data[index, 3] = R5560data.hybrid
                                    self.data[index, 4] = R5560data.ASIC
                                    self.data[index, 5] = R5560data.Channel
                                    self.data[index, 6] = R5560data.ADC
                                    self.data[index, 7] = R5560data.BC
                                    self.data[index, 8] = R5560data.OTh
                                    self.data[index, 9] = R5560data.TDC
                                    self.data[index, 10] = R5560data.GEO
                                    self.data[index, 11] = R5560data.timeCoarse
                                    self.data[index, 12] = PulseT
                                    self.data[index, 13] = PrevPT
                                    self.data[index, 14] = R5560data.G0  # if 1 is calibration
                                    self.data[index, 15] = R5560data.Channel1
                                    self.data[index, 16] = R5560data.ADC1
                                    self.data[index, 17] = R5560data.mult0
                                    self.data[index, 18] = R5560data.mult1
                                    
                                    
                               elif  self.InstrType == 'BM':

                                    mondata = MONdata(packetData[indexStart:indexStop], self.NSperClockTick)
                                
                                    self.data[index, 0] = mondata.Ring
                                    self.data[index, 1] = mondata.Fen
                                    self.data[index, 2] = 0   # VMM for MON always 0
                                    self.data[index, 3] = 0   # hybrid for MON always 0
                                    self.data[index, 4] = 0   # ASIC for MON always 0
                                    self.data[index, 5] = mondata.Channel
                                    self.data[index, 6] = mondata.ADC
                                    self.data[index, 7] = mondata.posX
                                    self.data[index, 8] = mondata.posY
                                    self.data[index, 9] = 0     # TDC for MON always 0
                                    self.data[index, 10] = mondata.Type
                                    self.data[index, 11] = mondata.timeCoarse
                                    self.data[index, 12] = PulseT
                                    self.data[index, 13] = PrevPT
                                    self.data[index, 14] = 0  # if 1 is calibration
                                    self.data[index, 15] = -1
                                    self.data[index, 16] = -1
                                    self.data[index, 17] = -1
                                    self.data[index, 18] = -1
                                   
                               else:
                                        
                                     print('\n\t\033[1;31mERROR: Data format not supported ---> Exiting ... \n\033[1;37m',end='') 
                                     sys.exit() 
                           
                           # overwrite if MONITOR 
                           is_lemo_mode = (self.MONtype == 'LEMO' and vmm3.Ring >= 11)
                           is_ring_mode = (self.MONtype == 'RING' and vmm3.Ring == 11 and vmm3.Ring == self.MONring)

                           if is_lemo_mode or is_ring_mode:
                               
                               mondata = MONdata(packetData[indexStart:indexStop], self.NSperClockTick)
                              
                               self.data[index, 0] = mondata.Ring
                               self.data[index, 1] = mondata.Fen
                               self.data[index, 2] = 0   # VMM for MON always 0
                               self.data[index, 3] = 0   # hybrid for MON always 0
                               self.data[index, 4] = 0   # ASIC for MON always 0
                               self.data[index, 5] = mondata.Channel
                               self.data[index, 6] = mondata.ADC
                               self.data[index, 7] = mondata.posX
                               self.data[index, 8] = mondata.posY
                               self.data[index, 9] = 0     # TDC for MON always 0
                               self.data[index, 10] = mondata.Type
                               self.data[index, 11] = mondata.timeCoarse
                               self.data[index, 12] = PulseT
                               self.data[index, 13] = PrevPT
                               self.data[index, 14] = 0  # if 1 is calibration
                               self.data[index, 15] = -1
                               self.data[index, 16] = -1
                               self.data[index, 17] = -1
                               self.data[index, 18] = -1
                            
  
                        # valid for normal mode 
                           if debugMode is True:
                               print(" \t Packet: {} ({} bytes), Readout: {}, Ring {}, FEN {}, VMM {}, hybrid {}, ASIC {}, Ch {}, Time Coarse {} ns, BC {}, OverTh {}, ADC {}, TDC {}, GO {} " \
                                           .format(self.counterValidESSpackets,ESSlength,currentReadout+1,vmm3.Ring,vmm3.Fen,vmm3.VMM,vmm3.hybrid,vmm3.ASIC,vmm3.Channel,vmm3.timeCoarse,vmm3.BC,vmm3.OTh,vmm3.ADC,vmm3.TDC,vmm3.G0))
    
           
                           ###########
                           
               self.readouts.heartbeats[indexPackets] = PulseT
            
    
           if np.mod(self.counterValidESSpackets,self.stepsForProgress) == 0:
                percents = int(round(100.0 * self.counterValidESSpackets / float(self.counterCandidatePackets), 1))
                print('['+format(percents,'01d') + '%]',end=' ')  
               
            # pb.progressBar(self.counterValidESSpackets,self.counterCandidatePackets)
           
           
        
        
class checkIfDataHasZeros():
     def __init__(self, data):
         
         self.dataIN = data
         
         self.OriginalLength = np.shape(self.dataIN)[0]
         
         datasum  = np.sum(data,axis=1)
         indexesIsNotZero  = np.argwhere(datasum>0)
        
         # self.trueLen  = np.shape(indexesIsNotZero[:,0]>0)[0]
    
         self.dataOUT = self.dataIN[indexesIsNotZero[:,0],:]
         self.NewLength = np.shape(self.dataOUT)[0]
         
         if self.NewLength  != self.OriginalLength :
             
            self.flag = True
            
            print('---> removing zeros left in data')
            
         else :
  
             self.flag = False
             


###############################################################################
###############################################################################

if __name__ == '__main__':
   # parser = argparse.ArgumentParser()
   # parser.add_argument("-f", metavar='file', help = "pcap file",
   #                     type = str, default = "VMM3a_Freia.pcapng")
   # parser.add_argument('-d', action='store_true', help = "add debug print")

   tProfilingStart = time.time()

   # arg = parser.parse_args()
   
   # filePath = './'+"VMM3a.pcapng"
   
   # path = '/Users/francescopiscitelli/Desktop/dataPcapUtgard/'
   
   filePath = '/Users/francescopiscitelli/Desktop/data4Testing/'
 
   
   file = '20230911_103949_pkts100_intpulser-H0-vmm1ch5-12-18-H1-vmm0ch20-21-22-cfg-0x6_00000.pcapng'
   
   
   filePath = '/Users/francescopiscitelli/Desktop/dataVMM/'
   file = '20230823_105243_duration_s_3600_testDetChopMON_00000.pcapng'
   
   file = '20230829_113913_duration_s_1800_DetRefurbishedMONandChopp_00002.pcapng'
   
   filePath = '/Users/francescopiscitelli/Documents/DOC/DATA/202311_PSI_AMOR_MBnewAMOR_VMM_neutrons/SamplesAndMasks/'
   file = '20231106_142811_duration_s_5_YESneutrons1240K1070Rth280_maskESS_00000.pcapng'
   
   filePath = '/Users/francescopiscitelli/Desktop/'
   file = 'DiagonaltestData.pcapng'
   file = 'DataRMMWrongHeader.pcapng'
   
   filePath = '/Users/francescopiscitelli/Documents/PYTHON/06_MBUTYcap_DETtests_Utgard/data/'
   file = 'ESSmask2023.pcapng'
   
   filePath = '/Users/francescopiscitelli/Desktop/dataVMM/'
   file ='20250320_095029_duration_s_1800_testCAB5-C0to3_00014.pcapng'
   
   filePath = '/Users/francescopiscitelli/Desktop/DATAtrainMBUTY/'
   file = 'miracles_trig2.pcapng'
   file = 'ESSmask2023_1000pkts.pcapng'
   # file = 'ESSmask2023.pcapng'
   
   # filePath = '/Users/francescopiscitelli/Desktop/DATAtrainMBUTY/'
   # file =   '20260203_090333_duration_s_600_FREIAsector0_00004.pcapng'
   
   
   
   
   # file = '20251010_145429_pkts2000_testRANDOM1_00000.pcapng'
   
   # file  = 'BM_loki_bm.pcapng'
   
   # filePath = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/data/'
   # file = 'sampleData_NormalMode.pcapng'
   # file = 'sampleData_ClusteredMode.pcapng'
   
   filePathAndFileName1 = filePath+file
   
   # filePath = path+'pcap_for_fra.pcapng'
   # filePath = path+'pcap_for_fra_ch2test.pcapng'
   # filePath = path+'pcap_for_fra_ch2test_take2.pcapng'
   # filePath = path+'pcap_for_fra_coinc.pcapng'
   # filePath = path+'freiatest.pcapng'
   
   # filePath = path+'20211005_091349_morten.pcapng'
   
   # path = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/data/'
   # filePath = path+'VMM3a_Freia.pcapng'

   # pr = pcapng_reader(filePath,timeResolutionType='fine')
   # # pr.debug = True
   # # pr.ret()
   # # data = pr.data
   # 

   
   # pr = pcapng_reader_PreAlloc(filePath)

   # # pr.debug = True
   
   # pr.allocateMemory()
   
   # pr.read(timeResolutionType='fine')
   
   # pcap = pcapng_reader(filePath,timeResolutionType='fine', sortByTimeStampsONOFF = True)
   # readouts = pcap.readouts
   
   # readouts.sortByTimeStamps()
   
   # readoutsArray = readouts.concatenateReadoutsInArrayForDebug()
   # 
   # ppp = plo.plottingReadouts(vmm3, config)
   # ppp.plotChRaw(parameters.cassettes.cassettes)
   # ppp.plotTimeStamps(parameters.cassettes.cassettes)
   
   # cc= checkWhich_RingFenHybrid_InFile(filePath)
   
   # aa = cc.check()
   
   # readouts = cc.readouts
   
   # r
   
   # NSperClockTick = 11.356860963629653  #ns per tick ESS for 88.0525 MHz
   
   # cc = checkWhich_RingFenHybrid_InFile(filePath,NSperClockTick).check()
   
   NSperClockTick = 11.356860963629653  #ns per tick ESS for 88.0525 MHz
    
    # cc = checkWhich_RingFenHybrid_InFile(filePath,NSperClockTick).check()
    
    
   # readouts = readouts()
   # pcapng = pcapng_reader_PreAlloc(NSperClockTick, MONTTLtype = True , MONring = 11, filePathAndFileName=filePathAndFileName, timeResolutionType='fine', operationMode='normal')

   # pcapng = pcapng_reader_PreAlloc(NSperClockTick, MONTTLtype = True , MONring = 11, filePathAndFileName=filePathAndFileName, timeResolutionType='fine', operationMode='normal')
   # pcapng.allocateMemory()
   # pcapng.read()
   # readouts = pcapng.readouts

   
   typeOfLoading = 'allocate'
   
   # typeOfLoading = 'quick'
   
   # pcapng = pcapng_reader_PreAlloc(NSperClockTick,MONTTLtype=True, MONring=11,filePathAndFileName=filePathAndFileName1,timeResolutionType='fine',operationMode='normal', kafkaStream = False)
   # pcapng.allocateMemory(typeOfLoading)

   pcap = pcapng_reader(filePathAndFileName1,NSperClockTick, MONtype='LEMO', MONring=11, timeResolutionType='fine', sortByTimeStampsONOFF=True, operationMode='normal',pcapLoadingMethod=typeOfLoading)

   readouts = pcap.readouts
   
   # pcap = pcapng_reader_PreAlloc(filePath,NSperClockTick)
   # pcap.allocateMemory()
   # pcap.read()
   
   # pcap = pcapng_reader(filePath, NSperClockTick, timeResolutionType = 'fine', sortByTimeStampsONOFF = False )

   
   
   # readouts = pcap.readouts 
   readoutsArray = readouts.concatenateReadoutsInArrayForDebug()
   
   # tdcs = VMM3A_convertCalibrate_TDCinSec(readouts.TDC, NSperClockTick).TDC_ns
   
   # timeS = readouts.timeHIs + 100e-9
   
   
    # timeDIff = readouts.timeStamp - readouts.timeHIns 
   # - readouts.timeLOns*1e-9
   
   # aa = np.concatenate((readouts.timeStamp[:,None],readouts.timeHIs[:,None],readouts.timeLOns[:,None]*1e-9,tdcs[:,None],timeDIff[:,None]),axis=1)
   
   # aa = pr.d
   # bb = pr.e
   
   # aaa = aa[446900:,5:9]
   # bbb = bb[446900:,5:9]
   
   # for k in range(446900,447000,1):
   #      print(" \t Ring {}, FEN {}, VMM {}, hybrid {}, ASIC {}, Ch {}, Time {} s, BC {}, OverTh {}, ADC {}, TDC {}, GEO {} " \
   #                               .format(vmm3.Ring[k],vmm3.Fen[k],vmm3.VMM[k],vmm3.hybrid[k],vmm3.ASIC[k],vmm3.Channel[k],vmm3.timeStamp[k],vmm3.BC[k],vmm3.OTh[k],vmm3.ADC[k],vmm3.TDC[k],vmm3.GEO[k]))
   
   tElapsedProfiling = time.time() - tProfilingStart
   print('\n Data Loading Completed in %.2f s' % tElapsedProfiling) 