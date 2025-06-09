# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 11:51:22 2025

@author: sheilamonera
"""

# gui_config.py
import os
from lib import libParameters as para

# Set current path
currentPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/'
parameters = para.parameters(currentPath)
para.checkPythonVersion()
profiling = para.profiling()

# Load available config files
configFilePath = os.path.join(currentPath, 'config')
config_json_files = [f for f in os.listdir(configFilePath) if f.endswith('.json')]

# Define configuration structure
config = {
    "static": {
        "configFileName": {
            "label": "Select Config File",
            "type": "dropdown",
            "options": config_json_files,
            "info": "Must select config file",
            "set": lambda val: globals().__setitem__('configFileName', val)

        },
        "parameters.acqMode": {
            "label": "Acquisition Mode",
            "type": "radio",
            "options": ["off", "pcap-sync", "pcap-local", "pcap-local-overwrite", "kafka"],
            "default": "off",
            "set": lambda val: setattr(parameters, 'acqMode', val)

        }
    }, 
    "file_management": {
        "parameters.dumpSettings.interface": {
            "label": "Network Interface",
            "type": "entry",
            "default": "ens2",
            "info": "Used for acqMode = pcap-local, pcap-local-overwrite, or kafka",
            "dependsOn": ("parameters.acqMode", ["pcap-local", "pcap-local-overwrite", "kafka"]),
            "set": lambda val: setattr(parameters.dumpSettings, 'interface', val)
        },
        "parameters.dumpSettings.typeOfCapture": {
            "label": "Type of Capture",
            "type": "radio",
            "options": ["packets", "duration"],
            "default": "packets",
            "info": "Choose whether to capture by number of packets or duration (in seconds)",
            "dependsOn": ("parameters.acqMode", ["pcap-local", "pcap-local-overwrite", "kafka"]),
            "set": lambda val: setattr(parameters.dumpSettings, 'typeOfCapture', val)
        },
        "parameters.dumpSettings.quantity": {
            "label": "Quantity",
            "type": "entry",
            "inputValidation": "int",
            "default": 100,
            "info": "Number of packets or seconds to capture based on 'typeOfCapture'",
            "dependsOn": ("parameters.acqMode", ["pcap-local", "pcap-local-overwrite", "kafka"]),
            "set": lambda val: setattr(parameters.dumpSettings, 'quantity', val)
        },
        "parameters.fileManagement.fileNameSave": {
            "label": "Save File Name",
            "type": "entry",
            "default": "test",
            "info": "Name of the file to save captured data",
            "set": lambda val: setattr(parameters.fileManagement, 'fileNameSave', val)
        },
        "parameters.kafkaSettings.broker": {
            "label": "Kafka Broker",
            "type": "entry",
            "inputValidation": "host:port",
            "default": "127.0.0.1:9092",
            "info": "Broker address in the format host:port. Relevant for acqMode = kafka",
            "dependsOn": ("parameters.acqMode", "kafka"),
            "set": lambda val: setattr(parameters.kafkaSettings, 'broker', val)
        },
        "parameters.kafkaSettings.topic": {
            "label": "Kafka Topic",
            "type": "entry",
            "default": "freia_debug",
            "dependsOn": ("parameters.acqMode", "kafka"),
            "set": lambda val: setattr(parameters.kafkaSettings, 'topic', val)
        },
        "parameters.kafkaSettings.numOfPackets": {
            "label": "Number of Packets",
            "type": "entry",
            "inputValidation": "int",
            "default": 100,
            "info": "Total number of packets to dump (used with acqMode = kafka)",
            "dependsOn": ("parameters.acqMode", "kafka"),
            "set": lambda val: setattr(parameters.kafkaSettings, 'numOfPackets', val)
        },
        "parameters.fileManagement.sourcePath": {
            "label": "Source Path",
            "type": "entry",
            "inputValidation": "remotepath",
            "default": "essdaq@172.30.244.50:~/pcaps/",
            "info": "Remote source path to rsync from. Relevant for acqMode = pcap-sync",
            "dependsOn": ("parameters.acqMode", "pcap-sync"),
            "set": lambda val: setattr(parameters.fileManagement, 'sourcePath', val)
        },
        "parameters.fileManagement.destPath": {
            "label": "Destination Path",
            "type": "entry",
            "inputValidation": "localPath",
            "info": "Local destination path to rsync to. Relevant for acqMode = pcap-sync",
            "dependsOn": ("parameters.acqMode", "pcap-sync"),
            "set": lambda val: setattr(parameters.fileManagement, 'destPath', val)
        },
        "parameters.fileManagement.filePath": {
            "label": "Data Folder Path",
            "type": "entry",
            "inputValidation": "localPath",
            "default": currentPath+'data/',
            "info": "Path to the folder containing data files. Relevant for acqMode = off, pcap-sync, and pcap-local",
            "dependsOn": ("parameters.acqMode", ["off", "pcap-sync", "pcap-local"]),
            "set": lambda val: setattr(parameters.fileManagement, 'filePath', val)
        },
        "parameters.fileManagement.fileName": {######################################################################### deal with this later passing a list of files
            "label": "Data File Name(s)",
            "type": "multiSelect",
            "default": ["ESSmask2023.pcapng"], #
            "options": None, #[f for f in os.listdir(parameters.fileManagement.filePath) if f.endswith('.pcapng')]
            "info": "List of file(s) to load from the data folder. Relevant for acqMode = off, pcap-sync, and pcap-local",
            "dependsOn": ("parameters.acqMode", ["off", "pcap-sync", "pcap-local"]),
            "set": lambda val: setattr(parameters.fileManagement, 'fileName', val)
        },
        "parameters.fileManagement.openMode": {
            "label": "File Open Mode",
            "type": "radio",
            "options": ["window", "fileName", "latest", "secondLast", "wholeFolder", "sequence"],
            "default": "fileName",
            "info": "Choose how files should be selected and loaded: 'window' opens file browser, 'fileName' uses preset file, 'latest' and 'secondLast' load most recent files, 'wholeFolder' analyzes all files, 'sequence' uses fileSerials.",
            "set": lambda val: setattr(parameters.fileManagement, 'openMode', val)
        },
        "parameters.fileManagement.fileSerials": { 
            "label": "File Serials",
            "type": "range",
            "default": [18,27],
            "inputValidation": "int",
            "info": "Used when openMode is 'sequence' to indicate file serial range (e.g., 18-27). Both boundaries are inclusive.",  
            "dependsOn": ("parameters.fileManagement.openMode", "sequence"),
            "set": lambda val: setattr(parameters.fileManagement, 'fileSerials', np.arange(val[0], val[1]+1, 1))
        },
        "parameters.fileManagement.pcapLoadingMethod": {
            "label": "PCAP Loading Method",
            "type": "bool",
            "options": ["allocate", "quick"],
            "default": "allocate",
            "info": "Controls how memory is allocated when loading PCAP files. 'allocate' is more rigorous, \n'quick' estimates the memory and is faster.",
            "set": lambda val: setattr(parameters.fileManagement, 'pcapLoadingMethod', val)
        },
        "parameters.fileManagement.calibFilePath": {
            "label": "Calibration File Path",
            "type": "entry",
            "inputValidation": "localPath",
            "default": parameters.fileManagement.currentPath+'calib/',
            "info": "Path to the calibration file folder.",
            "set": lambda val: setattr(parameters.fileManagement, 'calibFilePath', val)
        },
        "parameters.fileManagement.calibFileName": {
            "label": "Calibration File Name",
            "type": "dropdown",
            "options": [f for f in os.listdir(os.path.join(currentPath, 'calib')) if f.endswith('.json')],
            "default": "AMOR_calib_20231111002842.json",
            "info": "Name of the calibration file.",
            "set": lambda val: setattr(parameters.fileManagement, 'calibFileName', val)
        },
        "parameters.fileManagement.thresholdFilePath": {
            "label": "Threshold File Path",
            "type": "entry",
            "inputValidation": "localPath",
            "default": parameters.fileManagement.currentPath+'config/',
            "info": "Path to the threshold file folder.",
            "set": lambda val: setattr(parameters.fileManagement, 'thresholdFilePath', val)
        },
        "parameters.fileManagement.thresholdFileName": {
            "label": "Threshold File Name",
            "type": "entry",
            "default": [f for f in os.listdir(os.path.join(currentPath, 'config')) if f.endswith('.xlsx')],
            "info": "Name of the Excel threshold file.",
            "set": lambda val: setattr(parameters.fileManagement, 'thresholdFileName', val)
        },
        "parameters.fileManagement.pathToTshark": {
            "label": "Path to Tshark",
            "type": "entry",
            "inputValidation": "localPath",
            "default": "/Applications/Wireshark.app/Contents/MacOS/",
            "dependsOn": ("parameters.acqMode", ["pcap-local", "pcap-local-overwrite"]),
            "info": "Filesystem path to the Tshark binary. Used to convert PCAP to PCAPNG if needed.",
            "set": lambda val: setattr(parameters.fileManagement, 'pathToTshark', val)
        },
        "parameters.fileManagement.saveReducedFileONOFF": {
            "label": "Save Reduced File",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "Enable or disable saving a reduced HDF file with clusters.",
            "set": lambda val: setattr(parameters.fileManagement, 'saveReducedFileONOFF', val)
        },
        "parameters.fileManagement.saveReducedPath": {
            "label": "Reduced File Path",
            "type": "entry",
            "inputValidation": "localPath",
            "default": "/Users/francescopiscitelli/Desktop/reducedFile/",
            "dependsOn": ("parameters.fileManagement.saveReducedFileONOFF", True),
            "info": "Destination path for saving reduced HDF files.",
            "set": lambda val: setattr(parameters.fileManagement, 'saveReducedPath', val)
        },
        "parameters.fileManagement.reducedNameMainFolder": { # don't know if there are more options - if no more options remove from GUI and set fixed value
            "label": "Main Folder in HDF",
            "type": "entry",
            "default": "entry1",
            "set": lambda val: setattr(parameters.fileManagement, 'reducedNameMainFolder', val)
        },
        "parameters.fileManagement.reducedCompressionHDFT": {# don't know if there are more options - if no more options remove from GUI and set fixed value
            "label": "HDF Compression Type",
            "type": "radio",
            "options": ["gzip"],
            "default": "gzip",
            "info": "Compression method used for saving HDF files.",
            "set": lambda val: setattr(parameters.fileManagement, 'reducedCompressionHDFT', val)
        },
        "parameters.fileManagement.reducedCompressionHDFL": {
            "label": "HDF Compression Level",
            "type": "entry",
            "inputValidation": "int",
            "range": (0,9),
            "default": 9,
            "info": "Compression level (0-9) used with HDF file saving.",
            "set": lambda val: setattr(parameters.fileManagement, 'reducedCompressionHDFL', val)
        }

    },
    "analysis": {
        "parameters.dataReduction.calibrateVMM_ADC_ONOFF": {
            "label": "Calibrate VMM ADC",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "Calibration VMM ADC",
            "set": lambda val: setattr(parameters.dataReduction, 'calibrateVMM_ADC_ONOFF', val)
        },
        "parameters.VMMsettings.sortReadoutsByTimeStampsONOFF": {
            "label": "Sort Readouts by Time Stamps",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "Sorting readouts by time stamp, if OFF they are as in RMM stream",
            "set": lambda val: setattr(parameters.VMMsettings, 'sortReadoutsByTimeStampsONOFF', val)
        },
        "parameters.VMMsettings.timeResolutionType": {
            "label": "Time Resolution Type",
            "type": "bool",
            "options": ["fine", "coarse"],
            "default": "fine",
            "info": "Time stamp is time HI + time LO or if fine corrected with TDC ",
            "set": lambda val: setattr(parameters.VMMsettings, 'timeResolutionType', val)
        },
        "parameters.dataReduction.timeWindow": {
            "label": "Time Window (s)",
            "type": "entry",
            "inputValidation": "scientific",
            "default": "0.3e-6",
            "info": "Time window to search for clusters.\nThis is the maximum time allowed between events in a cluster.\nHalf the value is used as the recursive threshold between adjacent hits.",
            "set": lambda val: setattr(parameters.dataReduction, 'timeWindow', val)
        },
        "parameters.dataReduction.softThresholdType": {
            "label": "Soft Threshold Type",
            "type": "radio",
            "options": ["off", "fromFile", "userDefined"],
            "default": "off",
            "info": "Select how to define soft thresholds: off, from file, or user-defined.",
            "set": lambda val: (
                    setattr(parameters.dataReduction, 'softThresholdType', val),
                    parameters.dataReduction.createThArrays(parameters.config.DETparameters.cassInConfig, parameters)
                    if val == "userDefined" else None
                )[-1]
        },
        "parameters.dataReduction.softThArray.ThW[:,0]": {
            "label": "Soft Threshold W",
            "type": "entry",
            "inputValidation": "float",
            "dependsOn": ("parameters.dataReduction.softThresholdType", "userDefined"),
            "default": 15000,
            "set": lambda val: setattr(parameters.dataReduction.softThArray, 'ThW[:,0]', val)
        },
        "parameters.dataReduction.softThArray.ThS[:,0]": {
            "label": "Soft Threshold S",
            "type": "entry",
            "inputValidation": "float",
            "dependsOn": ("parameters.dataReduction.softThresholdType", "userDefined"),
            "default": 500,
            "set": lambda val: setattr(parameters.dataReduction.softThArray, 'ThS[:,0]', val)
        }
    },
    "wavelength": {
        "parameters.wavelength.distance": {
            "label": "Distance (mm)",
            "type": "entry",
            "default": 8000,
            "inputValidation": "int",
            "info": "Distance in mm from chopper and wires 0 of detector",
            "set": lambda val: setattr(parameters.wavelength, 'distance', val)
        },
        "parameters.wavelength.calculateLambda": {
            "label": "Calculate Lambda",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.wavelength, 'calculateLambda', val)
        },
        "parameters.wavelength.plotXLambda": {
            "label": "Plot X vs Lambda",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "2D plot of X vs Lambda",
            "set": lambda val: setattr(parameters.wavelength, 'plotXLambda', val)
        },
        "parameters.wavelength.plotLambdaDistr": {
            "label": "Plot Lambda Distribution",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "ON/OFF integrated over single cassettes",
            "set": lambda val: setattr(parameters.wavelength, 'plotLambdaDistr', val)
        },
        "parameters.wavelength.lambdaBins": {
            "label": "Lambda Bins",
            "type": "entry",
            "default": 128,
            "inputValidation": "int",
            "info": "Number of bins for the lambda histogram",
            "set": lambda val: setattr(parameters.wavelength, 'lambdaBins', val)
        },
        "parameters.wavelength.lambdaRange": {
            "label": "Lambda Range [min, max] (Å)",
            "type": "range",
            "default": [1, 16],
            "inputValidation": "int",
            "info": "Range of lambda values (in Å) as [min, max]",
            "set": lambda val: setattr(parameters.wavelength, 'lambdaRange', val)
        },
        "parameters.wavelength.chopperPeriod": {
            "label": "Chopper Period (s)",
            "type": "entry",
            "default": 0.12,
            "inputValidation": "float",
            "info": "Chopper period in seconds (relevant if multipleFramesPerRest > 1)",
            "set": lambda val: setattr(parameters.wavelength, 'chopperPeriod', val)
        },
        "parameters.wavelength.multipleFramePerReset": {
            "label": "Multiple Frames per Reset",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "ON/OFF toggle for if chopper has two openings or more per reset of ToF \n(This only affects the lambda calculation)",
            "set": lambda val: setattr(parameters.wavelength, 'multipleFramePerReset', val)
        },
        "parameters.wavelength.numOfBunchesPerPulse": {
            "label": "Bunches per Pulse",
            "type": "entry",
            "default": 2,
            "inputValidation": "int",
            "info": "Number of neutron bunches per pulse",
            "set": lambda val: setattr(parameters.wavelength, 'numOfBunchesPerPulse', val)
        },
        "parameters.wavelength.lambdaMIN": {
            "label": "Minimum Lambda (Å)",
            "type": "entry",
            "default": 2.5,
            "inputValidation": "float",
            "set": lambda val: setattr(parameters.wavelength, 'lambdaMIN', val)
        }
    },
    "monitor": {
        "parameters.MONitor.MONOnOff": {
            "label": "Enable Monitor",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "ON/OFF switch for including the monitor in the analysis.",
            "set": lambda val: setattr(parameters.MONitor, 'MONOnOff', val)
        },
        "parameters.MONitor.MONThreshold": {
            "label": "Monitor Threshold",
            "type": "entry",
            "default": 0,
            "inputValidation": "float",
            "info": "Threshold on monitor events. 0 disables threshold; any other value enables it.",
            "set": lambda val: setattr(parameters.MONitor, 'MONThreshold', val)
        },
        "parameters.MONitor.plotMONtofPHS": {
            "label": "Plot Monitor ToF & PHS",
            "type": "bool",
            "options": ["True", "False"],
            "default": "True",
            "info": "ON/OFF plotting for Monitor Time-of-Flight and Pulse Height spectra.",
            "set": lambda val: setattr(parameters.MONitor, 'plotMONtofPHS', val)
        },
        "parameters.MONitor.MONDistance": {
            "label": "Monitor Distance (mm)",
            "type": "entry",
            "default": 6000,
            "inputValidation": "int",
            "info": "Distance in mm from chopper to monitor (needed for lambda calculation of ToF).", 
            "dependsOn": ("parameters.MONitor.plotMONtofPHS", True),
            "set": lambda val: setattr(parameters.MONitor, 'MONDistance', val)
        }
    },
    "plotting": {
        "parameters.plotting.bareReadoutsCalculation": {
            "label": "Bare Readouts Only",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "Disables clustering and mapping for speed. Stops analysis at raw readouts.",
            "set": lambda val: setattr(parameters.plotting, 'bareReadoutsCalculation', val)
        },
        "parameters.plottingInSections": {
            "label": "Plot in Sections",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "If True, plots are split into blocks for easier visualization.",
            "set": lambda val: setattr(parameters, 'plottingInSections', val)
        },
        "parameters.plottingInSectionsBlocks": {
            "label": "Sections Per Block",
            "type": "entry",
            "default": 5,
            "inputValidation": "int",
            "dependsOn": ("parameters.plottingInSections", True),
            "info": "Number of cassettes per plotting section.",
            "set": lambda val: setattr(parameters, 'plottingInSectionsBlocks', val)
        },
        "parameters.plotting.showStat": {
            "label": "Statistics Display",
            "type": "radio",
            "options": ["None", "globalStat", "individualStat"],
            "default": "globalStat",
            "info": "Choose how to display statistical summaries.",
            "set": lambda val: setattr(parameters.plotting, 'showStat', val)
        },
        # Raw plotting options
        "parameters.plotting.plotRawReadouts": {
            "label": "Plot Raw Readouts",
            "type": "bool",
            "options": ["True", "False"],
            "default": "True",
            "set": lambda val: setattr(parameters.plotting, 'plotRawReadouts', val)
        },
        "parameters.plotting.plotReadoutsTimeStamps": {
            "label": "Plot Readouts Time Stamps",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotReadoutsTimeStamps', val)
        },
        "parameters.plotting.plotADCvsCh": {
            "label": "Plot ADC vs Channel",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotADCvsCh', val)
        },
        "parameters.plotting.plotADCvsChlog": {
            "label": "Plot ADC vs Channel (Log Scale)",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotADCvsChlog', val)
        },
        "parameters.plotting.plotChopperResets": {
            "label": "Plot Chopper Resets",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotChopperResets', val)
        },
        # Hit-level plotting
        "parameters.plotting.plotRawHits": {
            "label": "Plot Raw Hits",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotRawHits', val)
        },
        "parameters.plotting.plotHitsTimeStamps": {
            "label": "Plot Hits Time Stamps",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotHitsTimeStamps', val)
        },
        "parameters.plotting.plotHitsTimeStampsVSChannels": {
            "label": "Plot Hits Timestamps vs Channels",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotHitsTimeStampsVSChannels', val)
        },
        # Instantaneous Rate
        "parameters.plotting.plotInstRate": {
            "label": "Plot Instantaneous Rate",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotInstRate', val)
        },
        "parameters.plotting.instRateBin": {
            "label": "Rate Bin Width (s)",
            "type": "entry",
            "default": "100e-6",
            "inputValidation": "scientific",
            "dependsOn": ("parameters.plotting.plotInstRate", True),
            "set": lambda val: setattr(parameters.plotting, 'instRateBin', val)
        },
        # ToF (Time of Flight) plotting
        "parameters.plotting.plotToFDistr": {
            "label": "Plot ToF Distribution",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotToFDistr', val)
        },
        "parameters.plotting.ToFrange": {
            "label": "ToF Range (s)",
            "type": "entry",
            "default": 0.15,
            "inputValidation": "float",
            "set": lambda val: setattr(parameters.plotting, 'ToFrange', val)
        },
        "parameters.plotting.ToFbinning": {
            "label": "ToF Binning (s)",
            "type": "entry",
            "default": "100e-6",
            "inputValidation": "scientific",
            "set": lambda val: setattr(parameters.plotting, 'ToFbinning', val)
        },
        "parameters.plotting.ToFGate": {
            "label": "Enable ToF Gating",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'ToFGate', val)
        },
        "parameters.plotting.ToFGateRange": {
            "label": "ToF Gate Range [s]",
            "type": "range",
            "default": [0.02, 0.025],
            "inputValidation": "float",
            "dependsOn": ("parameters.plotting.ToFGate", True),
            "set": lambda val: setattr(parameters.plotting, 'ToFGateRange', val)
        },
        "parameters.plotting.plotMultiplicity": {
            "label": "Plot Multiplicity",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.plotting, 'plotMultiplicity', val)
        },
        "parameters.plotting.positionReconstruction": {
            "label": "Position Reconstruction Method",
            "type": "radio",
            "options": ["W.max-S.max", "W.cog-S.cog", "W.max-S.cog"],
            "default": "W.max-S.cog",
            "info": "'W.max-S.max' is max max,  'W.cog-S.cog' is CoG CoG, 'W.max-S.cog' is wires max and strips CoG ",
            "set": lambda val: setattr(parameters.plotting, 'positionReconstruction', val)
        },
        "parameters.plotting.plotABSunits": {
            "label": "Use Absolute Units",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "if True plot XY and XtoF plot in absolute unit (mm), if False plot in wire and strip ch no.",
            "set": lambda val: setattr(parameters.plotting, 'plotABSunits', val)
        },
        "parameters.plotting.plotIMGlog": {
            "label": "Log Scale for Images",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "plot XY and XToF in log scale",
            "set": lambda val: setattr(parameters.plotting, 'plotIMGlog', val)
        },
        "parameters.plotting.coincidenceWS_ONOFF": {
            "label": "Require Strip Coincidence",
            "type": "bool",
            "options": ["True", "False"],
            "default": "True",
            "info": "ON/OFF, if  Tof  and Lambdaplot needs to include only events with strip present (2D) is True otherwise all events also without strip set to False",
            "set": lambda val: setattr(parameters.plotting, 'coincidenceWS_ONOFF', val)
        },
        "parameters.plotting.removeInvalidToFs": {
            "label": "Remove Invalid ToFs",
            "type": "bool",
            "options": ["True", "False"],
            "default": "True",
            "info": "ON/OFF, if  invalid ToFs Tofare included in the plots or removed from events",
            "set": lambda val: setattr(parameters.plotting, 'removeInvalidToFs', val)
        },
        "parameters.plotting.hitogOutBounds": {
            "label": "Histogram Out-of-Bounds",
            "type": "bool",
            "options": ["True", "False"],
            "default": "True",
            "info": "histogram outBounds param set as True as default (Events out of bounds stored in first and last bin)",
            "set": lambda val: setattr(parameters.plotting, 'hitogOutBounds', val)
        }
    },
    "pulse_height": {
        "parameters.pulseHeigthSpect.plotPHS": {
            "label": "Plot PHS",
            "type": "bool",
            "options": ["True", "False"],
            "default": "True",
            "info": "Enable or disable pulse height spectra per channel and globally.",
            "set": lambda val: setattr(parameters.pulseHeigthSpect, 'plotPHS', val)
        },
        "parameters.pulseHeigthSpect.plotPHSlog": {
            "label": "PHS Log Scale",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "info": "If True, plot pulse height spectra using a logarithmic scale.",
            "set": lambda val: setattr(parameters.pulseHeigthSpect, 'plotPHSlog', val)
        },
        "parameters.pulseHeigthSpect.energyBins": {
            "label": "Energy Bins",
            "type": "entry",
            "default": 128,
            "inputValidation": "int",
            "info": "Number of bins to use in the pulse height histogram.",
            "set": lambda val: setattr(parameters.pulseHeigthSpect, 'energyBins', val)
        },
        "parameters.pulseHeigthSpect.maxEnerg": {
            "label": "Max Energy",
            "type": "entry",
            "default": 1700,
            "inputValidation": "int",
            "info": "Maximum energy value considered in pulse height analysis.",
            "set": lambda val: setattr(parameters.pulseHeigthSpect, 'maxEnerg', val)
        },
        "parameters.pulseHeigthSpect.plotPHScorrelation": {
            "label": "Plot PHS Correlation (Wires vs Strips)",
            "type": "bool",
            "options": ["True", "False"],
            "default": "False",
            "set": lambda val: setattr(parameters.pulseHeigthSpect, 'plotPHScorrelation', val)
        }
    }
}

# Export
__all__ = ["config", "parameters", "profiling", "currentPath"]
