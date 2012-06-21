import sys, time
#sys.path.append('c:/dafapp/dplk07/script_modules')
#sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

#import moduleapi, transaksiapi, AuthorizeTransaksi

import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "moduleapi",
    "transaksiapi",
    "scripts#transaksi.AuthorizeTransaksi"
  ]
)

def CreateHistoriPindahPaketInvestasi(config, oRegisterPindahPaketInvestasi, \
  rSQL):
  config.SendDebugMsg('pindahpaket31')
  oHistoriPindahPaketInvestasi = config.CreatePObject('HistoriPindahPaketInvestasi')
  oHistoriPindahPaketInvestasi.no_referensi = \
    oRegisterPindahPaketInvestasi.no_referensi
  oHistoriPindahPaketInvestasi.no_peserta = rSQL.no_peserta
  oHistoriPindahPaketInvestasi.terminal_id = rSQL.last_terminal_id
  oHistoriPindahPaketInvestasi.user_id = rSQL.user_id
  oHistoriPindahPaketInvestasi.auth_user_id = config.SecurityContext.userid
  oHistoriPindahPaketInvestasi.tanggal_histori = config.Now()
  oHistoriPindahPaketInvestasi.kode_paket_investasi = rSQL.kode_paket_investasi
  config.SendDebugMsg('pindahpaket32')

  return oHistoriPindahPaketInvestasi

def CountCostVal(config, oRekeningDPLK):
  akum_dana = oRekeningDPLK.akum_dana_pengembangan + \
    oRekeningDPLK.akum_dana_peralihan + oRekeningDPLK.akum_dana_iuran_pst + \
    oRekeningDPLK.akum_dana_iuran_pk

  yearNow = config.FormatDateTime('yyyy', config.Now())
  config.SendDebugMsg('year...... : '+str(yearNow))
  sSQL = 'select count(hppi.no_peserta) as totPindah from HISTORIPINDAHPAKETINVESTASI hppi ' \
         'where hppi.NO_PESERTA = \'%s\'  '\
          ' and datepart(year,hppi.tanggal_histori) = \'%s\' '\
          % (oRekeningDPLK.no_peserta, yearNow)
  config.SendDebugMsg('sQL : ' + sSQL)
  rSQL = config.CreateSQL(sSQL).RawResult

  ### End By Ade Herman 2011-07-22 ----

  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PERSEN_BIAYA_PINDAH_INVESTASI'
  biayaPindah = oP.Numeric_Value
  
  ## Tambahan By Ade Herman 2011-07-25 ---
  if rSQL.totPindah <= 2:
     config.SendDebugMsg('No Peserta          ...... : '+str(oRekeningDPLK.no_peserta))
     config.SendDebugMsg('Jumlah Pindah Paket ...... : '+str(rSQL.totPindah))
     biayaPindah = 0
  ## End 2011-07-25

  #set parameter persen biaya pindah paket investasi
  # Sementara di tutup Dulu
  #oP = config.CreatePObjImplProxy('Parameter')
  #oP.Key = 'PERSEN_BIAYA_PINDAH_INVESTASI'
  #return akum_dana * (oP.Numeric_Value / 100)
  return akum_dana * (biayaPindah / 100)

def CreateBiayaAdmTransaksi(config, oRegisterPindahPaketInvestasi, rSQL):
  oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
  oRekeningDPLK.key = rSQL.no_peserta
  
  oBiayaAdmTransaksi = config.CreatePObject('BiayaAdmTransaksi')
  oBiayaAdmTransaksi.isPindahPaket = 'T'
  oBiayaAdmTransaksi.branch_code = \
    oRegisterPindahPaketInvestasi.LUserApp.LBranchLocation.branch_code
  oBiayaAdmTransaksi.no_peserta = oRegisterPindahPaketInvestasi.no_peserta
  oBiayaAdmTransaksi.isCommitted = 'T'
  oBiayaAdmTransaksi.LPaketInvestasi = oRekeningDPLK.LPaketInvestasi
  oBiayaAdmTransaksi.keterangan = \
    'BiayaAdmTransaksi Pemindahan Paket Investasi peserta %s, %s ke %s' \
    % (oBiayaAdmTransaksi.no_peserta,\
       oRekeningDPLK.kode_paket_investasi,\
       oRegisterPindahPaketInvestasi.kode_paket_investasi)
  
  oBiayaAdmTransaksi.ID_TransactionBatch = \
    oRegisterPindahPaketInvestasi.ID_TransactionBatch
  oBiayaAdmTransaksi.terminal_id = oRegisterPindahPaketInvestasi.terminal_id
  oBiayaAdmTransaksi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oBiayaAdmTransaksi.user_id = oRegisterPindahPaketInvestasi.user_id
  oBiayaAdmTransaksi.user_id_auth = config.SecurityContext.userid
  oBiayaAdmTransaksi.tgl_sistem = config.Now()
  oBiayaAdmTransaksi.tgl_otorisasi = config.Now()
  #ita-250609-ambil tgl batch, bkn now
  #y,m,d = time.localtime()[:3]
  y, m, d = oRegisterPindahPaketInvestasi.LTransactionBatch.tgl_used[:3]

  oBiayaAdmTransaksi.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)

  moduleapi.TransCostOpr(config, oRekeningDPLK, oBiayaAdmTransaksi, \
    CountCostVal(config,oRekeningDPLK))

def CreateTransaksiPaketInvestasi(config, oRegisterPindahPaketInvestasi, \
  rSQL):
  #parameter isNew = 0: minuskan saldo untuk paket investasi lama
  #isNew = 1: munculkan saldo untuk paket investasi baru
  #sebenarnya ada kode khusus untuk jenis pindah paket: F - ubah jenis investasi
  oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
  oRekeningDPLK.key = rSQL.no_peserta
  
  oL = config.CreatePObject('TransaksiDPLK')
  oL.kode_jenis_transaksi = 'F'    
  #DI BAWAH MERUPAKAN KODE LAMA
  #oL = config.CreatePObject('TransaksiDPLKManual')
  #oN = config.CreatePObject('TransaksiDPLKManual')    

  #minuskan saldo, untuk transaksi Lama
  oL.mutasi_iuran_pk = -oRekeningDPLK.akum_dana_iuran_pk
  oL.mutasi_iuran_pst = -oRekeningDPLK.akum_dana_iuran_pst
  oL.mutasi_pengembangan = -oRekeningDPLK.akum_dana_pengembangan
  oL.mutasi_peralihan = -oRekeningDPLK.akum_dana_peralihan
  oL.kode_paket_investasi = oRekeningDPLK.kode_paket_investasi        
  
  #assign nilai umum
  oL.keterangan = 'Transaksi untuk penyeimbangan pindah paket investasi'
  oL.no_peserta = oRekeningDPLK.no_peserta
  oL.ID_TransactionBatch = \
    oRegisterPindahPaketInvestasi.ID_TransactionBatch
  oL.branch_code = \
    oRegisterPindahPaketInvestasi.LUserApp.LBranchLocation.branch_code
  oL.isCommitted = 'F'
  oL.user_id = config.SecurityContext.UserID
  oL.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oL.tgl_sistem = config.Now()
  #ita-250609-ambil tgl batch, bkn now
  #y,m,d = time.localtime()[:3]
  y, m, d = oRegisterPindahPaketInvestasi.LTransactionBatch.tgl_used[:3]

  oL.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)
 
  #otorisasi langsung, lama dulu kemudian yang baru
  AuthorizeTransaksi.ApproveOperation(config, 'TransaksiDPLK', oL.ID_Transaksi)  

  # hapus detail akumulasi paket lama, buat sesuai jenis investasi paket yang baru
  oRekeningDPLK.Ls_DetailAkumPengembangan.DeleteAllPObjs()
  
def UpdatePindahPaketInvestasi(config, oRegisterPindahPaketInvestasi, rSQL):
  CreateBiayaAdmTransaksi(config, oRegisterPindahPaketInvestasi, rSQL)
  CreateTransaksiPaketInvestasi(config, oRegisterPindahPaketInvestasi, rSQL) 

def UpdateRekeningDPLK(config, no_peserta):
  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.key = no_peserta
  oR.status_dplk = 'N'
  

def UpdateRekeningNasabah(config, no_peserta):
  oRN = config.CreatePObjImplProxy('RekeningNasabah')
  oRN.key = no_peserta[:10]
  
  oRN.akum_dana_iuran_pk = 0.0
  oRN.akum_dana_iuran_pst = 0.0
  oRN.akum_dana_iuran_tambahan = 0.0
  oRN.akum_dana_iuran_psl = 0.0
  oRN.akum_dana_pengembangan_pk = 0.0
  oRN.akum_dana_pengembangan_pst = 0.0
  oRN.akum_dana_pengembangan_tambahan = 0.0
  oRN.akum_dana_pengembangan_psl = 0.0
  oRN.unit_iuran_pk	= 0.0
  oRN.unit_iuran_pst = 0.0
  oRN.unit_iuran_tambahan	= 0.0
  oRN.unit_iuran_psl = 0.0
  oRN.unit_pengembangan_pk = 0.0
  oRN.unit_pengembangan_pst	= 0.0
  oRN.unit_pengembangan_tambahan = 0.0
  oRN.unit_pengembangan_psl	= 0.0

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterCIF = config.CreatePObjImplProxy('RegisterCIF')
  oRegisterCIF.Key = id
  config.SendDebugMsg('aaaa')
  config.BeginTransaction()
  try:
    oRegisterPindahPaketInvestasi = oRegisterCIF.CastAs('RegisterPindahPaketInvestasi')
    oNasabahDPLK = oRegisterPindahPaketInvestasi.LNasabahDPLK
    
    config.SendDebugMsg('bbbbbbb')
    sSQLR = "select * from rekeningnasabah\
    where nomor_rekening = '%s'" % (oRegisterPindahPaketInvestasi.no_peserta)
    rSQLR = config.CreateSQL(sSQLR).RawResult
    
    akum_dana_iuran_pk = rSQLR.akum_dana_iuran_pk or 0.0
    akum_dana_iuran_pst = rSQLR.akum_dana_iuran_pst or 0.0
    akum_dana_iuran_tambahan = rSQLR.akum_dana_iuran_tambahan or 0.0
    akum_dana_iuran_psl = rSQLR.akum_dana_iuran_psl or 0.0
    akum_dana_pengembangan_pk = rSQLR.akum_dana_pengembangan_pk or 0.0
    akum_dana_pengembangan_pst = rSQLR.akum_dana_pengembangan_pst or 0.0
    akum_dana_pengembangan_tambahan = rSQLR.akum_dana_pengembangan_tambahan or 0.0
    akum_dana_pengembangan_psl = rSQLR.akum_dana_pengembangan_psl or 0.0
    unit_iuran_pk	= rSQLR.unit_iuran_pk or 0.0
    unit_iuran_pst = rSQLR.unit_iuran_pst or 0.0
    unit_iuran_tambahan = rSQLR.unit_iuran_tambahan or 0.0
    unit_iuran_psl = rSQLR.unit_iuran_psl or 0.0
    unit_pengembangan_pk = rSQLR.unit_pengembangan_pk or 0.0
    unit_pengembangan_pst = rSQLR.unit_pengembangan_pst or 0.0
    unit_pengembangan_tambahan = rSQLR.unit_pengembangan_tambahan or 0.0
    unit_pengembangan_psl = rSQLR.unit_pengembangan_psl or 0.0
    
    config.SendDebugMsg('ccccc')
    # hapus yang lama
    sSQL = "SELECT * FROM REKENINGDPLK \
    WHERE NOMOR_REKENING = '%s'" % (oRegisterPindahPaketInvestasi.no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First() 
    i = 1
    while not rSQL.Eof:
      CreateHistoriPindahPaketInvestasi(config, oRegisterPindahPaketInvestasi, \
        rSQL)
      UpdatePindahPaketInvestasi(config, oRegisterPindahPaketInvestasi, rSQL)
      UpdateRekeningDPLK(config, rSQL.no_peserta)
      i += 1
      rSQL.Next()

    UpdateRekeningNasabah(config, oRegisterPindahPaketInvestasi.no_peserta)
    
    config.SendDebugMsg('ddddddd')
    # buat baru
    sSQL = "select * from RegisterPindahPaketInvestasiDetail\
    where registercif_id = %s" % (id)
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    while not rSQL.Eof:
      oR = config.CreatePObject('RekeningDPLK')
      oR.no_peserta = oRegisterPindahPaketInvestasi.no_peserta + str(i)
      oR.proporsi = rSQL.proporsi
      oR.kode_paket_investasi = rSQL.kode_paket_investasi
      
      rSQL.Next()
  
    config.SendDebugMsg('eeeee')
#     oRegisterCIF.Ls_RegisterPindahPaketInvestasiDetail.DeleteAllPObjs()
#     oRegisterCIF.Delete()

    config.SendDebugMsg('fffff')
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1
