import sys
sys.path.append('c:/dafapp/dplk/script_modules')
sys.path.append('c:/dafapp/dplk/scripts/transaction')
sys.path.append('c:/dafapp/dplk/scripts/investasi/transaksi')

import moduleapi, transaksiapi, registercif_auth, bagihasildeposito_auth_reconcile as bg

def SetKolektibilitasWasiatUmmat(config, oRekeningDPLK, oTransaksi):
  #ambil info besar premi di rekening wasiat ummat
  oRWU = moduleapi.GetRekeningWasiatUmmat(config, oRekeningDPLK.no_peserta)
  if oRWU <> None:
    selisihNominal = oTransaksi.mutasi_premi - oRWU.besar_premi
  
    if selisihNominal > 0.0:
      #ada kelebihan nominal dari besar premi yang dibayarkan
      #cek nominal kewajiban wasiat ummat
      if oRekeningDPLK.kewajiban_wasiat_ummat > 0.0:
        #masih ada sisa kewajiban sebelumnya
        sisaKewajiban = oRekeningDPLK.kewajiban_wasiat_ummat - selisihNominal
  
        #cek sisa kewajiban
        if sisaKewajiban > 0.0:
          #masih ada sisa yang belum terlunasi, jadikan sbg kewajiban yang baru
          oRekeningDPLK.kewajiban_wasiat_ummat = sisaKewajiban          
        else: 
          #sisa terlunasi semua, jika ada kelebihan dianggap sbg kelebihan
          #bayar premi peserta
          oRekeningDPLK.kewajiban_wasiat_ummat = 0.0
  
      #else: tidak ada sisa kewajiban sebelumnya, selisihNominal dianggap
      #kelebihan bayar premi peserta 
  
    if oRekeningDPLK.kewajiban_wasiat_ummat > 0.0:
      #masih ada sisa kewajiban yang belum dilunasi 
      oRekeningDPLK.collectivity_wasiat_ummat = 'F'
    else:
      #sisa kewajiban premi sudah dilunasi
      oRekeningDPLK.collectivity_wasiat_ummat = 'T'

  return 1

def CreateBiayaTransaksi(config, jenisTransaksi, classJenisBiaya, oTransaksi, \
  oRekening, valueBiaya):
  ##  KECUALI, untuk PenarikanDanaPHK: 
  ##  hanya boleh ditarik dari jumlah dana yang ditarik
  ##  dalam arti diambil dari akum_dana_iuran_pst

  oBiaya = config.CreatePObject(classJenisBiaya)
  if oTransaksi.kode_jenis_transaksi == 'W':
    #penarikanDanaPHK

    #kalkulasi mutasi biaya
    oBiaya.mutasi_iuran_pk = 0.0
    oBiaya.mutasi_iuran_pst = -valueBiaya
    oBiaya.mutasi_pengembangan = 0.0
    oBiaya.mutasi_peralihan = 0.0

    #kalkulasi akumulasi dana
    oRekening.akum_dana_iuran_pst = oRekening.akum_dana_iuran_pst - valueBiaya

    #akumulasi dana di bawah tidak diutak-utik
    #oRekening.akum_dana_iuran_pk = 0.0
    #oRekening.akum_dana_pengembangan = 0.0
    #oRekening.akum_dana_peralihan = 0.0
  else:
    #selain penarikan dana PHK
    moduleapi.TransCostOpr(config, oRekening, oBiaya, valueBiaya)

  if classJenisBiaya == 'BiayaAdmTransaksi':
    oTransaksi.ID_Transaksi_BAdmTrans = oBiaya.ID_Transaksi
    oBiaya.kode_jenis_transaksi = 'X'
    #tidak ada biaya transaksi untuk pindah paket investasi
    oBiaya.isPindahPaket = 'F'
  elif classJenisBiaya == 'BiayaPengelolaanDana':
    oTransaksi.ID_Transaksi_BPeng = oBiaya.ID_Transaksi
    oBiaya.kode_jenis_transaksi = 'C'
    oBiaya.saldo_yang_dibebani = oTransaksi.saldo_jml_dana
  elif classJenisBiaya == 'BiayaAdmTahunan':
    oTransaksi.ID_Transaksi_BAdmThn = oBiaya.ID_Transaksi
    oBiaya.kode_jenis_transaksi = 'D'

  oBiaya.no_peserta = oTransaksi.no_peserta
  oBiaya.ID_TransactionBatch = oTransaksi.ID_TransactionBatch
  oBiaya.isCommitted = 'T'
  oBiaya.user_id = oTransaksi.user_id
  oBiaya.user_id_auth = config.SecurityContext.UserID
  oBiaya.terminal_id = oTransaksi.terminal_id
  oBiaya.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oBiaya.tgl_transaksi = config.ModLibUtils.EncodeDate(oTransaksi.tgl_transaksi[0],\
    oTransaksi.tgl_transaksi[1],oTransaksi.tgl_transaksi[2])
  oBiaya.tgl_sistem = oBiaya.tgl_otorisasi = config.Now()
  oBiaya.branch_code = oTransaksi.branch_code
  oBiaya.keterangan = '%s %s peserta %s' % (classJenisBiaya, jenisTransaksi, \
    oBiaya.no_peserta)

  #assign kode paket investasi current
  transaksiapi.SetPaketInvestasi(config, oTransaksi)

  return 1

def ApproveOperation(config, jenisTransaksi, idTransaksi):
  config.SendDebugMsg('aprv1')
  o = config.CreatePObjImplProxy(jenisTransaksi)
  o.Key = idTransaksi
  
  config.SendDebugMsg('aprv1')
  if jenisTransaksi == 'IuranPendaftaran':
    config.SendDebugMsg('aprv2')
    #set status iuran pendaftaran rekening DPLK
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = o.no_peserta
    oR.status_biaya_daftar = 'T'
  
  elif jenisTransaksi == 'IuranPeserta':
    config.SendDebugMsg('aprv3')
    #tambahkan mutasi dana di rekening DPLK
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = o.no_peserta
    oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk + o.mutasi_iuran_pk
    oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + o.mutasi_iuran_pst
    oR.akum_dana_iuran_tambahan = oR.akum_dana_iuran_tambahan + o.mutasi_iuran_tambahan
    oR.unit_iuran_pk = oR.unit_iuran_pk + o.unit_iuran_pk
    oR.unit_iuran_pst = oR.unit_iuran_pst + o.unit_iuran_pst
    oR.unit_iuran_tambahan = oR.unit_iuran_tambahan + o.unit_iuran_tambahan

    oRN = config.CreatePObjImplProxy('RekeningNasabah')
    oRN.Key = oR.nomor_rekening
    oRN.akum_dana_iuran_pk = oRN.akum_dana_iuran_pk + o.mutasi_iuran_pk
    oRN.akum_dana_iuran_pst = oRN.akum_dana_iuran_pst + o.mutasi_iuran_pst
    oRN.akum_dana_iuran_tambahan = oRN.akum_dana_iuran_tambahan + o.mutasi_iuran_tambahan
    oRN.unit_iuran_pk = oRN.unit_iuran_pk + o.unit_iuran_pk
    oRN.unit_iuran_pst = oRN.unit_iuran_pst + o.unit_iuran_pst
    oRN.unit_iuran_tambahan = oRN.unit_iuran_tambahan + o.unit_iuran_tambahan
    
    oP = config.CreatePObjImplProxy('PaketInvestasi')
    oP.Key = oR.kode_paket_investasi
    oP.saldo_paket = oP.saldo_paket + o.mutasi_iuran_pk + o.mutasi_iuran_pst + o.mutasi_iuran_tambahan
    oP.unit = oP.unit + o.unit_iuran_pk + o.unit_iuran_pst + o.unit_iuran_tambahan
    
  elif jenisTransaksi == 'PenarikanDanaNormal':
    config.SendDebugMsg('aprv4')
    #tambahkan mutasi dana ke akumulasi dana di rekening
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = o.no_peserta

    #buat BiayaAdmTransaksi (biaya tarik)
    CreateBiayaTransaksi(config, jenisTransaksi, 'BiayaAdmTransaksi', o, oR, \
      o.biaya_tarik)

    #kalkulasi mutasi
    o.mutasi_iuran_pk = 0.0
    o.mutasi_iuran_pst = -o.jml_tarik 
    o.mutasi_pengembangan = 0.0
    o.mutasi_peralihan = 0.0

    #kalkulasi akumulasi dana
    oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk + o.mutasi_iuran_pk
    oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + o.mutasi_iuran_pst
    oR.akum_dana_pengembangan = oR.akum_dana_pengembangan + o.mutasi_pengembangan
    oR.akum_dana_peralihan = oR.akum_dana_peralihan + o.mutasi_peralihan

  elif jenisTransaksi == 'PenarikanDanaPHK':
    config.SendDebugMsg('aprv5')
    #kalkulasi mutasi dana ke akumulasi dana di rekening
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = o.no_peserta

    #buat BiayaAdmTransaksi (biaya tarik)
    CreateBiayaTransaksi(config, jenisTransaksi, 'BiayaAdmTransaksi', o, oR, \
      o.biaya_tarik)
    
    #kalkulasi mutasi
    o.mutasi_iuran_pk = -oR.akum_dana_iuran_pk
    o.mutasi_iuran_pst = oR.akum_dana_iuran_pk - (o.jml_tarik - o.biaya_tarik) 
    o.mutasi_pengembangan = 0.0
    o.mutasi_peralihan = 0.0
    
    #kalkulasi akumulasi dana
    oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + o.mutasi_iuran_pst
    oR.akum_dana_iuran_pk = 0.0
    
    #akumulasi dana di bawah tidak diutak-utik
    #oR.akum_dana_pengembangan = 0.0
    #oR.akum_dana_peralihan = 0.0  

  elif jenisTransaksi == 'PengalihanDariDPLKLain':
    config.SendDebugMsg('aprv6')
    #tambahkan mutasi dana ke akumulasi dana di rekening
    #script ini digunakan juga untuk pengalihan dari DPLK, DPPK, dan DPK lain
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = o.no_peserta

    oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk + o.mutasi_iuran_pk
    oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + o.mutasi_iuran_pst
    oR.akum_dana_pengembangan = oR.akum_dana_pengembangan + o.mutasi_pengembangan
    oR.akum_dana_peralihan = oR.akum_dana_peralihan + o.mutasi_peralihan
    oR.unit_iuran_pk = oR.unit_iuran_pk + o.unit_iuran_pk
    oR.unit_iuran_pst = oR.unit_iuran_pst + o.unit_iuran_pst
    oR.unit_iuran_tambahan = oR.unit_iuran_tambahan + o.unit_iuran_tambahan
    oR.unit_iuran_psl = oR.unit_iuran_psl + o.unit_iuran_psl

    oRN = config.CreatePObjImplProxy('RekeningNasabah')
    oRN.Key = oR.nomor_rekening
    oRN.akum_dana_iuran_pk = oRN.akum_dana_iuran_pk + o.mutasi_iuran_pk
    oRN.akum_dana_iuran_pst = oRN.akum_dana_iuran_pst + o.mutasi_iuran_pst
    oRN.akum_dana_iuran_tambahan = oRN.akum_dana_iuran_tambahan + o.mutasi_iuran_tambahan
    oRN.akum_dana_iuran_psl = oRN.akum_dana_iuran_psl + o.mutasi_peralihan
    oRN.unit_iuran_pk = oRN.unit_iuran_pk + o.unit_iuran_pk
    oRN.unit_iuran_pst = oRN.unit_iuran_pst + o.unit_iuran_pst
    oRN.unit_iuran_tambahan = oRN.unit_iuran_tambahan + o.unit_iuran_tambahan
    oRN.unit_iuran_psl= oRN.unit_iuran_psl + o.unit_iuran_psl
    
    oP = config.CreatePObjImplProxy('PaketInvestasi')
    oP.Key = oR.kode_paket_investasi
    oP.saldo_paket = oP.saldo_paket + o.mutasi_iuran_pk + o.mutasi_iuran_pst + o.mutasi_iuran_tambahan + o.mutasi_peralihan
    oP.unit = oP.unit + o.unit_iuran_pk + o.unit_iuran_pst + o.unit_iuran_tambahan + o.unit_iuran_psl
      
  elif jenisTransaksi == 'PengalihanKeDPLKLain':
    config.SendDebugMsg('aprv7')
    #kurangkan mutasi dana ke akumulasi dana di rekening
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = o.no_peserta
    
    #buat biayaPengelolaanDana
    CreateBiayaTransaksi(config, jenisTransaksi, 'BiayaPengelolaanDana', o, oR, \
      o.biaya_pengelolaan)
    
    #buat biayaAdmTahunan
    CreateBiayaTransaksi(config, jenisTransaksi, 'BiayaAdmTahunan', o, oR, \
      o.biaya_administrasi)
    
    #buat BiayaAdmTransaksi (biaya pengalihan)
    CreateBiayaTransaksi(config, jenisTransaksi, 'BiayaAdmTransaksi', o, oR, \
      o.biaya_pindah)
    
    #kalkulasi mutasi
    o.mutasi_iuran_pk = -oR.akum_dana_iuran_pk
    o.mutasi_iuran_pst = -oR.akum_dana_iuran_pst
    o.mutasi_pengembangan = -oR.akum_dana_pengembangan
    o.mutasi_peralihan = -oR.akum_dana_peralihan
    
    #kalkulasi akumulasi dana
    oR.akum_dana_iuran_pk = 0.0
    oR.akum_dana_iuran_pst = 0.0
    oR.akum_dana_pengembangan = 0.0
    oR.akum_dana_peralihan = 0.0

    #penutupan rekening, tanggal tutup samakan dengan tanggal transaksi
    oR.status_DPLK = 'N'
    oR.tgl_tutup = config.ModDateTime.EncodeDate(o.tgl_transaksi[0], \
      o.tgl_transaksi[1], o.tgl_transaksi[2])
  
  elif jenisTransaksi == 'TitipanPremi':
    config.SendDebugMsg('aprv8')
    #cek kewajiban wasiat ummat dan status kolektibilitas
    SetKolektibilitasWasiatUmmat(config, o.LRekeningDPLK, o)

  elif jenisTransaksi == 'TransaksiDPLK':
    config.SendDebugMsg('aprv9')
    #KASUS KHUSUS, perlu pengecekan kode jenis transaksinya 
    if o.kode_jenis_transaksi == 'F':
      oR = o.LRekeningDPLK
     
      #tambahkan mutasi dana ke akumulasi dana di rekening
      oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk + o.mutasi_iuran_pk
      oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + o.mutasi_iuran_pst
      oR.akum_dana_pengembangan = oR.akum_dana_pengembangan + o.mutasi_pengembangan
      oR.akum_dana_peralihan = oR.akum_dana_peralihan + o.mutasi_peralihan

  elif jenisTransaksi == 'TransaksiDPLKManual':
    config.SendDebugMsg('aprv10')
    #tambahkan mutasi dana ke akumulasi dana di rekening
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = o.no_peserta

    oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk + o.mutasi_iuran_pk
    oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + o.mutasi_iuran_pst
    oR.akum_dana_pengembangan = oR.akum_dana_pengembangan + o.mutasi_pengembangan
    oR.akum_dana_peralihan = oR.akum_dana_peralihan + o.mutasi_peralihan

  elif jenisTransaksi == 'TransaksiPremiManual':
    #belum perlu untuk mengeset objek lain
    pass
  
  elif jenisTransaksi == 'PengambilanManfaat':
    config.SendDebugMsg('aprv11')
    #kurangkan mutasi dana ke akumulasi dana di rekening
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = o.no_peserta
    
    #buat biayaPengelolaanDana
    CreateBiayaTransaksi(config, jenisTransaksi, 'BiayaPengelolaanDana', o, oR, \
      o.biaya_pengelolaan)
    
    #buat biayaAdmTahunan
    CreateBiayaTransaksi(config, jenisTransaksi, 'BiayaAdmTahunan', o, oR, \
      o.biaya_administrasi)
    
    #buat BiayaAdmTransaksi (biaya bila dana mengendap < 1th)
    CreateBiayaTransaksi(config, jenisTransaksi, 'BiayaAdmTransaksi', o, oR, \
      o.biaya_pencairan)
    
    #kalkulasi mutasi
    o.mutasi_iuran_pk = -oR.akum_dana_iuran_pk
    o.mutasi_iuran_pst = -oR.akum_dana_iuran_pst
    o.mutasi_pengembangan = -oR.akum_dana_pengembangan
    o.mutasi_peralihan = -oR.akum_dana_peralihan
    
    #kalkulasi akumulasi dana
    oR.akum_dana_iuran_pk = 0.0
    oR.akum_dana_iuran_pst = 0.0
    oR.akum_dana_pengembangan = 0.0
    oR.akum_dana_peralihan = 0.0
    
    #penutupan rekening, tanggal tutup samakan dengan tanggal transaksi
    oR.status_DPLK = 'N'
    oR.tgl_tutup = config.ModDateTime.EncodeDate(o.tgl_transaksi[0], \
      o.tgl_transaksi[1], o.tgl_transaksi[2])
      
    #checking untuk pembuatan register anuitas
    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'PRESISI_ANGKA_FLOAT'
    if o.manfaat_anuitas > oP.Numeric_Value:
      #buatkan register anuitas untuk peserta
      oRA = config.CreatePObject('RegisterAnuitas')
      oRA.nominal_anuitas = o.manfaat_anuitas
      oRA.keterangan = 'register bersamaan dengan Pengambilan Manfaat peserta ' +\
        o.no_peserta
      oRA.terminal_id = o.terminal_id
      oRA.kode_jenis_registercif = 'N'
      oRA.no_peserta = o.no_peserta
      oRA.user_id = o.user_id
      
      #tanggal register samakan dengan tanggal transaksi
      oRA.tanggal_register = config.ModDateTime.EncodeDate(o.tgl_transaksi[0], \
        o.tgl_transaksi[1], o.tgl_transaksi[2])
        
      #set status anuitas rekening DPLK
      oR.status_anuitas = 'F'
    
    #checking ikut Autodebet dan Wasiat Ummat
    oN = config.CreatePObjImplProxy('NasabahDPLK')
    oN.Key = o.no_peserta

    config.SendDebugMsg('aprv12')
    #cek status autodebet
    if oR.status_autodebet == 'T':
      #peserta ikut autodebet, tutup sekalian autodebetnya      
      oRAD = registercif_auth.GetRekeningAutoDebetByNasabah(config, oN)      
      registercif_auth.CreateHistoriAutodebet(config, oN, oRAD, 'TarikManfaat')
      registercif_auth.UpdateStatusAutodebetOut(config, oRAD)

    config.SendDebugMsg('aprv13')
    #cek status wasiat ummat
    if oR.status_wasiat_ummat == 'T':
      #peserta ikut wasiat ummat, tutup sekalian keikutsertaan wasiat ummat
      oRWU = registercif_auth.GetRekeningWasiatUmmatByNasabah(config, oN)
      registercif_auth.CreateHistoriWasiatUmmat(config, oN, oRWU, \
        'TarikManfaat', 'Telah memasuki usia pensiun', \
        'Penutupan bersamaan dengan penarikan manfaat')
      registercif_auth.UpdateStatusWasiatUmmatOut(config, oN, oRWU)
    config.SendDebugMsg('aprv14')

  #elif yang lain

  elif jenisTransaksi == 'TransLRInvestasi':
    bg.AuthBaghasDepo(config, idTransaksi)
    
  #set status committed true dan data otorisasi
  o.isCommitted = 'T'
  o.user_id_auth = config.SecurityContext.UserID
  o.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  o.tgl_otorisasi = config.Now()
  config.SendDebugMsg('aprv15')

  return 1

def RejectOperation(config, jenisTransaksi, idTransaksi):
  o = config.CreatePObjImplProxy(jenisTransaksi)
  o.Key = idTransaksi
  
  #hapus list Advis history
  if o.IsA("TransaksiDPLK"):
    o.Ls_AdvisHistory.DeleteAllPObjs()
  
  #hapus objek transaksi
  o.Delete()
    
  return 1

def AuthorizeOperationNonTrans(config, jenisTransaksi, idTransaksi, mode):
  config.SendDebugMsg('AuthorizeOperationNonTrans')
  if mode == 'A':
    #mode Approval
    status = ApproveOperation(config, jenisTransaksi, idTransaksi)

  elif mode == 'R':
    #mode Rejection
    status = RejectOperation(config, jenisTransaksi, idTransaksi)

  elif mode == 'V':
    #mode Verify, not defined yet...used in massal import
    pass

  return status

def AuthorizeOperation(config, jenisTransaksi, idTransaksi, mode):
  config.BeginTransaction()
  try:
    status = AuthorizeOperationNonTrans(config, jenisTransaksi, idTransaksi, mode)

    config.Commit()  
  except:
    config.Rollback()
    raise

  return status

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  jenisTransaksi = parameter.FirstRecord.jenistransaksi
  idTransaksi = parameter.FirstRecord.idtransaksi
  
  #mode value: 'A' Approve, 'R' Reject, 'V' Verify   
  mode = parameter.FirstRecord.mode 
  
  #execute authorize operation
  succeedStatus = AuthorizeOperation(config, jenisTransaksi, idTransaksi, mode)
  
  returnpacket.CreateValues(['status',succeedStatus])

  return 1