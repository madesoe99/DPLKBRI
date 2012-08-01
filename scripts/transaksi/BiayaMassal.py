import sys
import com.ihsan.util.modman as modman

kelas = {'1':'BiayaAdmTahunan','2':'BiayaPengelolaanDana'}

def CreateBiaya(config, code, nominalBiaya, pst, tglhitung):
  classJenisBiaya = kelas[code]
  user_id     = config.SecurityContext.UserID
  terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oBiaya = config.CreatePObject(classJenisBiaya)

  #field TransaksiDPLK
  #field TransaksiRekInvDPLK
  oBiaya.no_rekening = pst.no_rekening
  oBiaya.branch_code = pst.kode_cab_daftar
  oBiaya.keterangan = '%s peserta %s' % \
    (classJenisBiaya, pst.no_peserta)
  
  oBiaya.isCommitted     = 'T'
  oBiaya.user_id         = user_id
  oBiaya.user_id_auth    = user_id
  oBiaya.terminal_id     = terminal_id
  oBiaya.terminal_id_auth= terminal_id
  oBiaya.tgl_transaksi   = int(tglhitung)
  oBiaya.tgl_sistem      = oBiaya.tgl_otorisasi = config.ModLibUtils.Now()

  #do charge biaya
  moduleAPI = modman.getModule(config, 'moduleapi')
  moduleAPI.ProsesChargeBiaya(config, oBiaya, nominalBiaya)
  
def getPeserta(config):
  dSQL = "SELECT a.*,b.KODE_NASABAH_CORPORATE KNC FROM REKINVDPLK a, NASABAHDPLK b WHERE STATUS_DPLK='A' and a.NO_PESERTA=b.NO_PESERTA"
  pst = config.CreateSQL(dSQL).RawResult
  
  return pst
  

def NBTC(config,transaksiAPI,kode_korporat):
  #pakai parameter korporat
  listParameterKey =[]
  dictParameterKorporat = transaksiAPI.GetParameterCorporate(config, kode_korporat, listParameterKey)
  
  nominal = dictParameterKorporat['BIAYA_ADM_TAHUNAN'][1]
  PBP = dictParameterKorporat['PERSEN_BIAYA_PENGELOLAAN'][1]
  
  return nominal, PBP 
  
def HitungNominalPengelolaan(config,pst,PBP,transaksiAPI,tglhitung):
  proporsiHari = transaksiAPI.HitungProporsiHariSebulan(config, tglhitung)
  akum_pmb = pst.akum_pmb_pk + pst.akum_pmb_pst + pst.akum_pmb_tmb + pst.akum_pmb_psl    
  saldo_jml_dana = akum_pmb + \
    pst.akum_iuran_pk + \
    pst.akum_iuran_pst + \
    pst.akum_iuran_tmb + \
    pst.akum_psl
  nilai = proporsiHari * (PBP / 100 / 12) * saldo_jml_dana
  #raise BaseException, nilai
  return nilai

def DAFScriptMain(config, params, returns):
  status = returns.CreateValues(
     ['IsErr',0],
     ['ErrMessage',''],
  )
  transaksiAPI = modman.getModule(config, 'transaksiapi')  
  par = params.FirstRecord
  code = str(par.code)
  tglhitung = par.tglhitung
  # biaya ADM default
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'BIAYA_ADM_TAHUNAN'
  AdmTahunan = oParameter.Numeric_Value /12

  oParameter.Key = 'PERSEN_BIAYA_PENGELOLAAN'
  Par_PBP = oParameter.Numeric_Value

  config.BeginTransaction()
  try:
    pst = getPeserta(config)
    while not pst.Eof :
      if pst.KNC not in (None,''):
        Nilai = NBTC(config,transaksiAPI,pst.KNC)
        BiayaADM = Nilai[0] / 12
        PersenPD = Nilai[1] 
      else :
        BiayaADM = AdmTahunan
        PersenPD = Par_PBP
      if code == '1':
        nominal = BiayaADM
      elif code =='2':
        PBP = PersenPD
        nominal = HitungNominalPengelolaan(config,pst,PBP,transaksiAPI,tglhitung)
      #raise Exception,nominal
      # Buat transaksi biaya    
      CreateBiaya(config, code, nominal, pst, tglhitung)
      pst.Next()
    #raise Exception, 'as'    
      
    config.Commit()
  except:
    config.Rollback()
    status.IsErr = 1
    status.ErrMessage = str(sys.exc_info()[1])
    
  