#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 09:59:00 2024

@author: francescopiscitelli
"""

import numpy as np
import json
import os
import sys
import copy

from lib import libMapping 

# import pandas as pd
# from lib import libReadPcapng as pcapr
# from lib import libSampleData as sdat
# import libSampleData as sdat
# 
# import libReadPcapng as pcapr


# NOTE: THIS SUPPORTS ONLY 1 MONITOR

# hits and BM are loaded from the the default lib 
###############################################################################
###############################################################################   
""" Acts as a pointer/wrapper for the central library """
mapMonitor           = libMapping.mapMonitor
extractPartialConfig = libMapping.extractPartialConfig

# OR 

# class mapMonitor():
#     def __new__(cls, readouts, config):
#         """
#         Acts as a pointer/wrapper for the central library libMapping 
#         """
#         return libMapping.mapMonitor(readouts,config)
    

###############################################################################
###############################################################################   

        
class cassMap():
    def __init__(self):
        
        self.RingID   = None
        self.FenID    = None
        self.hybridWID = None
        self.hybridSID = None
        self.hybridSerial = None
 
class DETparameters():
    def __init__(self):
        
        self.name     = None
        
        self.type     = None
        
        self.operationMode = 'empty'
        
        self.orientation = 'vertical'
        
        self.numOfWires  = 0
        self.numOfStrips = 0
        
        self.numOfCassettes = 0
        
        self.cassInConfig = []
        
        # in degrees 
        self.angularOffset  = float(0)    
        
        # in mm 
        self.linearOffset1stWires  = float(0)
        
        # in mm
        self.wirePitchX  = float(0)
        self.wirePitchZ  = float(0)
        self.stripPitchY = float(0)
        
        self.wiresPerRow = 0
      
################################################        

class read_json_config():
    
    def __init__(self, configFile_PathAndFileName, printFlag = True):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.__init__(self, configFile_PathAndFileName, printFlag) 

    def openFile(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.openFile(self)    

    def __del__(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.__del__(self)  
        
    def __deepcopy__(self, memo):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.__deepcopy__(self, memo)  
        
    def dprint(self, msg): 
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.dprint(self, msg)
    
    def print_DETname(self): 
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.print_DETname(self)
 
    def print_check_operationMode(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.print_check_operationMode(self)

    def get_DETname(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.get_DETname(self)
    
    def get_DETtype(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.get_DETtype(self)
    
    def get_DETmap(self):  
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.get_DETmap(self)
    
    def get_DETcassettesInConfig(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.get_DETcassettesInConfig(self)
    
    def checkRing11(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.checkRing11(self)
    
    def check_cassetteLabelling(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.check_cassetteLabelling(self)
    
    def get_MONmap(self):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.read_json_config.get_MONmap(self)
    
    
        
    def checkOpModeMG(self):
        if self.DETparameters.operationMode == "clustered" and self.DETparameters.type == 'MG':
            print('\n\t\033[1;31mERROR: Operation mode (found {}) not supported yet for MG, only normal mode -> check config file! \n\033[1;37m'.format(self.DETparameters.operationMode),end='') 
            sys.exit()
 
    def get_allParameters(self):
        
        self.get_DETname()
        self.get_DETtype()
        self.get_DETparameters()
        self.get_DETmap()
        self.get_DETcassettesInConfig()
        self.get_MONmap()
        
        self.checkOpModeMG()
        
    def get_DETparameters(self):
        self.DETparameters.numOfWires  = self.conf.get('wires')
        self.DETparameters.numOfStrips = self.conf.get('strips')
        self.DETparameters.wirePitchX  = float(self.conf.get('wirePitchX_mm'))
        self.DETparameters.wirePitchZ  = float(self.conf.get('wirePitchZ_mm'))
        self.DETparameters.stripPitchY = float(self.conf.get('stripPitchY_mm'))
        self.DETparameters.angularOffset         = float(self.conf.get('angularOffset_deg'))
        self.DETparameters.linearOffset1stWires  = float(self.conf.get('linearOffset1stWires_mm'))
        self.DETparameters.numOfCassettes  = self.conf.get('cassettes')
        self.DETparameters.orientation     = self.conf.get('orientation')
        self.DETparameters.operationMode   = self.conf.get('operationMode')
        self.DETparameters.wiresPerRow  = self.conf.get('wiresPerRow')
        

    def get_cassID2RingFenHybrid(self,cassetteID):

        if not cassetteID in self.DETparameters.cassInConfig:
                self.cassMap.RingID   = None
                self.cassMap.FenID    = None
                self.cassMap.hybridWID = None
                self.cassMap.hybridSID = None
                self.cassMap.hybridSerial = None
                print('\t \033[1;33mWARNING: Cassette ID ',str(cassetteID),' not found! Skipped! This CONFIG file only contains cassettes:', end=' ')
                for cass in self.DETparameters.cassInConfig:
                    print(cass,end=' ')
                print('\033[1;37m')
                
        else:
             for cc in self.DETmap.cassettesMap:
                 if cc.get("ID") == cassetteID:
                     self.cassMap.RingID       = cc.get("Ring")
                     self.cassMap.FenID        = cc.get("Fen")
                     self.cassMap.hybridWID    = cc.get("HybridW")
                     self.cassMap.hybridSID    = cc.get("HybridS")
                     self.cassMap.hybridSerial = cc.get("HybridSerial")
                     


###############################################################################
###############################################################################

                
class mapDetector():
    def __init__(self, readouts, config):
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.mapDetector.__init__(self, readouts, config)

           
    def initCatData(self):    # debug
        """ Acts as a pointer/wrapper for the central library """
        return libMapping.mapDetector.initCatData(self)
    
            
    def dprint(self, msg):
       """ Acts as a pointer/wrapper for the central library """
       return libMapping.mapDetector.dprint(self,msg)
        
    def mapp1cass(self, cassette1ID):
        
        if self.debug:
            print(cassette1ID)
        
        self.config.get_cassID2RingFenHybrid(cassette1ID)
        
        if self.debug:
            print(self.config.cassMap.RingID,self.config.cassMap.FenID,self.config.cassMap.hybridWID,self.config.cassMap.hybridSID)
        
        RingLoc = self.readouts.Ring   == self.config.cassMap.RingID
        FenLoc  = self.readouts.Fen    == self.config.cassMap.FenID
        HyWLoc  = self.readouts.hybrid == self.config.cassMap.hybridWID
        HySLoc  = self.readouts.hybrid == self.config.cassMap.hybridSID
        
        selectionCol = np.logical_and(RingLoc,FenLoc)

        selection = np.logical_and(selectionCol , np.logical_or(HyWLoc,HySLoc))
        
        if np.any(selection):
            self.hits.Cassette[selection] = cassette1ID
            flag = True
        else:
            flag = False
            # print('\t \033[1;33m No data found for Cassette ID ',str(cassette1ID),'\033[1;37m')

        #########################################
        # MAPPING CHANNELS HERE : 
        
        ########################################## 
        # WIRES
        selectionWires  =  np.logical_and(selectionCol, HyWLoc)
        
        # tempW_1 = (63 - self.readouts.Channel[selectionWires] + 64*(1-self.readouts.ASIC[selectionWires]))
        
        # tempW_2 = (self.config.DETparameters.wiresPerRow-1) - np.mod( tempW_1 , self.config.DETparameters.wiresPerRow )
        
        # tempW_3 = np.floor_divide( tempW_1 , self.config.DETparameters.wiresPerRow )
        
        # tempW_4 = tempW_2 + tempW_3*self.config.DETparameters.wiresPerRow
        
        # is_even = np.mod(tempW_4 , 2 ) == 0
        
        # tempW  = np.copy(tempW_4)
        
        
        
        # tempW[is_even]  = tempW_4[is_even]  + 1
        # tempW[~is_even] = tempW_4[~is_even] - 1
        
        tempW = self.readouts.Channel[selectionWires] + 64*self.readouts.ASIC[selectionWires]

        # tempW    = (self.readouts.Channel[selectionWires] + 64*self.readouts.ASIC[selectionWires]) 
        # after mapping wires are 0 and strips 1 
        self.hits.WorS[selectionWires] = 0 
        temp1 = self.hits.WorS[selectionWires] 
        
        acceptW  =  tempW < self.config.DETparameters.numOfWires

        if np.any(~acceptW):
             print('Warning: found Wires above {} in MG column {}'.format(self.config.DETparameters.numOfWires-1,cassette1ID))
       
             
        tempW[~acceptW] = -1
        temp1[~acceptW] = -1
        
        self.hits.WiresStrips[selectionWires] = tempW
        self.hits.WorS[selectionWires]        = temp1
        
        ############################################################### 
        # GRIDS
 
        selectionStrips = np.logical_and(selectionCol , HySLoc)
        
        # tempS_1 = self.readouts.Channel[selectionStrips] + 64*self.readouts.ASIC[selectionStrips]
        
        # tempS_2 = 11 - tempS_1
        
        # is_evenS = np.mod(tempS_2 , 2 ) == 0
        
        # tempS  = np.copy(tempS_2)
        
        # tempS[is_evenS]  = tempS_2[is_evenS]  + 1
        # tempS[~is_evenS] = tempS_2[~is_evenS] - 1
        
        tempS = self.readouts.Channel[selectionStrips] + 64*self.readouts.ASIC[selectionStrips]
        
        
        # after mapping wires are 0 and strips 1 
        self.hits.WorS[selectionStrips] = 1 
        temp2 = self.hits.WorS[selectionStrips] 
        
        acceptS  =  tempS < self.config.DETparameters.numOfStrips

        if np.any(~acceptS):
              print('Warning: found Grids above {} in MG column {}'.format(self.config.DETparameters.numOfStrips-1,cassette1ID))
        
        tempS[~acceptS] = -1
        temp2[~acceptS] = -1

        self.hits.WiresStrips[selectionStrips] = tempS
        self.hits.WorS[selectionStrips]        = temp2
        
        ########################################## 
        
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
            print('\t \033[1;33mWARNING: Column IDs: ', end=' ')
            for cass in cassNotFound:
                  print(cass,end=' ')
            print(' not found in DATA file. Mapping skipped for those. \033[1;37m')        
                

            
    def mapChannelsGlob(self):

        # in this case the order is the arrangement in the json file 
        for k, cass in enumerate(self.config.DETparameters.cassInConfig): 
            
            index = k

            selection = np.logical_and( self.hits.Cassette == cass , self.hits.WorS == 0 ) #  wires is WorS = 0
            self.hits.WiresStrips[selection] = self.hits.WiresStrips[selection] + index*self.config.DETparameters.numOfWires
            
            
    def mappAllCassAndChannelsGlob(self):
        
        self.mappAllCass()
        self.mapChannelsGlob()
        
        self.hits.removeUnmappedData()


    
###############################################################################
###############################################################################

if __name__ == '__main__':

   filePath  = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcapMG/config/'+"MG.json"
   # filePathD = './'+"VMM3a_Freia.pcapng"

   config = read_json_config(filePath)
   
   filePath = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcapMG/data/'
   file = 'MG_2col_2clusters.pcapng'
     # file = 'sampleData_ClusteredMode.pcapng'
     
   # file = 'MG_2col_1cluster.pcapng'

   filePathAndFileName = filePath+file
   
   NSperClockTick = 11.356860963629653  #ns per tick ESS for 88.0525 MHz
   
   pcapng = pcapr.pcapng_reader(filePathAndFileName, NSperClockTick, config.MONmap.TTLtype, config.MONmap.RingID,  timeResolutionType='fine', sortByTimeStampsONOFF = False, operationMode=config.DETparameters.operationMode)

   readouts = pcapng.readouts
   readoutsArray = readouts.concatenateReadoutsInArrayForDebug()
   

   md  = mapDetector(readouts, config)
   md.mappAllCassAndChannelsGlob()
   hits = md.hits
   hitsArray  = hits.concatenateHitsInArrayForDebug()
   
   # parameters.loadConfigParameters(config)
   
   # config.check_cassetteLabelling()
   
   # name = config.get_DETname()
   # config.get_DETcassettesInConfig()
   
   # config.get_cassID2RingFenHybrid(5)
   # print(config.cassMap.RingID, config.cassMap.FenID, config.cassMap.hybridID, config.cassMap.hybridSerial)
   # # config.get_cassID2RingFenHybrid(55)
   # # print(config.RingID, config.FenID, config.hybridID)
   # # config.get_cassID2RingFenHybrid(1)
   # # print(config.RingID, config.FenID, config.hybridID)
   
   # # config.get_cassID2RingFenHybrid([1,41])
   
   # config.get_bladesInclination()
   # config.get_pitches()
   # config.get_offset1stWires()
   
   # pr = pcapr.pcap_reader(filePathD)
   #   # pr.debug = True
   #  pr.read()
   #  vmm1 = pr.readouts
   
   # vmm2 = sdat.sampleReadouts_2()
   # vmm2.fill()
   # readouts = vmm2.readouts

   
   
   # re  = mapDetector(readouts, config)
   # re.debug = True
   # re.initCatData()
   # data1 = re.catData
   

   # re.mapp1cass(1)
   # # # bb = re.mapp1cass(45)
   
   # aa  = re.mappAllCass([1,2,45,3,56])
   
   # # # cassettes = np.arange(0,34,1)
    
   # re.mappAllCassAndChannels()
   
   # re.mappAllCassAndChannelsGlob()
   
   # re.initCatData()
   # data = re.catData
   
   # re.mappAllCassAndChannelsGlob()
   # hits = re.hits
   
   # hits = re.hits
   # hitsArray = hits.concatenateHitsInArrayForDebug()
    
   # # # bb = re.mappAllCassAndChannels([345,6,25])
   
   # # aa = config.get_monitor()
   
   # bb = mapMonitor(vmm2, config)
   
   # ori = getALl