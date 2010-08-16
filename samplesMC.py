import samples

mc = samples.SampleHolder()
srm = 'utils.fileListFromSrmLs(location="/pnfs/hep.ph.ic.ac.uk/data/cms/store/user'

#PY QCD
mc.add("qcd_py_pt30",  '%s/gouskos//ICF/automated/2010_06_24_18_09_51/")'%srm, xs = 6.041e+07, ptHatMin =   30 )
mc.add("qcd_py_pt80",  '%s/gouskos//ICF/automated/2010_07_06_00_55_17/")'%srm, xs = 9.238e+05, ptHatMin =   80 )
mc.add("qcd_py_pt170", '%s/gouskos//ICF/automated/2010_07_06_01_33_23/")'%srm, xs = 2.547e+04, ptHatMin =  170 )
mc.add("qcd_py_pt300", '%s/gouskos//ICF/automated/2010_07_09_19_13_09/")'%srm, xs = 1.256e+03, ptHatMin =  300 )
mc.add("qcd_py_pt470", '%s/gouskos//ICF/automated/2010_07_10_04_22_06/")'%srm, xs = 8.798e+01, ptHatMin =  470 )
mc.add("qcd_py_pt800", '%s/gouskos//ICF/automated/2010_07_10_04_37_56/")'%srm, xs = 2.186e+00, ptHatMin =  800 )
mc.add("qcd_py_pt1400",'%s/gouskos//ICF/automated/2010_07_10_04_47_48/")'%srm, xs = 1.122e-02, ptHatMin = 1400 )
mc.adjustOverlappingSamples( ["qcd_py_pt%d"%i for i in [30,80,170,300,470,800,1400] ] )

#MG QCD
#mc.add("qcd_mg_ht_50_100",  '%s/as1604//ICF/automated/2010_08_15_23_34_33//QCD_Pt-50To100_7TeV-madgraph.Spring10-START3X_V26-v1.GEN-SIM-RECO/")'%srm, xs = None)
#mc.add("qcd_mg_ht_100_250", '%s/as1604//ICF/automated/2010_08_15_23_34_33//QCD_Pt100to250-madgraph.Spring10-START3X_V26_S09-v2.GEN-SIM-RECO/ ")'%srm, xs = None)
#mc.add("qcd_mg_ht_250_500", '%s/as1604//ICF/automated/2010_08_15_23_34_33//QCD_Pt250to500-madgraph.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/ ")'%srm, xs = None)
#mc.add("qcd_mg_ht_500_1000",'%s/as1604//ICF/automated/2010_08_15_23_34_33//QCD_Pt500to1000-madgraph.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/")'%srm, xs = None)
#mc.add("qcd_mg_ht_1000_inf",'%s/as1604//ICF/automated/2010_08_15_23_34_33//QCD_Pt1000toInf-madgraph.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/")'%srm, xs = None)
mc.add("qcd_mg_ht_250_500_old",'%s/as1604//ICF/automated/2010_07_27_14_33_00//QCD_Pt250to500-madgraph.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/")'%srm, xs = 171e+03 )

#MG GAMMA + JETS
mc.add("gammajets_mg_pt40_100", '%s/arlogb//ICF/automated/2010_07_26_15_14_40//PhotonJets_Pt40to100-madgraph.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/")'%srm, xs = 23620 )
mc.add("gammajets_mg_pt100_200",'%s/arlogb/ICF/automated/2010_07_26_15_14_40/PhotonJets_Pt100to200-madgraph.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/")'%srm,  xs = 3476 )
mc.add("gammajets_mg_pt200",    '%s/arlogb/ICF/automated/2010_07_26_15_14_40/PhotonJets_Pt200toInf-madgraph.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/")'%srm,  xs = 485 )
            
#MG TT/EWK
mc.add("tt_tauola_mg",'utils.getCommandOutput2("ls /vols/cms01/mstoye/ttTauola_madgraph_V11tag/SusyCAF_Tree*.root | grep -v 4_2").split("\\n")', xs = 95.0 )
mc.add("z_inv_mg",'%s/zph04/ICF/automated/2010_07_14_11_52_58/",itemsToSkip=["14_3.root"])'%srm, xs = 4500.0 )
mc.add("z_jets_mg",'%s/jad/ICF/automated//2010_07_05_22_43_20/", pruneList=False)'%srm, xs = 2400.0 )
mc.add("w_jets_mg",'%s/jad/ICF/automated//2010_06_18_22_33_23/")'%srm, xs = 24170.0 )

#SUSY
mc.add("lm0",'%s/bainbrid/ICF/automated/2010_07_16_12_54_00/LM0.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/")'%srm, xs = 38.93 )
mc.add("lm1",'%s/bainbrid/ICF/automated/2010_07_12_17_52_54/LM1.Spring10-START3X_V26_S09-v1.GEN-SIM-RECO/")'%srm, xs = 4.888 )

#MG EWK SKIMS
mc.add("z_inv_mg_skim", 'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/z_inv_mg/")', xs = 50.2 )
mc.add("z_jets_mg_skim", 'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/z_jets_mg/")', xs = 55.4 )
mc.add("w_jets_mg_skim", 'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/w_jets_mg/")', xs = 332.4 )

#PY QCD SKIMS
mc.add("qcd_py_pt80_skim", 'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/qcd_high_alphaT/pt80/")',  xs = 0.894,    ptHatMin =  80 )
mc.add("qcd_py_pt170_skim",'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/qcd_high_alphaT/pt170/")', xs = 0.377,    ptHatMin = 170 )
mc.add("qcd_py_pt300_skim",'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/qcd_high_alphaT/pt300/")', xs = 0.0409,   ptHatMin = 300 )
mc.add("qcd_py_pt470_skim",'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/qcd_high_alphaT/pt470/")', xs = 0.002362, ptHatMin = 470 )
mc.adjustOverlappingSamples( ["qcd_py_pt80_skim",
                              "qcd_py_pt170_skim",
                              "qcd_py_pt300_skim",
                              "qcd_py_pt470_skim"] )

#PY QCD SKIMS2
mc.add("qcd_py_pt30_skim2", 'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/alphaT.gt.0.525/pt30/")', xs = 12.56, ptHatMin = 30 )
mc.add("qcd_py_pt80_skim2", 'utils.fileListFromDisk(location="/vols/cms02/elaird1/06_skims/alphaT.gt.0.525/pt80/")', xs = 4.9,   ptHatMin = 80 )
mc.adjustOverlappingSamples( ["qcd_py_pt30_skim2",
                              "qcd_py_pt80_skim2"] )
