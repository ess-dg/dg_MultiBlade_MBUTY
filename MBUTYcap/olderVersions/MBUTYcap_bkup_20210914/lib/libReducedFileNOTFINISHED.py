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


import libReadPcapngVMM as pcapr
import libSampleData as sdat
import libMapDetector as maps
import libCluster as clu
import libAbsUnitsAndLambda as absu

###############################################################################
###############################################################################

class saveReducedDataToHDF():
    def __init__(self, savereducedpath, fileName = 'temp'):
        
        self.nameMainFolder  = 'entry1'

        self.compressionHDFT  = 'gzip'  
        self. compressionHDFL = 9 # gzip compression level 0 - 9
        
        ###########################
        
        if not os.path.exists(savereducedpath):
           os.makedirs(savereducedpath)
    
        # outfile = savereducedpath+fnamepart1[:-1]+'-reduced-PY-From'+str(format(acqnum[0],'03d'))+'To'+str(format(acqnum[-1],'03d'))+fnamepart3
        
        outfile = savereducedpath+fileName+'.h5'
    
        # check if file already exist and in case yes delete it 
        if os.path.exists(outfile):
            print('\n \033[1;33mWARNING: Reduced DATA file exists, it will be overwritten!\033[1;37m')
            os.system('rm '+outfile)
       
        # # if you want to save reduced data, it must include lambda, so lambda calculation is turned ON if not yet 
        # if calculateLambda is False:
        #     calculateLambda = True
        #     print('\n \t Lambda calculation turned ON to save reduced DATA')
     
        self.fid    = h5py.File(outfile, "w")
    
        # create groups in h5 file  
        self.gdet   = self.fid.create_group(self.nameMainFolder+'/detector')
        self.ginstr = self.fid.create_group(self.nameMainFolder+'/instrument')
    
        # for key, value in {
        #             'ToF-duration (s)': ToFduration,
        #             'DistanceAtWindow (mm)': DistanceAtWindow,
        #             'Distance (mm)': Distance,
        #             'DistanceSampleWindow (mm)': DistanceSampleWindow,
        #             'DistanceSample1stWire mm)' : DistanceSample1stWire,
        #             'PickUpTimeShift (s)': PickUpTimeShift,
        #             'BladeAngularOffset (deg)': BladeAngularOffset,
        #             'OffsetOf1stWires (mm)': OffsetOf1stWires,
        #             }.items():
        #     ginstr.attrs.create(key, value)
    
        self.grun   = self.fid.create_group(self.nameMainFolder+'/run')
    
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
        
        # self.events = events
    
        self.gdet.create_dataset('positionW', data= events.positionW, compression=self.compressionHDFT, compression_opts=self.compressionHDFL)
        
        # gdetdigit = self.gdet.create_group('digit'+ str(digitID[dd]))
        # gdetdigit.create_dataset('data', data=POPHcum, compression=compressionHDFT, compression_opts=compressionHDFL)
 
    
        self.__del__()
        
###############################################################################
###############################################################################

if __name__ == '__main__':

   configFilePath  = './'+"MB300_AMOR_config.json"
   filePathD       = './'+"VMM3a_Freia.pcapng"
   
   tProfilingStart = time.time()

   # config = read_detector_config(filePath)
   
   # name = config.get_DetectorName()
   # config.get_cassettesInConfig()
   
   # config.get_cassID2RingFenHybrid(5)
   # print(config.RingID, config.FenID, config.hybridID)
   # config.get_cassID2RingFenHybrid(55)
   # print(config.RingID, config.FenID, config.hybridID)
   # config.get_cassID2RingFenHybrid(1)
   # print(config.RingID, config.FenID, config.hybridID)
   
   # config.get_cassID2RingFenHybrid([1,41])
   

   
   # pr = pcapr.pcap_reader(filePathD)
   #   #  # pr.debug = True
   # pr.read()
   # vmm1 = pr.readouts
   
   # vmm2 = sdat.sampleData()
   # vmm2.fill()

   # cassettes = [1,2,3,4,5]

   # re  = maps.mapDetector(vmm1, filePath)
   #    # re.debug = False
   #    # re.initCatData()

   # re.mappAllCassAndChannels_GlobalCoord(cassettes)
   # hits = re.hits
   
   Nhits = 30
   cassettes = [1,2,4]
     
   hits = sdat.sampleHitsMultipleCassettes(cassettes)
   hits.generate(Nhits)
   
   
    
   # cc = clusterHits(hits) 
   
   # allEvents= events()
   # aa, bb = cc.clusterize1cassette(1,2e-6)
   
   # allEvents.append(cc.events)
   
   # dd = np.loadtxt('dataset1_large_Sorting=True_Filtering=False_Clustered.txt',dtype='float64',delimiter=' ')
   
   
   # aa1, bb1 = cc.clusterize1cassette(3,2e-6)
   
   # allEvents.append(cc.events)
   
   cassette = [1,2]
   
   cc = clu.clusterHits(hits)
   cc.clusterizeManyCassettes(cassette, 2e-6)
   
   events =  cc.allCassEvents
   
   vv = absu.calculateAbsUnits(events, configFilePath, cassette)
   
   offset1stWires = 11 #mm
   
   vv.calculatePositionAbsUnit(offset1stWires)
   
   Distance = 5000 #mm
   ToFduration = 0.1 #s
   
   # vv.calculateWavelength(Distance,ToFduration)
   
   vv.calculateToFandWavelength(0,Distance,ToFduration)
   
   events = vv.events
   
   
   
   tElapsedProfiling = time.time() - tProfilingStart
   print('\n Completed in %.2f s' % tElapsedProfiling) 
   
   savereducedpath = './'
   
   gg = saveReducedDataToHDF(savereducedpath)
   gg.save(events)
   
   # 