#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 13:15:57 2021

@author: francescopiscitelli
"""

import os
import glob
import sys
from PyQt5.QtWidgets import QFileDialog

from lib import libMapping as maps
from lib import libParameters as para

###############################################################################
###############################################################################

class fileDialogue():
    def __init__(self, parameters):
        
        self.openMode  = parameters.fileManagement.openMode
        self.filePath  = parameters.fileManagement.filePath
        
        self.fileName  = parameters.fileManagement.fileName
        
    def openFile(self):
        
        if self.openMode == 'window' :
           self.openWindow()
           
        elif self.openMode == 'fileName' :
           self.openFileName()
           
        elif self.openMode == 'latest' :
           self.openLatestFile()
            
        elif self.openMode == 'secondLast' :
           self.openSecondLastFile() 
            
        elif self.openMode == 'wholeFolder' :
           self.openWholeFolder() 
           
        else:
            print('\n \033[1;31mPlease select a correct open file mode: window, fileName, latest, secondLast or wholeFolder \033[1;37m\n')
            print(' ---> Exiting ... \n')
            print('------------------------------------------------------------- \n')
            sys.exit()
            
        self.checkIfExists()    
        
        if self.openMode == 'wholeFolder' :
            print('\033[1;36mAll Files selected in folder '+self.filePath+' \033[1;37m') 
        else:
            print('\033[1;36mFile selected: '+self.fileName[0]+' \033[1;37m') 
                     
    def checkIfExists(self):
        
        fileNameThatExist = []
            
        # check if file exists in folder
        for fn in self.fileName:
            
           if os.path.exists(self.filePath+fn) is False:
              print(' \033[1;31m---> File: '+fn+' DOES NOT EXIST \033[1;37m')
              print('  ---> in folder: '+self.filePath+' -> ... it will be skipped!')
              # print(' ---> Exiting ... \n')
              # print('------------------------------------------------------------- \n')
              # sys.exit()
              
           else:
                
                fileNameThatExist.append(fn)
                  
              
        self.fileName = fileNameThatExist
        
        if  len(self.fileName) == 0:
            print(' \033[1;31m---> NO File EXIST in given list \033[1;37m')
            print(' ---> Exiting ... \n')
            print('------------------------------------------------------------- \n')
            sys.exit()
            
        #####################################
            
    ###############################################

   
    def openWindow(self):
        
        temp1 = QFileDialog.getOpenFileName(None, "Select Files", self.filePath, "pcapng files (*.pcapng *pcap)")
        temp2 = os.path.split(temp1[0])
        self.filePath = temp2[0]+'/'
        self.fileName = [temp2[1]]
        if self.fileName == ['']:
            print('\n \033[1;31mNothing selected! \033[1;37m\n')
            print(' ---> Exiting ... \n')
            print('------------------------------------------------------------- \n')
            sys.exit()
            
    def openFileName(self):
        
        if isinstance(self.fileName, list) is False:
            
            self.fileName = [self.fileName]
            
        else:
            pass
        
    def openLatestFile(self):
        
        listOfFiles = glob.glob(self.filePath+'/*.pcapng') 
        if not len(listOfFiles):
            print('\n \033[1;31mNo file exists in directory \033[1;37m\n')
            print(' ---> Exiting ... \n')
            print('------------------------------------------------------------- \n')
            sys.exit()
            
        latestFile  = max(listOfFiles, key=os.path.getmtime)
        temp        = os.path.split(latestFile)
        self.filePath       = temp[0]+'/'
        self.fileName       = [temp[1]]
        
    def openSecondLastFile(self):
        
        listOfFiles = glob.glob(self.filePath+'/*.pcapng') 
        if not len(listOfFiles):
            print('\n \033[1;31mNo file exists in directory \033[1;37m\n')
            print(' ---> Exiting ... \n')
            print('------------------------------------------------------------- \n')
            sys.exit()
            
        listOfFiles.sort(key=os.path.getmtime)
        temp2        = os.path.split(listOfFiles[-2])
        self.filePath       = temp2[0]+'/'
        self.fileName       = [temp2[1]]
        
    def openWholeFolder(self):
        
        # here add the possibility to specifiy a piece of the filename as a tag
        
        listOfFiles = glob.glob(self.filePath+'/*.pcapng') 

        listOfFiles.sort(key=os.path.getmtime)
        
        fileName = []
        
        for fp in listOfFiles:
  
            temp = fp.rsplit('/',1)[1]
            
            fileName.append(temp)
            
        self.fileName = fileName  


    
###############################################################################
###############################################################################

if __name__ == '__main__' :
    
    path = '/Users/francescopiscitelli/Documents/PYTHON/MBUTY/develBinary/'
    
    configFilePath  = './'
    configFileName  = "MB300_AMOR_config.json"
    config = maps.read_json_config(configFilePath+configFileName)
    config.get_allParameters()

    parameters = para.parameters(config)
    # 
    parameters.fileManagement.openMode = 'wholeFolder'
    
    
    fileDetails  = fileDialogue(parameters)
    fileDetails.openFile()
    
    print(fileDetails.fileName)
    
    
    