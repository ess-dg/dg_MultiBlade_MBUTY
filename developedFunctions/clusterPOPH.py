#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:10:21 2019

@author: francescopiscitelli
"""
import numpy as np
import math as mt

#cluster
#this is the equivalent of the MATALB function 
#[POPH,Numevent] = clusterPOPH(data,Clockd,Timewindow,thermalNmultiplicityON);

def clusterPOPH (data,Clockd,Timewindow):

    #data is col 0: time stamp in 16ns precision, col 1: ch number (FROM 0 TOP 63), col2: ADC value, col3: global time reset delta in ms
    # if there is no strip it will be -1, with 0 PH and 0 multiplicity
    
    # # move ch starting from 1 beacuse for the weighting of calculation position would not work if starts at 0
    # data = np.copy(datain)
    # data[:,1] = data[:,1]+1;
    
    # this is a trick to accept also the clusters very close in time otherwise rejected
    Timewindowrec = mt.ceil(Timewindow*1e6/3)/1e6+0.01e-6;
    Timewindow    = Timewindow+0.01e-6;
    ##########
    
    data = np.concatenate((np.zeros([1,4]),data),axis=0)  #add a line at top not to lose the 1st event
    
    tof     = data[:,0]*Clockd           #tof column from 16ns steps in seconds
    tof1us  = np.around(tof, decimals=6) #tof rounded at 1us precision 
    #data[:,0] = data[:,0]*Clockd
    
    data[:,0] = tof1us
    
    dtof1us = np.diff(tof1us[:]) #1st derivative of tof 
    dtof1us = np.concatenate(([0],dtof1us),axis=0) #add a zero at top to restore length of vector
    
    clusterlogic = (np.absolute(dtof1us) <= Timewindowrec) #is zero when a new cluster starts 
    
    # data1 = np.concatenate((data,clusterlogic[:,None]),axis=1) #this is for debugging 
    
    index = np.argwhere(clusterlogic == 0) #find the index where a new cluster may start 
    
    NumClusters = len(index)
    
    #NumClusters = 6
    
    #np.arange(0,NumClusters,1)
    
    rejCounter = np.zeros(5)
    
    POPH = np.zeros((NumClusters,7))  #output data with col0 position wires, col1 poisiton strips, col2 tof, col3 pulse height wires, col4 pulse height strips, col 5 multiplicity w, col 6 muiltiplicity strips
    
    for kk in np.arange(0,NumClusters,1):
        
        if kk < (NumClusters-1): #any cluster in data but the last 
            clusterq = data[index[kk,0]:index[kk+1,0] , 0:3]
        elif kk == (NumClusters-1): #last cluster
            clusterq = data[index[kk,0]: , 0:3]
            
        acceptWindow = ((clusterq[-1,0] - clusterq[0,0]) <= Timewindow)  #max difference in time between first and last in cluster 
        
    #    clusterq_old = clusterq
            
        clusterq = clusterq[clusterq[:,1].argsort(kind='quicksort')]  #order cluster by ch number
        
        # IF CH FORM 1 TO 64
        # wws = clusterq[:,1] <= 32;    #wires 
        # sss = clusterq[:,1] >= 33;    #strips
        
        wws = clusterq[:,1] <= 31;    #wires 
        sss = clusterq[:,1] >= 32;    #strips
       
        # n wires n strips in cluster
        ww = sum(wws)  #num of wires in cluster
        ss = sum(sss)  #num of strips in cluster
    
        if (ww != 0 and ss != 0 and ss <= 32 and ww <= 32 and acceptWindow): #if there is at least 1 wire and 1 strip and no ch number above 32
        
            #check if they are neighbours 
            dcw   = np.concatenate( (np.diff(clusterq[wws,1]),[1.0]),axis=0)
            dcs   = np.concatenate( (np.diff(clusterq[sss,1]),[1.0]),axis=0)
            neigw = sum(dcw)*(sum(dcw == 1) == sum(dcw))    #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
            neigs = sum(dcs)*(sum(dcs == 1) == sum(dcs))
    
            if (neigw == ww and neigs == ss):    #if they are neighbour then...
    
                rejCounter[0] = rejCounter[0]+1;                #counter 2D
    
                Wires  = clusterq[wws,:]
                Strips = clusterq[sss,:]
                
                POPH[kk,5]   = neigw     #multiuplicity wires
                POPH[kk,6]   = neigs     #multiuplicity strips
                POPH[kk,2]   = clusterq[0,0]     #tof
                POPH[kk,3]   = sum(Wires[:,2])   #PH wires
                POPH[kk,4]   = sum(Strips[:,2])   #PH strips
                POPH[kk,0]   = round((sum(Wires[:,1]*Wires[:,2]))/(POPH[kk,3]),2)   #position wires
                POPH[kk,1]   = round((((sum(Strips[:,1]*Strips[:,2]))/(POPH[kk,4]))-32),2)  #position strips from 1 to 32 or from 0 to 31

            else:
                rejCounter[1] = rejCounter[1]+1;                #counter if they are no neighbour 
                
        elif (ww >= 1 and ss == 0 and ww <= 32 and acceptWindow): #put in 1D hist only for wires when there is no strip 
                
            #check if they are neighbours 
            dcw   = np.concatenate( (np.diff(clusterq[wws,1]),[1.0]),axis=0)
            neigw = sum(dcw)*(sum(dcw == 1) == sum(dcw))    #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
           
            if (neigw == ww):    #if they are neighbour then...
    
                rejCounter[2] = rejCounter[2]+1;                #counter 1D
    
                Wires  = clusterq[wws,:]
                
                POPH[kk,5]   = neigw     #multiuplicity wires
                POPH[kk,2]   = clusterq[0,0]     #tof
                POPH[kk,3]   = sum(Wires[:,2])   #PH wires
                POPH[kk,0]   = round((sum(Wires[:,1]*Wires[:,2]))/(POPH[kk,3]),2)   #position wires
                POPH[kk,1]   = -1 #position strips if absent
                
    #            if POPH[kk,3] != 0 :
    #                POPH[kk,0]   = (sum(Wires[:,1]*Wires[:,2]))/(POPH[kk,3])   #position wires
    #            else:
    #                POPH[kk,0]   =-3
      
                
            else:
                rejCounter[1] = rejCounter[1]+1              #counter if they are no neighbour 
                
        elif (ww >= 33 or ss >= 33):
             rejCounter[3] = rejCounter[3]+1               #counter if cluster above possible limits          
             print('\n cluster > 32 in either directions w or s -> probably rate too high \n')
             
        else:
            rejCounter[4] = rejCounter[4]+1               #any other case not taken into account previously
            
    
    rejected = np.logical_and((POPH[:,5] == 0),(POPH[:,6] == 0))    #remove rejected from data in rejCoiunter[4] it is when only strips and wire and sgtrip mult is 0, whole row in POPH is 0 actually 
    
    POPH     = POPH[np.logical_not(rejected),:];    #remove rejected from data
     
    NumeventNoRej = NumClusters - (rejCounter[1]+rejCounter[3]+rejCounter[4]);
    rej2 = 100*(rejCounter/NumClusters);
    rej3 = 100*(rejCounter/NumeventNoRej);
    
    print("\n \t N of events: %d -> not rejected (2D and 1D) %d " % (NumClusters,NumeventNoRej))
    print("\t not rej (2D) %.1f%%, only w (1D) %.1f%%, rejected (2D or 1D) %.1f%%, rejected >32 %.1f%%, rejected other reasons (only strips - noise)  %.1f%% " % (rej2[0],rej2[2],rej2[1],rej2[3],rej2[4]));
    print("\t not rej (2D) %.1f%%, only w (1D) %.1f%% \n " % (rej3[0],rej3[2]))
    

    mbins=np.arange(0,33,1)
    
    TwoDim = POPH[:,1] >= 0
    multiwhistcoinc = np.histogram(POPH[TwoDim,5],mbins)
    multishistcoinc = np.histogram(POPH[:,6],mbins)
        
    wirefire  = multiwhistcoinc[0]/sum(multiwhistcoinc[0])
    stripfire = multishistcoinc[0]/sum(multishistcoinc[0][1:])
        
    print("\n \t 2D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*wirefire[1],100*wirefire[2],100*wirefire[3],100*wirefire[4],100*wirefire[5])); 
    print(" \t 2D: percentage of strips fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*stripfire[1],100*stripfire[2],100*stripfire[3],100*stripfire[4],100*stripfire[5])); 
         
        
    OneDim = POPH[:,1] == -1
    multiwhist = np.histogram(POPH[OneDim,5],mbins)
        
    wirefire1D  = multiwhist[0]/sum(multiwhist[0]);
        
    print(" \t 1D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5) \n" % (100*wirefire1D[1],100*wirefire1D[2],100*wirefire1D[3],100*wirefire1D[4],100*wirefire1D[5])); 


    return POPH, NumClusters

#HERE ENDS CLUSTERPOPH