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
  
  recIuran = uideflist.uipIuranPeserta.Dataset.AddRecord()
  recIuran.mutasi_iuran_pk = regNR.iuran_pk
  recIuran.mutasi_iuran_pst = regNR.iuran_pst
  
def FormBeginSetData(uideflist, auiname, apobjconst):
  '''config = uideflist.Config
  isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
    'NeedLoginCoreBanking')
    
  keepGoingProcess = 1
  try:
    #khusus untuk user ialah TELLER
    if moduleapi.IsUserTeller(config, config.SecurityContext.userid) and \
      isNeedLoginCoreBanking == 'T':

      #checking teller timezone
      allowTransaction = CekUserTimeZone.CekAllowTransaction(config, \
        config.SecurityContext.userid)
      if not allowTransaction:
        raise '\nPERINGATAN!','\n\nWaktu resmi aktivitas banking telah selesai. '\
          'Tidak diperbolehkan melakukan transaksi.\nHubungi Administrator jika '\
          'masih ada transaksi yang akan dilakukan.'

      #cek adakah batch untuk CoreBanking Batch yang telah dibuat
      y,m,d = time.localtime()[:3]
      oCBB = config.CreatePObjImplProxy('CoreBankingBatch')
      oCBB.SetKey('User_ID',config.SecurityContext.UserID)
      oCBB.SetKey('Tanggal',d)
      oCBB.SetKey('Bulan',m)
      oCBB.SetKey('Tahun',y)

      if oCBB.IsNull:
        raise '\nPERINGATAN!','\n\nBatch Core Banking Aplikasi DPLK untuk hari ini '\
          'belum dibuat. Mohon buat sendiri terlebih dahulu.'

  except:
    raise
    
  return keepGoingProcess'''
  return 0

def FormGeneralSetData(uideflist, auiname, apobjconst):
  '''config = uideflist.Config
  uipIuranPendaftaran = uideflist.uipIuranPendaftaran

  oRegisterNasabahRekening = config.CreatePObjImplProxy('RegisterNasabahRekening')
  oRegisterNasabahRekening.Key = int(apobjconst)

  branch_code = oRegisterNasabahRekening.kode_cab_daftar
  oBranch = config.CreatePObjImplProxy('BranchLocation')
  oBranch.Key = branch_code
  BranchName = oBranch.BranchName

  #set umum Iuran Pendaftaran dan Iuran Peserta
  rec = uipIuranPendaftaran.Dataset.AddRecord()
  recIP = uideflist.uipIuranPeserta.Dataset.AddRecord()

  # inisialisasi check box bayar langsung iuran peserta
  recIP.isLangsungIuran = 1

  rec.SetFieldByName('LBranchLocation.branch_code',branch_code)
  rec.SetFieldByName('LBranchLocation.BranchName',BranchName)
  rec.user_id = config.SecurityContext.userid
  rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  rec.tgl_transaksi = config.Now()

  rec.registernr_id = int(apobjconst)
  rec.SetFieldByName('LRekeningDPLK.no_peserta',oRegisterNasabahRekening.no_peserta)
  rec.SetFieldByName('LRekeningDPLK.LNasabahDPLK.nama_lengkap',oRegisterNasabahRekening.nama_lengkap)

  #set khusus iuran pendaftaran
  rec.besar_biaya_daftar = moduleapi.GetBesarBiayaDaftar(config, oRegisterNasabahRekening)
  
  #set khusus iuran peserta
  recIP.mutasi_iuran_pst = oRegisterNasabahRekening.iuran_pst
  recIP.defaultIuran = recIP.mutasi_iuran_pst

  #cek cara pemilihan batch
  if moduleapi.IsUserTeller(config, config.SecurityContext.userid):
    rec.isBatchLimited = 1
    rec.batch_sub_type = 'T'

    #set batch registrasi
    oTransactionBatch = moduleapi.GetTransactionBatchObj(config, \
      config.SecurityContext.userid, 'O', 'R', 'T')
    rec.SetFieldByName('LTransactionBatch.ID_TransactionBatch',oTransactionBatch.ID_TransactionBatch)
    rec.SetFieldByName('LTransactionBatch.no_batch',oTransactionBatch.no_batch)
    
    #set batch transaksi
    oTB_Transaksi = moduleapi.GetTransactionBatchObj(config, \
      config.SecurityContext.userid, 'O', 'T', 'T')
    recIP.SetFieldByName('LTransactionBatch.ID_TransactionBatch',oTB_Transaksi.ID_TransactionBatch)
    recIP.SetFieldByName('LTransactionBatch.no_batch',oTB_Transaksi.no_batch)

    recIP.SetFieldByName('defaultID_TransactionBatch',oTB_Transaksi.ID_TransactionBatch)
    recIP.SetFieldByName('defaultNo_Batch',oTB_Transaksi.no_batch)

  else:
    rec.isBatchLimited = 0
    rec.batch_sub_type = 'M'

  #set parameter Batch Registrasi
  recP = uideflist.uipParameterBatch.Dataset.AddRecord()
  tglPakai = time.localtime()[:3]

  recP.TanggalPakai = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])

  recP.NeedUser = 0
  if string.upper(str(config.SecurityContext.GetUserInfo()[2])) == 'TELLER':
    recP.UserIDOwner = config.SecurityContext.UserID
    recP.NeedUser = 1
  else:
    recP.UserIDOwner = ''

  '''
  return 0
  
def FormGeneralProcessData(uideflist, data):
  '''config = uideflist.Config
  recPendaftaran = data.uipIuranPendaftaran.GetRecord(0)
  recIuran = data.uipIuranPeserta.GetRecord(0)

  oRNR = config.CreatePObjImplProxy('RegisterNasabahRekening')
  oRNR.Key = recPendaftaran.registernr_id

  try:
    isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
      'NeedLoginCoreBanking')

    if isNeedLoginCoreBanking == 'T':
      #user sudah login ke core banking
      #ambil batch untuk CoreBanking Batch yang telah dibuat
      y,m,d = time.localtime()[:3]
      oCBB = config.CreatePObjImplProxy('CoreBankingBatch')
      oCBB.SetKey('User_ID',config.SecurityContext.UserID)
      oCBB.SetKey('Tanggal',d)
      oCBB.SetKey('Bulan',m)
      oCBB.SetKey('Tahun',y)

    #simpan info dan create objek Iuran Pendaftaran
    oRNR.batch_registrasi = \
      recPendaftaran.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
    oRNR.keterangan_registrasi = recPendaftaran.keterangan

    oP = config.CreatePObject('IuranPendaftaran')

    #saving id transaksi iuran pendaftaran, untuk kebutuhan print slip transaksi teller
    recPendaftaran.HiddenIDPendaftaran = oP.ID_Transaksi
          
    oP.ID_TransactionBatch = \
      recPendaftaran.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
    oP.keterangan = recPendaftaran.keterangan
    oP.besar_biaya_daftar = recPendaftaran.besar_biaya_daftar

    if recIuran.isLangsungIuran:
      #simpan info dan create objek Iuran Peserta
      oRNR.batch_iuran = \
        recIuran.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
      oRNR.keterangan_iuran = recIuran.keterangan
      oRNR.catatan_bayar_iuran = 'Iuran Peserta pertama kali'

      oI = config.CreatePObject('IuranPeserta')

      #saving id transaksi iuran peserta, untuk kebutuhan print slip transaksi teller
      recIuran.HiddenIDIuran = oI.ID_Transaksi

      oI.ID_TransactionBatch = recIuran.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
      oI.keterangan = recIuran.keterangan
      oI.mutasi_iuran_pst = recIuran.mutasi_iuran_pst
      oI.mutasi_iuran_pk = oI.mutasi_pengembangan = oI.mutasi_peralihan = 0.0
      oI.catatan_bayar_iuran = 'Iuran Peserta pertama kali'
      oI.kode_paket_investasi = oRNR.kode_paket_investasi

      oI.isCommitted = 'F'
      oI.no_peserta = recPendaftaran.GetFieldByName('LRekeningDPLK.no_peserta')
      oI.branch_code = recPendaftaran.GetFieldByName('LBranchLocation.branch_code')
      oI.tgl_sistem = config.Now()
      oI.user_id = recPendaftaran.user_id
      oI.terminal_id = recPendaftaran.terminal_id
      y,m,d = config.ModLibUtils.DecodeDate(recPendaftaran.tgl_transaksi)
      oI.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)

      if oRNR.wasiat_ummat == 'T':
        oI.titipan_premi = 0.0

      oRNR.ID_Transaksi_IuranPeserta = oI.ID_Transaksi

    if oRNR.wasiat_ummat == 'T':
      #ikut wasiat ummat, set titipan premi 0
      oRNR.titipan_premi = 0.0

    oP.isCommitted = 'F'
    oP.no_peserta = recPendaftaran.GetFieldByName('LRekeningDPLK.no_peserta')
    oP.branch_code = recPendaftaran.GetFieldByName('LBranchLocation.branch_code')
    oP.tgl_sistem = config.Now()
    oP.user_id = recPendaftaran.user_id
    oP.terminal_id = recPendaftaran.terminal_id
    y,m,d = config.ModLibUtils.DecodeDate(recPendaftaran.tgl_transaksi)
    oP.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)

    #sambungkan link RegisterNasabahRekening dan set status biaya daftar
    oRNR.ID_Transaksi_IuranPendaftaran = oP.ID_Transaksi
    oRNR.STATUS_BIAYA_DAFTAR = 'T'

    if isNeedLoginCoreBanking == 'T':
      #user sudah login ke core banking
      #setor iuran pendaftaran dan iuran pertama, cek setor tunai / pindah buku
      if recIuran.isPindahBuku == 'F':
        if recIuran.isLangsungIuran:
          oPI = config.CreatePObjImplProxy('PaketInvestasi')
          oPI.Key = oI.kode_paket_investasi

          oI.isPindahBuku = recIuran.isPindahBuku

          #setor tunai pertama, sekaligus giro pendaftaran dan giro iuran peserta
          res = transaksiapi.SetorTunaiPertamaCoreBanking(config, oCBB.No_Batch, oP.no_peserta, \
          oRNR.nama_lengkap, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING',\
          'GiroPendaftaran'), oPI.no_giro, oP.ID_Transaksi, oI.ID_Transaksi, \
          oP.besar_biaya_daftar, oI.mutasi_iuran_pst + oI.mutasi_iuran_pk, \
          oP.keterangan, oI.keterangan)

          #simpan return value setor tunai sebagai referensi CoreBanking
          noRef = res[0]
          oI.Ref_CoreBanking = res[1]

        else:
          #KODE DI BAWAH NUNGGU KALAU DTS SUDAH BENAR
          #setor tunai giro pendaftaran di CoreBanking
          noRef = transaksiapi.SetorTunaiCoreBanking(config, oCBB.No_Batch, oP.no_peserta, \
            oRNR.nama_lengkap, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING',\
            'GiroPendaftaran'), oP.ID_Transaksi, oP.besar_biaya_daftar, oP.keterangan)

          #setor tunai giro iuran peserta (giro paket) di CoreBanking
          #transaksiapi.SetorTunaiCoreBanking(config, oCBB.No_Batch, oI.no_peserta, \
          #  oRNR.nama_lengkap, oPI.no_giro, oI.ID_Transaksi, \
          #  oI.mutasi_iuran_pst + oI.mutasi_iuran_pk, oI.keterangan)

        #simpan return value setor tunai sebagai referensi CoreBanking
        oP.Ref_CoreBanking = noRef

      else:
        if recIuran.isLangsungIuran:
          #pindah buku
          oPI = config.CreatePObjImplProxy('PaketInvestasi')
          oPI.Key = oI.kode_paket_investasi

          oI.isPindahBuku = recIuran.isPindahBuku

          oI.Rekening_Pindah_Buku = recIuran.Rekening_Pindah_Buku
          oI.Tipe_Rekening_Pindah_Buku = recIuran.Tipe_Rekening_Pindah_Buku

          #pindah buku pertama, sekaligus giro pendaftaran dan giro iuran peserta
          res = transaksiapi.PindahBukuPertamaCoreBanking(config, oCBB.No_Batch, oP.no_peserta, \
          oRNR.nama_lengkap, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING',\
          'GiroPendaftaran'), oPI.no_giro, oP.ID_Transaksi, oI.ID_Transaksi, \
          oP.besar_biaya_daftar, oI.mutasi_iuran_pst + oI.mutasi_iuran_pk, \
          recIuran.Rekening_Pindah_Buku, recIuran.Tipe_Rekening_Pindah_Buku, \
          oP.keterangan, oI.keterangan)

          #simpan return value setor tunai sebagai referensi CoreBanking
          noRef = res[0]
          oI.Ref_CoreBanking = res[1]
        else:
          #KODE DI BAWAH NUNGGU KALAU DTS SUDAH BENAR
          #pindah buku giro pendaftaran di CoreBanking
          noRef = transaksiapi.PindahBukuCoreBanking(config, oCBB.No_Batch, oP.no_peserta, \
            oRNR.nama_lengkap, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING',\
            'GiroPendaftaran'), oP.ID_Transaksi, oP.besar_biaya_daftar, \
            recIuran.Rekening_Pindah_Buku, recIuran.Tipe_Rekening_Pindah_Buku, \
            oP.keterangan)

          #pindah buku giro iuran peserta (giro paket) di CoreBanking
          #transaksiapi.PindahBukuCoreBanking(config, oCBB.No_Batch, oI.no_peserta, \
          #  oRNR.nama_lengkap, oPI.no_giro, oI.ID_Transaksi, \
          #  oI.mutasi_iuran_pst + oI.mutasi_iuran_pk, recIuran.Rekening_Pindah_Buku, \
          #  recIuran.Tipe_Rekening_Pindah_Buku, oI.keterangan)

        #simpan return value setor tunai sebagai referensi CoreBanking
        oP.Ref_CoreBanking = noRef

  except:
    raise

  '''
  return 0
  
def FormEndProcessData(uideflist, datapacket):
  '''config = uideflist.Config
  recPendaftaran = datapacket.uipIuranPendaftaran.GetRecord(0)
  recIuran = datapacket.uipIuranPeserta.GetRecord(0)

  uideflist.PrepareReturnDataset()
  recP = uideflist.uipParameterBatch.Dataset.AddRecord()
  
  #cek hidden id iuran pendaftaran
  if recPendaftaran.HiddenIDPendaftaran not in [None,0]:
    recP.FileSlipPendaftaran = SlipTransaksiTeller.CreateSlip(config, \
      'IuranPendaftaran', recPendaftaran.HiddenIDPendaftaran, \
      recPendaftaran.registernr_id)

  if recIuran.isLangsungIuran:
    #cek hidden id iuran peserta
    if recIuran.HiddenIDIuran not in [None,0]:
      recP.FileSlipIuran = SlipTransaksiTeller.CreateSlip(config, \
        'IuranPeserta', recIuran.HiddenIDIuran, recPendaftaran.registernr_id)

  '''
  return 4

def saveBiayaDaftar(config, params, returns):
  returns.CreateValues(['success', False], ['message', ''])
  
  recPB = params.uipParameterBatch.GetRecord(0)
  recRNR = params.uipRegisterNasabahRekening.GetRecord(0)
  recIPD = params.uipIuranPendaftaran.GetRecord(0)
  recIPS = params.uipIuranPeserta.GetRecord(0)
  
  config.BeginTransaction()
  try:
    oRNR = config.CreatePObjImplProxy("RegisterNasabahRekening")
    oIPD = config.CreatePObject("IuranPendaftaran")
    oIPS = config.CreatePObject("IuranPeserta")
    
    ''' SET PROPERTIES IURAN PENDAFTARAN '''
    oIPD.besar_biaya_daftar = oIPD.besar_biaya_daftar
    oIPD.user_id = config.SecurityContext.GetSessionInfo()[0]
    oIPD.TGL_TRANSAKSI = recIPD.tgl_transaksi
    #oIPD.TGL_OTORISASI
    oIPD.TGL_SISTEM = config.Now()
    #oIPD.USER_ID_AUTH
    oIPD.TERMINAL_ID = config.SecurityContext.GetSessionInfo()[1]
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
    
    ''' SET PROPERTIES IURAN PESERTA '''
    oIPS.catatan_bayar_iuran = recIPS.keterangan
    #oIPS.id_trans_sales
    oIPS.user_id = config.SecurityContext.GetSessionInfo()[0]
    oIPS.TGL_TRANSAKSI = recIPD.tgl_transaksi
    #oIPS.TGL_OTORISASI
    oIPS.TGL_SISTEM = config.Now()
    #oIPS.USER_ID_AUTH
    oIPS.TERMINAL_ID = config.SecurityContext.GetSessionInfo()[1]
    #oIPS.TERMINAL_ID_AUTH
    oIPS.KETERANGAN = recIPS.keterangan
    #oIPS.JENIS_TRANSAKSI
    oIPS.ISCOMMITTED = recIPD.isCommitted
    oIPS.BRANCH_CODE = recIPS.GetFieldByName('LBranchLocation.branch_code')
    #oIPS.REF_COREBANKING
    #oIPS.NO_REKENING = recRNR.no_rekening
    oIPS.mutasi_iuran_pk = recIPS.mutasi_iuran_pk
    oIPS.mutasi_iuran_pst = recIPS.mutasi_iuran_pst
    #oIPS.mutasi_iuran_tmb
    #oIPS.mutasi_psl
    #oIPS.mutasi_pmb_pk
    #oIPS.mutasi_pmb_pst
    #oIPS.mutasi_pmb_tmb
    #oIPS.mutasi_pmb_psl
    #oIPS.KODE_JENIS_TRANSAKSI
    #oIPS.ISPINDAHPAKET = 'F'
    #oIPS.COUNT_ADVIS
    #oIPS.saldo_yang_dibebani
    #oIPS.catatan
    #oIPS.idbghasil
    
    ''' SET LINK PROPERTY TO BAYAR DAFTAR DAN IURAN AWAL '''
    oRNR.LRegisterIuranPendaftaran = oIPD
    oRNR.LRegisterIuranPeserta = oIPS
    
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

