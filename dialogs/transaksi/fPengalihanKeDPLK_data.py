import sys
import com.ihsan.util.modman as modman

def downloadFile(config, parameter, returns):
  fileName = config.UserHomeDirectory + parameter.FirstRecord.fileName
  sw = returns.AddStreamWrapper()
  sw.LoadFromFile(fileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(fileName)

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config
  transaksiAPI = modman.getModule(config, 'transaksiapi')

  recParameterForm = parameterForm.FirstRecord
  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recParameterForm.no_peserta)
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  uipTransaksi = uideflist.uipTransaksi
  uipPeserta = uideflist.uipPeserta
  uipRekening = uideflist.uipRekening
  uipParameter = uideflist.uipParameter
  
  # CEK USER LOGIN (UNTUK KEPERLUAN HAK AKSES)

  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recPeserta = uipPeserta.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)
  recParameter = uipParameter.Dataset.AddRecord()
  
  #cek rekening investasi DPLK
  if recRekening.operation_code != 'F':
    raise Exception, "Rekening DPLK peserta berstatus Sedang Diubah. Transaksi tidak diperbolehkan!"

  #set parameter default
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'
  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  recParameter.JUMLAH_HARI_SETAHUN = oParameter.Numeric_Value

  oParameter.Key = 'BIAYA_SKN'
  recParameter.BiayaSKN = oParameter.Numeric_Value
  oParameter.Key = 'BIAYA_RTGS'
  recParameter.BiayaRTGS = oParameter.Numeric_Value
  oParameter.Key = 'BIAYA_TUNAI'
  recParameter.BiayaTunai = oParameter.Numeric_Value
  oParameter.Key = 'BIAYA_PINDAH_BUKU'
  recParameter.BiayaPindahBuku = oParameter.Numeric_Value

  oParameter.Key = 'MIN_KEPESERTAAN_ALIH_KELUAR'
  recParameter.MIN_KEPESERTAAN_ALIH_KELUAR = oParameter.Numeric_Value

  #cek parameter default atau parameter korporat
  if recPeserta.kode_nasabah_corporate not in (None,''):
    #pakai parameter korporat
    listParameterKey =[]
    dictParameterKorporat = transaksiAPI.GetParameterCorporate(config, \
      recPeserta.kode_nasabah_corporate, listParameterKey)
    
    recParameter.BiayaADM = dictParameterKorporat['BIAYA_ADM_TAHUNAN'][1]
    recParameter.PERSEN_BIAYA_PENGELOLAAN = dictParameterKorporat['PERSEN_BIAYA_PENGELOLAAN'][1]
   
    recParameter.MODUS_BIAYA_PINDAH_DPLK = dictParameterKorporat['MODUS_BIAYA_PINDAH_DPLK'][0]
    recParameter.FIX_BIAYA_PINDAH_DPLK = dictParameterKorporat['FIX_BIAYA_PINDAH_DPLK'][1]
    recParameter.BiayaPindah = dictParameterKorporat['PERSEN_BIAYA_PINDAH_DPLK'][1]

    recParameter.MIN_KEPESERTAAN_ALIH_KELUAR = dictParameterKorporat['MIN_KEPESERTAAN_ALIH_KELUAR'][1]
  else:
    #pakai parameter default aplikasi
    oParameter.Key = 'BIAYA_ADM_TAHUNAN'
    recParameter.BiayaADM = oParameter.Numeric_Value
    oParameter.Key = 'PERSEN_BIAYA_PENGELOLAAN'
    recParameter.PERSEN_BIAYA_PENGELOLAAN = oParameter.Numeric_Value
   
    oParameter.Key = 'MODUS_BIAYA_PINDAH_DPLK'
    recParameter.MODUS_BIAYA_PINDAH_DPLK = oParameter.Varchar_Value
    oParameter.Key = 'FIX_BIAYA_PINDAH_DPLK'
    recParameter.FIX_BIAYA_PINDAH_DPLK = oParameter.Numeric_Value
    oParameter.Key = 'PERSEN_BIAYA_PINDAH_DPLK'
    recParameter.BiayaPindah = oParameter.Numeric_Value
    
    oParameter.Key = 'MIN_KEPESERTAAN_ALIH_KELUAR'
    recParameter.MIN_KEPESERTAAN_ALIH_KELUAR = oParameter.Numeric_Value
  
  recParameter.isHitungMode = 1

  #cek masa kepesertaan
  minMasaKepesertaan = recParameter.MIN_KEPESERTAAN_ALIH_KELUAR * recParameter.JUMLAH_HARI_SETAHUN
  transaksiAPI.CekMasaKepesertaan(config, recParameterForm.no_rekening, minMasaKepesertaan)

  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  #set field Data Transaksi
  recTransaksi.tgl_transaksi = config.ModLibUtils.Now()
  #alternatif: model tanggal transaksi tanpa NOW
  #recTransaksi.tgl_transaksi = config.ModLibUtils.CutDate(config.ModLibUtils.Now())
  recTransaksi.jenis_biaya = 'S'
  recTransaksi.biaya_lain = recParameter.BiayaSKN
  
  #do get proporsi biaya untuk biaya pengelolaan dan biaya administrasi
  transaksiAPI = modman.getModule(config, 'transaksiapi')
  recParameter.proporsiHari = transaksiAPI.HitungProporsiHariSebulan(config, recTransaksi.tgl_transaksi)
  
def SimpanTransaksi(config, params, returns):
  recT = params.uipTransaksi.GetRecord(0)
  recP = params.uipPeserta.GetRecord(0)
  recR = params.uipRekening.GetRecord(0) 
  recH = params.uipHitung.GetRecord(0) 
  
  config.BeginTransaction()
  try:
    #pengalihan ke dplk lain
    oT = config.CreatePObject('PengalihanKeDPLKLain')
    oT.kode_dp = recT.GetFieldByName('LLDP.kode_dp')
    oT.jenis_biaya = recT.jenis_biaya
    oT.ktr_biaya_lain = recT.ktr_biaya_lain
    
    oT.saldo_iuran_pk = recH.saldo_iuran_pk
    oT.saldo_iuran_pst = recH.saldo_iuran_pst
    #oT.saldo_iuran_tmb??
    oT.saldo_pengembangan = recH.saldo_pmb
    oT.saldo_peralihan = recH.saldo_psl
    
    oT.saldo_jml_dana = recH.saldo_jml_dana
    oT.biaya_pengelolaan = recH.biaya_pengelolaan
    oT.biaya_administrasi = recH.biaya_administrasi 
    oT.biaya_pindah = recH.biaya_pengalihan
    oT.saldo_dana_dipindahkan = recH.saldo_dana_dialihkan
    oT.biaya_lain = recT.biaya_lain
    oT.dana_dialihkan = recH.dana_dialihkan
    
    #field object TransaksiDPLK
    #mutasi akan di set ulang saat otorisasi, untuk kalkulasi biaya 
    oT.mutasi_iuran_pk = -recR.akum_iuran_pk
    oT.mutasi_iuran_pst = -recR.akum_iuran_pst
    oT.mutasi_iuran_tmb = -recR.akum_iuran_tmb
    oT.mutasi_psl = -recR.akum_psl
    oT.mutasi_pmb_pk = -recR.akum_pmb_pk
    oT.mutasi_pmb_pst = -recR.akum_pmb_pst
    oT.mutasi_pmb_tmb = -recR.akum_pmb_tmb
    oT.mutasi_pmb_psl = -recR.akum_pmb_psl
    oT.kode_jenis_transaksi = 'H'
    
    #field object TransaksiRekInvDPLK
    oT.no_rekening = recR.no_rekening
    oT.tgl_transaksi = recT.tgl_transaksi
    oT.keterangan = recT.keterangan
    oT.jenis_transaksi = 'T'
  
    oT.isCommitted = 'F'
    oT.user_id = config.SecurityContext.UserID
    oT.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    oT.tgl_sistem = config.ModLibUtils.Now()
    # TEMPORARY CODE
    if config.SecurityContext.UserID.upper() == 'ROOT': 
      oT.branch_code = '000'
    else:
      oT.branch_code = config.SecurityContext.GetSessionInfo()[4]
    
    #buat detil transaksi DPLK
    oRekInv = config.CreatePObjImplProxy('RekInvDPLK')
    oRekInv.Key = recR.no_rekening
    Ls_RekeningDPLK = oRekInv.Ls_RekeningDPLK
    while not Ls_RekeningDPLK.EndOfList:
      oRekDPLK = Ls_RekeningDPLK.CurrentElement 
      if oRekDPLK.is_deleted == 'F':
        
        #rekening DPLK masih aktif 
        oDetilTransaksi = config.CreatePObject('DetilTransaksiDPLK')
        oDetilTransaksi.ID_Transaksi = oT.ID_Transaksi
        oDetilTransaksi.nomor_rekening = oRekDPLK.nomor_rekening 
        oDetilTransaksi.kode_paket_investasi = oRekDPLK.kode_paket_investasi
        
        oDetilTransaksi.mutasi_iuran_pk = (oRekDPLK.pct_alokasi / 100.0) * oT.mutasi_iuran_pk  
        oDetilTransaksi.mutasi_iuran_pst = (oRekDPLK.pct_alokasi / 100.0) * oT.mutasi_iuran_pst  
        oDetilTransaksi.mutasi_iuran_tmb = (oRekDPLK.pct_alokasi / 100.0) * oT.mutasi_iuran_tmb
        oDetilTransaksi.mutasi_psl = (oRekDPLK.pct_alokasi / 100.0) * oT.mutasi_psl
        oDetilTransaksi.mutasi_pmb_pk = (oRekDPLK.pct_alokasi / 100.0) * oT.mutasi_pmb_pk
        oDetilTransaksi.mutasi_pmb_pst = (oRekDPLK.pct_alokasi / 100.0) * oT.mutasi_pmb_pst 
        oDetilTransaksi.mutasi_pmb_tmb = (oRekDPLK.pct_alokasi / 100.0) * oT.mutasi_pmb_tmb 
        oDetilTransaksi.mutasi_pmb_psl = (oRekDPLK.pct_alokasi / 100.0) * oT.mutasi_pmb_psl 
      
      Ls_RekeningDPLK.Next()
    #-- 
    
    config.Commit()
    errorStatus = 0
    errorMessage = ""
  except:
    config.Rollback()
    errorStatus = 1
    errorMessage = "Gagal menyimpan transaksi: "+ str(sys.exc_info()[1])
    #raise Exception, "Gagal menyimpan transaksi!"
      
  # pattern untuk catch status dan error
  ds = returns.AddNewDatasetEx("status", "error_status: integer; error_message: string;")
  rec = ds.AddRecord()
  rec.error_status = errorStatus
  rec.error_message = errorMessage