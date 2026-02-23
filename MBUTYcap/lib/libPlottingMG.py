#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 10:46:16 2021

@author: francescopiscitelli
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import time

# from lib import libSampleData as sdat
# from lib import libMapping as maps
# from lib import libCluster as clu
# from lib import libAbsUnitsAndLambda as absu
from lib import libHistogramsMG as hh
# from lib import libParameters as para
# from lib import libReadPcapngVMM as pcapr

from lib import libPlotting

# import libSampleData as sdat
# import libMappingMG as maps
# import libCluster as clu
# import libAbsUnitsAndLambda as absu
# import libHistograms as hh
# import libParameters as para
# import libReadPcapngVMM as pcapr

###############################################################################
############################################################################### 

# import default lib 

preparePlotMatrix  = libPlotting.preparePlotMatrix
checkReadoutsClass = libPlotting.checkReadoutsClass
checkHitsClass     = libPlotting.checkHitsClass
checkEventsClass   = libPlotting.checkEventsClass
logScaleMap        = libPlotting.logScaleMap
plottingMON        = libPlotting.plottingMON

###############################################################################
###############################################################################   
        
class plottingReadouts():
   
    def __init__(self, readouts, parameters, outOfBounds = True):
    
        self.parameters  = parameters
        self.config      = parameters.config
        self.outOfBounds = outOfBounds
        
        checkke = checkReadoutsClass(readouts)
        self.readouts = checkke.readouts
        self.flag = checkke.flag 
        
        # self.parameters = parameters
        if self.flag is True:
            self.xbins = np.linspace(0,63,64)
            
    
    def selectHybridFromCassetteID(self,cassette1ID):
        if self.flag is True:
             self.config.get_cassID2RingFenHybrid(cassette1ID)
    
             sel1 = self.readouts.Ring   == self.config.cassMap.RingID
             sel2 = self.readouts.Fen    == self.config.cassMap.FenID
             sel3 = self.readouts.hybrid == self.config.cassMap.hybridWID
             sel4 = self.readouts.hybrid == self.config.cassMap.hybridSID
            
             selectedHybridfromCassID_BoolArrayW = sel1 & sel2 & sel3
             selectedHybridfromCassID_BoolArrayS = sel1 & sel2 & sel4
            
             return selectedHybridfromCassID_BoolArrayW, selectedHybridfromCassID_BoolArrayS
         
        
    def histChRaw1hybrid(self,cassette1ID):
        
        if self.flag is True:
            self.config.get_cassID2RingFenHybrid(cassette1ID)
    
            # cassette correpsonds to a particluar triplet of ring fen and hybrid so Icanuse cassette to loop over hybrids
            
            # print(self.config.cassMap.RingID)
            # print(self.config.cassMap.FenID)
            # print(self.config.cassMap.hybridID)
            
            sel1 = self.readouts.Ring   == self.config.cassMap.RingID
            sel2 = self.readouts.Fen    == self.config.cassMap.FenID
            sel3 = self.readouts.hybrid == self.config.cassMap.hybridWID
            sel4 = self.readouts.hybrid == self.config.cassMap.hybridSID
            
            # sel = sel1 & sel2 & sel3
            
            selW = sel1 & sel2 & sel3
            selS = sel1 & sel2 & sel4
            
            # wireCh0to31 = np.mod(self.hits.WiresStrips[cass & wires],self.config.DETparameters.numOfWires)
            
            if self.config.DETparameters.operationMode == 'normal':
                asic0  = self.readouts.ASIC == 0
                asic1  = self.readouts.ASIC == 1
                self.histo0 = hh.histog(self.outOfBounds).hist1D(self.xbins, self.readouts.Channel[selW & asic0])
                self.histo1 = hh.histog(self.outOfBounds).hist1D(self.xbins, self.readouts.Channel[selW & asic1])
                self.histo2 = hh.histog(self.outOfBounds).hist1D(self.xbins, self.readouts.Channel[selS & asic0])
                self.histo3 = hh.histog(self.outOfBounds).hist1D(self.xbins, self.readouts.Channel[selS & asic1])
                
            elif self.config.DETparameters.operationMode == 'clustered':
                print(' --> other modes than normal is not supported for MG')
  
        
    def plotChRaw(self,cassetteIDs): 
        
        if self.flag is True:
        
            self.ploth = preparePlotMatrix(1001, 4, len(cassetteIDs))
            
            self.ploth.figHandle.suptitle('Readouts - raw channels')
    
            for k, cc in enumerate(cassetteIDs):
                
                self.histChRaw1hybrid(cc)  
    
                self.ploth.axHandle[0][k].bar(self.xbins,self.histo0,0.8,color='r') 
                self.ploth.axHandle[1][k].bar(self.xbins,self.histo1,0.8,color='m')
                self.ploth.axHandle[2][k].bar(self.xbins,self.histo2,0.8,color='b') 
                self.ploth.axHandle[3][k].bar(self.xbins,self.histo3,0.8,color='c')
                
                self.ploth.axHandle[0][k].set_xlabel('WIRE H ASIC 0 ch no.')
                self.ploth.axHandle[1][k].set_xlabel('WIRE H ASIC 1 ch no.')
                self.ploth.axHandle[2][k].set_xlabel('GRID H ASIC 0 ch no.')
                self.ploth.axHandle[3][k].set_xlabel('GRID H ASIC 1 ch no.')
                
                self.ploth.axHandle[0][k].set_title('MG.'+str(cc)) 
            
    def extractTimeStamp1hybrid(self,cassette1ID):
        
        if self.flag is True:
        
            self.config.get_cassID2RingFenHybrid(cassette1ID)
            
            sel1 = self.readouts.Ring   == self.config.cassMap.RingID
            sel2 = self.readouts.Fen    == self.config.cassMap.FenID
            sel3 = self.readouts.hybrid == self.config.cassMap.hybridWID
            sel4 = self.readouts.hybrid == self.config.cassMap.hybridSID
            
            selW = sel1 & sel2 & sel3
            selS = sel1 & sel2 & sel4
            
            if self.config.DETparameters.operationMode == 'normal':
                asic0  = self.readouts.ASIC == 0
                asic1  = self.readouts.ASIC == 1

                self.timeStamp0 = self.readouts.timeStamp[selW & asic0]
                self.timeStamp1 = self.readouts.timeStamp[selW & asic1]
                self.timeStamp2 = self.readouts.timeStamp[selS & asic0]
                self.timeStamp3 = self.readouts.timeStamp[selS & asic1]
                
            elif self.config.DETparameters.operationMode == 'clustered':
                print(' --> other modes than normal is not supported for MG')
            
    def plotTimeStamps(self,cassetteIDs):
        
        if self.flag is True:
        
            self.plotht = preparePlotMatrix(1002, 4, len(cassetteIDs))
            
            self.plotht.figHandle.suptitle('Readouts - raw channels time stamps')
            
            for k, cc in enumerate(cassetteIDs):
                
                self.extractTimeStamp1hybrid(cc)  
                
                xx0 = np.arange(0,len(self.timeStamp0),1)
                xx1 = np.arange(0,len(self.timeStamp1),1)
                xx2 = np.arange(0,len(self.timeStamp2),1)
                xx3 = np.arange(0,len(self.timeStamp3),1)
                
                self.plotht.axHandle[0][k].scatter(xx0,self.timeStamp0,0.8,color='r',marker='+') 
                self.plotht.axHandle[1][k].scatter(xx1,self.timeStamp1,0.8,color='m',marker='+')
                self.plotht.axHandle[2][k].scatter(xx2,self.timeStamp2,0.8,color='b',marker='+') 
                self.plotht.axHandle[3][k].scatter(xx3,self.timeStamp3,0.8,color='c',marker='+')
                self.plotht.axHandle[0][k].set_xlabel('WIRE H ASIC 0 trigger no.')
                self.plotht.axHandle[1][k].set_xlabel('WIRE H ASIC 1 trigger no.')
                self.plotht.axHandle[2][k].set_xlabel('GRID H ASIC 0 trigger no.')
                self.plotht.axHandle[3][k].set_xlabel('GRID H ASIC 1 trigger no.')
                self.plotht.axHandle[0][k].set_ylabel('time (ns)')
                self.plotht.axHandle[1][k].set_ylabel('time (ns)')
                self.plotht.axHandle[2][k].set_ylabel('time (ns)')
                self.plotht.axHandle[3][k].set_ylabel('time (ns)')
                self.plotht.axHandle[0][k].set_title('MG.'+str(cc)) 
                self.plotht.axHandle[0][k].grid(axis='x', alpha=0.75)
                self.plotht.axHandle[1][k].grid(axis='x', alpha=0.75)
                self.plotht.axHandle[2][k].grid(axis='x', alpha=0.75)
                self.plotht.axHandle[3][k].grid(axis='x', alpha=0.75)
                self.plotht.axHandle[0][k].grid(axis='y', alpha=0.75)
                self.plotht.axHandle[1][k].grid(axis='y', alpha=0.75)
                self.plotht.axHandle[2][k].grid(axis='y', alpha=0.75)
                self.plotht.axHandle[3][k].grid(axis='y', alpha=0.75)
            
    
    
    def plotChoppResets(self):
        """
        Acts as a pointer/wrapper for the central library libPlotting  
        """
        return libPlotting.plottingReadouts.plotChoppResets(self)
    
        
    def plotADCvsCh(self,cassetteIDs,allAxis,logScale = False):
        
    
        self.allAxis = allAxis
        
        if self.flag is True:

            normColors = logScaleMap(logScale).normColors
            
            self.plothtch = preparePlotMatrix(1006, 4, len(cassetteIDs))
            
            self.plothtch.figHandle.suptitle('ADC vs CH')
                     
            for k, cc in enumerate(cassetteIDs):
    
                selW, selS = self.selectHybridFromCassetteID(cc)
                
                if self.config.DETparameters.operationMode == 'normal':
                    asic0  = self.readouts.ASIC == 0
                    asic1  = self.readouts.ASIC == 1
                    self.histoch0 = hh.histog(self.outOfBounds).hist2D(self.allAxis.axEnergy.axis, self.readouts.ADC[selW & asic0] , self.xbins, self.readouts.Channel[selW & asic0])
                    self.histoch1 = hh.histog(self.outOfBounds).hist2D(self.allAxis.axEnergy.axis, self.readouts.ADC[selW & asic1] , self.xbins, self.readouts.Channel[selW & asic1])
                    self.histoch2 = hh.histog(self.outOfBounds).hist2D(self.allAxis.axEnergy.axis, self.readouts.ADC[selS & asic0] , self.xbins, self.readouts.Channel[selS & asic0])
                    self.histoch3 = hh.histog(self.outOfBounds).hist2D(self.allAxis.axEnergy.axis, self.readouts.ADC[selS & asic1] , self.xbins, self.readouts.Channel[selS & asic1])
                    
                else:
                    print(' --> other modes than normal is not supported for MG')
                   
                   
                self.plothtch.axHandle[0][k].imshow(self.histoch0,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,self.xbins[0],self.xbins[-1]], origin='lower',cmap='jet')
                self.plothtch.axHandle[1][k].imshow(self.histoch1,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,self.xbins[0],self.xbins[-1]], origin='lower',cmap='jet')
                self.plothtch.axHandle[2][k].imshow(self.histoch2,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,self.xbins[0],self.xbins[-1]], origin='lower',cmap='jet')
                self.plothtch.axHandle[3][k].imshow(self.histoch3,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,self.xbins[0],self.xbins[-1]], origin='lower',cmap='jet')
            
                self.plothtch.axHandle[0][k].set_xlabel('ADC')
                self.plothtch.axHandle[1][k].set_xlabel('ADC')
                self.plothtch.axHandle[2][k].set_xlabel('ADC')
                self.plothtch.axHandle[3][k].set_xlabel('ADC')
                
                self.plothtch.axHandle[0][k].set_title('hyb.s of ID'+str(cc)) 
                
                if k == 0:
                   self.plothtch.axHandle[0][k].set_ylabel('hyb 0 ASIC 0 ch no.')
                   self.plothtch.axHandle[1][k].set_ylabel('hyb 0 ASIC 1 ch no.')
                   self.plothtch.axHandle[2][k].set_ylabel('hyb 1 ASIC 0 ch no.')
                   self.plothtch.axHandle[3][k].set_ylabel('hyb 1 ASIC 1 ch no.')
                   
                   
###############################################################################
############################################################################### 
        
class plottingHits():
    def __init__(self, hits, parameters, outOfBounds = True):
        
        self.hits = hits
        self.parameters  = parameters
        self.config      = parameters.config
        self.outOfBounds = outOfBounds 
        
        checkke = checkHitsClass(hits)
        self.flag     = checkke.flag 
        
        self.xbins = np.linspace(0,127,128)
        
    def histChRaw1Cass(self,cassette1ID):
        
        
            cass = self.hits.Cassette == cassette1ID
            
            if self.config.DETparameters.operationMode == 'normal':
                wires  = self.hits.WorS == 0
                strips = self.hits.WorS == 1
                wireCh0to31 = np.mod(self.hits.WiresStrips[cass & wires],self.config.DETparameters.numOfWires)
                self.histow = hh.histog(self.outOfBounds).hist1D(self.xbins, wireCh0to31)
                self.histos = hh.histog(self.outOfBounds).hist1D(self.xbins, self.hits.WiresStrips[cass & strips])
                
            else:
                
                print('other modes than normal is not supported for MG')
                
            # elif self.config.DETparameters.operationMode == 'clustered':
            #     wireCh0to31 = np.mod(self.hits.WiresStrips1[cass],self.config.DETparameters.numOfWires)
            #     self.histow = hh.histog().hist1D(self.xbins, wireCh0to31)
            #     self.histos = hh.histog().hist1D(self.xbins, self.hits.WiresStrips[cass])
            

    def plotChRaw(self,cassetteIDs): 
     """
     Acts as a pointer/wrapper for the central library libPlotting  
     """
     return libPlotting.plottingHits.plotChRaw(self,cassetteIDs)

     
            
    def extractTimeStamp1Cass(self,cassette1ID):
             
        sel = self.hits.Cassette == cassette1ID
        
        if self.config.DETparameters.operationMode == 'normal':
            isWire   = self.hits.WorS == 0
            isStrip  = self.hits.WorS == 1
            
            self.timeStampW = self.hits.timeStamp[sel] * isWire[sel]
            self.timeStampS = self.hits.timeStamp[sel] * isStrip[sel]
        else:
               
               print('other modes than normal is not supported for MG') 
 
            
        
    def extractTimeStampAndCh1Cass(self,cassette1ID):
           
        self.extractTimeStamp1Cass(cassette1ID) 
        
        sel = self.hits.Cassette == cassette1ID
        
        if self.config.DETparameters.operationMode == 'normal':
            isWire   = self.hits.WorS == 0
            isStrip  = self.hits.WorS == 1
            
            wireCh0to31 = np.mod(self.hits.WiresStrips,self.config.DETparameters.numOfWires) 
            
            self.WireCh  = np.round((wireCh0to31[sel]+10) * isWire[sel])
            self.StripCh = np.round((self.hits.WiresStrips[sel]+20) * isStrip[sel])
   
        elif self.config.DETparameters.operationMode == 'clustered':
            print('other modes than normal is not supported for MG') 
            
        self.WireCh[self.WireCh == 0]   = np.ma.masked # same as np.nan for int64 instead of floats   
        self.StripCh[self.StripCh == 0] = np.ma.masked # same as np.nan for int64 instead of floats
        
        self.WireCh  = self.WireCh   - 10
        self.StripCh = self.StripCh  - 20 + self.config.DETparameters.numOfWires
        
   
    def plotTimeStamps(self,cassetteIDs): 
     """
     Acts as a pointer/wrapper for the central library libPlotting  
     """
     return libPlotting.plottingHits.plotTimeStamps(self,cassetteIDs)
   
    
    def plotTimeStampsVSCh(self,cassetteIDs): 
     """
     Acts as a pointer/wrapper for the central library libPlotting  
     """
     return libPlotting.plottingHits.plotTimeStampsVSCh(self,cassetteIDs)
            
  

################################################################################################
################################################################################################


class plottingEvents():
    
    def __init__(self, events, parameters, allAxis, coincidenceWS_ONOFF, outOfBounds = True):
        
        self.parameters  = parameters
        self.config      = parameters.config
        self.allAxis     = allAxis
        self.coincidenceWS_ONOFF = coincidenceWS_ONOFF
        self.outOfBounds = outOfBounds 
  
        checkke = checkEventsClass(events)
        self.events = checkke.events
        self.flag   = checkke.flag
    
        if self.flag is True:
            if self.coincidenceWS_ONOFF is True:
                print('\t building histograms ... coincidence W/S ON for ToF and Lambda ...')
                self.selc = events.positionS >= 0 
            else:
                print('\t building histograms ... coincidence W/S OFF for ToF and Lambda ...')
                self.selc = events.positionS >= - np.inf
        
        # self.sharex='col'
        # self.sharey='row' 
            
    def plotXYToF(self, logScale = False, absUnits = False, orientation = 'vertical'):

        
        if self.flag is True:
            normColors = logScaleMap(logScale).normColors
         
            if absUnits == False:
                
                # if  len(self.events.ToF) == 0 :
                #    print('\t \033[1;33mWARNING: ToF array is empty ')
                #    self.events.ToF = np.zeros((len(self.events.positionW)),dtype='int64')
                
                h2D, _, hToF = hh.histog(self.outOfBounds).histXYZ(self.allAxis.axWires.axis, self.events.positionW[self.selc], self.allAxis.axStrips.axis, self.events.positionS[self.selc], self.allAxis.axToF.axis, self.events.ToF[self.selc]/1e9)
        
        
                # h2D[0,0]    = 8
                # h2D[10,237] = 8
                    
                hProjAll = hh.histog(self.outOfBounds).hist1D(self.allAxis.axWires.axis, self.events.positionW)
                
                hProj2D  = np.sum(h2D,axis=0)
                
                if orientation == 'vertical':
                
                    fig2D, ax22 = plt.subplots(num=101,figsize=(9,9), nrows=2, ncols=2)    
                    # #fig.add_axes([0,0,1,1]) #if you want to position absolute coordinate
                    pos1  = ax22[0][0].imshow(h2D,aspect='auto',norm=normColors,interpolation='none', extent=[self.allAxis.axWires.start-0.5,self.allAxis.axWires.stop+0.5,self.allAxis.axStrips.start-0.5,self.allAxis.axStrips.stop+0.5], origin='lower',cmap='viridis')
                    
                   
                    #  temporary fix because LogNorm crashes tihe imShow when Log 
                    try:
                        fig2D.colorbar(pos1, ax=ax22[0][0], orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
                    except:
                        print('\n --> \033[1;33mWARNING: Cannot plot XY in Log scale, changed to linear\033[1;37m',end='')
                        
                    # cbar1 =fig2D.colorbar(pos1,ax=ax1)
                    # cbar2.minorticks_on()
                    # ax1.set_aspect('tight')
                    ax22[0][0].set_xlabel('Wire ch.')
                    ax22[0][0].set_ylabel('Grid ch.')
                    fig2D.suptitle('DET image')
                    
                    # add magenta lines to plot IMG
                    for k in np.arange(0,self.config.DETparameters.numOfCassettes*self.config.DETparameters.numOfWires,self.config.DETparameters.wiresPerRow):
                        ax22[0][0].plot([k-0.5,k-0.5],[-0.5,11.5],'r',linewidth=1)
                        
                    # add red lines to plot IMG
                    for k in range(1,self.config.DETparameters.numOfCassettes):
                        ax22[0][0].plot([k*self.config.DETparameters.numOfWires-0.5, k*self.config.DETparameters.numOfWires-0.5], [-0.5, self.config.DETparameters.numOfStrips-1+0.5], color='m', linewidth = 1)
                        
                    
                    
                elif orientation == 'horizontal':  
                    
                    print('\n --> \033[1;33mWARNING: horizontal is not supported for MG for now, change in config file\033[1;37m',end='')
                   
                           
 
                    
    
                
                pos2 = ax22[1][0].step(self.allAxis.axWires.axis,hProjAll,'r',where='mid',label='1D')
                ax22[1][0].step(self.allAxis.axWires.axis,hProj2D,'b',where='mid',label='2D')
                if logScale is True:
                   ax22[1][0].set_yscale('log')
                ax22[1][0].set_xlabel('Wire ch.')
                ax22[1][0].set_ylabel('counts')
                ax22[1][0].set_xlim(self.allAxis.axWires.start,self.allAxis.axWires.stop)
                legend = ax22[1][0].legend(loc='upper right', shadow=False, fontsize='large')
                
                
                # projected over window in depth image 2D
                
                wireChforX = np.floor_divide(self.events.positionW[self.selc],self.config.DETparameters.wiresPerRow)
                
                if np.mod(self.config.DETparameters.numOfWires,self.config.DETparameters.wiresPerRow) != 0 :
                    print('Warning: num of Wires / Wires per row is not integer!')
                    time.sleep(2)
                
                rowsPerCol = int(self.config.DETparameters.numOfWires/self.config.DETparameters.wiresPerRow)
                
                steps   = self.config.DETparameters.numOfCassettes*rowsPerCol
                stop    = steps - 1

                rowsAxis = np.linspace(0,stop,steps)
                
                h2DprojWin, _, _ = hh.histog().histXYZ(rowsAxis, wireChforX, self.allAxis.axStrips.axis, self.events.positionS[self.selc], self.allAxis.axToF.axis, self.events.ToF[self.selc]/1e9)

                
                pos10  = ax22[0][1].imshow(h2DprojWin,aspect='auto',norm=normColors,interpolation='none',extent=[-0.5,stop+0.5,self.allAxis.axStrips.start-0.5,self.allAxis.axStrips.stop+0.5], origin='lower',cmap='viridis')
                
                
                try:
                    fig2D.colorbar(pos10, ax=ax22[0][1], orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
                except:
                    print('\n --> \033[1;33mWARNING: Cannot plot XY in Log scale, changed to linear\033[1;37m',end='')
    
                ax22[0][1].set_xlabel('Row no.')
                ax22[0][1].set_ylabel('Grid ch.')
                
                
                for k in range(1,self.config.DETparameters.numOfCassettes):
                    ax22[0][1].plot([k*rowsPerCol-0.5, k*rowsPerCol-0.5], [-0.5, self.config.DETparameters.numOfStrips-1+0.5], color='m', linewidth = 1)
                    
                    
                    
                hProjAll2 = hh.histog().hist1D(rowsAxis, wireChforX)
                    
                hProj2D2  = np.sum(h2DprojWin,axis=0)
                
                
                pos2 = ax22[1][1].step(rowsAxis,hProjAll2,'r',where='mid',label='1D')
                ax22[1][1].step(rowsAxis,hProj2D2,'b',where='mid',label='2D')
                if logScale is True:
                   ax22[1][1].set_yscale('log')
                ax22[1][1].set_xlabel('Row no.')
                ax22[1][1].set_ylabel('counts')
                ax22[1][1].set_xlim(0,stop)
                legend = ax22[1][1].legend(loc='upper right', shadow=False, fontsize='large')
    
                ########
                # 2D image of detector ToF vs Wires 
                # ToFxgms = ToFxg*1e3 # in ms 
            
                fig2, ax2 = plt.subplots(num=102,figsize=(6,6), nrows=1, ncols=1) 
                pos2  = ax2.imshow(hToF,aspect='auto',norm=normColors,interpolation='nearest',extent=[self.allAxis.axToF.start*1e3,self.allAxis.axToF.stop*1e3,self.allAxis.axWires.start,self.allAxis.axWires.stop], origin='lower',cmap='viridis')
                
                #  temporary fix because LogNorm crashes tihe imShow when Log 
                try:
                    fig2.colorbar(pos2, ax=ax2)
                except:
                    print('\n --> \033[1;33mWARNING: Cannot plot YToF in Log scale, changed to linear\033[1;37m',end='')
                
                ax2.set_ylabel('Wire ch.')
                ax2.set_xlabel('ToF (ms)')
                fig2.suptitle('DET ToF')
            
            elif absUnits == True:
                
                print('\n --> \033[1;33mWARNING: absUnits is not supported for MG for now, change to False to get det image\033[1;37m',end='')
               
          
                # if  len(self.events.ToF) == 0 :
                #     print('\t \033[1;33mWARNING: ToF arrasy is empty ')
                #     self.events.ToF = np.zeros(len(self.events.positionWmm),dtype='int64')
                
                
                # h2D, hProj, hToF = hh.histog(self.outOfBounds).histXYZ(self.allAxis.axWires_mm.axis, self.events.positionWmm[self.selc], self.allAxis.axStrips_mm.axis, self.events.positionSmm[self.selc], self.allAxis.axToF.axis, self.events.ToF[self.selc]/1e9)    
        
                # hProjAll = hh.histog(self.outOfBounds).hist1D(self.allAxis.axWires_mm.axis, self.events.positionWmm)
                
                # hProj2D  = np.sum(h2D,axis=0)
                
                # if orientation == 'vertical':
                
                #     fig2D, (ax1, ax2) = plt.subplots(num=101,figsize=(6,12), nrows=2, ncols=1)    
                #     # #fig.add_axes([0,0,1,1]) #if you want to position absolute coordinate
                #     pos1  = ax1.imshow(h2D,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axWires_mm.start,self.allAxis.axWires_mm.stop,self.allAxis.axStrips_mm.stop,self.allAxis.axStrips_mm.start], origin='upper',cmap='viridis')
                    
                #     #  temporary fix because LogNorm crashes tihe imShow when Log 
                #     try:
                #         fig2D.colorbar(pos1, ax=ax1, orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
                #     except:
                #         print('\n --> \033[1;33mWARNING: Cannot plot XY in Log scale, changed to linear\033[1;37m',end='')
                        
                    
                #     # cbar1 =fig2D.colorbar(pos1,ax=ax1)
                #     # cbar2.minorticks_on()
                #     # ax1.set_aspect('tight')
                #     ax1.set_xlabel('Wire coord. (mm)')
                #     ax1.set_ylabel('Grid (mm)')
                #     fig2D.suptitle('DET image')
     
                   
                # elif orientation == 'horizontal':  
                #     print(' --> horizontal is not supported for MG for now')
      
        
        
                # pos2 = ax2.step(self.allAxis.axWires_mm.axis,hProjAll,'r',where='mid',label='1D')
                # ax2.step(self.allAxis.axWires_mm.axis,hProj2D,'b',where='mid',label='2D')
                # if logScale is True:
                #    ax2.set_yscale('log')
                # ax2.set_xlabel('Wire coord. (mm)')
                # ax2.set_ylabel('counts')
                # ax2.set_xlim(self.allAxis.axWires_mm.start,self.allAxis.axWires_mm.stop)
                # legend = ax2.legend(loc='upper right', shadow=False, fontsize='large')
            
            
                # fig2, ax2 = plt.subplots(num=102,figsize=(6,6), nrows=1, ncols=1) 
                # pos2  = ax2.imshow(hToF,aspect='auto',norm=normColors,interpolation='nearest',extent=[self.allAxis.axToF.start*1e3,self.allAxis.axToF.stop*1e3,self.allAxis.axWires_mm.start,self.allAxis.axWires_mm.stop], origin='lower',cmap='viridis')
                
                # #  temporary fix because LogNorm crashes tihe imShow when Log 
                # try:
                #      fig2.colorbar(pos2, ax=ax2)
                # except:
                #      print('\n --> \033[1;33mWARNING: Cannot plot XY in Log scale, changed to linear\033[1;37m',end='')
                
                
                # ax2.set_ylabel('Wire coord. (mm)')
                # ax2.set_xlabel('ToF (ms)')
                # fig2.suptitle('DET ToF')
                
            # return h2D
        
            
    def plotXLambda(self,logScale=False, absUnits = False): 
         """
         Acts as a pointer/wrapper for the central library libPlotting  
         """
         return libPlotting.plottingEvents.plotXLambda(self,logScale, absUnits)

    

    def plotMultiplicity(self, cassettes):
        
        if self.flag is True:
        
            self.width      = 0.2
            self.extentplot = 7

            ########

            self.plotMult = preparePlotMatrix(401, 2, len(cassettes))
            
            self.plotMult.figHandle.suptitle('Events - multiplicity')
            
            xx =  self.allAxis.axMult.axis

            for k, cass in enumerate(cassettes):
   
                selc  = self.events.Cassette  == cass
                sel2D = self.events.positionS >= 0

                myw  = hh.histog(self.outOfBounds).hist1D(xx,self.events.multW[selc]) # wires all
                mys  = hh.histog(self.outOfBounds).hist1D(xx,self.events.multS[selc]) # strips all
                mywc = hh.histog(self.outOfBounds).hist1D(xx,self.events.multW[selc & sel2D]) # wires coinc
           
                my2Dwc = hh.histog().hist2D(xx,self.events.multW[selc & sel2D],xx,self.events.multS[selc & sel2D]) # wires coinc with strips 2D
                
                if np.any(selc):
                    mywnorm    = myw/np.sum(myw[1:])
                    mysnorm    = mys/np.sum(mys[1:])
                    mysnormall = mys/np.sum(mys)
                    mywcnorm   = mywc/np.sum(mywc[1:])
                    my2Dwcnorm = my2Dwc/np.sum(my2Dwc)
                else:
                    mywnorm    = np.zeros((len(xx)))
                    mysnorm    = np.zeros((len(xx)))
                    mysnormall = np.zeros((len(xx)))
                    mywcnorm   = np.zeros((len(xx)))
                    my2Dwcnorm = np.zeros((len(xx),len(xx)))

             ########
       
                self.plotMult.axHandle[0][k].bar(xx[:self.extentplot]-self.width,mywnorm[:self.extentplot],self.width,color='m',label='w') 
                self.plotMult.axHandle[0][k].bar(xx[1:self.extentplot]+self.width,mysnorm[1:self.extentplot],self.width,color='b',label='s')
                self.plotMult.axHandle[0][k].bar(xx[0]+self.width,mysnormall[0],self.width,color='c',label='no s')
                self.plotMult.axHandle[0][k].bar(xx[:self.extentplot],mywcnorm[:self.extentplot],self.width,color='r',label='w/s')
                self.plotMult.axHandle[0][k].set_xlabel('multiplicity')
                self.plotMult.axHandle[0][k].set_title('ID '+str(cass))
                legend = self.plotMult.axHandle[0][k].legend(loc='upper right', shadow=False, fontsize='large')
                if k == 0:
                    self.plotMult.axHandle[0][k].set_ylabel('probability')
                
                
                pos1 = self.plotMult.axHandle[1][k].imshow(my2Dwcnorm[:self.extentplot,:self.extentplot],aspect='auto',norm=None,interpolation='none',extent=[xx[0]-0.5,xx[self.extentplot]-0.5,xx[0]-0.5,xx[self.extentplot]-0.5], origin='lower',cmap='jet')
                self.plotMult.axHandle[1][k].set_xlabel('multiplicity wires')
                if k == 0:
                    self.plotMult.axHandle[1][k].set_ylabel('multiplicity grids')
                    
                plt.colorbar(pos1,ax=self.plotMult.axHandle[1][k])
       

    def plotPHS(self, cassetteIDs, logScale = False):
        
        if self.flag is True:
        
            normColors = logScaleMap(logScale).normColors
            
            self.plotPHS = preparePlotMatrix(601, 4, len(cassetteIDs))
            
            self.plotPHS.figHandle.suptitle('Pulse Heigth Spectra')
            
            wireCh0to31Round = np.round(np.mod(self.events.positionW,self.config.DETparameters.numOfWires))
                    
            stripChRound     = np.round(self.events.positionS)
            
            wireAx  = np.linspace(0,self.config.DETparameters.numOfWires-1, self.config.DETparameters.numOfWires)
            
            stripAx = np.linspace(0,self.config.DETparameters.numOfStrips-1, self.config.DETparameters.numOfStrips)
            
            for k, cass in enumerate(cassetteIDs):
       
                    selc  = self.events.Cassette  == cass
                    sel2D = self.events.positionS >= 0
                    
                    PHSw  = hh.histog(self.outOfBounds).hist2D(self.allAxis.axEnergy.axis,self.events.PHW[selc],wireAx,wireCh0to31Round[selc]) # wires 
                    PHSs  = hh.histog(self.outOfBounds).hist2D(self.allAxis.axEnergy.axis,self.events.PHS[selc & sel2D],stripAx,stripChRound[selc & sel2D]) # strips
                    PHSwc = hh.histog(self.outOfBounds).hist2D(self.allAxis.axEnergy.axis,self.events.PHW[selc & sel2D],wireAx,wireCh0to31Round[selc & sel2D]) # wires coinc with strips 2D
                    
                    self.plotPHS.axHandle[0][k].imshow(PHSw,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,wireAx[0],wireAx[-1]], origin='lower',cmap='jet')
                    self.plotPHS.axHandle[1][k].imshow(PHSs,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,stripAx[0],stripAx[-1]], origin='lower',cmap='jet')
                    self.plotPHS.axHandle[2][k].imshow(PHSwc,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,wireAx[0],wireAx[-1]], origin='lower',cmap='jet')
                    
                    self.plotPHS.axHandle[0][k].set_title('ID '+str(cass))
                    if k == 0:
                        self.plotPHS.axHandle[0][k].set_ylabel('wires ch. no.')
                        self.plotPHS.axHandle[1][k].set_ylabel('grid ch. no.')
                        self.plotPHS.axHandle[2][k].set_ylabel('wires coinc. ch. no.')
               
                       #global PHS
                    PHSGw  = np.sum(PHSw,axis=0)
                    PHSGs  = np.sum(PHSs,axis=0)
                    PHSGwc = np.sum(PHSwc,axis=0)
           
                    # global PHS plot
                    self.plotPHS.axHandle[3][k].step(self.allAxis.axEnergy.axis,PHSGw,'r',where='mid',label='w')
                    self.plotPHS.axHandle[3][k].step(self.allAxis.axEnergy.axis,PHSGs,'b',where='mid',label='g')
                    self.plotPHS.axHandle[3][k].step(self.allAxis.axEnergy.axis,PHSGwc,'k',where='mid',label='w/g')
                    self.plotPHS.axHandle[3][k].set_xlabel('pulse height (a.u.)')
                    self.plotPHS.axHandle[3][k].legend(loc='upper right', shadow=False, fontsize='large')
                    if k == 0:
                       self.plotPHS.axHandle[3][k].set_ylabel('counts')
                   
    def plotPHScorrelation(self, cassetteIDs, logScale = False):
        
        if self.flag is True:
              
           normColors = logScaleMap(logScale).normColors
        
           self.plotPHScorr = preparePlotMatrix(602, 1, len(cassetteIDs), figSize=(12,6))
           
           self.plotPHScorr.figHandle.suptitle('Pulse Heigth Spectrum - Correlation W/G')
        
           for k, cass in enumerate(cassetteIDs):
   
                selc  = self.events.Cassette  == cass
                sel2D = self.events.positionS >= 0
                
                PHScorr  = hh.histog(self.outOfBounds).hist2D(self.allAxis.axEnergy.axis,self.events.PHW[selc & sel2D],self.allAxis.axEnergy.axis,self.events.PHS[selc & sel2D]) 
               
                self.plotPHScorr.axHandle[0][k].imshow(PHScorr,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop], origin='lower',cmap='jet')
                
                self.plotPHScorr.axHandle[0][k].set_title('ID '+str(cass))
                self.plotPHScorr.axHandle[0][k].set_xlabel('pulse height wires (a.u.)')
                if k == 0:
                    self.plotPHScorr.axHandle[0][k].set_ylabel('pulse height grids (a.u.)')
    
            
    def plotInstantaneousRate(self,cassetteIDs): 
         """
         Acts as a pointer/wrapper for the central library libPlotting  
         """
         return libPlotting.plottingEvents.plotInstantaneousRate(self,cassetteIDs)
    
                   
    def plotToF(self, cassetteIDs):
        
        if self.flag is True:
           
          self.plotTT = preparePlotMatrix(333, 1, len(cassetteIDs))
          
          self.plotTT.figHandle.suptitle('ToF distr per column')
          
          for k, cass in enumerate(cassetteIDs):
               
               selc  = self.events.Cassette  == cass
               sel2D = self.events.positionS >= 0
               
               histTT  = hh.histog(self.outOfBounds).hist1D(self.allAxis.axToF.axis,self.events.ToF[selc & sel2D]/1e9) 
               
               histTT1 = hh.histog(self.outOfBounds).hist1D(self.allAxis.axToF.axis,self.events.ToF[selc]/1e9)
               
               self.plotTT.axHandle[0][k].step(self.allAxis.axToF.axis*1e3,histTT1,'r',where='mid',label='all')
               self.plotTT.axHandle[0][k].step(self.allAxis.axToF.axis*1e3,histTT,'b',where='mid',label='2D')
               self.plotTT.axHandle[0][k].set_xlabel('ToF (ms)')
               self.plotTT.axHandle[0][k].set_title('ID '+str(cass))
               if k == 0:
                   self.plotTT.axHandle[0][k].set_ylabel('counts')
                   
              
               legend = self.plotTT.axHandle[0][k].legend(loc='upper right', shadow=False, fontsize='large')
               
    def plotLambda(self, cassetteIDs):
        
        if self.flag is True:
           
          self.plotWA = preparePlotMatrix(339, 1, len(cassetteIDs))
          
          self.plotWA.figHandle.suptitle('Wavelength distr per column')
          
          for k, cass in enumerate(cassetteIDs):
               
               selc  = self.events.Cassette  == cass
               sel2D = self.events.positionS >= 0
               
               histWA  = hh.histog(self.outOfBounds).hist1D(self.allAxis.axLambda.axis,self.events.wavelength[selc & sel2D]) 
               
               histWA1 = hh.histog(self.outOfBounds).hist1D(self.allAxis.axLambda.axis,self.events.wavelength[selc])
               
               self.plotWA.axHandle[0][k].step(self.allAxis.axLambda.axis,histWA1,'r',where='mid',label='all')
               self.plotWA.axHandle[0][k].step(self.allAxis.axLambda.axis,histWA,'b',where='mid',label='2D')
               self.plotWA.axHandle[0][k].set_xlabel('wavelength (A)')
               self.plotWA.axHandle[0][k].set_title('ID '+str(cass))
               if k == 0:
                   self.plotWA.axHandle[0][k].set_ylabel('counts')
                   
              
               legend = self.plotWA.axHandle[0][k].legend(loc='upper right', shadow=False, fontsize='large')
  

            
###############################################################################
###############################################################################

if __name__ == '__main__' :
    
    plt.close("all")
    
    parameters  = para.parameters('./')
    
    filePath  = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap_MGdevel/config/'+"MG.json"

    config = maps.read_json_config(filePath)
    
    parameters.loadConfigAndSetParameters(config)
    
    filePath = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap_MGdevel/data/'
    file = 'MG_2col_2clusters.pcapng'
    
    
    filePathAndFileName = filePath+file
    
    NSperClockTick = 11.356860963629653  #ns per tick ESS for 88.0525 MHz
    
    pcapng = pcapr.pcapng_reader(filePathAndFileName, NSperClockTick, config.MONmap.TTLtype, config.MONmap.RingID,  timeResolutionType='fine', sortByTimeStampsONOFF = False, operationMode=config.DETparameters.operationMode)

    readouts = pcapng.readouts
    readoutsArray = readouts.concatenateReadoutsInArrayForDebug()
 
    plread = plottingReadouts(readouts, config)
    plread.plotChRaw(parameters.config.DETparameters.cassInConfig)
    
    # allAxis = hh.allAxis()
    # allAxis.createAllAxis(parameters)
    

        
    ##################


    
    
    
    