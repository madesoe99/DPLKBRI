#import sys
#sys.path.append('c:/dafapp/dplk/script_modules/')
#import moduleapi

import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

def setDataEx(uideflist, params):
  uideflist.SetData('uipNasabahDPLK', params.FirstRecord.key)
  
def FormEndSetData(uideflist, auiname, apobjconst):
  moduleapi.CheckHistoriRestriction(uideflist, auiname, apobjconst)

