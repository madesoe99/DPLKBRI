#import sys
#sys.path.append('c:/dafapp/dplk/script_modules/')
#import moduleapi

import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

#moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

def setDataEx(uideflist, params):
  uideflist.SetData('uipRekInvDPLK', params.FirstRecord.key)

def FormEndSetData(uideflist, auiname, apobjconst):
  pass
  #moduleapi.CheckHistoriRestriction(uideflist, auiname, apobjconst)

