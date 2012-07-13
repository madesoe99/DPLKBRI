import sys
import com.ihsan.util.modman as modman

#DEBUG MODE
#import rpdb2;rpdb2.start_embedded_debugger('haryo',True,True)

def CreateBiayaTransaksi(config, classJenisBiaya, oTransaksi, nominalBiaya):
  oBiaya = config.CreatePObject(classJenisBiaya)

  if classJenisBiaya == 'BiayaAdmTransaksi':
    oTransaksi.ID_Transaksi_BAdmTrans = oBiaya.ID_Transaksi
    #tidak ada biaya transaksi untuk pindah paket investasi
  elif classJenisBiaya == 'BiayaPengelolaanDana':
    oTransaksi.ID_Transaksi_BPeng = oBiaya.ID_Transaksi
    oBiaya.saldo_yang_dibebani = oTransaksi.saldo_jml_dana
  elif classJenisBiaya == 'BiayaAdmTahunan':
    oTransaksi.ID_Transaksi_BAdmThn = oBiaya.ID_Transaksi
  else:
    raise Exception, "ID: Jenis Biaya Transaksi tidak terdefinisi!"

  #field TransaksiDPLK
  #field TransaksiRekInvDPLK
  oBiaya.LRekeningDPLK = oTransaksi.LRekeningDPLK
  oBiaya.branch_code = oTransaksi.branch_code
  oBiaya.keterangan = '%s %s peserta %s' % \
    (classJenisBiaya, \
    oTransaksi.LJenisTransaksiDPLK.nama_transaksi, \
    oBiaya.LRekeningDPLK.LNasabahDPLK.no_peserta)
  
  oBiaya.isCommitted = 'T'
  oBiaya.user_id = oTransaksi.user_id
  oBiaya.user_id_auth = config.SecurityContext.UserID
  oBiaya.terminal_id = oTransaksi.terminal_id
  oBiaya.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  
  oBiaya.tgl_transaksi = config.ModLibUtils.EncodeDate(oTransaksi.tgl_transaksi[0],\
    oTransaksi.tgl_transaksi[1],oTransaksi.tgl_transaksi[2]) + \
    config.ModLibUtils.EncodeTime(oTransaksi.tgl_transaksi[3],oTransaksi.tgl_transaksi[4],\
    oTransaksi.tgl_transaksi[5],oTransaksi.tgl_transaksi[6])
  oBiaya.tgl_sistem = oBiaya.tgl_otorisasi = config.ModLibUtils.Now()

  #do charge biaya
  moduleAPI = modman.getModule(config, 'moduleapi')
  moduleAPI.ProsesChargeBiaya(config, oBiaya, nominalBiaya)
  
  return oBiaya

def ApproveOperation(config, oTransaksi): 
  oTransaksi = oTransaksi.CastToLowestDescendant()
  oRekInv = oTransaksi.LRekeningDPLK
  
  if oTransaksi.IsA("IuranPeserta"):
    #tambahkan mutasi dana di RekeningInvDPLK
    oRekInv.akum_iuran_pk += oTransaksi.mutasi_iuran_pk
    oRekInv.akum_iuran_pst += oTransaksi.mutasi_iuran_pst
    oRekInv.akum_iuran_tmb += oTransaksi.mutasi_iuran_tmb
    
    #tambahkan mutasi dana dan unit di tiap RekeningDPLK terkait investasi
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk += oDetilTransaksi.mutasi_iuran_pk
      oRekDPLK.akum_iuran_pst += oDetilTransaksi.mutasi_iuran_pst
      oRekDPLK.akum_iuran_tmb += oDetilTransaksi.mutasi_iuran_tmb
      
      Ls_DetilTransaksi.Next()
    #--
  
  elif oTransaksi.IsA("PenarikanDanaNormal"):
    #buat transaksi biaya transaksi (biaya tarik dana)
    oBiayaAdmTransaksi = CreateBiayaTransaksi(config, 'BiayaAdmTransaksi', oTransaksi, \
      oTransaksi.biaya_tarik)
    oBiayaAdmTransaksi.isPindahPaket = 'F'

    #tambahkan mutasi dana di RekeningInvDPLK
    oRekInv.akum_iuran_pk += oTransaksi.mutasi_iuran_pk
    oRekInv.akum_iuran_pst += oTransaksi.mutasi_iuran_pst
    oRekInv.akum_iuran_tmb += oTransaksi.mutasi_iuran_tmb

    #tambahkan mutasi dana dan unit di tiap RekeningDPLK terkait investasi
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk += oDetilTransaksi.mutasi_iuran_pk
      oRekDPLK.akum_iuran_pst += oDetilTransaksi.mutasi_iuran_pst
      oRekDPLK.akum_iuran_tmb += oDetilTransaksi.mutasi_iuran_tmb
      
      Ls_DetilTransaksi.Next()
    #--
    
  elif oTransaksi.IsA("PenarikanDanaPHK"):
    #buat transaksi biaya transaksi (biaya tarik dana)
    oBiayaAdmTransaksi = CreateBiayaTransaksi(config, 'BiayaAdmTransaksi', oTransaksi, \
      oTransaksi.biaya_tarik)
    oBiayaAdmTransaksi.isPindahPaket = 'F'

    #tambahkan mutasi dana di RekeningInvDPLK
    oRekInv.akum_iuran_pk += oTransaksi.mutasi_iuran_pk
    oRekInv.akum_iuran_pst += oTransaksi.mutasi_iuran_pst
    oRekInv.akum_iuran_tmb += oTransaksi.mutasi_iuran_tmb

    #tambahkan mutasi dana dan unit di tiap RekeningDPLK terkait investasi
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk += oDetilTransaksi.mutasi_iuran_pk
      oRekDPLK.akum_iuran_pst += oDetilTransaksi.mutasi_iuran_pst
      oRekDPLK.akum_iuran_tmb += oDetilTransaksi.mutasi_iuran_tmb
      
      Ls_DetilTransaksi.Next()
    #--

  elif oTransaksi.IsA("PengalihanKeDPLKLain"):
    #buat transaksi biaya pengelolaan
    oBiayaPengelolaan = CreateBiayaTransaksi(config, 'BiayaPengelolaanDana', oTransaksi, \
      oTransaksi.biaya_pengelolaan)
    
    #buat transaksi biaya administrasi
    oBiayaAdmTahunan = CreateBiayaTransaksi(config, 'BiayaAdmTahunan', oTransaksi, \
      oTransaksi.biaya_administrasi)
    
    #buat transaksi biaya transaksi (biaya pengalihan)
    oBiayaAdmTransaksi = CreateBiayaTransaksi(config, 'BiayaAdmTransaksi', oTransaksi, \
      oTransaksi.biaya_pindah)
    oBiayaAdmTransaksi.isPindahPaket = 'F'
    
    #nihilkan saldo RekeningInvDPLK
    oRekInv.akum_iuran_pk = 0.0
    oRekInv.akum_iuran_pst = 0.0
    oRekInv.akum_iuran_tmb = 0.0
    oRekInv.akum_psl = 0.0
    oRekInv.akum_pmb_pk = 0.0
    oRekInv.akum_pmb_pst = 0.0
    oRekInv.akum_pmb_tmb = 0.0
    oRekInv.akum_pmb_psl = 0.0
    
    #nihilkan saldo tiap RekeningDPLK
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk = 0.0
      oRekDPLK.akum_iuran_pst = 0.0
      oRekDPLK.akum_iuran_tmb = 0.0
      oRekDPLK.akum_psl = 0.0
      oRekDPLK.akum_pmb_pk = 0.0
      oRekDPLK.akum_pmb_pst = 0.0
      oRekDPLK.akum_pmb_tmb = 0.0
      oRekDPLK.akum_pmb_psl = 0.0
      
      Ls_DetilTransaksi.Next()
    #--
    
    #penutupan RekeningInvDPLK, samakan tgl tutup dengan tgl transaksi
    oRekInv.status_DPLK = 'N'
    oRekInv.tgl_tutup = oTransaksi.tgl_transaksi
  
  elif oTransaksi.IsA("PengalihanDariDPLKLain") or \
    oTransaksi.kode_jenis_transaksi in ('I','O','P'):
    #cek apakah pengalihan dari DPLK / DPPK / DPK?
    if oTransaksi.kode_jenis_transaksi == 'I':
      #pengalihan dari DPLK lain
      pass
    elif oTransaksi.kode_jenis_transaksi == 'O':
      #pengalihan dari DPPK lain
      pass 
    elif oTransaksi.kode_jenis_transaksi == 'P':
      #pengalihan dari DPK lain
      pass 

    oRekInv.akum_iuran_pk += oTransaksi.mutasi_iuran_pk
    oRekInv.akum_iuran_pst += oTransaksi.mutasi_iuran_pst
    oRekInv.akum_iuran_tmb += oTransaksi.mutasi_iuran_tmb
    oRekInv.akum_psl += oTransaksi.mutasi_psl

    #tambahkan mutasi dana dan unit di tiap RekeningDPLK terkait investasi
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk += oDetilTransaksi.mutasi_iuran_pk
      oRekDPLK.akum_iuran_pst += oDetilTransaksi.mutasi_iuran_pst
      oRekDPLK.akum_iuran_tmb += oDetilTransaksi.mutasi_iuran_tmb
      oRekDPLK.akum_psl += oDetilTransaksi.mutasi_psl
      
      Ls_DetilTransaksi.Next()
    #--

  #set status committed true dan data otorisasi
  oTransaksi.isCommitted = 'T'
  oTransaksi.user_id_auth = config.SecurityContext.UserID
  oTransaksi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oTransaksi.tgl_otorisasi = config.ModLibUtils.Now()

def RejectOperation(config, oTransaksi):
  oTransaksi = oTransaksi.CastToLowestDescendant()
  
  #hapus list Advis history dan detil transaksi DPLK
  if oTransaksi.IsA("TransaksiDPLK"):
    oTransaksi.Ls_AdvisHistory.DeleteAllPObjs()
    oTransaksi.Ls_DetilTransaksiDPLK.DeleteAllPObjs()
  
  #hapus objek transaksi
  oTransaksi.Delete()
    
  return 1

def GoOperasiWithMode(config, idTransaksi, mode):
  oTransaksi = config.CreatePObjImplProxy('TransaksiRekInvDPLK')
  oTransaksi.Key = idTransaksi

  if mode == 'A':
    #mode Approval
    ApproveOperation(config, oTransaksi)

  elif mode == 'R':
    #mode Rejection
    RejectOperation(config, oTransaksi)

  elif mode == 'V':
    #mode Verify, not defined yet...used in massal import
    pass

  return 1

def ProsesOtorisasi(config, idTransaksi, mode):
  config.BeginTransaction()
  try:
    GoOperasiWithMode(config, idTransaksi, mode)

    config.Commit()
    errorStatus = 0
    errorMessage = ""
  except:
    config.Rollback()
    errorStatus = 1
    errorMessage = "Gagal otorisasi transaksi: "+ str(sys.exc_info()[1])

  return errorStatus, errorMessage

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  #mode value: 'A' Approve, 'R' Reject, 'V' Verify   
  mode = parameter.FirstRecord.mode 
  idTransaksi = parameter.FirstRecord.id_transaksi
  #proses otorisasi transaksi
  errorStatus, errorMessage = ProsesOtorisasi(config, idTransaksi, mode)
  
  ds = returnpacket.AddNewDatasetEx("status", "error_status: integer; error_message: string;")
  rec = ds.AddRecord()
  rec.error_status = errorStatus
  rec.error_message = errorMessage

  return 1