#!/usr/bin/env python
import os,sys,copy,cPickle,collections,tempfile
import utils,steps,samples,configuration,calculables,organizer,wrappedChain
from analysisLooper import analysisLooper
import ROOT as r
#####################################
class analysis(object) :
    """base class for an analysis

    Methods before __init__ can be overridden in inheriting class.
    """

    def listOfSteps(self,config) :       raise Exception("NotImplemented", "Implement a member function %s"%"listOfSteps(self,config)")
    def listOfCalculables(self,config) : raise Exception("NotImplemented", "Implement a member function %s"%"listOfCalculables(self,config)")
    def listOfSampleDictionaries(self) : raise Exception("NotImplemented", "Implement a member function %s"%"sampleDict(self)")
    def listOfSamples(self,config) :     raise Exception("NotImplemented", "Implement a member function %s"%"listOfSamples(self,config)")

    def mainTree(self) : return ("susyTree","tree")
    def otherTreesToKeepWhenSkimming(self) : return [("lumiTree","tree")]
    def leavesToBlackList(self) : return []
    def parameters(self) : return {}
    def conclude(self, org) : return
    def concludeAll(self) :
        for conf in self.configurations :
            self.conclude( organizer.organizer( conf['tag'], self.sampleSpecs(conf['tag'])))

############
    def __init__(self, options) :
        self.__batch   = options.batch
        self.__loop    = int(options.loop)   if options.loop!=None else None
        self.__nSlices = int(options.slices) if options.slices!=None else 1
        self.__profile = options.profile
        self.__jobId   = options.jobId
        self.__site    = options.site if options.site!=None else configuration.sitePrefix()

        self.localStem  = "%s/%s"%(configuration.siteInfo(site = self.__site, key = "localOutputDir" ), self.name)
        self.globalStem = "%s/%s"%(configuration.siteInfo(site = self.__site, key = "globalOutputDir"), self.name)
    
        self.sampleDict = samples.SampleHolder()
        map(self.sampleDict.update,self.listOfSampleDictionaries())

        if self.__loop!=None :
            os.system("mkdir -p %s"%self.localStem)
            if self.__jobId==None :
                os.system("mkdir -p %s"%self.globalStem)
                self.makeInputFileLists()

        self.__listsOfLoopers = []
        self.__jobs = []
        for iConf,conf in enumerate(self.configurations) :
            self.__listsOfLoopers.append( self.sampleLoopers(conf) )
            for iSample in range(len(self.__listsOfLoopers[-1])) :
                for iSlice in range(self.__nSlices) :
                    self.__jobs.append({"iConfig":iConf,"iSample":iSample,"iSlice":iSlice})

        if self.__jobId==None and self.__loop!=None : utils.writePickle( self.jobsFile, (self.__loop,self.jobs) )

############
    @property
    def name(self) : return self.__class__.__name__
    @property
    def jobs(self) : return self.__jobs
    @property
    def jobsFile(self) : return "%s/%s.jobs"%(self.globalStem, self.name)
    @property
    def configurations(self) :
        if not hasattr(self,"_analysis__configs") :
            parameters = self.parameters()
            assert "tag" not in parameters
            self.__configs = [ dict( [("tag",[])] + [(key,val) for key,val in parameters.iteritems() if type(val)!=dict] ) ]
            for param,variations in parameters.iteritems() :
                if type(variations) is dict :
                    self.__configs = sum([[ dict( list(conf.iteritems()) + [ (param,val), ("tag",conf["tag"]+[str(key)]) ] )
                                            for key,val in variations.iteritems()] for conf in self.__configs],[])
            for conf in self.__configs : conf['tag'] = '_'.join(conf['tag'])
        return self.__configs
        
############
    def psFileName(self,tag = "") : return "%s/%s%s.ps"%(self.globalStem, self.name, "_"+tag if len(tag) else "")

    def sampleSpecs(self, tag = "") :
        iConf = [conf["tag"] for conf in self.configurations].index(tag)
        confSamples = self.listOfSamples(self.configurations[iConf])
        def sampleSpecDict(looper) :
            looper.setupSteps(minimal = True)
            sampleSpec = next( s for s in confSamples if s.weightedName == looper.name ) 
            return {"name":looper.name, "outputFileName":looper.steps[0].outputFileName,
                    "color":sampleSpec.color, "markerStyle":sampleSpec.markerStyle }
        return [ sampleSpecDict(looper) for looper in self.__listsOfLoopers[iConf]]
    
############
    def inputFilesListFile(self, sampleName) : return "%s/%s.inputFiles"%(self.globalStem, sampleName)

    def globalToLocal(self, globalFileName) :
        tmpDir = tempfile.mkdtemp(dir = self.localStem)
        localFileName = globalFileName.replace(self.globalStem, tmpDir)
        return tmpDir,localFileName,globalFileName

    def localToGlobal(self, tmpDir, localFileName, globalFileName) :
        os.system(configuration.mvCommand(site = self.__site, src = localFileName, dest = globalFileName))
        os.system("rm -r %s"%tmpDir)

    def makeInputFileLists(self) :
        def inputFilesEvalWorker(q):
            while True:
                sampleName,command = q.get()
                if not (os.path.exists(self.inputFilesListFile(sampleName)) and configuration.useCachedFileLists()) :
                    fileNames = eval(command)
                    assert fileNames, "The command '%s' produced an empty list of files"%command
                    tmpDir,localFileName,globalFileName = self.globalToLocal(self.inputFilesListFile(sampleName))
                    utils.writePickle(localFileName, fileNames)
                    self.localToGlobal(tmpDir, localFileName, globalFileName)
                q.task_done()

        sampleNames = set(sum([[sampleSpec.name for sampleSpec in self.listOfSamples(conf)] for conf in self.configurations],[]))
        argsList = [(name, self.sampleDict[name].filesCommand) for name in sampleNames]
        utils.operateOnListUsingQueue(self.__loop,inputFilesEvalWorker,argsList)

############
    def loop(self) :
        listOfLoopers = [ self.__listsOfLoopers[job["iConfig"]][job["iSample"]].slice(job["iSlice"], self.__nSlices)
                          for iJob,job in enumerate(self.jobs) if self.__jobId==None or int(self.__jobId)==iJob ]

        if self.__jobId!=None : listOfLoopers[0].go()
        elif not self.__profile : utils.operateOnListUsingQueue(self.__loop, utils.goWorker, listOfLoopers)
        else :
            import cProfile
            self.listOfLoopersForProf = listOfLoopers
            cProfile.run("someInstance.goLoop()","resultProfile.out")

    def goLoop(self) : [ looper.go() for looper in self.listOfLoopersForProf ]
        
############
    def sampleLoopers(self, conf) :

        def parseForNumberEvents(spec,tup,nFiles,nSlices) :
            if not spec.effectiveLumi : return (spec.nEventsMax,nFiles)
            if spec.nEventsMax>=0: print "Warning: %s nEventsMax ignored in favor of effectiveLumi."%spec.weightedName
            assert not tup.lumi, "Cannot calculate effectiveLumi for _data_ sample %s"%spec.weightedName
            nJobs = min(nFiles, nSlices)
            nEventsTotal = spec.effectiveLumi * tup.xs
            if nEventsTotal < nJobs : return (1,int(nEventsTotal+0.9))
            return (1+int(nEventsTotal/nJobs), nFiles)

        def lumiWarn(isData, nEventsMax, nFilesMax) :
            invalid = isData and (nEventsMax>=0 or nFilesMax>=0)
            if invalid : print "Warning: Not running over full data sample: wrong lumi?"
            return invalid

        def allCalculables(calcs,weights,adjustedSteps) :
            secondaries = [ s for s in adjustedSteps if issubclass(type(s),wrappedChain.wrappedChain.calculable) ]
            weightsAlready = [next(c for c in secondaries+calcs if c.name==w) for w in weights if type(w)==str ]
            weightsAdditional = [ w for w in weights if type(w)!=str ]
            def check(As,Bs) :
                intersect = set([a.name for a in As]).intersection(set([b.name for b in Bs]))
                assert not intersect, "Warning: { %s } are already listed in listOfCalculables."%','.join(intersect)
            check(calcs,weightsAdditional)
            check(calcs,secondaries)
            check(weightsAdditional,secondaries)
            return calcs + [calculables.weight(weightsAdditional+weightsAlready)] + weightsAdditional + secondaries

        def looper(spec) :
            assert spec.weightedName not in sampleNames,"Duplicate sample name %s is not allowed."%spec.weightedName ; sampleNames.add(spec.weightedName)
            pars = dict( list(conf.iteritems()) + [("baseSample",spec.name), ("sample",spec.weightedName) ] )
            tup = self.sampleDict[spec.name]
            inputFiles = utils.readPickle(self.inputFilesListFile(spec.name))[:spec.nFilesMax]
            nEventsMax,nFilesMax = parseForNumberEvents(spec, tup, len(inputFiles), self.__nSlices)
            inputFiles = inputFiles[:nFilesMax]

            adjustedSteps = [ steps.Master.Master(xs = tup.xs, xsPostWeights = spec.xsPostWeights,
                                                  lumi = spec.overrideLumi if spec.overrideLumi!=None else tup.lumi,
                                                  lumiWarn = lumiWarn(tup.lumi, nEventsMax, spec.nFilesMax) )
                              ] + steps.adjustSteps(self.listOfSteps(pars), "Data" if tup.lumi else "Mc")

            return analysisLooper( mainTree = self.mainTree(),   otherTreesToKeepWhenSkimming = self.otherTreesToKeepWhenSkimming(),
                                   nEventsMax = nEventsMax,      leavesToBlackList = self.leavesToBlackList(),
                                   steps = adjustedSteps,        calculables = allCalculables( self.listOfCalculables(pars), spec.weights, adjustedSteps ),
                                   inputFiles = inputFiles,      name = pars["sample"],
                                   localStem  = self.localStem,  subDir = "%(tag)s"%conf,
                                   globalStem = self.globalStem, quietMode = self.__loop>1 )
        sampleNames = set()
        return [ looper(sampleSpec) for sampleSpec in self.listOfSamples(conf) ]
    
############
    def mergeOutput(self) :
        if not os.path.exists(self.jobsFile) : return

        def mergeWorker(q):
            while True:
                looper,slices = q.get()
                looper.mergeFunc(slices)
                q.task_done()

        nCores,jobs = utils.readPickle(self.jobsFile)
        mergeDict = collections.defaultdict(list)
        for job in jobs : mergeDict[(job['iConfig'],job['iSample'])].append(job['iSlice'])
        workList = [ (self.__listsOfLoopers[key[0]][key[1]], val) for key,val in mergeDict.iteritems() ]

        if not all([looper.readyMerge(slices) for looper,slices in workList]) : sys.exit(0)
        utils.operateOnListUsingQueue(nCores, mergeWorker, workList)
        os.remove(self.jobsFile)
