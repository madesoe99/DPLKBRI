import sys
sys.path.append('c:/dafapp/dplk07/script_modules/')
import moduleapi

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  rec = uideflist.uipNoData.ActiveRecord

  moduleapi.IsNasabahAvail(config, rec.GetFieldByName('LPeserta.no_peserta'))
  moduleapi.CheckRegisterCIFUniq(config, rec.GetFieldByName('LPeserta.no_peserta'), \
    rec.GetFieldByName('LJenisRegisterCIF.kode_jenis_registercif'))

