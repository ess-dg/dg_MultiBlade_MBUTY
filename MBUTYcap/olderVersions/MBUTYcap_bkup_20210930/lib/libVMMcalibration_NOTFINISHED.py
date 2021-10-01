#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 11:05:36 2021

@author: francescopiscitelli
"""
import numpy as np
import json
import os

import sys

# import pandas as pd
import libReadPcapngVMM as pcapr

###############################################################################
###############################################################################

# class calibration():
    
    

class read_json_calib():
    def __init__(self, calibFile_PathAndFileName):
        
        temp =  os.path.split(calibFile_PathAndFileName)
            
        self.calibFilePath = temp[0]+'/'
        self.calibFileName = temp[1]
        
        try:
            self.ff   = open(calibFile_PathAndFileName,'r') 
        except:
            print('\n \033[1;31m---> Calibration File: ' + self.calibFileName + ' not found \033[1;37m')
            print('\n ---> in folder: ' + self.calibFilePath + ' \n -> exiting.')
            sys.exit()
            
        self.calib = json.load(self.ff)
        
        
        
        
###############################################################################
###############################################################################       

class calibrateVMM():
    def __init__(self,readouts,calib):
        
        self.readouts = readouts
        self.calib    = calib
        
    def calibrateTimeStamp(self,timeResolution):
        
        time_offset = 1000
        
        time_slope  = 1
        
        TDC_calib = pcapr.VMM3A_convertCalibrate_TDCinSec(self.readouts.TDC,timeResolution,time_offset,time_slope).TDC_ns
          
        self.readouts.timeStamp  = self.readouts.timeCoarse  + TDC_calib
       
        
    def calibrateADC(self):  
        
        ADC_offset = 100
        
        ADC_slope = 1
        
        self.readouts.ADC = pcapr.VMM3A_calibrate_ADC(self.readouts.ADC,ADC_offset,ADC_slope).ADC_calibrated     
        
      
  
###############################################################################
###############################################################################

if __name__ == '__main__':

   filePathCalib  = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/config/'+"TBCALIB.json"
   path = '/Users/francescopiscitelli/Desktop/dataPcapUtgard/'
   
   filePath = path+'pcap_for_fra.pcapng'
   # filePath = path+'pcap_for_fra_ch2test.pcapng'
   # filePath = path+'pcap_for_fra_ch2test_take2.pcapng'
   filePath = path+'pcap_for_fra_coinc.pcapng'
   # filePath = path+'freiatest.pcapng'
   timeResolution = 11.356860963629653  #s per tick ESS for 88.0525 MHz
   pcap = pcapr.pcapng_reader(filePath, timeResolution, sortByTimeStampsONOFF = True)
   readouts = pcap.readouts 
   readoutsArrayIn = readouts.concatenateReadoutsInArrayForDebug()
   
   aa = readouts.timeCoarse - readouts.timeStamp

   # calib = read_json_calib(filePathCalib)
   
   # cali = calibrateVMM(readouts,calib)
   # cali.calibrateADC()
   # cali.calibrateTimeStamp(timeResolution)
   
   # readoutsOut = cali.readouts
   # readoutsArrayOut = readoutsOut.concatenateReadoutsInArrayForDebug()
   
   # aa = readouts.ADC - readoutsOut.ADC
   
   # bb = readouts.timeStamp - readoutsOut.timeStamp
   
   # aa1 = readoutsArrayIn[0,8] - readoutsArrayOut[0,8]
   
   # bb1 = readoutsArrayIn[0,0] - readoutsArrayOut[0,0]