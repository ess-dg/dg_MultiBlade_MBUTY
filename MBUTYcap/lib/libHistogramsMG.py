#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 16:51:12 2021

@author: francescopiscitelli
"""

import numpy as np



# from lib import libSampleData as sdat
# from lib import libMapping as maps
# from lib import libCluster as clu
# from lib import libParameters as para
# from lib import libHistograms as hh
# from lib import libAbsUnitsAndLambda as absu

# from lib import libReadPcapngVMM as pcapr
# from lib import libFileManagmentUtil as fd
# from lib import libTerminal as ta
# from lib import libPlotting as plo

from lib import libHistograms

# import libSampleData as sdat
# import libMapping as maps
# import libCluster as clu
# import libParameters as para
# import libHistograms as hh
# import libAbsUnitsAndLambda as absu
# import libReadPcapngVMM as pcapr
# import libFileManagmentUtil as fd
# import libTerminal as ta
# import libPlotting as plo

 
# makes 1D or 2D histograms

###############################################################################
############################################################################### 

# import default lib 

createAx = libHistograms.createAx
histog   = libHistograms.histog

###############################################################################
############################################################################### 

class allAxis():        
    def __init__(self):
        
        start = 0
        stop  = 1
        steps = 1

        self.axEnergyMON    = createAx(start, stop, steps)
        self.axEnergy    = createAx(start, stop, steps)
        self.axLambda    = createAx(start, stop, steps)
        self.axWires     = createAx(start, stop, steps)
        self.axStrips    = createAx(start, stop, steps)
        self.axWires_mm  = createAx(start, stop, steps)
        self.axStrips_mm = createAx(start, stop, steps)
        self.axToF       = createAx(start, stop, steps)
        self.axMult      = createAx(start, stop, steps)
        self.axInstRate  = createAx(start, stop, steps)
        
    def createAllAxis(self,parameters,cassOffset=0): 
        
        # param.update()
        
        # sine = np.sin(np.deg2rad(parameters.config.DETparameters.bladesInclination))
        
        sinne = 1 
        
        self.axEnergyMON = createAx(0, parameters.MONitor.maxEnerg, parameters.MONitor.energyBins) 
        
        self.axEnergy = createAx(0, parameters.pulseHeigthSpect.maxEnerg, parameters.pulseHeigthSpect.energyBins)
        self.axToF    = createAx(0, parameters.plotting.ToFrange, parameters.plotting.ToFbins)
        self.axLambda = createAx(parameters.wavelength.lambdaRange[0], parameters.wavelength.lambdaRange[1], parameters.wavelength.lambdaBins)
        
        offset = cassOffset*parameters.config.DETparameters.numOfWires
        start  = offset
        stop   = len(parameters.config.DETparameters.cassInConfig)*parameters.config.DETparameters.numOfWires-1 + offset
        steps  = len(parameters.config.DETparameters.cassInConfig)*parameters.plotting.posWbins - int(parameters.plotting.posWbins/parameters.config.DETparameters.numOfWires - 1)
        self.axWires  = createAx(start, stop, steps)
        
        start  = 0
        stop   = parameters.config.DETparameters.numOfStrips-1
        steps  = parameters.plotting.posSbins - int(parameters.plotting.posSbins/parameters.config.DETparameters.numOfStrips - 1)

        self.axStrips = createAx(start, stop, steps)
        
        
        # offset_mm = cassOffset*parameters.config.DETparameters.numOfWires*parameters.config.DETparameters.wirePitch*sine
        # start  = offset_mm
        start  = 0
        
        sine = 1

        stop   = (len(parameters.config.DETparameters.cassInConfig)*parameters.config.DETparameters.numOfWires-1)*4*sine
        steps  = len(parameters.config.DETparameters.cassInConfig)*parameters.plotting.posWbins - int(parameters.plotting.posWbins/parameters.config.DETparameters.numOfWires - 1)

        self.axWires_mm  = createAx(start, stop, steps)
        
        start  = 0
        stop   = (parameters.config.DETparameters.numOfStrips-1)*4
        steps  = parameters.plotting.posSbins - int(parameters.plotting.posSbins/parameters.config.DETparameters.numOfStrips - 1)
        
        self.axStrips_mm = createAx(start, stop, steps)
        
        self.axMult = createAx(0, parameters.config.DETparameters.numOfStrips-1, parameters.config.DETparameters.numOfStrips)
        
        start = -parameters.plotting.ToFrange
        stop  = parameters.plotting.ToFrange
        steps = round((stop-start)/parameters.plotting.instRateBin)
        self.axInstRate = createAx(start, stop, steps)
        
    def updateAllAxis(self):
        
        self.axEnergyMON.update()
        self.axEnergy.update()
        self.axLambda.update()
        self.axWires.update()
        self.axStrips.update()
        self.axWires_mm.update()
        self.axStrips_mm.update()
        self.axToF.update()
        self.axMult.update()
        self.axInstRate.update()
        

    
###############################################################################
############################################################################### 
    
if __name__ == '__main__' :
    
    configFilePath  = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/config/'+"MB300_AMOR_config.json"
    filePathD       = './'+"VMM3a_Freia.pcapng"
   
    parameters  = para.parameters('/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/')
    config = maps.read_json_config(configFilePath)
   
    parameters.loadConfigParameters(config)
    
    parameters.cassettes.cassettes = [1,2]
    
    # parameters.plotting.positionReconstruction = 1
    
    # # parameters.update()
    
    # ax = allAxis()
    
    # ax.axEnergy.start = 0
    # ax.axEnergy.stop  = 65535
    # ax.axEnergy.steps = 128
    
    # ax.axLambda.stop  = 12
    # ax.axLambda.steps = 32
    
    # ax.updateAllAxis()
    
    # ax.axEnergy.update()
    
    # ax.generateAllAxis(config, cassettes)
    
    # ax.axEnergy.stop = 1000
    # ax.updateAllAxis()
    
    # ax.createAllAxis(parameters)
    
    # aa = ax.axStrips_mm.axis
    
    # print(aa)
    
    Nhits = 1e4
    cassettes1 = [1,2,3,4]
      
    bb = sdat.sampleHitsMultipleCassettes(cassettes1)
    bb.generateGlob(Nhits)
    hits = bb.hits

    cc = clu.clusterHits(hits,'globalStat')
    cc.clusterizeManyCassettes(parameters.cassettes.cassettes, parameters.dataReduction.timeWindow)
    events = cc.events
    
    vv = absu.calculateAbsUnits(events, parameters)
    vv.calculatePositionAbsUnit()
    vv.calculateToFandWavelength(0)
    events = vv.events
    
    
    allAxis = hh.allAxis()
    allAxis.createAllAxis(parameters)
    
    selc = events.positionS >= 0
    
    h2D, hProj, hToF = hh.histog().histXYZ(allAxis.axWires.axis, events.positionW, allAxis.axStrips.axis,events.positionS, allAxis.axToF.axis, events.ToF,coincidence=True,showStats=True)
    
    hProjAll = hh.histog().hist1D(allAxis.axWires.axis, events.positionW)
    
    h2D, hProj, hToF = hh.histog().histXYZ(allAxis.axWires.axis, events.positionW[selc], allAxis.axStrips.axis,events.positionS[selc], allAxis.axToF.axis, events.ToF[selc],coincidence=True,showStats=True)
    
    
    # pp = plo.plottingEvents(eventsAT,allAxis)
    # pp.plotXYToF(logScale=False, absUnits = False)
    
    