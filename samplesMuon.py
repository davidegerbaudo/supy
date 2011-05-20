import samples
from configuration import srm
muon = samples.SampleHolder()

#2011
muon.add("SingleMu.Run2011A-PR-v2.Robin1",'%s/rnandi/ICF/automated/2011_05_02_11_24_48/")'%srm, lumi = 999999.9)
muon.add("SingleMu.Run2011A-PR-v2.Robin2",'%s/rnandi/ICF/automated/2011_05_07_17_01_57/")'%srm, lumi = 999999.9)
muon.add("SingleMu.Run2011A-PR-v2.Alex",'%s/as1604/ICF/automated/2011_04_25_17_30_19/")'%srm, lumi = 999999.9)
muon.add("SingleMu.Run2011A-PR-v2.Burt",'%s/bbetchar/ICF/automated/2011_05_18_22_24_58/")'%srm, lumi = 999999.9)

#skims requiring one tight muon with pT>23 GeV
dir = "/vols/cms02/elaird1/29_skims/05_muons/1mu"
muon.add("SingleMu.Run2011A-PR-v2.Alex_1muskim",   'utils.fileListFromDisk(location = "%s/SingleMu.Run2011A-PR-v2.Alex.jsonWeight_*_skim.root", isDirectory = False)'%dir,
         lumi = 1.227000e+01)
muon.add("SingleMu.Run2011A-PR-v2.Robin1_1muskim", 'utils.fileListFromDisk(location = "%s/SingleMu.Run2011A-PR-v2.Robin1.jsonWeight_*_skim.root", isDirectory = False)'%dir,
         lumi = 8.731000e+01)
muon.add("SingleMu.Run2011A-PR-v2.Robin2_1muskim", 'utils.fileListFromDisk(location = "%s/SingleMu.Run2011A-PR-v2.Robin2.jsonWeight_*_skim.root", isDirectory = False)'%dir,
         lumi = 7.934000e+01)
muon.add("tt_tauola_mg_1muskim", 'utils.fileListFromDisk(location = "%s/tt_tauola_mg_*_skim.root", isDirectory = False)'%dir, xs = 1.527872e-01 * 1.575000e+02)
muon.add("w_jets_mg_1muskim", 'utils.fileListFromDisk(location = "%s/w_jets_mg_*_skim.root", isDirectory = False)'%dir, xs = 1.774398e-01 * 3.192400e+04)
muon.add("dyll_jets_mg_1muskim", 'utils.fileListFromDisk(location = "%s/dyll_jets_mg_*_skim.root", isDirectory = False)'%dir,xs = 2.536323e-01 * 3.048000e+03)

#skims of the above requiring the leading muon with pT>25 GeV and a second muon with pT>10 GeV, and not a third muon with pT>10 GeV and ID
dir = "/vols/cms02/elaird1/29_skims/05_muons/2mu"
muon.add("SingleMu.Run2011A-PR-v2.Alex_2muskim",   'utils.fileListFromDisk(location = "%s/SingleMu.Run2011A-PR-v2.Alex_1muskim.jsonWeight_*_skim.root", isDirectory = False)'%dir, lumi = 1.227000e+01)
muon.add("SingleMu.Run2011A-PR-v2.Robin1_2muskim", 'utils.fileListFromDisk(location = "%s/SingleMu.Run2011A-PR-v2.Robin1_1muskim.jsonWeight_*_skim.root", isDirectory = False)'%dir, lumi = 8.731000e+01)
muon.add("SingleMu.Run2011A-PR-v2.Robin2_2muskim", 'utils.fileListFromDisk(location = "%s/SingleMu.Run2011A-PR-v2.Robin2_1muskim.jsonWeight_*_skim.root", isDirectory = False)'%dir, lumi = 7.934000e+01)
muon.add("tt_tauola_mg_2muskim", 'utils.fileListFromDisk(location = "%s/tt_tauola_mg_1muskim_*_skim.root", isDirectory = False)'%dir, xs = 6.188606e-02 * 2.406398e+01)
muon.add("w_jets_mg_2muskim", 'utils.fileListFromDisk(location = "%s/w_jets_mg_1muskim_*_skim.root", isDirectory = False)'%dir, xs = 2.163140e-05 * 5.664588e+03)
muon.add("dyll_jets_mg_2muskim", 'utils.fileListFromDisk(location = "%s/dyll_jets_mg_1muskim_*_skim.root", isDirectory = False)'%dir, xs = 5.612258e-01 * 7.730713e+02)

muon.add("325_scaled_data", 'utils.fileListFromDisk(location = "/home/hep/elaird1/85_muonLook/07_displays/325_scaled_data.root", isDirectory = False)', lumi = 1.0)

########## 2010 #############
#38X SKIMS
muon.add("Mu.Run2010B_skim", 'utils.fileListFromDisk(location="/vols/cms02/bbetchar/01_skims/Mu.Run2010B-Nov4ReReco.RECO.Jad/")',lumi = 32.96)
muon.add("Mu.Run2010A_skim", 'utils.fileListFromDisk(location = "/vols/cms02/bbetchar/01_skims/Mu.Run2010A-Nov4ReReco.RECO.Jad/")',lumi = 3.18)

muon.add("Mu.Run2010_skim", 'utils.fileListFromDisk(location = "/vols/cms02/elaird1/11_skims/17_markus_mu_dataset/")', lumi = 14.511) #/pb
muon.add("Run2010_muonSkim", 'utils.fileListFromDisk(location = "/vols/cms02/elaird1/11_skims/10_markus_muons/*_skim.root", isDirectory = False)', lumi = 32) #/pb #fake number

#38X ORIGINALS
muon.add("Mu.Run2010A-Nov4ReReco.RECO.Jad", '%s/jad//ICF/automated/2010_12_17_14_44_28/")'%srm, lumi =  3.18)
muon.add("Mu.Run2010B-Nov4ReReco.RECO.Jad", '%s/jad//ICF/automated/2010_12_17_14_49_33/")'%srm, lumi = 32.96)
#
muon.add("Mu.Run2010A-Sep17ReReco_v2.RECO.Robin",             '%s/rnandi//ICF/automated/2010_10_13_14_30_58/")'%srm, lumi = 99999.9 )
muon.add("Mu.Run2010B-PromptReco-v2.RECO.Arlo1",              '%s/arlogb//ICF/automated/2010_10_13_14_09_24/")'%srm, lumi = 99999.9 )
muon.add("Mu.Run2010B-PromptReco-v2.RECO.Arlo2",              '%s/arlogb//ICF/automated/2010_10_24_16_41_15/")'%srm, lumi = 99999.9 )
muon.add("Mu.Run2010B-PromptReco-v2.RECO.Martyn",             '%s/mjarvis//ICF/automated/2010_10_22_16_11_58/")'%srm, lumi = 99999.9 )
