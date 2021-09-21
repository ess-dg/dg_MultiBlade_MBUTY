#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 09:03:24 2021

@author: francescopiscitelli
"""

import numpy as np
from lib import libMapping as maps
from lib import libReadPcapngVMM as pcapr
from lib import libCluster as clu

###############################################################################
###############################################################################
# sample data for AMOR topology

class sampleReadouts_1():
    
      def __init__(self): 
           
            self.readouts = pcapr.readouts()                
            
      def fill(self):
            # ring 0
            self.readouts.Ring[0:10] = 0
            
            self.readouts.Fen[0:10]   = 1
            
            self.readouts.hybrid[0:10]   = 0
            
            self.readouts.ASIC[0]   = 0
            self.readouts.ASIC[1]   = 1
            self.readouts.ASIC[2]   = 0
            self.readouts.ASIC[3]   = 1
            self.readouts.ASIC[4]   = 0
            self.readouts.ASIC[5]   = 1
            self.readouts.ASIC[6]   = 0
            self.readouts.ASIC[7]   = 1
            self.readouts.ASIC[8]   = 0
            self.readouts.ASIC[9]   = 1
            
            self.readouts.VMM = self.readouts.ASIC
            
            self.readouts.Channel[0:10] = np.arange(17,27,1) 
            
            self.readouts.ADC[0:10] = 1000
            
            # self.readouts.timeStamp[0]= 1.1475e-6
            # self.readouts.timeStamp[1]= 2.2725e-6
            # self.readouts.timeStamp[2]= 3.3975e-6
            # self.readouts.timeStamp[3]= 4.5225e-6
            # self.readouts.timeStamp[4]= 5.6475e-6
            # self.readouts.timeStamp[5]= 6.7725e-6
            # self.readouts.timeStamp[6]= 7.8975e-6
            # self.readouts.timeStamp[7]= 9.0225e-6
            # self.readouts.timeStamp[8]= 10.1475e-6
            # self.readouts.timeStamp[9]= 11.27225e-6
            
            # self.readouts.timeStamp[0]= 2.0e-6
            # self.readouts.timeStamp[1]= 3.0e-6
            # self.readouts.timeStamp[2]= 5.0e-6
            # self.readouts.timeStamp[3]= 6.0e-6
            # self.readouts.timeStamp[4]= 8.0e-6
            # self.readouts.timeStamp[5]= 9.0e-6
            # self.readouts.timeStamp[6]= 11.0e-6
            # self.readouts.timeStamp[7]= 12.0e-6
            # self.readouts.timeStamp[8]= 14.0e-6
            # self.readouts.timeStamp[9]= 15.0e-6
            
            self.readouts.timeStamp[0]= 2.0e-6
            self.readouts.timeStamp[1]= 2.5e-6
            self.readouts.timeStamp[2]= 3.5e-6
            self.readouts.timeStamp[3]= 4.0e-6
            self.readouts.timeStamp[4]= 5.0e-6
            self.readouts.timeStamp[5]= 5.9e-6
            self.readouts.timeStamp[6]= 8.0e-6
            self.readouts.timeStamp[7]= 8.6e-6
            self.readouts.timeStamp[8]= 9.7e-6
            self.readouts.timeStamp[9]= 10e-6

class sampleReadouts_2():
        def __init__(self): 
            
            self.readouts = pcapr.readouts() 
            
            rando = 999
            Nreadouts = 1500
            
            self.readouts.Ring  = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.Fen   = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.VMM   = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.hybrid  = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.ASIC    = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.Channel = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.ADC     = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.timeStamp  = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.BC      = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.OTh     = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.TDC     = rando*np.ones((Nreadouts), dtype = 'float64')
            self.readouts.GEO     = rando*np.ones((Nreadouts), dtype = 'float64')
        
        def fill(self):
            # ring 0
            self.readouts.Ring[0:800] = 0
            
            self.readouts.Fen[0:400]   = 1
            self.readouts.Fen[400:800] = 2
            
            self.readouts.hybrid[0:200]   = 0
            self.readouts.hybrid[200:400] = 1
            self.readouts.hybrid[400:600] = 0
            self.readouts.hybrid[600:800] = 1
            
            self.readouts.ASIC[0:200]   = 0
            self.readouts.ASIC[200:400] = 1
            self.readouts.ASIC[400:600] = 0
            self.readouts.ASIC[600:800] = 1
            
            self.readouts.Channel[0:64] = np.arange(0,64,1) 
            self.readouts.Channel[100:164]   = np.arange(0,64,1)
            self.readouts.Channel[200:264]   = np.arange(0,64,1)
            self.readouts.Channel[300:364]   = np.arange(0,64,1)
            self.readouts.Channel[400:464]   = np.arange(0,64,1) 
            self.readouts.Channel[500:564]   = np.arange(0,64,1)
            self.readouts.Channel[600:664]   = np.arange(0,64,1)
            self.readouts.Channel[700:764]   = np.arange(0,64,1)
            
            # ring 1
            self.readouts.Ring[1000:1400] = 1

            self.readouts.Fen[1000:1400]  = 1 

            self.readouts.hybrid[1000:1200] = 0
            self.readouts.hybrid[1200:1400] = 1
            
            self.readouts.ASIC[1000:1100]   = 0
            self.readouts.ASIC[1100:1200] = 1
            self.readouts.ASIC[1200:1300] = 0
            self.readouts.ASIC[1300:1400] = 1

            self.readouts.Channel[1000:1064]   = np.arange(0,64,1) 
            self.readouts.Channel[1100:1164]   = np.arange(0,64,1)
            self.readouts.Channel[1200:1264]   = np.arange(0,64,1)
            self.readouts.Channel[1300:1364]   = np.arange(0,64,1)
 
                           
###############################################################################
###############################################################################
# sample data from hdf5 old files

class sampleHits1Cass():
    
    def __init__(self, cassette1ID, dataFilePath):
        
        self.hits = maps.hits()
        
        self.dataFilePath = dataFilePath
        
        self.cassette1ID = cassette1ID
        
        self.Channel   = np.zeros((0), dtype = 'float64')
            
    def read(self,Nhits):
        
         Nhits = int(Nhits)
         
         dataTemp = np.loadtxt(self.dataFilePath,dtype='float64',delimiter=' ')
         
         if Nhits > np.shape(dataTemp)[0]:
             Nhits = np.shape(dataTemp)[0]
             print('Nhits too large, set to max hits '+str(Nhits)+' for cass ID '+str(self.cassette1ID))
         
         self.data = dataTemp[:Nhits,:]
       
         self.hits.timeStamp = self.data[:,0]
         self.hits.ADC       = self.data[:,2]
         
         leng = self.data[:,0].shape[0] 
         
         self.hits.WorS    = 99*np.ones((leng), dtype = 'float64')
         # self.Channel = 999*np.ones((leng), dtype = 'float64')
         self.hits.Cassette = self.cassette1ID*np.ones((leng), dtype = 'float64')  
         
         self.hits.WiresStrips = 9999*np.ones((leng), dtype = 'float64')
         # self.WiresStripsGlob = 9999*np.ones((leng), dtype = 'float64')
       
    def transform(self):
         
         self.Channel = self.data[:,1]
         # wires
         selw = self.data[:,1] <= 31
        
         self.hits.WorS[selw] = 0
         self.hits.WiresStrips[selw] = self.data[selw,1]
         
         # strips
         sels = self.data[:,1] >= 32
         self.hits.WorS[sels] = 1
         self.hits.WiresStrips[sels] = self.data[sels,1] - 32
         
         
         
class sampleHitsMultipleCassettes(): 
    def __init__(self, cassetteIDs=[1,2,3,4,5,6], dataPath='./data/' ,  whichDataset='ESSmask'):
        
        self.whichDataset = whichDataset
        
        self.cassetteIDs = cassetteIDs
        
        self.hits = maps.hits()
        
        self.dataPath = dataPath+'dataJadaqConverted/'
        
        self.Channel   = np.zeros((0), dtype = 'float64')
        
        if self.whichDataset == 'ESSmask':
            self.fileName1    = 'ESSmask_cass'
        elif  self.whichDataset == 'DirectBeam': 
            self.fileName1    = 'DirectBeam_cass'
            
        self.fileName2    =  '_Sorting=True_Filtering=False_Input.txt'
        
    def append(self, hit):
        
        self.Channel   = np.append(self.Channel, hit.Channel)
        self.hits.append(hit.hits)

    def generate(self,Nhits):
        
        print('generating sample hits ... dataset: ',self.whichDataset)
        
        Nhits = int(Nhits)
        
        for k, cass in enumerate(self.cassetteIDs):
            
            self.fileName = self.fileName1+str(k+1)+self.fileName2
            
            aa = sampleHits1Cass(cass,self.dataPath+self.fileName)
            aa.read(Nhits)
            aa.transform()

            self.append(aa)
            
            
    def generateGlob(self,Nhits):
        
        print('generating sample hits ... dataset: ',self.whichDataset)
        
        Nhits = int(Nhits)
        
        for k, cass in enumerate(self.cassetteIDs):
            
            self.fileName = self.fileName1+str(k+1)+self.fileName2
            
            aa = sampleHits1Cass(cass,self.dataPath+self.fileName)
            aa.read(Nhits)
            aa.transform()
            
            # aa.WiresStripsGlob  = np.copy(aa.WiresStripsIndiv)
            #  global coord
            selectionW = aa.hits.WorS == 0   #select wires
            aa.hits.WiresStrips[selectionW] = aa.hits.WiresStrips[selectionW] + k*32
            
            self.append(aa)
                     
 ############################################
           
class sampleHitsMultipleCassettes_2(): 
     def __init__(self):
    
          # self.cassetteIDs = cassetteIDs
        
          self.hits = maps.hits()
          
     def generateGlob(self):
        
        print('generating sample hits 2 ...')
        
        # Nhits = int(Nhits)
        
        # C2 ######################
        self.hits.Cassette    = float(2)
        self.hits.ADC         = float(1000)
        self.hits.WiresStrips = float(18+32)
        self.hits.WorS        = float(0)
        self.hits.timeStamp   = float(0.000001)
        
        self.hits.Cassette    = np.append(self.hits.Cassette,2)
        self.hits.ADC         = np.append(self.hits.ADC,800)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,63)
        self.hits.WorS        = np.append(self.hits.WorS,1)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,2e-6)
        
        # C2 ######################
        
        self.hits.Cassette    = np.append(self.hits.Cassette,2)
        self.hits.ADC         = np.append(self.hits.ADC,5006)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,20+32)
        self.hits.WorS        = np.append(self.hits.WorS,0)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,7e-6)
        
        self.hits.Cassette    = np.append(self.hits.Cassette,2)
        self.hits.ADC         = np.append(self.hits.ADC,5004)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,3)
        self.hits.WorS        = np.append(self.hits.WorS,1)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,7.5e-6)
        
        # C1 ######################
        
        self.hits.Cassette    = np.append(self.hits.Cassette,1)
        self.hits.ADC         = np.append(self.hits.ADC,501)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,0)
        self.hits.WorS        = np.append(self.hits.WorS,0)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,15.5e-6)
        
        self.hits.Cassette    = np.append(self.hits.Cassette,1)
        self.hits.ADC         = np.append(self.hits.ADC,502)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,0)
        self.hits.WorS        = np.append(self.hits.WorS,1)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,15.7e-6)
        
        # C1 ######################
        
        self.hits.Cassette    = np.append(self.hits.Cassette,1)
        self.hits.ADC         = np.append(self.hits.ADC,506)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,9)
        self.hits.WorS        = np.append(self.hits.WorS,0)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,20e-6)
        
        self.hits.Cassette    = np.append(self.hits.Cassette,1)
        self.hits.ADC         = np.append(self.hits.ADC,507)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,31)
        self.hits.WorS        = np.append(self.hits.WorS,1)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,21e-6)
        
        self.hits.Cassette    = np.append(self.hits.Cassette,1)
        self.hits.ADC         = np.append(self.hits.ADC,509)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,2)
        self.hits.WorS        = np.append(self.hits.WorS,0)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,100e-6)
        
        self.hits.Cassette    = np.append(self.hits.Cassette,1)
        self.hits.ADC         = np.append(self.hits.ADC,509)
        self.hits.WiresStrips = np.append(self.hits.WiresStrips,3)
        self.hits.WorS        = np.append(self.hits.WorS,1)
        self.hits.timeStamp   = np.append(self.hits.timeStamp,100e-6)
        
        for k in range(20):
            self.hits.Cassette    = np.append(self.hits.Cassette,3)
            self.hits.ADC         = np.append(self.hits.ADC,1000)
            self.hits.WiresStrips = np.append(self.hits.WiresStrips,32*2+5+k)
            self.hits.WorS        = np.append(self.hits.WorS,0)
            self.hits.timeStamp   = np.append(self.hits.timeStamp,30e-6+k*4e-6)
            
            self.hits.Cassette    = np.append(self.hits.Cassette,3)
            self.hits.ADC         = np.append(self.hits.ADC,1203)
            self.hits.WiresStrips = np.append(self.hits.WiresStrips,10+2*k)
            self.hits.WorS        = np.append(self.hits.WorS,1)
            self.hits.timeStamp   = np.append(self.hits.timeStamp,30e-6+k*4e-6)
       
        
###############################################################################
###############################################################################
# sample data from hdf5 old files

class sampleEvents1Cass():
    
     def __init__(self, cassette1ID, dataFilePath):
        
        self.events = clu.events() 
        
        self.dataFilePath = dataFilePath
        
        self.cassette1ID = cassette1ID
           
     def read(self,Nevents):
        
         Nevents = int(Nevents)
         
         dataTemp = np.loadtxt(self.dataFilePath,dtype='float64',delimiter=' ')
         
         if Nevents > np.shape(dataTemp)[0]:
             Nevents = np.shape(dataTemp)[0]
             print('Nevents too large, set to max hits '+str(Nevents)+' for cass ID '+str(self.cassette1ID))
         
         self.data = dataTemp[:Nevents,:]
         
         # return self.data
       
         self.events.positionW = self.data[:,0]
         self.events.positionS = self.data[:,1]
         self.events.timeStamp = self.data[:,2]
         self.events.PHW       = self.data[:,3]
         self.events.PHS       = self.data[:,4]
         self.events.multW     = self.data[:,5]
         self.events.multS     = self.data[:,6]

         self.events.NeventsNotRejAll = Nevents
         
         self.events.Cassette = self.cassette1ID*np.ones(len(self.events.positionW),dtype='float64')
               
         
class sampleEventsMultipleCassettes():        
            
      def __init__(self, cassetteIDs=[1,2,3,4,5,6], dataPath='./data/', whichDataset='ESSmask'):
          
          self.whichDataset = whichDataset
          
          self.cassetteIDs = cassetteIDs
        
          self.events = clu.events()
        
          self.dataPath = dataPath+'dataJadaqConverted/'

          if self.whichDataset == 'ESSmask':
            self.fileName1    = 'ESSmask_cass'
          elif  self.whichDataset == 'DirectBeam': 
            self.fileName1    = 'DirectBeam_cass'
         
          self.fileName2    =  '_Sorting=True_Filtering=False_Clustered.txt'
          
      def generateGlob(self,Nevents):
        
        print('generating sample events ... dataset: ',self.whichDataset)
        
        Nevents = int(Nevents)
        
        for k, cass in enumerate(self.cassetteIDs):
            
            self.fileName = self.fileName1+str(k+1)+self.fileName2
            
            aa = sampleEvents1Cass(cass,self.dataPath+self.fileName)
            aa.read(Nevents)
  
            #  global coord
            # selectionWcass = aa.events.Cassette == cass 
            aa.events.positionW = aa.events.positionW + k*32
            
            self.events.append(aa.events)
            
            
###############################################################################
###############################################################################   
   
if __name__ == '__main__':
    
        Nhits = 10
        
        # cassette = 1 
        
        # aa = sampleHits(cassette)
        # aa.read(Nhits)
        # data = aa.transform()
        
        # indata = aa.data
        
        # does not matter the order, it will generata hits for those cass and the posotion is the same as json file, cass ID 1 is first etc...
        cassettes = [1,2]
        
        # bb = sampleHitsMultipleCassettes(cassettes,'./data/')
        # bb.generateGlob(Nhits)
        
        # hits = bb.hits
        
        # hitsArray = bb.hits.concatenateHitsInArrayForDebug()
        
        # Nevents = 10
        
        # # cc = sampleEvents(cassettes, './data/dataJadaqConverted/ESSmask_dataset1_large_cass1_Sorting=True_Filtering=False_Clustered.txt')
        # # data = cc.read(Nevents)
   
        # dd = sampleEventsMultipleCassettes(cassettes,'./data/')
        # dd.generateGlob(Nevents)
        
        # events  = dd.events
        
        # evetnsArray = events.concatenateEventsInArrayForDebug()
        
        # hiit = sampleHitsMultipleCassettes_2()
        # hiit.generateGlob()
        # hits = hiit.hits
        
        hiit = sampleHitsMultipleCassettes(whichDataset='DirectBeam')
        hiit.generateGlob(1e9)
        hits = hiit.hits
        
        hitsArray = hits.concatenateHitsInArrayForDebug()