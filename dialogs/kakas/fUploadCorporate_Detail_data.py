import com.ihsan.foundation.pobjecthelper as pobjecthelper
import com.ihsan.foundation.pobject as pobject
import com.ihsan.net.message as message
import com.ihsan.util.otorisasi as otorisasi
import com.ihsan.util.modman as modman
import rpdb2

import sys

def dbg(msg):
  #app.ConWriteln(msg)
  #app.ConRead(msg2)
  message.send_udp(msg + "\n", 'localhost', 9123)
 
def saveData(config, params, returns):
  helper = pobjecthelper.PObjectHelper(config)
  app = config.AppObject
  status = returns.CreateValues(
    ['success', False],
    ['message', ''],
  )
  #recDetails = params.uipDetails.GetRecord(0)
  
  config.BeginTransaction()
  try :
    config.Commit()
    status.success = True
    status.message = 'Data berhasil disimpan...'
  except :
    config.Rollback()
    status.message = "Data gagal disimpan...\n" + str(sys.exc_info()[1])
  

def createTrxIuran(config, params, returns):
  status = returns.CreateValues(
    ['success', False],
    ['message', ''],
  )
  
  id = params.FirstRecord.id
  oUploadCorporate = config.CreatePObjImplProxy('UploadCorporate')
  oUploadCorporate.Key = id
  
  config.BeginTransaction()
  try :
    sSQL = '''
      SELECT * 
      FROM   UploadCorpIuranPeserta
      WHERE  trx_session_id = %d
             AND is_auth = 'F'
             AND is_valid = 'T'
      ''' % oUploadCorporate.trx_session_id
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    while not rSQL.Eof:
      recT = rSQL
      
      #bayar iuran peserta
      oIuranPeserta = config.CreatePObject('IuranPeserta')
      oIuranPeserta.catatan_bayar_iuran = 'iuran dari upload massal'
      
      #field object TransaksiDPLK
      oIuranPeserta.mutasi_iuran_pk = recT.iuran_pk
      oIuranPeserta.mutasi_iuran_pst = recT.iuran_pst
      oIuranPeserta.kode_jenis_transaksi = 'K'
      
      #field object TransaksiRekInvDPLK
      oIuranPeserta.no_rekening = recT.no_rekening
      oIuranPeserta.tgl_transaksi = oUploadCorporate.session_time
      oIuranPeserta.keterangan = recT.keterangan
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
      oRekInv.Key = recT.no_rekening
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
      
      moduleOtor = modman.getModule(config, "scripts#transaksi/OtorisasiTransaksi")
      otorStatus, otorMessage = moduleOtor.ProsesOtorisasi(config, oIuranPeserta.ID_Transaksi, 'A')
      if otorStatus == 0:
        oUCIuranPeserta = config.CreatePObjImplProxy('UploadCorpIuranPeserta')
        oUCIuranPeserta.Key = rSQL.upload_id
        oUCIuranPeserta.is_auth = 'T'
      
      rSQL.Next()

    oUploadCorporate.is_auth = 'T'

    config.Commit()
    status.success = True
    status.message = 'Data berhasil disimpan...'
  except:
    config.Rollback()
    status.message = "Data gagal disimpan...\n" + str(sys.exc_info()[1])
#--end--createTrxIuran

def createTrxBiayaDaftar(config, params, returns):
  status = returns.CreateValues(
    ['success', False],
    ['message', ''],
  )
  
  id = params.FirstRecord.id
  oUploadCorporate = config.CreatePObjImplProxy('UploadCorporate')
  oUploadCorporate.Key = id
  
  config.BeginTransaction()
  try :
    sSQL = '''
      SELECT * 
      FROM   UploadCorpBiayaDaftar
      WHERE  trx_session_id = %d
             AND is_auth = 'F'
             AND is_valid = 'T'
      ''' % oUploadCorporate.trx_session_id
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    while not rSQL.Eof:
      recT = rSQL
      
      #bayar iuran peserta
      oIuranPendaftaran = config.CreatePObject('IuranPendaftaran')
      #field object TransaksiRekInvDPLK
      oIuranPendaftaran.besar_biaya_daftar = recT.biaya_daftar
      oIuranPendaftaran.no_rekening = recT.no_rekening
      oIuranPendaftaran.tgl_transaksi = oUploadCorporate.session_time
      oIuranPendaftaran.keterangan = recT.keterangan
      oIuranPendaftaran.jenis_transaksi = 'D'
    
      oIuranPendaftaran.isCommitted = 'F'
      oIuranPendaftaran.user_id = config.SecurityContext.UserID
      oIuranPendaftaran.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      oIuranPendaftaran.tgl_sistem = config.ModLibUtils.Now()
      
      # TEMPORARY CODE
      if config.SecurityContext.UserID.upper() == 'ROOT': 
        oIuranPendaftaran.branch_code = '000'
      else:
        oIuranPendaftaran.branch_code = config.SecurityContext.GetSessionInfo()[4]
      
      moduleOtor = modman.getModule(config, "scripts#transaksi/OtorisasiTransaksi")
      otorStatus, otorMessage = moduleOtor.ProsesOtorisasi(config, oIuranPendaftaran.ID_Transaksi, 'A')
      if otorStatus == 0:
        oUCBiayaDaftar = config.CreatePObjImplProxy('UploadCorpBiayaDaftar')
        oUCBiayaDaftar.Key = rSQL.upload_id
        oUCBiayaDaftar.is_auth = 'T'
        
        oRekInvDPLK = config.CreatePObjImplProxy('RekInvDPLK')
        oRekInvDPLK.Key = recT.no_rekening
        oRekInvDPLK.status_biaya_daftar = 'T'
        
      rSQL.Next()

    oUploadCorporate.is_auth = 'T'

    config.Commit()
    status.success = True
    status.message = 'Data berhasil disimpan...'
  except:
    config.Rollback()
    status.message = "Data gagal disimpan...\n" + str(sys.exc_info()[1])
#--end--createTrxBiayaDaftar
  
def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  key = params.FirstRecord.key
  if str(key) != '':
    uideflist.SetData('uipUploadCorporate', key)
    rec = uideflist.uipUploadCorporate.Dataset.GetRecord(0)
  pass