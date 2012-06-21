import sys

sys.path.append("c:/dafapp/dplk07/script_modules")
import moduleapi

def reserveNumber(config, params, returns):
  kode_cab = params.FirstRecord.GetFieldByName("cabang.branch_code")
  no_reserve = params.FirstRecord.reserve_count

  config.BeginTransaction()
  try:
    numRange = moduleapi.GetCounterNumber(config, 'NASABAHDPLK', kode_cab, no_reserve)
    no_peserta_awal  = '%s99%s' % (moduleapi.TruncateString(kode_cab, 3), moduleapi.MyZFill(str(numRange[0]), 6))
    no_peserta_akhir = '%s99%s' % (moduleapi.TruncateString(kode_cab, 3), moduleapi.MyZFill(str(numRange[1]), 6))
    returns.CreateValues(['no_awal', no_peserta_awal], ['no_akhir', no_peserta_akhir])
    config.Commit()
  except:
    config.Rollback()
    raise


