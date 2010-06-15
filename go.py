#!/usr/bin/env python
import sys,base
import ROOT as r

#choose the analysis
#name="triggerSkim"
#name="jetAlgoComparison"
#name="metDistLook"
name="example"
#name="jetKineLook"
#name="deltaPhiLook"
#name="metGroupCleanupLook"
#name="Icf_Ra1_DiJet"
#name="Icf_Ra1_NJet"
#name="RecHitTest"
#name="Ra1_NJet"
#name="HcalTechTriggerCheck"
#name="mSugraLook"
#name="MetPasSkim"
#name="MetPasSkim1"
#name="MetPasSkim2"
#name="MetPasSpeedTest"

#choose the output directory
outputDir="~"
    
def globalSetup() :
    sourceFiles=["SusyCAFpragmas.h","helpers.C"]
    for sourceFile in sourceFiles :
        r.gROOT.LoadMacro(sourceFile+"+")
    r.gROOT.SetStyle("Plain")
    r.gStyle.SetPalette(1)
    r.TH1.SetDefaultSumw2(True)
    r.gErrorIgnoreLevel=2000

def makeSampleSpecs(name) :
    import samples,lists,analyses
    #build dictionaries of files and xs
    sampleHolder=samples.sampleDictionaryHolder()
    sampleHolder.buildDictionaries()
    fileListDict=sampleHolder.getFileListDictionary()
    xsDict=sampleHolder.getXsDictionary()

    #build dictionary of lists
    listHolder=lists.listDictionaryHolder()
    listHolder.buildDictionary()
    listDict=listHolder.getDictionary()

    #build dictionary of analyses
    analysisHolder=analyses.analysisDictionaryHolder(fileListDict,xsDict,listDict)
    analysisHolder.buildDictionary()
    sampleSpecs=analysisHolder.getDictionary()[name]
    return sampleSpecs

def goFunc(x) :
    x.go()

def looperPrint(parent,looper) :
    print looper.hyphens
    print parent
    looper.quietMode=False
    looper.printStats()
    print looper.hyphens

def makeParentDict(looperList) :
    parentDict={}
    for iLooper in range(len(looperList)) :
        looper=looperList[iLooper]
        if looper.splitMode :
            if looper.parentName in parentDict :
                parentDict[looper.parentName].append(iLooper)
            else :
                parentDict[looper.parentName]=[iLooper]
    return parentDict

def mergeSplitOutput(looperList) :
    import os,cPickle
    
    #make dictionary
    parentDict=makeParentDict(looperList)

    #combine output
    for parent in parentDict :
        #print parent,parentDict[parent]
        iSomeLooper=parentDict[parent][0]
        someLooper=looperList[iSomeLooper]
        outputPlotFileName=someLooper.outputPlotFileName.replace(someLooper.name,parent)
        inFileList=""

        isFirstLooper=True
        for iLooper in parentDict[parent] :
            #add the root file to hadd command
            inFileList+=" "+looperList[iLooper].outputPlotFileName

            #read in the step data
            stepDataFileName=os.path.expanduser(looperList[iLooper].outputStepDataFileName)
            stepDataFile=open(stepDataFileName)
            stepDataList=cPickle.load(stepDataFile)
            stepDataFile.close()

            #add stats to those of someLooper
            for i in range(len(someLooper.steps)) :
                #need to zero in case sample is split but not run in multi mode
                if isFirstLooper :
                    someLooper.steps[i].nTotal=0
                    someLooper.steps[i].nPass =0
                    someLooper.steps[i].nFail =0
                someLooper.steps[i].nTotal+=stepDataList[i]["nTotal"]
                someLooper.steps[i].nPass +=stepDataList[i]["nPass" ]
                someLooper.steps[i].nFail +=stepDataList[i]["nFail" ]
            isFirstLooper=False

        looperPrint(parent,someLooper)
            
        cmd="hadd -f "+outputPlotFileName+inFileList+" | grep -v 'Source file' | grep -v 'Target path'"
        #print "hadding",outputPlotFileName,"..."
        os.system(cmd)
        print someLooper.hyphens
        
def loopOverSamples() :
        looperList=[]
        for sample in sampleSpecs :
            looperList.append(base.analysisLooper(sample,outputDir))

        if ("multi" in sys.argv) :
            from multiprocessing import Pool
            pool=Pool(processes=6)
            #pool=Pool(processes=len(looperList))
            pool.map(goFunc,looperList)
        else :
            map(goFunc,looperList)

        mergeSplitOutput(looperList)
        
#set up
globalSetup()
sampleSpecs=makeSampleSpecs(name)

#loop over samples and make TFiles containing histograms
if ("loop" in sys.argv and not "prof" in sys.argv) :
    loopOverSamples()

#profile the code
if ("prof" in sys.argv and not "multi" in sys.argv) :
    import cProfile
    cProfile.run("loopOverSamples()","resultProfile.out")

#make plots from the output histograms
if ("plot" in sys.argv) :
    import plotter
    plotter.plotAll(name,sampleSpecs,outputDir)

