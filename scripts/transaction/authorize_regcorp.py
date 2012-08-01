import sys, time
#sys.path.append('c:/dafapp/dplk/script_modules')

import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman 

modman.loadStdModules(globals(),
  [
    "moduleapi",
  ]
)

def CreateNasabahDPLKCorporate(config, oRegEditNasabahDPLKCorporate):
  if oRegEditNasabahDPLKCorporate.operation_code == 'N':
    oNasabahDPLKCorporate = config.CreatePObject('NasabahDPLKCorporate')
    oNasabahDPLKCorporate.kode_nasabah_corporate = oRegEditNasabahDPLKCorporate.kode_nasabah_corporate
  else:
    # edit
    oNasabahDPLKCorporate = config.CreatePObjImplProxy('NasabahDPLKCorporate')
    oNasabahDPLKCorporate.Key = oRegEditNasabahDPLKCorporate.kode_nasabah_corporate

    if oNasabahDPLKCorporate.kode_jenis_usaha <> oRegEditNasabahDPLKCorporate.kode_jenis_usaha:
      # update link jenisusaha di semua nasabah korporat yang terkait
      strSQL = \
        'update NasabahDPLK '\
        'set kode_jenis_usaha = \'%s\' '\
        'where kode_nasabah_corporate = \'%s\'' \
        % (oRegEditNasabahDPLKCorporate.kode_jenis_usaha, oNasabahDPLKCorporate.kode_nasabah_corporate)
      config.ExecSQL(strSQL)

    if oNasabahDPLKCorporate.kode_pemilikan <> oRegEditNasabahDPLKCorporate.kode_pemilikan:
      # update link jenisusaha di semua nasabah korporat yang terkait
      strSQL = \
        'update NasabahDPLK '\
        'set kode_pemilikan = \'%s\' '\
        'where kode_nasabah_corporate = \'%s\'' \
        % (oRegEditNasabahDPLKCorporate.kode_pemilikan, oNasabahDPLKCorporate.kode_nasabah_corporate)
      config.ExecSQL(strSQL)

  oNasabahDPLKCorporate.no_referensi = oRegEditNasabahDPLKCorporate.no_referensi
  oNasabahDPLKCorporate.nama_perusahaan = oRegEditNasabahDPLKCorporate.nama_perusahaan
  oNasabahDPLKCorporate.npwp = oRegEditNasabahDPLKCorporate.npwp
  oNasabahDPLKCorporate.no_perjanjian = oRegEditNasabahDPLKCorporate.no_perjanjian
  oNasabahDPLKCorporate.LJenisUsaha = oRegEditNasabahDPLKCorporate.LJenisUsaha
  oNasabahDPLKCorporate.LKepemilikan = oRegEditNasabahDPLKCorporate.LKepemilikan
  oNasabahDPLKCorporate.tgl_bayar_iuran = oRegEditNasabahDPLKCorporate.tgl_bayar_iuran
  oNasabahDPLKCorporate.biaya_daftar_anggota = oRegEditNasabahDPLKCorporate.biaya_daftar_anggota
  oNasabahDPLKCorporate.alamat_kantor_jalan = oRegEditNasabahDPLKCorporate.alamat_kantor_jalan
  oNasabahDPLKCorporate.alamat_kantor_kelurahan = oRegEditNasabahDPLKCorporate.alamat_kantor_kelurahan
  oNasabahDPLKCorporate.alamat_kantor_kecamatan = oRegEditNasabahDPLKCorporate.alamat_kantor_kecamatan
  #oNasabahDPLKCorporate.alamat_kantor_kota = oRegEditNasabahDPLKCorporate.alamat_kantor_kota
  #oNasabahDPLKCorporate.alamat_kantor_propinsi = oRegEditNasabahDPLKCorporate.alamat_kantor_propinsi
  #oNasabahDPLKCorporate.alamat_kantor_kode_pos = oRegEditNasabahDPLKCorporate.alamat_kantor_kode_pos
  oNasabahDPLKCorporate.LAKPropinsi = oRegEditNasabahDPLKCorporate.LAKPropinsi
  oNasabahDPLKCorporate.LAKKota = oRegEditNasabahDPLKCorporate.LAKKota
  oNasabahDPLKCorporate.LAKKecamatan = oRegEditNasabahDPLKCorporate.LAKKecamatan
  oNasabahDPLKCorporate.LAKKodePos = oRegEditNasabahDPLKCorporate.LAKKodePos
  oNasabahDPLKCorporate.alamat_kantor_telepon = oRegEditNasabahDPLKCorporate.alamat_kantor_telepon
  oNasabahDPLKCorporate.alamat_kantor_telepon2 = oRegEditNasabahDPLKCorporate.alamat_kantor_telepon2
  oNasabahDPLKCorporate.alamat_kantor_fax = oRegEditNasabahDPLKCorporate.alamat_kantor_fax
  oNasabahDPLKCorporate.keterangan = oRegEditNasabahDPLKCorporate.keterangan
  oNasabahDPLKCorporate.keterangan1 = oRegEditNasabahDPLKCorporate.keterangan1
  oNasabahDPLKCorporate.keterangan2 = oRegEditNasabahDPLKCorporate.keterangan2
  oNasabahDPLKCorporate.keterangan3 = oRegEditNasabahDPLKCorporate.keterangan3
  oNasabahDPLKCorporate.keterangan4 = oRegEditNasabahDPLKCorporate.keterangan4
  oNasabahDPLKCorporate.tgl_bergabung =  moduleapi.DateTimeTupleToFloat(config, oRegEditNasabahDPLKCorporate.tgl_bergabung)
  oNasabahDPLKCorporate.tanggal_register =  moduleapi.DateTimeTupleToFloat(config, oRegEditNasabahDPLKCorporate.tanggal_register)
  oNasabahDPLKCorporate.kode_holding = oRegEditNasabahDPLKCorporate.kode_holding 
  oNasabahDPLKCorporate.kode_negara = oRegEditNasabahDPLKCorporate.kode_negara 
  oNasabahDPLKCorporate.user_id = oRegEditNasabahDPLKCorporate.user_id
  oNasabahDPLKCorporate.terminal_id = oRegEditNasabahDPLKCorporate.terminal_id
  oNasabahDPLKCorporate.auth_user_id = config.SecurityContext.userid
  oNasabahDPLKCorporate.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oNasabahDPLKCorporate.last_update = config.ModDateTime.Now()
  oNasabahDPLKCorporate.isCommitted = 'T'
  oNasabahDPLKCorporate.operation_code = 'F'
  oNasabahDPLKCorporate.REFR_ACCNO = oRegEditNasabahDPLKCorporate.REFR_ACCNO
  oNasabahDPLKCorporate.REFR_NAMA = oRegEditNasabahDPLKCorporate.REFR_NAMA
  oNasabahDPLKCorporate.REFR_UKER = oRegEditNasabahDPLKCorporate.REFR_UKER
  oNasabahDPLKCorporate.BENEFICIAL_OWNER = oRegEditNasabahDPLKCorporate.BENEFICIAL_OWNER

  if oRegEditNasabahDPLKCorporate.operation_code == 'N':
    sSQL = """SELECT *
      FROM   MASTERPARAMETER
      WHERE  PARAM_TYPE = 'C'
      ORDER BY KEY_PARAMETER ASC
      """
        
    rSQL = config.CreateSQL(sSQL).RawResult
    while not rSQL.Eof:
      oNCParams = config.CreatePObject('NASABAHCORPPARAMS')
      oNCParams.LNasabahDPLKCorporate = oNasabahDPLKCorporate
      oNCParams.KEY_PARAMETER = rSQL.KEY_PARAMETER
      oNCParams.NUMERIC_VALUE = rSQL.NUMERIC_VALUE
      oNCParams.VARCHAR_VALUE = rSQL.VARCHAR_VALUE
      oNCParams.DESCRIPTION = rSQL.DESCRIPTION
      rSQL.Next()

  return oNasabahDPLKCorporate

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegEditNasabahDPLKCorporate = config.CreatePObjImplProxy('RegEditNasabahDPLKCorporate')
  oRegEditNasabahDPLKCorporate.Key = id

  config.BeginTransaction()
  try:
    CreateNasabahDPLKCorporate(config, oRegEditNasabahDPLKCorporate)
    oRegEditNasabahDPLKCorporate.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise


  return 1