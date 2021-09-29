#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:24:18 2021

@author: francescopiscitelli
"""
import argparse
import os
import sys
from datetime import datetime

class dumpToPcapngUtil():

    def __init__(self, pathToTshark, interface='en0', destPath='./', fileName='temp'):

        if os.path.isfile(pathToTshark+'tshark') is False:
            print('\n \033[1;31mFile Tshark not found in your system, either set right path to Thark in parameters or install it.\033[1;37m\n')
            print('... exiting.')
            sys.exit()

        self.pathToTshark = pathToTshark
        self.interface    = interface
        
        nowTime = datetime.now()
        current_date = nowTime.strftime("%Y%m%d")
        current_time = nowTime.strftime("%H%M%S")

        self.fileh = destPath+current_date+'_'+current_time+'_'+fileName+'.pcapng'
        
    def dump(self,typeCapture='packets',extraArgs=100):
    
        self.typeCapture = typeCapture
        # comm = 'sudo tcpdump -1 eno1 -w filename udp port 9000'
        
        print('\n ... recording pcapng file ...')

        ###############################
        if self.typeCapture == 'packets':
            
            print(' by packets -> {} packets'.format(extraArgs))
            
            numOfPackets = extraArgs
            
            self.recordByNumOfPackets(numOfPackets)
            
        elif self.typeCapture == 'filesize':
            
            print(' by file size -> {} kbytes'.format(extraArgs))
            
            sizekbytes = extraArgs
            
            self.recordBySize(sizekbytes)
            
            
        elif self.typeCapture == 'duration':
            
            print(' by duration -> {} s'.format(extraArgs))
            
            duration_s = extraArgs
            
            self.recordByDuration(duration_s)  
            
        ###############################   
        
        string1 = self.pathToTshark+'tshark'+' -i '+str(self.interface)
        string2 = ' -w '+self.fileh
        
        self.command = string1+self.commandDetails+string2
        
        status = os.system(self.command)

        if status == 0: 
              print('\n recording completed!')
        else:
              print('\n \033[1;31mERROR ... \n\033[1;37m')
              
 ###############################       
    def recordByNumOfPackets(self,numOfPackets):
          
        self.commandDetails = ' -c '+str(numOfPackets)

    def recordBySize(self,sizekbytes):  
        
        self.commandDetails = ' -a filesize:'+str(sizekbytes)
    
    def recordByDuration(self,duration_s):  
        
        self.commandDetails = ' -a duration:'+str(duration_s)
        
        
    
        
###############################################################################
###############################################################################        
        
if __name__ == '__main__':
    
   # parser = argparse.ArgumentParser()
   # # parser.add_argument("-i", metavar='interface', help = "interface", type = str, default = "enp0s25")
   # parser.add_argument("-f", "--file", metavar='fileName', help = "pcapng file", type = str, default = "temp")
   # parser.add_argument("-i", "--interface", metavar='interface', help = "interface", type = str, default = "en0")
   # parser.add_argument("-t", "--tshark", metavar='pathToTshark', help = "tshark path", type = str, default = "/Applications/Wireshark.app/Contents/MacOS/")
   # parser.add_argument("-d", "--destination", metavar='dest path', help = "dest path", type = str, default = "/Users/francescopiscitelli/Desktop/reducedFile/")
   
   # parser.add_argument("-c", "--captureType", metavar='captureType', help = "captureType: packets, filesize (kb) or duration (s)", type = str, default = "packets")
   
   # parser.add_argument("-q", "--quantity", metavar='quantity', help = "quantity: num ofpackets, or kb filesize, or s for duration", type = str, default = "100")
   
   parser = argparse.ArgumentParser()
   # parser.add_argument("-i", metavar='interface', help = "interface", type = str, default = "enp0s25")
   parser.add_argument("-f", "--file", metavar='fileName', help = "pcapng file", type = str, default = "temp")
   parser.add_argument("-i", "--interface", metavar='interface', help = "interface", type = str, default = "enp0s25")
   parser.add_argument("-t", "--tshark", metavar='pathToTshark', help = "tshark path", type = str, default = "/usr/sbin/")
   parser.add_argument("-d", "--destination", metavar='dest path', help = "dest path", type = str, default = "/home/essdaq/pcaps/")
   
   parser.add_argument("-c", "--captureType", metavar='captureType', help = "captureType: packets, filesize (kb) or duration (s)", type = str, default = "packets")
   
   parser.add_argument("-q", "--quantity", metavar='quantity', help = "quantity: num ofpackets, or kb filesize, or s for duration", type = str, default = "100")
   
   args  = parser.parse_args()
   
   rec = dumpToPcapngUtil(pathToTshark=args.tshark, interface=args.interface, destPath=args.destination, fileName=args.file)

   # rec = dumpToPcapngUtil(pathToTshark, interface='en0', destPath='/Users/francescopiscitelli/Desktop/reducedFile/', fileName='temp')

   # rec.dump('duration',2)
   
   # rec.dump('filesize',130)
   
   rec.dump(args.captureType,args.quantity)
