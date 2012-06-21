import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipNoData = uideflist.uipNoData

  rec = uipNoData.Dataset.AddRecord()
  now = config.Now()
  y, m, d = config.ModDateTime.DecodeDate(now)
  initTanggal = config.ModDateTime.EncodeDate(y, m, d)
  initTanggal_Next = moduleapi.GetNextDayDateTime(config, initTanggal)

  rec.dari_tanggal = initTanggal
  rec.hingga_tanggal = initTanggal
  rec.true_hingga_tanggal = initTanggal_Next

  return 0

