#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 16:38:55 2021

@author: francescopiscitelli
"""

import os 
from lib import libParameters as para
import sys

###############################################################################
############################################################################### 

class transferDataUtil():
             
    def syncData(self,sourcePath,destPath):
        
        command = 'rsync -av --progress'

        # command = 'cp'
        
        comm = command + ' ' + sourcePath + ' ' + destPath
        
        # print(comm)
        
        print('\n ... syncing data ...')
        
        status = os.system(comm)
        
        # NOTE: it will ask for password 
        
        # disp(cmdout)
        
        if status == 0: 
              print('\n data sync completed')
        else:
              print('\n \033[1;31mERROR ... \n\033[1;37m')
        
        # print(status)      
              
        print('\n-----')
        
        return status 
   
    
class dumpTopcapngUtil():

    def __init__(self, parameters):

        self.parameters = parameters


    
    def recordPcapFile(self):

        pathToTshark = self.parameters.fileManagement.pathToTshark

        comm = 'tshark -i asds -c numofpacket -r capture.pcapng'

        if os.path.isfile(pathToTshark+'tshark') is False:
            print('\n \033[1;31mFile conversion pcap to pcapng cannot be performed. \n Tshark not found in your system, either set right path to Thark in parameters or install it.\033[1;37m\n')
            print('... exiting.')
            sys.exit()

        else:

            print(' -> converting pcap to pcapng ...',end='')

        print(1)

        #  to be finished 
        
        # comm = 'sudo tcpdump -1 eno1 -w filename udp port 9000'
        
        # print('\n ... recording pcap data ...')
        
        # status = os.system(comm)
        
        # if status == 0: 
        #       print('\n record completed')
        # else:
        #       print('\n \033[1;31mERROR ... \n\033[1;37m')
        
        # self.syncData(pathsource, desitnationpath)
    

class pcapConverter():
    def __init__(self, parameters):
        
        self.parameters = parameters   
        
        self.flag  = None
        
        self.fileName_OUT = ''
     
    def convertPcap2Pcapng(self,pcapFile_PathAndFileName_IN,pcapngFile_PathAndFileName_OUT):
        
        # comm = 'tcpdump -r file_to_convert -w file_converted '
        
        # self.parameters.pathToTshark = '/Applications/Wireshark.app/Contents/MacOS/'
        
        pathToTshark = self.parameters.fileManagement.pathToTshark
        
        if os.path.isfile(pathToTshark+'tshark') is False: 
            print('\n \033[1;31mFile conversion pcap to pcapng cannot be performed. \n Tshark not found in your system, either set right path to Thark in parameters or install it.\033[1;37m\n')
            print('... exiting.')
            sys.exit()
        
        else:
        
            print(' -> converting pcap to pcapng ...',end='')

            status = os.system(pathToTshark+'tshark -F pcapng -r ' + pcapFile_PathAndFileName_IN + ' -w '+ pcapngFile_PathAndFileName_OUT )
        
            if status == 0: 
              print(' conversion completed!')
            else:
              print('\033[1;31mERROR ... \n\033[1;37m')

      
    def checkExtensionAndConvertPcap(self, pcapFile_PathAndFileName_IN):   
          
          if os.path.isfile(pcapFile_PathAndFileName_IN) is True:
              
             temp1 = os.path.split(pcapFile_PathAndFileName_IN)
             pcapFilePath    = temp1[0]+'/'
             pcapFileNameExt = temp1[1]
             
             temp2 = os.path.splitext(pcapFileNameExt)
             pcapFileName = temp2[0]
             pcapFileExt  = temp2[1]
   
             if pcapFileExt == '.pcap':
                 
                 self.flag = False
                 
                 print('pcap file selected',end='')
                 
                 self.fileName_OUT = pcapFileName + '_convertedToPcapng.pcapng'
                 
                 # check if already converted 
                 if os.path.isfile(pcapFilePath+self.fileName_OUT) is False:
                 
                     self.convertPcap2Pcapng(pcapFile_PathAndFileName_IN, pcapFilePath+self.fileName_OUT)
                     
                 else:
                     print(' -> converted file already exists.')
              
             elif pcapFileExt == '.pcapng':
                 
                 self.flag = True
                 
                 self.fileName_OUT = pcapFileNameExt
                 
             # return self.flag    
                 
          else:
              
              temp1 = os.path.split(pcapFile_PathAndFileName_IN)
              pcapFilePath    = temp1[0]+'/'
              pcapFileNameExt = temp1[1]
              
              print('\n \033[1;31m---> File: ' + pcapFileNameExt + ' DOES NOT EXIST \033[1;37m')
              print('\n ---> in folder: ' + pcapFilePath + ' \n')
              print(' ---> Exiting ... \n')
              print('------------------------------------------------------------- \n')
              sys.exit()

              
          
    
        
###############################################################################
###############################################################################

if __name__ == '__main__':

   path  = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/data/'
   file1 = path+'freia_1k.pcap'
   
   file2 = path+'freia_1k_converted.pcapng'
   
   currentPath = os.path.abspath(os.path.dirname(__file__))+'/'

   parameters = para.parameters(currentPath)
   
   # a = tsharkUtil(parameters)
   
   # a.convertPcan2Pcapng(file1, file2)
   
   b = pcapConverter(parameters).checkExtensionAndConvertPcap(file1)
   
   
   
