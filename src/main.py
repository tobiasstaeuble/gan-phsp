import numpy as np
import torch
import torch.nn as nn
import gaga
import gatetools.phsp as phsp
import gatetools as gt
from torch._C import * # this fails

def infoPHSP(file):
  return None
  #gt_phsp_info(file)


def loadPHSP(file):
  return None
  #gaga.load(file, False, True)


#infoPHSP('data/VarianTrueBeam6MV_01.')
#gt.print_gate_info(True)
#gt.gt_phsp_info('data/Varian_TrueBeam6MV_01.IAEAphsp')