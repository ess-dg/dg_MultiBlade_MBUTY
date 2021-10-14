#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 14:18:41 2021

@author: francescopiscitelli
"""

import numpy as np
import time
import os
import h5py


from lib import libReadPcapngVMM as pcapr
from lib import libSampleData as sdat
from lib import libMapping as maps
from lib import libCluster as clu
from lib import libAbsUnitsAndLambda as absu
from lib import libParameters as para

###############################################################################
###############################################################################

class saveReducedDataToHDF():
    def __init__(self, parameters, saveReducedPath, fileName):
        
        self.par = parameters
        
        self.nameMainFolder  = self.par.fileManagement.reducedNameMainFolder

        self.compressionHDFT  = self.par.fileManagement.reducedCompressionHDFT
        self.compressionHDFL  = self.par.fileManagement.reducedCompressionHDFL
        
        ###########################
        
        if not os.path.exists(saveReducedPath):
           os.makedirs(saveReducedPath)

        self.outfile = saveReducedPath+fileName+'.h5'
    
        # check if file already exist and in case yes delete it 
        if os.path.exists(self.outfile):
            print('\n \033[1;33mWARNING: Reduced DATA file exists, it will be overwritten!\033[1;37m')
            os.system('rm '+self.outfile)
      
        self.fid    = h5py.File(self.outfile, "w")
    
        # create groups in h5 file  
        self.gdet   = self.fid.create_group(self.nameMainFolder+'/detector')
        self.ginstr = self.fid.create_group(self.nameMainFolder+'/instrument')
        self.grun   = self.fid.create_group(self.nameMainFolder+'/run')
        
        self.gdet_data  = self.gdet.create_group('events')
        self.gdet_param = self.gdet.create_group('parameters')
        
        # self.gdet_param.create_dataset('positionW', data= events.positionW, compression=self.compressionHDFT, compression_opts=self.compressionHDFL)

        for key, value in {
                    'clockFreq': self.par.clockTicks.clockFreq,
                    'NSperClockTick': self.par.clockTicks.NSperClockTick,
                    'detectorName': self.par.configJsonFile.detectorName,
                    'cassettesInConfig': self.par.configJsonFile.cassInConfig,
                    'numOfCassettes': self.par.configJsonFile.numOfCassettes,
                    'numOfWires': self.par.configJsonFile.numOfWires,
                    'numOfStrips': self.par.configJsonFile.numOfStrips,
                    'orientation': self.par.configJsonFile.orientation,
                    'wirePitch': self.par.configJsonFile.wirePitch,
                    'stripPitch': self.par.configJsonFile.stripPitch,
                    'offset': self.par.configJsonFile.offset1stWires,
                    'inclination': self.par.configJsonFile.bladesInclination,
                    }.items():
            self.gdet_param.create_dataset(key, data=value)
            
        for key, value in {
                    'chopperFreq': self.par.wavelength.chopperFreq,
                    'chopperPeriod': self.par.wavelength.chopperPeriod,
                    'distance': self.par.wavelength.distance,
                    }.items():
            self.ginstr.create_dataset(key, data=value)
    
        #for key, value in {
        #             'ToF-duration (s)': parameters.ToF,
        #             'DistanceAtWindow (mm)': DistanceAtWindow,
        #             'Distance (mm)': Distance,
        #             'DistanceSampleWindow (mm)': DistanceSampleWindow,
        #             'DistanceSample1stWire mm)' : DistanceSample1stWire,
        #             'PickUpTimeShift (s)': PickUpTimeShift,
        #             'BladeAngularOffset (deg)': BladeAngularOffset,
        #             'OffsetOf1stWires (mm)': OffsetOf1stWires,
        #             }.items():
        #     ginstr.attrs.create(key, value)
    
        
    
        # if MONfound is True:
        #     gmon = fid.create_group(nameMainFolder+'/monitor')
        #     gmon.attrs.create('columns:ToF,PH,lambda',1)
        #     gmon.attrs.create('units:seconds,a.u.,angstrom',1)
    ##### 

    #grun.create_dataset('duration', data=(len(acqnum)*(SingleFileDuration or 0)))
    #grun.attrs.create('seconds',1)
    
        self.gdet.attrs.create('columns:X,Y,ToF,PHwires,PHstrips,multW,multS,Z,lambda',1)
        # if reducedDataInAbsUnit is True:
        #     gdet.attrs.create('units:mm,mm,seconds,a.u.,a.u.,int,int,mm,angstrom',1)
        #     elif reducedDataInAbsUnit is False:
        #         gdet.attrs.create('units:chNum,chNum,seconds,a.u.,a.u.,int,int,mm,temp.angstrom',1)
 
        # gdet.create_dataset('arrangement', data=digitID ) #physical order of the digitizers
        
    def __del__(self):
        try:
            self.fid.close()
        except:
            pass
 
    def save(self, events):
        print('saving data  to  h5 file')
        
        self.events = events
        
        # self.gdet_data.create_dataset('events', data = self.events, compression=self.compressionHDFT, compression_opts=self.compressionHDFL)
        
        for key, value in {
                    'Cassette': self.events.Cassette,
                    'CassetteIDs': self.events.CassetteIDs,
                    'Duration': self.events.Duration,
                    'Durations': self.events.Durations,
                    'Nevents': self.events.Nevents,
                    'NeventsNotRej2D': self.events.NeventsNotRej2D,
                    'NeventsNotRejAfterTh': self.events.NeventsNotRejAfterTh,
                    'NeventsNotRejAll': self.events.NeventsNotRejAll,
                    'PHS': self.events.PHS,
                    'PHW': self.events.PHW,
                    'PrevPT': self.events.PrevPT,
                    'PulseT': self.events.PulseT,
                    'ToF': self.events.ToF,
                    'multS': self.events.multS,
                    'multW': self.events.multW,
                    'positionS': self.events.positionS,
                    'positionSmm': self.events.positionSmm,
                    'positionW': self.events.positionW,
                    'positionWmm': self.events.positionWmm,
                    'positionZmm': self.events.positionZmm,
                    'timeStamp': self.events.timeStamp,
                    'wavelength': self.events.wavelength,
                    
                    }.items():
             self.gdet_data.create_dataset(key, data = value, compression=self.compressionHDFT, compression_opts=self.compressionHDFL)
       
        
    
        
        # gdetdigit = self.gdet.create_group('digit'+ str(digitID[dd]))
        # gdetdigit.create_dataset('data', data=POPHcum, compression=compressionHDFT, compression_opts=compressionHDFL)
 
    
        self.__del__()
        
         
###############################################################################
###############################################################################       
        
class readReducedDataFromHDF():
    # def __init__(self, parameters, saveReducedPath, fileName):
        
        print('to be implemented')
        
###############################################################################
###############################################################################

if __name__ == '__main__':

    configFilePath  = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/config/'+"MB300_AMOR_config.json"
    filePathD       = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/data/'+"freiatest.pcapng"
   
    tProfilingStart = time.time()
    parameters  = para.parameters('/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/')
    config = maps.read_json_config(configFilePath)
   
    parameters.loadConfigParameters(config)
    
    # pcap = pcapr.pcapng_reader(filePathD, parameters.clockTicks.NSperClockTick, sortByTimeStampsONOFF = False)
    # readouts = pcap.readouts
    # md  = maps.mapDetector(readouts, config)
    # md.mappAllCassAndChannelsGlob()
    # hits = md.hits
    # cc = clu.clusterHits(hits,parameters.plotting.showStat)
    # cc.clusterizeManyCassettes(parameters.cassettes.cassettes, parameters.dataReduction.timeWindow)
    # events = cc.events


    sav = saveReducedDataToHDF(parameters,'/Users/francescopiscitelli/Desktop/reducedFile/','temp')
    
    Nevents = 10
    
    dd = sdat.sampleEventsMultipleCassettes([1,2,3,4,5,6],'/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/data/')
    dd.generateGlob(Nevents)
    events  = dd.events
    eventsArray = events.concatenateEventsInArrayForDebug()


    # events = 1
    sav.save(events)