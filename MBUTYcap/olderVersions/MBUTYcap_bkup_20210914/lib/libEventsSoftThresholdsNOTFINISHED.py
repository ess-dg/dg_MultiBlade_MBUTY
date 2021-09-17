#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:04:54 2021

@author: francescopiscitelli
"""


import numpy as np
import time
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd


import libReadPcapngVMM as pcapr
import libSampleData as sdat
import libMapDetector as maps
import libCluster as clu
import libAbsUnitsAndLambda as absu
import libHistograms as hh
import libParameters as para
import libPlotting as plo


###############################################################################
###############################################################################

class thresholdFile():
    
    def __init__(self, parameters):
        
        self.parameters = parameters
    
    def load(self, cassettes):
        
        self.softTh = np.zeros((len(cassettes),self.parameters.configJsonFile.numOfWires+self.parameters.configJsonFile.numOfStrips))
        
        sthfullpath = self.parameters.fileManagement.thresholdFilePath+self.parameters.fileManagement.thresholdFileName
            
        if os.path.exists(sthfullpath) == False:
            print('\n \033[1;33m---> WARNING ... File: '+sthfullpath+' NOT FOUND\033[1;37m')
            print("\t ... software thresholds switched OFF ... ")
            self.parameters.dataReduction.softThreshold = 0
            time.sleep(2)
            return self.softTh, self.parameters.dataReduction.softThreshold
        else:
            cassInFile  = pd.read_excel(sthfullpath).columns
            temp  = pd.read_excel(sthfullpath).values
            temp  = np.matrix.transpose(temp)
                 
        for k, cc in enumerate(cassettes):
            
            print(cc)
           
            if not(cc in cassInFile):
                 print('\n \033[1;33m---> WARNING ... Threshold File does NOT contain all the cassettes IDs\033[1;37m')
                 print("\t ... software thresholds switched OFF for cassette ID  "+str(cc))
                 self.softTh[k,:] = 0  
            else:
                 index = np.where(cc == cassInFile)
                 self.softTh[k,:] = temp[index,:]
                
                
                NOTA NOTA NOTA
                
               fallo diverso dove gli  ID seguono le th
               
               self.ID
               self.wireChTh
               self.stripChTh
               
               
        
        return self.softTh, self.parameters.dataReduction.softThreshold









###############################################################################
###############################################################################

if __name__ == '__main__':

    plt.close("all")
    
    configFilePath = './'+"MB300_AMOR_config.json"
    
    config = maps.read_json_config(configFilePath)
    
    parameters = para.parameters(config)
    
    parameters.cassettes.cassettes = [1,2,3,4,5]
    
    parameters.wavelength.distance = 19000
    
    parameters.fileManagement.thresholdFilePath = './'
    parameters.fileManagement.thresholdFileName = 'MB300L_thresholds.xlsx'
    
    parameters.configJsonFile.offset1stWires = 10
    
    
    th = thresholdFile(parameters)
    softTh, parameters.dataReduction.softThreshold = th.load([1,2,9])
    

    #  generate sample hits 
    Nhits = 1e4
    cassettes1 = [1,2,4]
      
    hits2 = sdat.sampleHitsMultipleCassettes(cassettes1)
    hits2.generateGlob(Nhits)
    
    cassettes = [1,2,3]
    
    timeWindow = 2e-6
    
    cc = clu.clusterHits(hits2,0)
    cc.clusterizeManyCassettes(parameters.cassettes.cassettes, timeWindow)
    
    vv = absu.calculateAbsUnits(cc.events, parameters)
   
    vv.calculatePositionAbsUnit()

    vv.calculateToFandWavelength(0)
   
    events = vv.events
    
    allAxis = hh.allAxis()
    allAxis.createAllAxis(parameters)
    
    pp = plo.plottingEvents(events,allAxis)
    # pp.plotXYToF(logScale=True, absUnits = True)
    
    # pp.plotXLambda(logScale=False, absUnits = False)
    
    # aa = pp.plotMultiplicity([1,2,3])
    
    pp.plotPHS([1,2,3],parameters)
    
    # pp.plotPHScorrelation([1,2,3])