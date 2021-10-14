#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 09:14:18 2021

@author: francescopiscitelli
"""

import numpy as np
import json
import os

import sys

# import pandas as pd
# from lib import libReadPcapngVMM as pcapr
from lib import libSampleData as sdat


# NOTE: THIS SUPPORTS ONLY 1 MONITOR

###############################################################################
###############################################################################

class hits():            
    def __init__(self): 
        
        datype = 'int64'
        
        self.Cassette    = np.zeros((0), dtype = datype)
        self.ADC         = np.zeros((0), dtype = datype)
        self.timeStamp   = np.zeros((0), dtype = datype)
        self.WorS        = np.zeros((0), dtype = datype)
        self.WiresStrips = np.zeros((0), dtype = datype)
        self.PulseT      = np.zeros((0), dtype = datype)
        self.PrevPT      = np.zeros((0), dtype = datype)
        self.Durations   = np.zeros((0), dtype = datype)
        self.Duration    = np.zeros((1), dtype = datype)
        
    def importReadouts(self,readouts):    
        
        self.ADC       = readouts.ADC
        self.timeStamp = readouts.timeStamp
        self.PulseT    = readouts.PulseT
        self.PrevPT    = readouts.PrevPT
        
        self.Durations = readouts.Durations
        self.Duration  = np.sum(readouts.Durations)
        
        leng = len(readouts.Channel)
        
        # 0 if wire, 1 if strip 
        self.WorS = np.copy(readouts.ASIC)
        
        self.Cassette    = -1*np.ones((leng), dtype = 'int64')        

        self.WiresStrips = -1*np.ones((leng), dtype = 'int64')
        
    def append(self, hit):
        
        self.Cassette    = np.concatenate((self.Cassette, hit.Cassette), axis=0)
        self.ADC         = np.concatenate((self.ADC, hit.ADC), axis=0)
        self.WorS        = np.concatenate((self.WorS, hit.WorS), axis=0)
        self.timeStamp   = np.concatenate((self.timeStamp, hit.timeStamp), axis=0)
        self.WiresStrips = np.concatenate((self.WiresStrips, hit.WiresStrips), axis=0)
        self.PulseT      = np.concatenate((self.PulseT, hit.PulseT), axis=0)
        self.PrevPT      = np.concatenate((self.PrevPT, hit.PrevPT), axis=0)
        
        self.Durations   = np.append(self.Durations, hit.Durations)
        self.Duration    = self.Duration+hit.Duration
             
    def concatenateHitsInArrayForDebug(self):
        
        leng = len(self.WiresStrips)
        
        hitsArray = np.zeros((leng,7),dtype = 'int64')
        
        hitsArray[:,0] = self.timeStamp
        hitsArray[:,1] = self.Cassette
        hitsArray[:,2] = self.WorS
        hitsArray[:,3] = self.WiresStrips
        hitsArray[:,4] = self.ADC
        hitsArray[:,5] = self.PulseT
        hitsArray[:,6] = self.PrevPT

        return hitsArray
   
    
class extractHitsPortion():
    
    def extract(hits,start,stop):
        
        hitsEx = hits
    
        hitsEx.Cassette  = hits.Cassette[start:stop]
        hitsEx.ADC       = hits.ADC[start:stop]
        hitsEx.WorS      = hits.WorS[start:stop]
        hitsEx.timeStamp = hits.timeStamp[start:stop]
        hitsEx.WiresStrips = hits.WiresStrips[start:stop]
        hitsEx.PulseT    = hits.PulseT[start:stop]
        hitsEx.PrevPT    = hits.PrevPT[start:stop]
        
        return hitsEx

###############################################################################
###############################################################################   

class MONmap():
    def __init__(self):
  
        self.ID       = None
        self.RingID   = None
        self.FenID    = None
        self.hybridID = None
        self.ASICID   = None
        self.channel  = None
        
class DETmap():
    def __init__(self):
  
        self.cassettesMap = []
        
class cassMap():
    def __init__(self):
        
        self.RingID   = None
        self.FenID    = None
        self.hybridID = None
        
        
class DETparameters():
    def __init__(self):
        
        self.name     = None
        
        self.orientation = 'vertical'
        
        self.numOfWires  = 0
        self.numOfStrips = 0
        
        self.numOfCassettes = 0
        
        self.cassInConfig = []
        
        # in degrees 
        self.bladesInclination  = float(0)
        
        # in mm 
        self.offset1stWires  = float(0)
        
        # in mm
        self.wirePitch  = float(0)
        self.stripPitch = float(0)
      
        

class read_json_config():
    def __init__(self, configFile_PathAndFileName):
        
        temp =  os.path.split(configFile_PathAndFileName)
            
        self.configFilePath = temp[0]+'/'
        self.configFileName = temp[1]
        
        self.MONmap = MONmap()
        self.DETmap = DETmap()
        self.DETparameters = DETparameters()
        self.cassMap = cassMap()
        
        self.debug    = False
         
        try:
            self.ff   = open(configFile_PathAndFileName,'r') 
        except:
            print('\n \033[1;31m---> Config File: ' + self.configFileName + ' not found \033[1;37m')
            print('\n ---> in folder: ' + self.configFilePath + ' \n -> exiting.')
            sys.exit()
            
        self.conf = json.load(self.ff)
        
        self.get_allParameters()
        
        self.print_DETname()
              
    def __del__(self):
        try:
            self.ff.close()
        except:
            pass
        
    def dprint(self, msg):
        if self.debug:
            print("{}".format(msg))
            
    def get_allParameters(self):
        self.get_DETname()
        self.get_DETparameters()
        self.get_DETmap()
        self.get_DETcassettesInConfig()
        self.get_MONmap()
            
    def print_DETname(self):
        print('\033[1;36mConfiguration for Detector: {}\033[1;37m'.format(self.DETparameters.name))
        
    def get_DETname(self):
        self.DETparameters.name = self.conf.get('Detector')
        return self.DETparameters.name
    
    def get_DETparameters(self):
        self.DETparameters.numOfWires  = self.conf.get('wires')
        self.DETparameters.numOfStrips = self.conf.get('strips')
        self.DETparameters.wirePitch  = float(self.conf.get('wirePitch_mm'))
        self.DETparameters.stripPitch = float(self.conf.get('stripPitch_mm'))
        self.DETparameters.bladesInclination  = float(self.conf.get('bladesInclination_deg'))
        self.DETparameters.offset1stWires  = float(self.conf.get('offset1stWires_mm'))
        self.DETparameters.numOfCassettes  = self.conf.get('cassettes')
        self.DETparameters.orientation     = self.conf.get('orientation')
        
    def get_DETmap(self):  
        self.DETmap.cassettesMap = self.conf.get('Cassette2ElectronicsConfig')
    
    def get_DETcassettesInConfig(self):
                
        for cc in self.DETmap.cassettesMap:
            ID = cc.get("ID")
            self.DETparameters.cassInConfig.append(ID)
                
        self.dprint('cassettes in config file: {}'.format(self.DETparameters.cassInConfig))   
        
    def get_cassID2RingFenHybrid(self,cassetteID):

        if not cassetteID in self.DETparameters.cassInConfig:
                self.cassMap.RingID   = None
                self.cassMap.FenID    = None
                self.cassMap.hybridID = None
                print('\t \033[1;33mWARNING: Cassette ID ',str(cassetteID),' not found! Skipped! This CONFIG file only contains cassettes:', end=' ')
                for cass in self.DETparameters.cassInConfig:
                    print(cass,end=' ')
                print('\033[1;37m')
                
        else:
             for cc in self.DETmap.cassettesMap:
                 if cc.get("ID") == cassetteID:
                     self.cassMap.RingID = cc.get("Ring")
                     self.cassMap.FenID  = cc.get("Fen")
                     self.cassMap.hybridID = cc.get("Hybrid")
                    
        
    def get_MONmap(self):
             
        self.mapm = self.conf.get('Monitor')
        
        if self.mapm is None:
            print('\t \033[1;33mWARNING: No monitor config found in json file \033[1;37m')
        
        else:
            
             for cc in self.mapm:
            
                 self.MONmap.ID     = cc.get("ID")
                 self.MONmap.RingID = cc.get("Ring")
                 self.MONmap.FenID  = cc.get("Fen")
                 self.MONmap.hybridID  = cc.get("Hybrid")
                 self.MONmap.ASICID    = cc.get("ASIC")
                 self.MONmap.channel  = cc.get("Channel")
            
                  

###############################################################################
###############################################################################

                
class mapDetector():
    def __init__(self, readouts, config):
        
        self.debug    = False
        
        self.readouts = readouts 
        
        self.hits = hits()
        self.hits.importReadouts(self.readouts)
   
        self.config = config
                
    def initCatData(self):    # debug
        if self.debug:
            self.catData = np.zeros((len(self.readouts.Ring),9), dtype = 'int64')
            self.catData[:,0] = self.hits.Cassette
            self.catData[:,1] = self.readouts.Ring
            self.catData[:,2] = self.readouts.Fen
            self.catData[:,3] = self.readouts.hybrid
            self.catData[:,4] = self.readouts.ASIC
            self.catData[:,5] = self.readouts.Channel
            self.catData[:,6] = self.hits.WiresStrips
            self.catData[:,7] = self.hits.WorS
            # self.catData[:,8] = self.hits.WiresStripsGlob
            
    def dprint(self, msg):
        if self.debug:
            print("{}".format(msg))     
        
    def mapp1cass(self, cassette1ID):
        
        if self.debug:
            print(cassette1ID)
        
        self.config.get_cassID2RingFenHybrid(cassette1ID)
        
        if self.debug:
            print(self.config.cassMap.RingID,self.config.cassMap.FenID,self.config.cassMap.hybridID)
        
        RingLoc = self.readouts.Ring   == self.config.cassMap.RingID
        FenLoc  = self.readouts.Fen    == self.config.cassMap.FenID
        HyLoc   = self.readouts.hybrid == self.config.cassMap.hybridID
        
        # selection = RingLoc & FenLoc & HyLoc
        
        selection = np.logical_and(np.logical_and(RingLoc,FenLoc) , HyLoc)
        
        if np.any(selection):
            self.hits.Cassette[selection] = cassette1ID
            flag = True
        else:
            flag = False
            # print('\t \033[1;33m No data found for Cassette ID ',str(cassette1ID),'\033[1;37m')
            
        return flag    
            
    
    def mappAllCass(self):
        
        # mapped according to the json file
        cassettesIDs = self.config.DETparameters.cassInConfig
        
        cassNotFound = []
        
        for cass in cassettesIDs:
            flag = self.mapp1cass(cass)
            
            if flag is False:
                cassNotFound.append(cass)
        
        if len(cassNotFound) > 0:
            print('\t \033[1;33mWARNING: Cassette IDs: ', end=' ')
            for cass in cassNotFound:
                  print(cass,end=' ')
            print(' not found in DATA file. Mapping skipped for those. \033[1;37m')        
                

    def mapChannels(self):
        
        #  wires
        sel1 = self.readouts.ASIC == 0 
        sel2 = self.readouts.Channel >= 16
        sel3 = self.readouts.Channel <= 47
        
        selectionWires  = sel1 & sel2 & sel3

        self.hits.WiresStrips[selectionWires] = 31 - (self.readouts.Channel[selectionWires] - 16)
        
        self.hits.WiresStrips[~selectionWires] = np.ma.masked # same as np.nan for int64 instead of floats
        
        # strips
        selectionStrips = self.readouts.ASIC == 1
        
        self.hits.WiresStrips[selectionStrips] = self.readouts.Channel[selectionStrips]
        
        # if some ch of vmm are not used then nan, it is not a wire or strip 
        self.hits.WorS[~selectionWires & ~selectionStrips] = np.ma.masked # same as np.nan for int64 instead of floats
        
    def mapChannelsGlob(self):
        
        self.mapChannels()
        
        # # global coord
        # self.hits.WiresStripsGlob  = np.copy(self.hits.WiresStrips)
        # #  if one cassette is absent in eiither the config file or the data there will be a blank space for the wanted cassette
        
        # # for k, cass in enumerate(cassettesIDs):
        #     #  does not matter the cassette ID the cassettes are arrangted one after the other according to the order in cassettesIDs,   
        
        #  # in this case the order is the arrangemtn in the json file 
        # for k, cass in enumerate(self.config.presentCass): 
        #     selection = np.logical_and( self.hits.Cassette == cass , self.hits.WorS == 0 ) #  wires is WorS = 0
        #     self.hits.WiresStripsGlob[selection] = self.hits.WiresStrips[selection] + k*self.config.numOfWires
        
                  # in this case the order is the arrangemtn in the json file 
        for k, cass in enumerate(self.config.DETparameters.cassInConfig): 
            selection = np.logical_and( self.hits.Cassette == cass , self.hits.WorS == 0 ) #  wires is WorS = 0
            
            #  if just add +32 every cassette in config does not matter the ID
            # index = k
            #  if the cassette ID drives the position in the  space, 1 is the bottom cassette orthe most left 
            index = cass-1
                
            self.hits.WiresStrips[selection] = self.hits.WiresStrips[selection] + index*self.config.DETparameters.numOfWires
        
    
    def mappAllCassAndChannels(self):
        
        self.mappAllCass()
        self.mapChannels()  
            
    def mappAllCassAndChannelsGlob(self):
        
        self.mappAllCass()
        self.mapChannelsGlob()


class mapMonitor():
    def __init__(self, readouts, config):
        
        self.readouts = readouts 
        
        self.hits = hits()
           
        self.config = config
        self.config.get_MONmap()
        
        RingLoc = self.readouts.Ring    == self.config.MONmap.RingID
        FenLoc  = self.readouts.Fen     == self.config.MONmap.FenID
        HyLoc   = self.readouts.hybrid  == self.config.MONmap.hybridID
        ASICLoc = self.readouts.ASIC    == self.config.MONmap.ASICID
        ChLoc   = self.readouts.Channel == self.config.MONmap.channel
    
        selection = RingLoc & FenLoc & HyLoc & ASICLoc & ChLoc
 
        if np.any(selection):
            self.hits.timeStamp = self.readouts.timeStamp[selection]
            self.hits.ADC       = self.readouts.ADC[selection]
        else:
            print('\t \033[1;33mNo MONITOR data found in DATA file\033[1;37m')
        

###############################################################################
###############################################################################

if __name__ == '__main__':

   filePath  = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/config/'+"MB300_AMOR_config.json"
   filePathD = './'+"VMM3a_Freia.pcapng"

   config = read_json_config(filePath)
   
   # # name = config.get_DetectorName()
   # # config.get_cassettesInConfig()
   
   # # config.get_cassID2RingFenHybrid(5)
   # # print(config.RingID, config.FenID, config.hybridID)
   # # config.get_cassID2RingFenHybrid(55)
   # # print(config.RingID, config.FenID, config.hybridID)
   # # config.get_cassID2RingFenHybrid(1)
   # # print(config.RingID, config.FenID, config.hybridID)
   
   # # config.get_cassID2RingFenHybrid([1,41])
   
   # config.get_bladesInclination()
   # config.get_pitches()
   # config.get_offset1stWires()
   
   # pr = pcapr.pcap_reader(filePathD)
   #  # pr.debug = True
   # pr.read()
   # vmm1 = pr.readouts
   
   vmm2 = sdat.sampleReadouts()
   vmm2.fill()

   
   
   re  = mapDetector(vmm2, config)
   re.debug = True
   re.initCatData()
   data1 = re.catData
   

   # re.mapp1cass(1)
   # # # bb = re.mapp1cass(45)
   
   # # # aa  = re.mappAllCass([1,2,45,3,56])
   
   # # # cassettes = np.arange(0,34,1)
    
   # # # re.mappAllCassAndChannels()
   
   re.mappAllCassAndChannelsGlob()
   
   re.initCatData()
   data = re.catData
   
   # # # re.mappAllCassAndChannels(cassettes)
   
   hits = re.hits
    
   # # # bb = re.mappAllCassAndChannels([345,6,25])
   
   # # aa = config.get_monitor()
   
   bb = mapMonitor(vmm2, config)
   
   # ori = getALl