import ROOT

f = ROOT.TFile.Open("data/output-PhS-g.root")
myTree = f.Get("tree")
for entry in myTree:
      print entry