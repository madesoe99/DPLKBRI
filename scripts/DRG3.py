from suds.client import Client
import sys
import com.ihsan.util.modman as modman

''' TRANCODE = 8746
    BUCKET 1	No Rekening Nasabah. 
    BUCKET 2	Besar amount yang ditransfer 
    BUCKET 9	Besar Charge yang dikenakan. Defaul isian ""
    BUCKET 11	Besar Charge yang dikenakan. Defaul isian 0
    BUCKET 15	No Rekening IA Product DPLK
    BUCKET 16	Besar amount yang ditransfer
    BRANCHCODE	Kode Branch
    DEFAULTCURRENCY	Default "IDR"
    ALTERNATECURRENCY	Default "IDR"
    APPLICATION	Nama Aplikasi. Defaul "Aplikasi DPLK"
'''

def Pindah_Bukukan(config, parameter, returnpacket):
  status = returnpacket.CreateValues(
     ['IsErr',0],
     ['ErrMessage',''],
     ['proced_nominal',0],
  )
  ket = {'A':'Auto Payment','E':'E_Channel'}
  par = parameter.FirstRecord
  id_reconcile = par.id_reconcile
  jenis = par.jenis
  ParApp = {'TRANCODE':8746,
            'BUCKET 1':'',                   
            'BUCKET 2':0,                   
            'BUCKET 9':'',                  
            'BUCKET 11':0,                   
            'BUCKET 15':'',                  
            'BUCKET 16':0,                   
            'BRANCHCODE':'',                 
            'DEFAULTCURRENCY':'IDR',
            'ALTERNATECURRENCY':'IDR',
            'APPLICATION':'Aplikasi DPLK'}
  config.BeginTransaction()
  try:
    RG = config.CreatePObjImplProxy('RiwayatGiro')
    RG.SetKey('id_reconcile',id_reconcile)
    RG.SetKey('account_giro',par.account_giro)
    
    
    conn = KoneksiWeb(config)
    result = conn.service.Adder(1,2)
    #raise Exception,result
    if 2==1:
      RG.sum_pindahbuku    += RG.sum_procced_nominal
      RG.is_pindahbuku      = 'T'
    
    status.proced_nominal = RG.sum_procced_nominal
    config.Commit()
  except:
    config.Rollback()
    status.IsErr = 1
    status.ErrMessage = str(sys.exc_info()[1])
    
def KoneksiWeb(config):
    url_web = config.SysVarIntf.GetStringSysVar('URLWEBSERVICES','BRINet')
    get_conn = Client(url_web)  

    return get_conn
    
def invalid_status(config, parameter, returnpacket):
  status = returnpacket.CreateValues(
     ['IsErr',0],
     ['ErrMessage',''],
  )
  key = parameter.FirstRecord.key
  config.BeginTransaction()
  try:
    DRG = config.AccessPObject(key)
    DRG.is_valid = 'F'
    config.Commit()
  except:
    config.Rollback()
    status.IsErr = 1
    status.ErrMessage = str(sys.exc_info()[1])
    
def SimpanTransaksi(config, parameter, returnpacket):
  status = returnpacket.CreateValues(
     ['IsErr',0],
     ['ErrMessage',''],
     ['proced_nominal',0],
  )
  ket = {'A':'Auto Payment','E':'E_Channel'}
  par = parameter.FirstRecord
  id_reconcile = par.id_reconcile
  jenis = par.jenis
  config.BeginTransaction()
  try:
    OtorisasiTransaksi = modman.getModule(config,'scripts#transaksi.OtorisasiTransaksi')
    strSQL  = "SELECT * FROM DETILRIWAYATGIRO WHERE ID_RECONCILE=%s \
               AND IS_VALID='T' AND IS_CREATED_TRANSACTION='F'" % id_reconcile
    res = config.CreateSQL(strSQL).RawResult
    nominal_sukses = 0
    while not res.Eof:
      iuran ={'PK':0.0,'PST':0.0,'TMB':0.0}
      #bayar iuran peserta
      oIuranPeserta = config.CreatePObject('IuranPeserta')
      oIuranPeserta.catatan_bayar_iuran = jenis
       
      #field object TransaksiDPLK
      if res.is_corporate =='T':
         iuran['TMB'] = res.nominal
      else :
         iuran['PST'] = res.nominal

      oIuranPeserta.mutasi_iuran_pk  = iuran['PK']
      oIuranPeserta.mutasi_iuran_pst = iuran['PST']
      oIuranPeserta.mutasi_iuran_tmb = iuran['TMB']
      oIuranPeserta.mutasi_psl = oIuranPeserta.mutasi_pmb_pk = \
        oIuranPeserta.mutasi_pmb_pst = oIuranPeserta.mutasi_pmb_tmb = \
        oIuranPeserta.mutasi_pmb_psl = 0.0
      oIuranPeserta.kode_jenis_transaksi = 'K'
      
      #field object TransaksiRekInvDPLK
      oIuranPeserta.no_rekening = res.no_rekening
      oIuranPeserta.tgl_transaksi = par.waktu_mulai
      oIuranPeserta.keterangan = 'Transaksi reconcile '+ket[par.jenis]
      oIuranPeserta.jenis_transaksi = 'T'
    
      oIuranPeserta.isCommitted = 'F'
      oIuranPeserta.user_id = config.SecurityContext.UserID
      oIuranPeserta.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      oIuranPeserta.tgl_sistem = config.ModLibUtils.Now()
      # TEMPORARY CODE
      if config.SecurityContext.UserID.upper() == 'ROOT': 
        oIuranPeserta.branch_code = '000'
      else:
        oIuranPeserta.branch_code = config.SecurityContext.GetSessionInfo()[4]
      
      #buat detil transaksi DPLK
      oRekInv = config.CreatePObjImplProxy('RekInvDPLK')
      oRekInv.Key = res.no_rekening
      Ls_RekeningDPLK = oRekInv.Ls_RekeningDPLK
      while not Ls_RekeningDPLK.EndOfList:
        oRekDPLK = Ls_RekeningDPLK.CurrentElement 
        
        oDetilTransaksi = config.CreatePObject('DetilTransaksiDPLK')
        oDetilTransaksi.ID_Transaksi = oIuranPeserta.ID_Transaksi
        oDetilTransaksi.nomor_rekening = oRekDPLK.nomor_rekening 
        oDetilTransaksi.kode_paket_investasi = oRekDPLK.kode_paket_investasi
        
        oDetilTransaksi.mutasi_iuran_pk = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_pk  
        oDetilTransaksi.mutasi_iuran_pst = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_pst  
        oDetilTransaksi.mutasi_iuran_tmb = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_tmb
        oDetilTransaksi.mutasi_psl = oDetilTransaksi.mutasi_pmb_pk = \
          oDetilTransaksi.mutasi_pmb_pst = oDetilTransaksi.mutasi_pmb_tmb = \
          oDetilTransaksi.mutasi_pmb_psl = 0.0
        
        Ls_RekeningDPLK.Next()
      #-- 
      returns = OtorisasiTransaksi.ProsesOtorisasi(config, oIuranPeserta.ID_Transaksi, 'A')
      updateDetil(config,res.id_detil_giro)
      nominal_sukses += res.nominal
      res.Next()
    
    if nominal_sukses == 0:
      raise Exception,'Tidak ada transaksi valid yang diproses'  
    RG = config.CreatePObjImplProxy('RiwayatGiro')
    RG.SetKey('id_reconcile',id_reconcile)
    RG.SetKey('account_giro',res.account_giro)
    RG.sum_procced_nominal += nominal_sukses
    RG.is_reconciled       = 'T'
    
    status.proced_nominal = nominal_sukses
    config.Commit()
  except:
    config.Rollback()
    status.IsErr = 1
    status.ErrMessage = str(sys.exc_info()[1])
    
def updateDetil(config,id_detil_giro):
    strSQL  = "UPDATE DETILRIWAYATGIRO SET IS_CREATED_TRANSACTION='T' WHERE ID_DETIL_GIRO="+str(id_detil_giro)
    resSQL = config.ExecSQL(strSQL)
