import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

#sys.path.append('c:/dafapp/dplk/script_modules/')
#import moduleapi

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  rec = uideflist.uipNoData.ActiveRecord

  moduleapi.IsNasabahAvail(config, rec.GetFieldByName('LPeserta.no_peserta'))
  #moduleapi.CheckRegisterCIFUniq(config, rec.GetFieldByName('LPeserta.no_peserta'), 'U')

