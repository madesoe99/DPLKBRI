import string, sys, time
sys.path.append('c:/dafapp/dplk07/scripts/report')
sys.path.append('c:/dafapp/dplk07/script_modules')

import AdvisTransaksi, transaksiapi

def FormBeginSetData(uideflist, uipNasabah, key):
  config = uideflist.config
  recJM = uideflist.uipJenisManfaat.Dataset.AddRecord()
  
  #inisialisasi
  keepGoingProcess = 1
  recJM.isDipercepatAllowed = 0
  recJM.isBiasaAllowed = 0

  #checking tanggal pensiun (pensiun dipercepat) peserta
  try:
    #ambil no_peserta
    noPeserta = string.split(key, '=')[1]

    #ambil tanggal pensiun dipercepat peserta
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = noPeserta

    tglNow = time.localtime()[:3]
    #bandingkan tanggal sekarang dengan tanggal pensiun
    if tglNow < oR.tgl_pensiun_dipercepat[:3]:
      #belum memasuki tanggal pensiun dipercepat sekalipun
      #hanya boleh pensiun cacat atau meninggal, do nothing
      pass

    elif (tglNow >= oR.tgl_pensiun_dipercepat[:3]) and \
      (tglNow < oR.tgl_pensiun[:3]):
      #berada diantara tgl pensiun dipercepat dan pensiun biasa
      #boleh pensiun cacat, meninggal atau dipercepat (tinggal set dipercepat)
      recJM.isDipercepatAllowed = 1
    else:
      #bisa semua jenis manfaat pensiun
      recJM.isDipercepatAllowed = 1
      recJM.isBiasaAllowed = 1
  except:
    raise

  return keepGoingProcess

def FormEndSetData(uideflist, uiname, objdata):

  config = uideflist.config

  #set Parameter Default
  uipParameter = uideflist.uipParameter
  recParameter = uipParameter.Dataset.AddRecord()
  oP = config.CreatePObjImplProxy('Parameter')

  #set Parameter Biaya Lain
  oP.Key = 'BIAYA_TUNAI'
  recParameter.BiayaTunai = oP.Numeric_Value
  oP.Key = 'BIAYA_SKN'
  recParameter.BiayaSKN = oP.Numeric_Value
  oP.Key = 'BIAYA_RTGS'
  recParameter.BiayaRTGS = oP.Numeric_Value
  oP.Key = 'BIAYA_PINDAH_BUKU'
  recParameter.BiayaPindahBuku = oP.Numeric_Value

  #set Parameter Jumlah hari dalam setahun
  oP.Key = 'JUMLAH_HARI_SETAHUN'
  recParameter.JUMLAH_HARI_SETAHUN = oP.Numeric_Value

  #set Parameter Presisi Angka Float Default
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  recParameter.PRESISI_ANGKA_FLOAT = oP.Numeric_Value
  
  oP.Key = 'PERSEN_DENDA_NPWP'
  recParameter.PERSEN_DENDA_NPWP = oP.Numeric_Value

  #set field Transaksi
  recTransaksi = uideflist.uipTransaksi.Dataset.AddRecord()
  recTransaksi.jenis_biaya = 'T'
  recTransaksi.biaya_lain = recParameter.BiayaTunai
  recTransaksi.CekAturanMenkeu = 1
  #batch transaksi diset lewat FormShow saja!

  #set field untuk flag mode hitung
  recUserInfo = uideflist.uipUserInfo.Dataset.AddRecord()
  recUserInfo.HitungMode = 1

  #cek jika ada dana pengalihan yang mengendap kurang dari 1 tahun
  
  dtTglSetahunlalu = config.ModLibUtils.Now() - recParameter.JUMLAH_HARI_SETAHUN
  y,m,d = config.ModLibUtils.DecodeDate(dtTglSetahunlalu)
  sTglSetahunLalu = '%d-%d-%d' % (y,m,d)
  
  #ambil no_peserta
  noPeserta = string.split(objdata,'=')[1]
  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.Key = noPeserta

  #cek memakai SQL
  sSQL = 'select t.tgl_transaksi, t.KODE_JENIS_TRANSAKSI, '\
                 'isnull(sum(t.MUTASI_IURAN_PST),0.0) as sum_mutasi_iuran_pst, '\
                 'isnull(sum(t.MUTASI_IURAN_PK), 0.0) as sum_mutasi_iuran_pk, '\
                 'isnull(sum(t.MUTASI_PENGEMBANGAN),0.0) as sum_mutasi_pengembangan, '\
                 'isnull(sum(t.MUTASI_PERALIHAN),0.0) as sum_mutasi_peralihan '\
         'from TRANSAKSIDPLK t '\
         'where t.NO_PESERTA = \'%s\' and '\
                '( (t.KODE_JENIS_TRANSAKSI in (\'I\',\'O\',\'P\')) or '\
                '(t.KODE_JENIS_TRANSAKSI = \'M\' and t.KODE_TRANSAKSI_MANUAL in (\'I\',\'O\',\'P\')) ) and '\
                't.TGL_TRANSAKSI >= \'%s\' '\
         'group by t.tgl_transaksi, t.KODE_JENIS_TRANSAKSI' \
         % (noPeserta, sTglSetahunLalu)
  config.SendDebugMsg(sSQL)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  #set inisialisasi untuk mutasi-mutasinya yang < 1 tahun
  recTransaksi.SumKurangSetahunMutasiIuran = 0.0
  recTransaksi.SumKurangSetahunMutasiPengembangan = 0.0
  recTransaksi.SumKurangSetahunMutasiPeralihan = 0.0
  recTransaksi.skip_pajak = 'F'

  rSQL.First()
  while not rSQL.Eof:
    recTransaksi.SumKurangSetahunMutasiPeralihan += rSQL.sum_mutasi_peralihan + rSQL.sum_mutasi_iuran_pst + \
      rSQL.sum_mutasi_iuran_pk + rSQL.sum_mutasi_pengembangan

    rSQL.Next()
    
  #sementara di by pass
  if noPeserta == '12199000285':
     recTransaksi.SumKurangSetahunMutasiPeralihan = 64590466.61
     
  recTransaksi.isAdaKurangSetahunPengalihan = \
    recTransaksi.SumKurangSetahunMutasiPeralihan > 0.0

  return 0

def CekTglPensiunDipercepat(config, jenisMP, tgl_pensiun_dipercepat):
    y,m,d = time.localtime()[:3]
    tglNow = config.ModLibUtils.EncodeDate(y,m,d)
    if tglNow < tgl_pensiun_dipercepat and jenisMP in ('B','D'):
        raise Exception, 'Peringatan!' + 'Peserta belum mencapai tanggal pensiun dipercepat'
    
def FormGeneralProcessData(uideflist, data):

  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)
  recH = data.uipHitung.GetRecord(0)
  recUI = data.uipUserInfo.GetRecord(0)
  recNasabah = data.uipNasabah.GetRecord(0)

  try:
    CekTglPensiunDipercepat(config, rec.GetFieldByName('Ljenis_penerimaan_manfaat.kode_jns_manfaat'), recNasabah.TglPensiunDipercepat)
    if recUI.HitungMode:
      #mode hitung, lanjutkan di EndProcessData
      pass

    else:      
      #rec.HitungMode == 0, mode simpan
      oP = config.CreatePObject('PengambilanManfaat')

      #saving id transaksi, untuk kebutuhan print advis
      rec.HiddenIDTransaksi = oP.ID_Transaksi

      tgl = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
      oP.tgl_transaksi = config.ModDateTime.EncodeDate(tgl[0], tgl[1], tgl[2])

      oP.keterangan = rec.keterangan
      oP.kode_jns_manfaat = rec.GetFieldByName('Ljenis_penerimaan_manfaat.kode_jns_manfaat')
      oP.ahliwaris_id = rec.GetFieldByName('LAhliWaris.ahliwaris_id')
      if rec.nama_anuitas != '' or rec.nama_anuitas != None:
        oP.nama_anuitas = rec.nama_anuitas
      oP.jenis_biaya = recH.jenis_biaya
      oP.biaya_lain = recH.biaya_lain
      oP.saldo_peralihan_1th = recH.pengalihan_bwh1th

      oP.saldo_iuran_pk = recH.saldo_iuran_pk
      oP.saldo_iuran_pst = recH.saldo_iuran_pst
      oP.saldo_pengembangan = recH.saldo_pengembangan
      oP.saldo_peralihan = recH.saldo_peralihan
      oP.saldo_jml_dana = recH.saldo_jml_dana
      
      oP.biaya_pencairan = recH.biaya_pencairan
      oP.biaya_pengelolaan = recH.biaya_pengelolaan
      oP.biaya_administrasi = recH.biaya_administrasi

      oP.saldo_manfaat = recH.saldo_manfaat
      oP.pajak = recH.pajak
      
      oP.manfaat_stlh_pajak = recH.manfaat_stlh_pajak
      oP.manfaat_tunai = recH.manfaat_tunai
      oP.manfaat_anuitas = recH.manfaat_anuitas

      oP.manfaat_tunai_diterima = recH.manfaat_tunai_diterima

      #set field parent (TransaksiDPLK)
      oP.mutasi_iuran_pk = 0.0
      oP.mutasi_iuran_pst = 0.0
      oP.mutasi_pengembangan = 0.0
      oP.mutasi_peralihan = 0.0

      oP.no_peserta = recNasabah.no_peserta
      oP.kode_jenis_transaksi = 'J'
      oP.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')

      #set status
      oP.isCommitted = 'F'
      oP.user_id = config.SecurityContext.UserID
      oP.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      oP.tgl_sistem = config.Now()
      oP.branch_code = rec.TB_BranchCode

      #assign kode paket investasi current
      transaksiapi.SetPaketInvestasi(config, oP)

  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  recT = datapacket.uipTransaksi.GetRecord(0)
  recN = datapacket.uipNasabah.GetRecord(0)
  recUI = datapacket.uipUserInfo.GetRecord(0)
  returnValue = 2

  if recUI.HitungMode:
    #mode hitung
    uideflist.PrepareReturnDataset()
    recH = uideflist.uipHitung.Dataset.AddRecord()

    recH.saldo_iuran_pk = recN.DanaPk
    recH.saldo_iuran_pst = recN.DanaPst
    recH.saldo_pengembangan = recN.DanaPengembangan
    recH.saldo_peralihan = recN.DanaPeralihan
    recH.saldo_jml_dana = recH.saldo_iuran_pk + recH.saldo_iuran_pst + \
      recH.saldo_pengembangan + recH.saldo_peralihan
    recH.pengalihan_bwh1th = recT.SumKurangSetahunMutasiPeralihan

    #siapkan objek Parameter Biaya default
    oP = config.CreatePObjImplProxy('Parameter')

    oP.Key = 'PSN_CM_ALIH_<1TH'
    persenCairAlih1Th = oP.Numeric_Value

    #oP.Key = 'PERSEN_CAIR_MANFAAT_>=1TH'
    #persenCairUmum = oP.Numeric_Value
    #oP.Key = 'PERSEN_CAIR_MANFAAT_<1TH'
    #persenCairKurangSetahun = oP.Numeric_Value

    if recT.isAdaKurangSetahunPengalihan:
      #ada pengalihan dana yang mengendap kurang dari 1 tahun
      recH.biaya_pencairan = (persenCairAlih1Th / 100) * recT.SumKurangSetahunMutasiPeralihan
    else:
      #tidak ada pengalihan dana yang mengendap kurang dari 1 tahun
      #biaya pencairan nol, hanya dikenakan biaya pengelolaan
      recH.biaya_pencairan = 0.0

    #BIAYA PENGELOLAAN DAN ADMINISTRASI DIHITUNG PROPORSIONAL
    tgl = config.ModDateTime.DecodeDate(recT.tgl_transaksi)
    proporsiBiaya = transaksiapi.HitungProporsiBiaya(config, 'C', \
      recN.no_peserta, tgl)
    # biaya pengelolaan dihitung proporsional
    oP.Key = 'PERSEN_BIAYA_PENGELOLAAN'
    #recH.biaya_pengelolaan = proporsiBiaya * (oP.Numeric_Value / 100) * (recH.saldo_jml_dana - recH.pengalihan_bwh1th)

    #Tambahan By Ade - 2009-05-28
    if recH.saldo_jml_dana < 100000001:
       oP.Numeric_Value = 1.25
    else:
       oP.Numeric_Value = 1

    recH.biaya_pengelolaan = proporsiBiaya * (oP.Numeric_Value / 100) * (recH.saldo_jml_dana - recH.pengalihan_bwh1th)
    #---------- End By Ade


    # biaya administrasi tidak dihitung proporsional
    oP.Key = 'BIAYA_ADM_TAHUNAN'
    #recH.biaya_administrasi = oP.Numeric_Value
    
    #Tambahan By Ade - 2009-05-27
    blnTrans = int(tgl[1])
    if blnTrans <= 6:       
       recH.biaya_administrasi = (blnTrans*1500)
    else:
       recH.biaya_administrasi = ((blnTrans-6)*1500)
    #---------- End By Ade
       
    recH.saldo_manfaat = recH.saldo_jml_dana - recH.biaya_pencairan - \
      recH.biaya_pengelolaan - recH.biaya_administrasi

    #set pajak
    if recT.skip_pajak == 'T':
      recH.pajak = 0.0
    else:
      recH.pajak = transaksiapi.HitungPajakPengambilanManfaat(config, recH.saldo_manfaat)
      oP.Key = 'PERSEN_DENDA_NPWP'
      if recN.NPWP in ['','-', None]:
          recH.pajak = (recH.pajak) * (1 + (oP.Numeric_Value/100))      

    recH.manfaat_stlh_pajak = recH.saldo_manfaat - recH.pajak
    
    #PENENTUAN BESAR MANFAAT TUNAI DAN MANFAAT ANUITAS
    oP.Key = 'BATAS_MANFAAT_KENA_ANUITAS'
    kode_jenis_manfaat = recT.GetFieldByName('Ljenis_penerimaan_manfaat.kode_jns_manfaat')
    if recT.CekAturanMenkeu and recH.manfaat_stlh_pajak >= oP.Numeric_Value and kode_jenis_manfaat <> 'J':
      oP.Key = 'PERSEN_BATAS_TUNAI_MANFAAT'
      recH.manfaat_tunai = recH.manfaat_stlh_pajak * oP.Numeric_Value / 100
      recH.manfaat_anuitas = recH.manfaat_stlh_pajak - recH.manfaat_tunai
    else:
      recH.manfaat_tunai = recH.manfaat_stlh_pajak
      recH.manfaat_anuitas = 0.0

    recH.jenis_biaya = recT.jenis_biaya
    recH.biaya_lain = recT.biaya_lain
    recH.manfaat_tunai_diterima = recH.manfaat_tunai - recH.biaya_lain

    returnValue = 4
  else:
    #mode simpan
    if recUI.isPrintAdvis:
      #cetak advis pengambilan manfaat pensiun
      uideflist.PrepareReturnDataset()
      recUI = uideflist.uipUserInfo.Dataset.AddRecord()

      recUI.isPrintAdvis = 1
      recUI.FileAdvis = AdvisTransaksi.CreateAdvis(config, \
        'PengambilanManfaat', recT.HiddenIDTransaksi)

      returnValue = 4

  return returnValue

