import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

def uipRegisterNasabahOnSetData(sender):
  ## sender is TPClassUIDef
  config = sender.UIDefList.Config
  #import rpdb2; rpdb2.start_embedded_debugger('solusi', True, True)
  if sender.ActiveInstance.LNasabahDPLKCorporate.IsNull:
    sender.ActiveRecord.nasabah_korporat = 0
  else:
    sender.ActiveRecord.nasabah_korporat = 1
  
def OnSetDataEx(uideflist, params):
  config = uideflist.Config   
  uideflist.SetData('uipRegisterNasabahRekening', params.FirstRecord.key)
  rec = uideflist.uipRegisterNasabahRekening.Dataset.GetRecord(0)
    
  oUser = config.CreatePObjImplProxy('UserApp')
  oUser.Key = config.SecurityContext.GetUserInfo()[0]
  rec.nolimitlocation = oUser.NoLimitLocation

  oBranch = config.CreatePObjImplProxy('BranchLocation')
  oBranch.Key = rec.kode_cab_daftar
  if oBranch.IsNull:
    oBranch.Key = config.SecurityContext.GetUserInfo()[4]
  rec.SetFieldByName('LBranchLocation.branch_code',oBranch.branch_code)
  rec.SetFieldByName('LBranchLocation.BranchName',oBranch.BranchName)

  #set parameter
  recP = uideflist.uipParameter.Dataset.AddRecord()
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'MIN_JML_IURAN_PST'
  recP.MIN_JML_IURAN_PST = oP.Numeric_Value

  oP.Key = 'MIN_JML_IURAN_PK'
  recP.MIN_JML_IURAN_PK = oP.Numeric_Value

  oP.Key = 'MIN_JML_IURAN_TMB'
  recP.MIN_JML_IURAN_TMB = oP.Numeric_Value

  oP.Key = 'IS_ONLY_MIN_JML_IURAN_PST'
  recP.IS_ONLY_MIN_JML_IURAN_PST = int(oP.Numeric_Value)

  oP.Key = 'MIN_SELISIH_TGL_DAFTAR-PENSIUN'
  recP.MIN_SELISIH_TGL_DAFTAR_PENSIUN = oP.Numeric_Value

  sSQL = "SELECT * FROM paketinvestasi"
  rSQL = config.CreateSQL(sSQL).RawResult
  while not rSQL.Eof:
    recTmpPI = uideflist.uipTmpPaket.Dataset.AddRecord()
    recTmpPI.kode_pi = rSQL.kode_paket_investasi
    recTmpPI.nama_pi = rSQL.nama_paket_investasi
    rSQL.Next()
    
def uipRegisterNasabahRekeningApplyRow(sender, oData):
  config = sender.UIDefList.Config
  rec = sender.ActiveRecord

  #if rec.no_referensi in ['', None]:
  #  raise BaseException, '\n\nPERINGATAN\nNomor Referensi belum terdefinisi! Mohon isi dahulu.'

  if rec.jenis_kelamin in ['', None]:
    raise BaseException, '\n\nPERINGATAN\nJenis Kelamin belum terdefinisi! Mohon isi dahulu.'

  if rec.usia_pensiun in [None,''] or \
    (rec.usia_pensiun < 45 or rec.usia_pensiun > 65):
    raise BaseException, '\n\nPERINGATAN\nUsia Pensiun tidak valid! Usia Pensiun yang diperbolehkan antara 45 - 65 tahun.'

  #cek usia sekarang peserta dan keikutsertaan asuransi
  y,m,d = time.localtime()[:3]
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  JumlahHariSetahun = oParameter.Numeric_Value
  usiaPeserta = (config.ModDateTime.EncodeDate(y,m,d) - rec.tanggal_lahir) /JumlahHariSetahun
  if rec.ikut_asuransi == 'T' and usiaPeserta > 55.0:
    raise BaseException, '\n\nPERINGATAN\nStatus Ikut Asuransi tidak valid! Usia peserta Ikut '\
      'Asuransi hanya diperbolehkan dibawah usia 55 tahun.'

  if rec.nasabah_korporat:
    if oData.LNasabahDPLKCorporate.IsNull:
      raise BaseException, '\n\nPERINGATAN\nData Perusahaan belum terdefinisi! Mohon isi dahulu.'

  #oData.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oData.kode_cab_daftar = rec.GetFieldByName('LBranchLocation.branch_code')

def cekPeserta(config, params, results):
  params = params.FirstRecord
  status = results.CreateValues(
    ['success', False],
    ['message', ''],
    ['no_peserta', ''],
    ['registernr_id', 0],
    ['is_otor', False]
  )
  
  #y,m,d = params.tanggal_lahir[:3]
  #tanggal_lahir = config.ModDateTime.EncodeDate(y,m,d)
  tanggal_lahir = config.FormatDateTimeForQuery(params.tanggal_lahir)
  
  sSQL = """
    SELECT * FROM NasabahDPLK 
    WHERE  ibu_kandung = '%s'
           AND nama_lengkap = '%s'
           AND tanggal_lahir =  %s
    """ % (params.ibu_kandung, params.nama_lengkap, tanggal_lahir)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  if not rSQL.Eof:
    status.success = True
    status.is_otor = True
    status.no_peserta = rSQL.no_peserta
  else:
    sSQL = """
      SELECT * FROM REGISTERNASABAHREKENING 
      WHERE  ibu_kandung = '%s'
             AND nama_lengkap = '%s'
             AND tanggal_lahir =  %s
      """ % (params.ibu_kandung, params.nama_lengkap, tanggal_lahir)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    if not rSQL.Eof:
      status.success = True
      status.is_otor = False
      status.registernr_id = rSQL.registernr_id
      status.no_peserta = rSQL.no_peserta
    else:
      status.message = "Peserta belum terdaftar di data kepesertaan DPLK"

