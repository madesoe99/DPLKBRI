import sys
sys.path.append('c:/dafapp/dplk07/script_modules/')
import moduleapi

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  rec = uideflist.uipNoData.ActiveRecord

  id_investasi = rec.GetFieldByName('LInvestasi.id_investasi')

  #moduleapi.IsInvestasiAvail(config, id_investasi)
  moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

