#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 10:46:16 2021

@author: francescopiscitelli
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


from lib import libReadPcapngVMM as pcapr
from lib import libSampleData as sdat
from lib import libMapping as maps
from lib import libCluster as clu
from lib import libAbsUnitsAndLambda as absu
from lib import libHistograms as hh
from lib import libParameters as para

###############################################################################
###############################################################################

class preparePlotMatrix():
    def __init__(self, figNum, Nrows,  Ncols=1, figSize=(12,12)):
        
        self.Ncols = Ncols
        self.Nrows = Nrows
        
        self.figSize = figSize
        
        self.sharex='col'
        self.sharey='row' 
        
        self.figHandle, self.axHandle = plt.subplots(num=figNum, figsize=self.figSize, nrows=self.Nrows, ncols=self.Ncols, sharex=self.sharex, sharey=self.sharey)
        self.axHandle.shape      = (self.Nrows,self.Ncols)
        self.axHandle            = np.atleast_2d(self.axHandle)
  
################################
        
class plottingReadouts():
   
    def __init__(self, readouts, config):
    
        self.readouts = readouts
        
        self.config   = config
        
        # self.parameters = parameters
        
        self.xbins = np.linspace(0,63,64)
        
    def histChRaw1hybrid(self,cassette1ID):
        
        self.config.get_cassID2RingFenHybrid(cassette1ID)

        # cassette correpsonds to a particluar triplet of ring fen and hybrid so Icanuse cassette to loop over hybrids
        
        # print(self.config.cassMap.RingID)
        # print(self.config.cassMap.FenID)
        # print(self.config.cassMap.hybridID)
        
        sel1 = self.readouts.Ring   == self.config.cassMap.RingID
        sel2 = self.readouts.Fen    == self.config.cassMap.FenID
        sel3 = self.readouts.hybrid == self.config.cassMap.hybridID
        
        sel = sel1 & sel2 & sel3
        
        asic0  = self.readouts.ASIC == 0
        asic1  = self.readouts.ASIC == 1
        
        # wireCh0to31 = np.mod(self.hits.WiresStrips[cass & wires],self.parameters.configJsonFile.numOfWires)
        
        self.histo0 = hh.histog().hist1D(self.xbins, self.readouts.Channel[sel & asic0])
        self.histo1 = hh.histog().hist1D(self.xbins, self.readouts.Channel[sel & asic1])
        
    def plotChRaw(self,hybrids): 
        
        self.ploth = preparePlotMatrix(1001, 2, len(hybrids))
        
        self.ploth.figHandle.suptitle('Readouts - raw channels')

        for k, cc in enumerate(hybrids):
            
            self.histChRaw1hybrid(cc)  

            self.ploth.axHandle[0][k].bar(self.xbins,self.histo0,0.8,color='r') 
            self.ploth.axHandle[1][k].bar(self.xbins,self.histo1,0.8,color='b')
            self.ploth.axHandle[0][k].set_xlabel('ASIC 0 ch no.')
            self.ploth.axHandle[1][k].set_xlabel('ASIC 1 ch no.')
            self.ploth.axHandle[0][k].set_title('hybrid '+str(cc)) 
            
    def extractTimeStamp1hybrid(self,cassette1ID):
        
        self.config.get_cassID2RingFenHybrid(cassette1ID)
        
        sel1 = self.readouts.Ring   == self.config.cassMap.RingID
        sel2 = self.readouts.Fen    == self.config.cassMap.FenID
        sel3 = self.readouts.hybrid == self.config.cassMap.hybridID
        
        sel = sel1 & sel2 & sel3
        
        asic0  = self.readouts.ASIC == 0
        asic1  = self.readouts.ASIC == 1
        
        # wireCh0to31 = np.mod(self.hits.WiresStrips[cass & wires],self.parameters.configJsonFile.numOfWires)
        
        self.timeStamp0 = self.readouts.timeStamp[sel & asic0]
        self.timeStamp1 = self.readouts.timeStamp[sel & asic1]
            
    def plotTimeStamps(self,hybrids):
        
        self.plotht = preparePlotMatrix(1002, 2, len(hybrids))
        
        self.plotht.figHandle.suptitle('Readouts - raw channels time stamps')
        
        for k, cc in enumerate(hybrids):
            
            self.extractTimeStamp1hybrid(cc)  
            
            xx0 = np.arange(0,len(self.timeStamp0),1)
            xx1 = np.arange(0,len(self.timeStamp1),1)
            
            self.plotht.axHandle[0][k].scatter(xx0,self.timeStamp0,0.8,color='r',marker='+') 
            self.plotht.axHandle[1][k].scatter(xx1,self.timeStamp1,0.8,color='b',marker='+')
            self.plotht.axHandle[0][k].set_xlabel('ASIC 0 trigger no.')
            self.plotht.axHandle[1][k].set_xlabel('ASIC 1 trigger no.')
            self.plotht.axHandle[0][k].set_ylabel('time (s)')
            self.plotht.axHandle[1][k].set_ylabel('time (s)')
            self.plotht.axHandle[0][k].set_title('hybrid '+str(cc)) 
            self.plotht.axHandle[0][k].grid(axis='x', alpha=0.75)
            self.plotht.axHandle[1][k].grid(axis='x', alpha=0.75)
            self.plotht.axHandle[0][k].grid(axis='y', alpha=0.75)
            self.plotht.axHandle[1][k].grid(axis='y', alpha=0.75)
            
        
################################
        
class plottingHits():
   
    def __init__(self, hits, parameters):
        
        self.hits = hits
        
        self.parameters = parameters
        
        self.xbins = np.linspace(0,63,64)
        
    def histChRaw1Cass(self,cassette1ID):
        
        cass = self.hits.Cassette == cassette1ID
        
        wires  = self.hits.WorS == 0
        strips = self.hits.WorS == 1
        
        wireCh0to31 = np.mod(self.hits.WiresStrips[cass & wires],self.parameters.configJsonFile.numOfWires)
        
        self.histow = hh.histog().hist1D(self.xbins, wireCh0to31)
        self.histos = hh.histog().hist1D(self.xbins, self.hits.WiresStrips[cass & strips])
        
        
    def plotChRaw(self,cassettes): 
        
        self.ploth = preparePlotMatrix(1003, 2, len(cassettes))
        
        self.ploth.figHandle.suptitle('Hits - raw channels')

        for k, cc in enumerate(cassettes):
            
            self.histChRaw1Cass(cc)  

            self.ploth.axHandle[0][k].bar(self.xbins,self.histow,0.8,color='r') 
            self.ploth.axHandle[1][k].bar(self.xbins,self.histos,0.8,color='b')
            self.ploth.axHandle[0][k].set_xlabel('hit wire ch no.')
            self.ploth.axHandle[1][k].set_xlabel('hit strip ch no.')
            self.ploth.axHandle[0][k].set_title('cass ID '+str(cc))                       
        
            # self.ploth.axHandle[0][k]
            
    def extractTimeStamp1Cass(self,cassette1ID):
             
        sel = self.hits.Cassette == cassette1ID
        
        isWire   = self.hits.WorS == 0
        isStrip  = self.hits.WorS == 1
        
        # wireCh0to31 = np.mod(self.hits.WiresStrips[sel & isWire],self.parameters.configJsonFile.numOfWires)
        
        self.timeStampW = self.hits.timeStamp[sel] * isWire[sel]
        self.timeStampS = self.hits.timeStamp[sel] * isStrip[sel]
        
        self.timeStampW[self.timeStampW == 0] = None   
        self.timeStampS[self.timeStampS == 0] = None
        
    def extractTimeStampAndCh1Cass(self,cassette1ID):
           
        self.extractTimeStamp1Cass(cassette1ID) 
        
        sel = self.hits.Cassette == cassette1ID
        
        isWire   = self.hits.WorS == 0
        isStrip  = self.hits.WorS == 1
        
        wireCh0to31 = np.mod(self.hits.WiresStrips,self.parameters.configJsonFile.numOfWires) 
        
        self.WireCh  = np.round((wireCh0to31[sel]+10) * isWire[sel])
        self.StripCh = np.round((self.hits.WiresStrips[sel]+20) * isStrip[sel])
        
        self.WireCh[self.WireCh == 0]   = None   
        self.StripCh[self.StripCh == 0] = None
        
        self.WireCh  = self.WireCh   - 10
        self.StripCh = self.StripCh  - 20 + self.parameters.configJsonFile.numOfWires
            
    def plotTimeStamps(self,cassettes):
        
        self.plotht = preparePlotMatrix(1004, 1, len(cassettes))
        
        self.plotht.figHandle.suptitle('Hits - w and S time stamps')
        
        for k, cc in enumerate(cassettes):
            
            self.extractTimeStamp1Cass(cc)  
            
            xx0 = np.arange(0,len(self.timeStampW),1)
            xx1 = np.arange(0,len(self.timeStampS),1)
            
            self.plotht.axHandle[0][k].scatter(xx0,self.timeStampW,0.8,color='r',marker='+') 
            self.plotht.axHandle[0][k].scatter(xx1,self.timeStampS,0.8,color='b',marker='+')
            self.plotht.axHandle[0][k].set_xlabel('trigger no.')   
            self.plotht.axHandle[0][k].set_ylabel('time (s)')
            self.plotht.axHandle[0][k].set_title('cass ID '+str(cc)) 
            self.plotht.axHandle[0][k].grid(axis='x', alpha=0.75)
            self.plotht.axHandle[0][k].grid(axis='y', alpha=0.75)
            
    def plotTimeStampsVSCh(self,cassettes):
        
        self.plothtvs = preparePlotMatrix(1005, 1, len(cassettes))
        
        self.plothtvs.figHandle.suptitle('Hits - w and S VS time stamps')
        
        for k, cc in enumerate(cassettes):
            
            self.extractTimeStampAndCh1Cass(cc)  
            
            self.plothtvs.axHandle[0][k].scatter(self.WireCh,self.timeStampW,0.8,color='r',marker='+') 
            self.plothtvs.axHandle[0][k].scatter(self.StripCh,self.timeStampS,0.8,color='b',marker='+')
            self.plothtvs.axHandle[0][k].set_xlabel('trigger no.')   
            self.plothtvs.axHandle[0][k].set_ylabel('time (s)')
            self.plothtvs.axHandle[0][k].set_title('cass ID '+str(cc)) 
            self.plothtvs.axHandle[0][k].grid(axis='x', alpha=0.75)
            self.plothtvs.axHandle[0][k].grid(axis='y', alpha=0.75)
        

################################

class logScaleMap():
    def __init__(self,logScale):
        
        if logScale is True:
            self.normColors = LogNorm()
        elif logScale is False:
            self.normColors = None
            
        
        
class plottingEvents():
    
    def __init__(self, events, allAxis, coincidenceWS_ONOFF):
        
        # self.Ncass = Ncass
        
        self.events  = events
        self.allAxis = allAxis
        
        # self.selectCoinc = events.positionS >= -2
        
        self.coincidenceWS_ONOFF = coincidenceWS_ONOFF
    
        if self.coincidenceWS_ONOFF is True:
            print('\t building histograms ... coincidence W/S ON for ToF and Lambda ...')
            self.selc = events.positionS >= 0 
        else:
            print('\t building histograms ... coincidence W/S OFF for ToF and Lambda ...')
            self.selc = events.positionS >= - np.inf
        
        # self.sharex='col'
        # self.sharey='row' 
            
    def plotXYToF(self, logScale = False, absUnits = False, orientation = 'vertical'):
        
        normColors = logScaleMap(logScale).normColors
     
        if absUnits == False:
 
            h2D, _, hToF = hh.histog().histXYZ(self.allAxis.axWires.axis, self.events.positionW[self.selc], self.allAxis.axStrips.axis, self.events.positionS[self.selc], self.allAxis.axToF.axis, self.events.ToF[self.selc])
    
            hProjAll = hh.histog().hist1D(self.allAxis.axWires.axis, self.events.positionW)
            
            hProj2D  = np.sum(h2D,axis=0)
            
            if orientation == 'vertical':
            
                fig2D, (ax1, ax2) = plt.subplots(num=101,figsize=(6,12), nrows=2, ncols=1)    
                # #fig.add_axes([0,0,1,1]) #if you want to position absolute coordinate
                pos1  = ax1.imshow(h2D,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axWires.start,self.allAxis.axWires.stop,self.allAxis.axStrips.stop,self.allAxis.axStrips.start], origin='upper',cmap='viridis')
                fig2D.colorbar(pos1, ax=ax1, orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
                # cbar1 =fig2D.colorbar(pos1,ax=ax1)
                # cbar2.minorticks_on()
                # ax1.set_aspect('tight')
                ax1.set_xlabel('Wire ch.')
                ax1.set_ylabel('Strip ch.')
                fig2D.suptitle('DET image')
                
                
            elif orientation == 'horizontal':     
    
                fig2D, (ax1, ax2) = plt.subplots(num=101,figsize=(12,6), nrows=1, ncols=2)    
                pos1  = ax1.imshow(np.rot90(h2D,1),aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axStrips.start,self.allAxis.axStrips.stop,self.allAxis.axWires.start,self.allAxis.axWires.stop], origin='upper',cmap='viridis')
                fig2D.colorbar(pos1, ax=ax1, orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
                ax1.set_ylabel('Wire ch.')
                ax1.set_xlabel('Strip ch.')
                fig2D.suptitle('DET image')
                

            
            pos2 = ax2.step(self.allAxis.axWires.axis,hProjAll,'r',where='mid',label='1D')
            ax2.step(self.allAxis.axWires.axis,hProj2D,'b',where='mid',label='2D')
            if logScale is True:
               ax2.set_yscale('log')
            ax2.set_xlabel('Wire ch.')
            ax2.set_ylabel('counts')
            ax2.set_xlim(self.allAxis.axWires.start,self.allAxis.axWires.stop)
            legend = ax2.legend(loc='upper right', shadow=False, fontsize='large')

            ########
            # 2D image of detector ToF vs Wires 
            # ToFxgms = ToFxg*1e3 # in ms 
        
            fig2, ax2 = plt.subplots(num=102,figsize=(6,6), nrows=1, ncols=1) 
            pos2  = ax2.imshow(hToF,aspect='auto',norm=normColors,interpolation='nearest',extent=[self.allAxis.axToF.start,self.allAxis.axToF.stop,self.allAxis.axWires.start,self.allAxis.axWires.stop], origin='lower',cmap='viridis')
            fig2.colorbar(pos2, ax=ax2)
            ax2.set_ylabel('Wire ch.')
            ax2.set_xlabel('ToF (s)')
            fig2.suptitle('DET ToF')
        
        elif absUnits == True:
            
            h2D, hProj, hToF = hh.histog().histXYZ(self.allAxis.axWires_mm.axis, self.events.positionWmm[self.selc], self.allAxis.axStrips_mm.axis, self.events.positionSmm[self.selc], self.allAxis.axToF.axis, self.events.ToF[self.selc])
    
            hProjAll = hh.histog().hist1D(self.allAxis.axWires_mm.axis, self.events.positionWmm)
            
            hProj2D  = np.sum(h2D,axis=0)
            
            if orientation == 'vertical':
            
                fig2D, (ax1, ax2) = plt.subplots(num=101,figsize=(6,12), nrows=2, ncols=1)    
                # #fig.add_axes([0,0,1,1]) #if you want to position absolute coordinate
                pos1  = ax1.imshow(h2D,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axWires_mm.start,self.allAxis.axWires_mm.stop,self.allAxis.axStrips_mm.stop,self.allAxis.axStrips_mm.start], origin='upper',cmap='viridis')
                fig2D.colorbar(pos1, ax=ax1, orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
                # cbar1 =fig2D.colorbar(pos1,ax=ax1)
                # cbar2.minorticks_on()
                # ax1.set_aspect('tight')
                ax1.set_xlabel('Wire coord. (mm)')
                ax1.set_ylabel('Strip (mm)')
                fig2D.suptitle('DET image')
 
               
            elif orientation == 'horizontal':  
                
                fig2D, (ax1, ax2) = plt.subplots(num=101,figsize=(6,12), nrows=2, ncols=1)    
                # #fig.add_axes([0,0,1,1]) #if you want to position absolute coordinate
                pos1  = ax1.imshow(np.rot90(h2D,1),aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axStrips_mm.start,self.allAxis.axStrips_mm.stop,self.allAxis.axWires_mm.start,self.allAxis.axWires_mm.stop], origin='upper',cmap='viridis')
                fig2D.colorbar(pos1, ax=ax1, orientation="horizontal",fraction=0.07,anchor=(1.0,0.0))
                ax1.set_ylabel('Wire coord. (mm)')
                ax1.set_xlabel('Strip (mm)')
                fig2D.suptitle('DET image')
    
    
            pos2 = ax2.step(self.allAxis.axWires_mm.axis,hProjAll,'r',where='mid',label='1D')
            ax2.step(self.allAxis.axWires_mm.axis,hProj2D,'b',where='mid',label='2D')
            if logScale is True:
               ax2.set_yscale('log')
            ax2.set_xlabel('Wire coord. (mm)')
            ax2.set_ylabel('counts')
            ax2.set_xlim(self.allAxis.axWires_mm.start,self.allAxis.axWires_mm.stop)
            legend = ax2.legend(loc='upper right', shadow=False, fontsize='large')
        
        
            fig2, ax2 = plt.subplots(num=102,figsize=(6,6), nrows=1, ncols=1) 
            pos2  = ax2.imshow(hToF,aspect='auto',norm=normColors,interpolation='nearest',extent=[self.allAxis.axToF.start,self.allAxis.axToF.stop,self.allAxis.axWires_mm.start,self.allAxis.axWires_mm.stop], origin='lower',cmap='viridis')
            fig2.colorbar(pos2, ax=ax2)
            ax2.set_ylabel('Wire coord. (mm)')
            ax2.set_xlabel('ToF (s)')
            fig2.suptitle('DET ToF')
            
        # return h2D
            

    def plotXLambda(self, logScale=False, absUnits = False):
        
        normColors = logScaleMap(logScale).normColors
        
        if absUnits is False:
            h = hh.histog().hist2D(self.allAxis.axLambda.axis, self.events.wavelength[self.selc], self.allAxis.axWires.axis , self.events.positionW[self.selc])
            
            figl, axl = plt.subplots(num=103,figsize=(6,6), nrows=1, ncols=1) 
            posl1  = axl.imshow(h,aspect='auto',norm=normColors,interpolation='nearest',extent=[self.allAxis.axLambda.start,self.allAxis.axLambda.stop,self.allAxis.axWires.start,self.allAxis.axWires.stop], origin='lower',cmap='viridis')
            figl.colorbar(posl1, ax=axl)
            axl.set_ylabel('Wire ch.')
            axl.set_xlabel('wavelength (A)')
            figl.suptitle('DET wavelength')
            
        elif absUnits == True:
            
            h = hh.histog().hist2D(self.allAxis.axLambda.axis, self.events.wavelength[self.selc], self.allAxis.axWires_mm.axis , self.events.positionWmm[self.selc])
            
            figl, axl = plt.subplots(num=103,figsize=(6,6), nrows=1, ncols=1) 
            posl1  = axl.imshow(h,aspect='auto',norm=normColors,interpolation='nearest',extent=[self.allAxis.axLambda.start,self.allAxis.axLambda.stop,self.allAxis.axWires_mm.start,self.allAxis.axWires_mm.stop], origin='lower',cmap='viridis')
            figl.colorbar(posl1, ax=axl)
            axl.set_ylabel('Wire coord. (mm)')
            axl.set_xlabel('wavelength (A)')
            figl.suptitle('DET wavelength')

    def plotMultiplicity(self, cassettes):
        
            self.width      = 0.2
            self.extentplot = 7

            ########

            self.plotMult = preparePlotMatrix(401, 2, len(cassettes))
            
            self.plotMult.figHandle.suptitle('Events - multiplicity')
            
            xx =  self.allAxis.axMult.axis

            for k, cass in enumerate(cassettes):
   
                selc  = self.events.Cassette  == cass
                sel2D = self.events.positionS >= 0

                myw  = hh.histog().hist1D(xx,self.events.multW[selc]) # wires all
                mys  = hh.histog().hist1D(xx,self.events.multS[selc]) # strips all
                mywc = hh.histog().hist1D(xx,self.events.multW[selc & sel2D]) # wires coinc
           
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
                self.plotMult.axHandle[0][k].set_title('cass ID '+str(cass))
                legend = self.plotMult.axHandle[0][k].legend(loc='upper right', shadow=False, fontsize='large')
                if k == 0:
                    self.plotMult.axHandle[0][k].set_ylabel('probability')
                
                
                pos1 = self.plotMult.axHandle[1][k].imshow(my2Dwcnorm[:self.extentplot,:self.extentplot],aspect='auto',norm=None,interpolation='none',extent=[xx[0]-0.5,xx[self.extentplot]-0.5,xx[0]-0.5,xx[self.extentplot]-0.5], origin='lower',cmap='jet')
                self.plotMult.axHandle[1][k].set_xlabel('multiplicity wires')
                if k == 0:
                    self.plotMult.axHandle[1][k].set_ylabel('multiplicity strips')
                    
                plt.colorbar(pos1,ax=self.plotMult.axHandle[1][k])
       

    def plotPHS(self, cassettes, parameters, logScale = False):
        
        normColors = logScaleMap(logScale).normColors
        
        self.plotPHS = preparePlotMatrix(601, 4, len(cassettes))
        
        self.plotPHS.figHandle.suptitle('Pulse Heigth Spectra')
        
        wireCh0to31Round = np.round(np.mod(self.events.positionW,parameters.configJsonFile.numOfWires))
                
        stripChRound     = np.round(self.events.positionS)
        
        wireAx  = np.linspace(0,parameters.configJsonFile.numOfWires-1, parameters.configJsonFile.numOfWires)
        
        stripAx = np.linspace(0,parameters.configJsonFile.numOfStrips-1, parameters.configJsonFile.numOfStrips)
        
        for k, cass in enumerate(cassettes):
   
                selc  = self.events.Cassette  == cass
                sel2D = self.events.positionS >= 0
                
                PHSw  = hh.histog().hist2D(self.allAxis.axEnergy.axis,self.events.PHW[selc],wireAx,wireCh0to31Round[selc]) # wires 
                PHSs  = hh.histog().hist2D(self.allAxis.axEnergy.axis,self.events.PHS[selc & sel2D],wireAx,stripChRound[selc & sel2D]) # strips
                PHSwc = hh.histog().hist2D(self.allAxis.axEnergy.axis,self.events.PHW[selc & sel2D],wireAx,wireCh0to31Round[selc & sel2D]) # wires coinc with strips 2D
                
                self.plotPHS.axHandle[0][k].imshow(PHSw,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,wireAx[0],wireAx[-1]], origin='lower',cmap='jet')
                self.plotPHS.axHandle[1][k].imshow(PHSs,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,stripAx[0],stripAx[-1]], origin='lower',cmap='jet')
                self.plotPHS.axHandle[2][k].imshow(PHSwc,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,wireAx[0],wireAx[-1]], origin='lower',cmap='jet')
                
                self.plotPHS.axHandle[0][k].set_title('cass ID '+str(cass))
                if k == 0:
                    self.plotPHS.axHandle[0][k].set_ylabel('wires ch. no.')
                    self.plotPHS.axHandle[1][k].set_ylabel('strips ch. no.')
                    self.plotPHS.axHandle[2][k].set_ylabel('wires coinc. ch. no.')
           
                   #global PHS
                PHSGw  = np.sum(PHSw,axis=0)
                PHSGs  = np.sum(PHSs,axis=0)
                PHSGwc = np.sum(PHSwc,axis=0)
       
                # global PHS plot
                self.plotPHS.axHandle[3][k].step(self.allAxis.axEnergy.axis,PHSGw,'r',where='mid',label='w')
                self.plotPHS.axHandle[3][k].step(self.allAxis.axEnergy.axis,PHSGs,'b',where='mid',label='s')
                self.plotPHS.axHandle[3][k].step(self.allAxis.axEnergy.axis,PHSGwc,'k',where='mid',label='w/s')
                self.plotPHS.axHandle[3][k].set_xlabel('pulse height (a.u.)')
                self.plotPHS.axHandle[3][k].legend(loc='upper right', shadow=False, fontsize='large')
                if k == 0:
                   self.plotPHS.axHandle[3][k].set_ylabel('counts')
                   
    def plotPHScorrelation(self, cassettes, logScale = False):
              
           normColors = logScaleMap(logScale).normColors
        
           self.plotPHScorr = preparePlotMatrix(602, 1, len(cassettes), figSize=(12,6))
           
           self.plotPHScorr.figHandle.suptitle('Pulse Heigth Spectrum - Correlation W/S')
        
           for k, cass in enumerate(cassettes):
   
                selc  = self.events.Cassette  == cass
                sel2D = self.events.positionS >= 0
                
                PHScorr  = hh.histog().hist2D(self.allAxis.axEnergy.axis,self.events.PHW[selc & sel2D],self.allAxis.axEnergy.axis,self.events.PHS[selc & sel2D]) 
               
                self.plotPHScorr.axHandle[0][k].imshow(PHScorr,aspect='auto',norm=normColors,interpolation='none',extent=[self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop,self.allAxis.axEnergy.start,self.allAxis.axEnergy.stop], origin='lower',cmap='jet')
                
                self.plotPHScorr.axHandle[0][k].set_title('cass ID '+str(cass))
                self.plotPHScorr.axHandle[0][k].set_xlabel('pulse height wires (a.u.)')
                if k == 0:
                    self.plotPHScorr.axHandle[0][k].set_ylabel('pulse height strips (a.u.)')
            
    def plotInstantaneousRate(self, cassettes):
           
           self.plotInst = preparePlotMatrix(209, 1, len(cassettes))
           
           self.plotInst.figHandle.suptitle('Instantaneous Rate')
           
           for k, cass in enumerate(cassettes):
               
               selc  = self.events.Cassette  == cass
               sel2D = self.events.positionS >= 0
               diffeTime = np.diff(self.events.timeStamp[selc & sel2D])
               
               histRate = hh.histog().hist1D(self.allAxis.axInstRate.axis,diffeTime) 
               
               self.plotInst.axHandle[0][k].step(self.allAxis.axInstRate.axis*1e6,histRate,'k',where='mid',label='w')
               self.plotInst.axHandle[0][k].set_xlabel('delta time between events (us)')
               self.plotInst.axHandle[0][k].set_title('cass ID '+str(cass))
               if k == 0:
                   self.plotInst.axHandle[0][k].set_ylabel('num of events')
                   
                   
    def plotToF(self, cassettes):
           
          self.plotTT = preparePlotMatrix(333, 1, len(cassettes))
          
          self.plotTT.figHandle.suptitle('ToF distr per cassette')
          
          for k, cass in enumerate(cassettes):
               
               selc  = self.events.Cassette  == cass
               sel2D = self.events.positionS >= 0
               
               histTT  = hh.histog().hist1D(self.allAxis.axToF.axis,self.events.ToF[selc & sel2D]) 
               
               histTT1 = hh.histog().hist1D(self.allAxis.axToF.axis,self.events.ToF[selc])
               
               self.plotTT.axHandle[0][k].step(self.allAxis.axToF.axis*1e3,histTT1,'r',where='mid',label='all')
               self.plotTT.axHandle[0][k].step(self.allAxis.axToF.axis*1e3,histTT1,'b',where='mid',label='2D')
               self.plotTT.axHandle[0][k].set_xlabel('ToF (ms)')
               self.plotTT.axHandle[0][k].set_title('cass ID '+str(cass))
               if k == 0:
                   self.plotTT.axHandle[0][k].set_ylabel('counts')
                   
              
               legend = self.plotTT.axHandle[0][k].legend(loc='upper right', shadow=False, fontsize='large')
          
###############################################################################
###############################################################################

if __name__ == '__main__' :
    
    plt.close("all")
    
    configFilePath = '/Users/francescopiscitelli/Documents/PYTHON/MBUTYcap/config/'+"MB300_AMOR_config.json"
    
    
    parameters  = para.parameters('./')
    
    
    
    
    config = maps.read_json_config(configFilePath)
    parameters.loadConfigParameters(config)


    parameters.plotting.positionReconstruction = 'W.max-S.max'
    
    parameters.cassettes.cassettes = [1,2,3]
    
    # parameters.wavelength.distance = 19000
    
    parameters.configJsonFile.offset1stWires = 10

    #  generate sample hits 
    
    # Nhits = 1e4
    # bb = sdat.sampleHitsMultipleCassettes()
    # bb.generateGlob(Nhits)
    
    bb = sdat.sampleHitsMultipleCassettes_2()
    bb.generateGlob()
    
    
    
    hits = bb.hits 
    
    hitsArray = hits.concatenateHitsInArrayForDebug()

    
    
    timeWindow = 2e-6
    
    cc = clu.clusterHits(hits,0)
    cc.clusterizeManyCassettes(parameters.cassettes.cassettes, timeWindow)
    
    vv = absu.calculateAbsUnits(cc.events, parameters)
   
    vv.calculatePositionAbsUnit()

    vv.calculateToFandWavelength(0)
   
    events = vv.events
    
    # events = cc.events
    
    # # # 
    

    
    allAxis = hh.allAxis()
    allAxis.createAllAxis(parameters)
    
    # axall.axLambda.start = 2.5
    # axall.axLambda.stop = 12
    # axall.axLambda.steps = 127

    # axall.axEnergy.stop  = 70000
    # axall.axEnergy.steps = 256
    
    # axall.axToF.stop  = 0.1
    # axall.axToF.steps = round(0.1/100e-6)
    
    # axall.axStrips.stop  = config.numOfStrips
    # axall.axStrips.steps = 129  #cog
    
    # axall.axWires.stop  = len(cassettes)*config.numOfWires
    # axall.axWires.steps = len(cassettes)*config.numOfWires+1
    
    # axall.updateAllAxis()
    
    # 
    
    # filePathD = './'+"VMM3a.pcapng"
    
    # pr = pcapr.pcap_reader(filePathD)
    #   #  # pr.debug = True
    # pr.read()
    # vmm1 = pr.readouts
    

    # ppp = plottingReadouts(vmm1, config)
    # ppp.plotChRaw([1,2,3,4])
    
    # ppp.plotTimeStamps([1,2,3,4])
   
    # vmm2 = sdat.sampleData()
    # vmm2.fill()

    # cassettes = [1,2,3,4,5]

    # # map data
    # md  = maps.mapDetector(vmm1, config)
    # md.mappAllCassAndChannelsGlob()
    # hits = md.hits
    

    
    # dd = plottingHits(hits2, parameters)
    # dd.plotChRaw(parameters.cassettes.cassettes)
    
    pp = plottingEvents(events,allAxis,coincidenceWS_ONOFF=True)
    # pp.plotXYToF(logScale=True, absUnits = True)
    
    # pp.plotXLambda(logScale=False, absUnits = False)
    
    # aa = pp.plotMultiplicity([1,2,3])
    
    # aa = pp.plotPHS([1,2,3],parameters)
    
    # pp.plotPHScorrelation([1,2,3])
    
    h2D = pp.plotXYToF(logScale = False, absUnits = False, orientation='vertical')

        
    ##################


    
    
    
    