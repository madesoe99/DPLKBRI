import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def UpdateNasabahDPLK(config, oRegEditNasabahRekening):
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = oRegEditNasabahRekening.no_peserta
  oNasabahDPLK.nama_lengkap = oRegEditNasabahRekening.nama_lengkap
  oNasabahDPLK.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oRegEditNasabahRekening.tanggal_lahir)
  oNasabahDPLK.tempat_lahir = oRegEditNasabahRekening.tempat_lahir
  oNasabahDPLK.pekerjaan = oRegEditNasabahRekening.pekerjaan
  oNasabahDPLK.nama_perusahaan = oRegEditNasabahRekening.nama_perusahaan
  oNasabahDPLK.LJenisUsaha = oRegEditNasabahRekening.LJenisUsaha
  oNasabahDPLK.LKepemilikan = oRegEditNasabahRekening.LKepemilikan
  oNasabahDPLK.LDaerahAsal = oRegEditNasabahRekening.LDaerahAsal
  oNasabahDPLK.keterangan = oRegEditNasabahRekening.keterangan_nasabahdplk

  oNasabahDPLK.tgl_registrasi = moduleapi.DateTimeTupleToFloat(config, oRegEditNasabahRekening.tanggal_register)
  oNasabahDPLK.user_id = oRegEditNasabahRekening.user_id
  oNasabahDPLK.terminal_id = oRegEditNasabahRekening.terminal_id
  oNasabahDPLK.auth_user_id = config.SecurityContext.userid
  oNasabahDPLK.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oNasabahDPLK.last_update = config.ModDateTime.Now()
  oNasabahDPLK.isCommitted = 'T'
  oNasabahDPLK.operation_code = 'F'

  return oNasabahDPLK

def UpdateRekeningDPLK(config, oRegEditNasabahRekening):
  oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
  oRekeningDPLK.Key = oRegEditNasabahRekening.no_peserta
  oRekeningDPLK.sumber_dana = oRegEditNasabahRekening.sumber_dana
  oRekeningDPLK.keterangan = oRegEditNasabahRekening.keterangan_rekeningdplk

  if oRekeningDPLK.usia_pensiun <> oRegEditNasabahRekening.usia_pensiun:
    tgl_pensiun = moduleapi.AddYearToDateTuple(config, oRegEditNasabahRekening.tanggal_lahir, oRegEditNasabahRekening.usia_pensiun)
    tgl_pensiun_dipercepat = moduleapi.AddYearToDateTuple(config, oRegEditNasabahRekening.tanggal_lahir, oRegEditNasabahRekening.usia_pensiun - 10)
    oRekeningDPLK.tgl_pensiun = moduleapi.DateTimeTupleToFloat(config, tgl_pensiun)
    oRekeningDPLK.tgl_pensiun_dipercepat = moduleapi.DateTimeTupleToFloat(config, tgl_pensiun_dipercepat)

    oRekeningDPLK.usia_pensiun = oRegEditNasabahRekening.usia_pensiun

  return oRekeningDPLK

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegEditNasabahRekening = config.CreatePObjImplProxy('RegEditNasabahRekening')
  oRegEditNasabahRekening.Key = id

  config.BeginTransaction()
  try:
    UpdateNasabahDPLK(config, oRegEditNasabahRekening)
    UpdateRekeningDPLK(config, oRegEditNasabahRekening)

    oRegEditNasabahRekening.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

