#import sys
#sys.path.append('c:/dafapp/dplk/script_modules/')
#import moduleapi

import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

def FormEndSetData(uideflist, auiname, apobjconst):
  #moduleapi.CheckHistoriRestriction(uideflist, auiname, apobjconst)
  pass

def OnSetDataEx(uideflist, params):
  uideflist.SetData("uipRekeningDPLK", params.FirstRecord.key)