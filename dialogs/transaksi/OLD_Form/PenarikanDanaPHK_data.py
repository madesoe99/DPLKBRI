import string, sys
sys.path.append('c:/dafapp/dplk07/scripts/report')
sys.path.append('c:/dafapp/dplk07/script_modules')

import AdvisTransaksi, transaksiapi

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

  #set Parameter Presisi Angka Float Default
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  recParameter.PRESISI_ANGKA_FLOAT = oP.Numeric_Value

  #set Parameter Persen Denda NPWP Default
  oP.Key = 'PERSEN_DENDA_NPWP'
  recParameter.PERSEN_DENDA_NPWP = oP.Numeric_Value

  #set field Transaksi
  uipTransaksi = uideflist.uipTransaksi
  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recTransaksi.jml_tarik = 0.0
  recTransaksi.jenis_biaya = 'T'
  recTransaksi.biaya_lain = recParameter.BiayaTunai
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
      oP = config.CreatePObject('PenarikanDanaPHK')

      #saving id transaksi, untuk kebutuhan print advis
      rec.HiddenIDTransaksi = oP.ID_Transaksi

      tgl = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
      oP.tgl_transaksi = config.ModDateTime.EncodeDate(tgl[0], tgl[1], tgl[2])

      oP.keterangan = rec.keterangan
      oP.jenis_biaya = recH.jenis_biaya
      oP.biaya_lain = recH.biaya_lain
      oP.ktr_biaya_lain = rec.ktr_biaya_lain

      oP.jml_tarik = recH.jml_tarik
      oP.biaya_tarik = recH.biaya_tarik
      oP.saldo_iuran_awal = recH.saldo_iuran_awal
      oP.saldo_iuran_akhir = recH.saldo_iuran_akhir
      oP.pajak = recH.pajak
      oP.dana_diterima = recH.dana_diterima

      #set field parent (TransaksiDPLK)
      oP.mutasi_iuran_pk = 0.0
      oP.mutasi_iuran_pst = 0.0
      oP.mutasi_pengembangan = 0.0
      oP.mutasi_peralihan = 0.0

      oP.no_peserta = recNasabah.no_peserta
      oP.kode_jenis_transaksi = 'W'
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
    raise '\nProses Error', str(sys.exc_info()[1])

  return 0

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  recT = datapacket.uipTransaksi.GetRecord(0)
  recN = datapacket.uipNasabah.GetRecord(0)
  recUI = datapacket.uipUserInfo.GetRecord(0)
  recParameter = datapacket.uipParameter.GetRecord(0)
  
  returnValue = 2
  if recUI.HitungMode:
    #mode hitung
    uideflist.PrepareReturnDataset()
    recH = uideflist.uipHitung.Dataset.AddRecord()

    recH.jml_tarik = recT.jml_tarik
    recH.saldo_iuran_awal = recN.DanaPk + recN.DanaPst
    recH.saldo_iuran_akhir = recH.saldo_iuran_awal - recH.jml_tarik
    #hasil akhirnya pasti 0.0

    #ambil Parameter Default untuk Persen Biaya Tarik PHK
    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'PERSEN_BIAYA_TARIK_PHK'
    recH.biaya_tarik = oP.Numeric_Value / 100 * recH.jml_tarik
    oP.Key = 'MIN_BIAYA_TARIK'
    minbiaya = oP.Numeric_Value
    if recH.biaya_tarik < minbiaya: recH.biaya_tarik = minbiaya

    #hitung total penarikan sebelumnya, untuk prediksi yang kena pajak
    total_sebelum = transaksiapi.TotalPenarikanSebelumnya(config, \
      recT.tgl_transaksi, recN.no_peserta)

    #hitung pajak
    recH.pajak = transaksiapi.HitungPajakTarikDana(config, \
      recH.jml_tarik - recH.biaya_tarik, total_sebelum)

    if recN.NPWP in ['', None]:
        recH.pajak = (recH.pajak) * (1 + (recParameter.PERSEN_DENDA_NPWP/100))
        
    recH.jenis_biaya = recT.jenis_biaya
    recH.biaya_lain = recT.biaya_lain
    recH.dana_diterima = (recH.jml_tarik - recH.biaya_tarik) - recH.pajak - \
      recH.biaya_lain

    returnValue = 4
  else:
    if recUI.isPrintAdvis:
      #cetak advis penarikan dana PHK
      uideflist.PrepareReturnDataset()
      recUI = uideflist.uipUserInfo.Dataset.AddRecord()

      recUI.isPrintAdvis = 1
      recUI.FileAdvis = AdvisTransaksi.CreateAdvis(config, \
        'PenarikanDanaPHK', recT.HiddenIDTransaksi)

      returnValue = 4

  return returnValue
