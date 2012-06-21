import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "moduleapi",
    "transaksiapi",
    "scripts#report.SlipTransaksiTeller",
    "scripts#transaksi.CekUserTimeZone"
  ]
)

#sys.path.append('c:/dafapp/dplk07/script_modules')
#sys.path.append('c:/dafapp/dplk07/scripts/report')
#sys.path.append('c:/dafapp/dplk07/scripts/transaksi')
#import moduleapi, transaksiapi, SlipTransaksiTeller, CekUserTimeZone

def FormOnSetDataEx(uideflist, params):
  config = uideflist.Config   
  
  #oRNR = config.AccessPObject(skey)
  #raise Exception, oRNR.no_peserta
  
  uideflist.SetData('uipRegisterNasabahRekening', params.FirstRecord.key)
  regNR = uideflist.uipRegisterNasabahRekening.Dataset.GetRecord(0)
  
  oUser = config.CreatePObjImplProxy('UserApp')
  oUser.Key = config.SecurityContext.GetUserInfo()[0]
  
  oBranch = config.CreatePObjImplProxy('BranchLocation')
  oBranch.Key = regNR.kode_cab_daftar
  if oBranch.IsNull:
    oBranch.Key = config.SecurityContext.GetUserInfo()[4]
  
  recDaftar = uideflist.uipIuranPendaftaran.Dataset.AddRecord()
  recDaftar.SetFieldByName('LBranchLocation.branch_code',oBranch.branch_code)
  recDaftar.SetFieldByName('LBranchLocation.BranchName',oBranch.BranchName)
  recDaftar.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  recDaftar.tgl_transaksi = config.Now()
  recDaftar.user_id = oUser.user_id
  recDaftar.isCommitted = 'F'
  
  #recIuran = uideflist.uipIuranPeserta.Dataset.AddRecord()
  #recIuran.mutasi_iuran_pk = regNR.iuran_pk
  #recIuran.mutasi_iuran_pst = regNR.iuran_pst
  
def saveBiayaDaftar(config, params, returns):
  returns.CreateValues(['success', False], ['message', ''])
  
  recPB = params.uipParameterBatch.GetRecord(0)
  recRNR = params.uipRegisterNasabahRekening.GetRecord(0)
  recIPD = params.uipIuranPendaftaran.GetRecord(0)
  #recIPS = params.uipIuranPeserta.GetRecord(0)
  
  config.BeginTransaction()
  try:
    oRNR = config.CreatePObjImplProxy("RegisterNasabahRekening"); oRNR.Key = recRNR.registernr_id    
    oIPD = config.CreatePObject("IuranPendaftaran")
    #oIPS = config.CreatePObject("IuranPeserta")
    
    ''' SET PROPERTIES IURAN PENDAFTARAN '''
    oIPD.besar_biaya_daftar = recIPD.besar_biaya_daftar
    oIPD.user_id = recIPD.user_id
    oIPD.TGL_TRANSAKSI = recIPD.tgl_transaksi
    #oIPD.TGL_OTORISASI
    oIPD.TGL_SISTEM = config.Now()
    #oIPD.USER_ID_AUTH
    oIPD.TERMINAL_ID = recIPD.terminal_id
    #oIPD.TERMINAL_ID_AUTH
    oIPD.KETERANGAN = recIPD.keterangan
    #oIPD.JENIS_TRANSAKSI
    oIPD.ISCOMMITTED = recIPD.isCommitted
    oIPD.BRANCH_CODE = recIPD.GetFieldByName('LBranchLocation.branch_code')
    #oIPD.REF_COREBANKING
    #oIPD.NO_REKENING = recRNR.no_rekening
    #oIPD.mutasi_iuran_pk
    #oIPD.mutasi_iuran_pst
    #oIPD.mutasi_iuran_tmb
    #oIPD.mutasi_psl
    #oIPD.mutasi_pmb_pk
    #oIPD.mutasi_pmb_pst
    #oIPD.mutasi_pmb_tmb
    #oIPD.mutasi_pmb_psl
    #oIPD.KODE_JENIS_TRANSAKSI
    #oIPD.ISPINDAHPAKET = 'F'
    #oIPD.COUNT_ADVIS
    #oIPD.saldo_yang_dibebani
    #oIPD.catatan
    #oIPD.idbghasil
    
    ''' SET LINK PROPERTY TO BAYAR DAFTAR DAN IURAN AWAL '''
    oRNR.LRegisterIuranPendaftaran = oIPD
    oRNR.status_biaya_daftar = 'T'
    #oRNR.LRegisterIuranPeserta = oIPS
    
    config.Commit()
    returns.FirstRecord.success = True
  except:
    config.Rollback()
    returns.FirstRecord.message = str(sys.exc_info()[1])

def downloadFile(config, parameter, returns):
  fileName = config.UserHomeDirectory + parameter.FirstRecord.fileName
  sw = returns.AddStreamWrapper()
  sw.LoadFromFile(fileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(fileName)

