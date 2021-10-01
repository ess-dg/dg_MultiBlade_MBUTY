#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:24:18 2021

@author: francescopiscitelli
"""
import argparse
# import os
# import sys
# from datetime import datetime
# import subprocess

from lib import libTerminal as ta

############################################################################### 
###############################################################################

class dumpToFile():
    
     def __init__(self, pathToTshark, interface='en0', destPath='./', fileName='temp', captureType='packets', quantity=100):
         
         rec = ta.dumpToPcapngUtil(pathToTshark, interface, destPath, fileName)
         
         sta = ta.acquisitionStatus(destPath)  
         sta.set_RecStatus()
         
         status = rec.dump(captureType,quantity)
        
         if status == 0: 
              sta.set_FinStatus()
         else:
              sta.set_RecStatus()
      

###############################################################################
###############################################################################        
        
if __name__ == '__main__':
    
   parser = argparse.ArgumentParser()
     
   #  ARGS for FRAPIS LAPTOP
   # parser.add_argument("-i", "--interface", metavar='interface', help = "interface", type = str, default = "en0")
   # parser.add_argument("-t", "--tshark", metavar='pathToTshark', help = "tshark path", type = str, default = "/Applications/Wireshark.app/Contents/MacOS/")
   # parser.add_argument("-d", "--destination", metavar='dest path', help = "dest path", type = str, default = "/Users/francescopiscitelli/Desktop/reducedFile/")

   
   #  ARGS for ESSDAQ
   parser.add_argument("-i", "--interface", metavar='interface', help = "interface", type = str, default = "p4p1")
   parser.add_argument("-t", "--tshark", metavar='pathToTshark', help = "tshark path", type = str, default = "/usr/sbin/")
   parser.add_argument("-d", "--destination", metavar='dest path', help = "dest path", type = str, default = "/home/essdaq/pcaps/")
   
   
   parser.add_argument("-f", "--file", metavar='fileName', help = "pcapng file", type = str, default = "temp")
   parser.add_argument("-c", "--captureType", metavar='captureType', help = "captureType: packets, filesize (kb) or duration (s)", type = str, default = "packets")
   parser.add_argument("-q", "--quantity", metavar='quantity', help = "quantity: num of packets, or kb filesize, or s for duration", type = str, default = "100")
   
   args  = parser.parse_args()
   
   rec = dumpToFile(pathToTshark=args.tshark, interface=args.interface, destPath=args.destination, fileName=args.file,captureType=args.captureType,quantity=args.quantity)

   
