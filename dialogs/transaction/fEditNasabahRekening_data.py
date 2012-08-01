import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  try:
    #checking status dplk peserta
    uiCalled = uideflist.GetPClassUIByName(auiname)
    if auiname == 'uipMaster':
      no_peserta = uiCalled.ActiveRecord.no_peserta
    else:
      no_peserta = uiCalled.ActiveRecord.GetFieldByName('LNasabahDPLK.no_peserta')      
    
    moduleapi.IsPesertaAktif(config, no_peserta)
    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    
    if uideflist.uipMaster.Dataset.RecordCount > 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'Z')
  except:
    raise

  uipRegisterCIF = uideflist.uipRegisterCIF

  if uipRegisterCIF.DataSet.RecordCount > 0:
    rec = uipRegisterCIF.DataSet.GetRecord(0)
  else:
    rec = uipRegisterCIF.DataSet.AddRecord()

  rec.user_id = config.SecurityContext.userid
  rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  rec.tanggal_register = config.Now()
  
  return 0

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode

  #if oData.no_referensi in ['', None]:
  #  raise Exception, 'Registrasi Error' + 'Nomor referensi tidak terdefinisi.'

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
