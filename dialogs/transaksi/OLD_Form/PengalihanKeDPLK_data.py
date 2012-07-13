import string, sys
sys.path.append('c:/dafapp/dplk/scripts/report')
sys.path.append('c:/dafapp/dplk/script_modules')

import AdvisTransaksi, transaksiapi

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config

  #set Parameter Default
  uipParameter = uideflist.uipParameter
  recParameter = uipParameter.Dataset.AddRecord()
  oP = config.CreatePObjImplProxy('Parameter')

  #set Parameter Biaya Lain
  oP.Key = 'BIAYA_SKN'
  recParameter.BiayaSKN = oP.Numeric_Value
  oP.Key = 'BIAYA_RTGS'
  recParameter.BiayaRTGS = oP.Numeric_Value

  #set field Transaksi
  uipTransaksi = uideflist.uipTransaksi
  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recTransaksi.jenis_biaya = 'S'
  recTransaksi.biaya_lain = recParameter.BiayaSKN
  #batch transaksi diset lewat FormShow saja!

  #set field untuk flag mode hitung
  uipUserInfo = uideflist.uipUserInfo
  recUserInfo = uipUserInfo.Dataset.AddRecord()
  recUserInfo.HitungMode = 1

  return 0
  
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)
  recH = data.uipHitung.GetRecord(0)
  recUI = data.uipUserInfo.GetRecord(0)
  recNasabah = data.uipNasabah.GetRecord(0)

  try:
    if recUI.HitungMode:
      #mode hitung, lanjutkan di EndProcessData
      pass
    else:
      #rec.HitungMode == 0, mode simpan
      oP = config.CreatePObject('PengalihanKeDPLKLain')

      #saving id transaksi, untuk kebutuhan print advis
      rec.HiddenIDTransaksi = oP.ID_Transaksi

      tgl = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
      oP.tgl_transaksi = config.ModDateTime.EncodeDate(tgl[0], tgl[1], tgl[2])

      oP.keterangan = rec.keterangan
      oP.kode_dp = rec.GetFieldByName('LLDP.kode_dp')
      oP.jenis_biaya = rec.jenis_biaya
      oP.biaya_lain = rec.biaya_lain
      oP.ktr_biaya_lain = rec.ktr_biaya_lain

      oP.saldo_iuran_pk = recH.saldo_iuran_pk
      oP.saldo_iuran_pst = recH.saldo_iuran_pst
      oP.saldo_pengembangan = recH.saldo_pengembangan
      oP.saldo_peralihan = recH.saldo_peralihan
      oP.saldo_jml_dana = recH.saldo_jml_dana
      oP.biaya_pengelolaan = recH.biaya_pengelolaan
      oP.biaya_administrasi = recH.biaya_administrasi
      oP.biaya_pindah = recH.biaya_pindah
      oP.saldo_dana_dipindahkan = recH.saldo_dana_dipindahkan
      oP.dana_dialihkan = recH.dana_dialihkan

      #set field parent (TransaksiDPLK)
      oP.mutasi_iuran_pk = 0.0
      oP.mutasi_iuran_pst = 0.0
      oP.mutasi_pengembangan = 0.0
      oP.mutasi_peralihan = 0.0

      oP.no_peserta = recNasabah.no_peserta
      oP.kode_jenis_transaksi = 'H'
      oP.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')

      #set status
      oP.isCommitted = 'F'
      oP.user_id = config.SecurityContext.UserID
      oP.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      oP.tgl_sistem = config.Now()
      oP.branch_code = rec.TB_BranchCode

      #assign kode paket investasi current
      transaksiapi.SetPaketInvestasi(config, oP)

      #perlu status penutupan rekening? set saat otorisasi saja!
  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  recN = datapacket.uipNasabah.GetRecord(0)
  recT = datapacket.uipTransaksi.GetRecord(0)
  recUI = datapacket.uipUserInfo.GetRecord(0)
  returnValue = 2

  if recUI.HitungMode:
    #mode hitung
    uideflist.PrepareReturnDataset()
    recH = uideflist.uipHitung.Dataset.AddRecord()

    recH.saldo_iuran_pk = recN.DanaPk
    recH.saldo_iuran_pst = recN.DanaPst
    recH.saldo_pengembangan = recN.DanaPengembangan + recN.return_reksadana + recN.return_saham
    recH.saldo_peralihan = recN.DanaPeralihan
    recH.saldo_jml_dana = recH.saldo_iuran_pk + recH.saldo_iuran_pst + \
      recH.saldo_pengembangan + recH.saldo_peralihan

    #BIAYA PENGELOLAAN DAN ADMINISTRASI DIHITUNG PROPORSIONAL
    tgl = config.ModDateTime.DecodeDate(recT.tgl_transaksi)

    #siapkan objek Parameter Biaya default
    oP = config.CreatePObjImplProxy('Parameter')
    
    recH.biaya_pengelolaan = 0.0

    #set Biaya Administrasi (Tahunan)
    oP.Key = 'BIAYA_ADM_TAHUNAN'
    recH.biaya_administrasi = oP.Numeric_Value

    #set Biaya Pindah ke DPLK lain
    oP.Key = 'PERSEN_BIAYA_PINDAH_DPLK'
    recH.biaya_pindah = (oP.Numeric_Value / 100) * recH.saldo_jml_dana

    recH.saldo_dana_dipindahkan = recH.saldo_jml_dana - recH.biaya_pengelolaan - \
      recH.biaya_administrasi - recH.biaya_pindah
    recH.jenis_biaya = recT.jenis_biaya
    recH.biaya_lain = recT.biaya_lain
    recH.dana_dialihkan = recH.saldo_dana_dipindahkan - recH.biaya_lain

    returnValue = 4
  else:
    #mode simpan
    if recUI.isPrintAdvis:
      #cetak advis pengambilan manfaat pensiun
      uideflist.PrepareReturnDataset()
      recUI = uideflist.uipUserInfo.Dataset.AddRecord()

      recUI.isPrintAdvis = 1
      recUI.FileAdvis = AdvisTransaksi.CreateAdvis(config, \
        'PengalihanKeDPLKLain', recT.HiddenIDTransaksi)

      returnValue = 4

  return returnValue
