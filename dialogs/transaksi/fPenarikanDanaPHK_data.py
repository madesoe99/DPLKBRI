import sys
import com.ihsan.util.modman as modman

def downloadFile(config, parameter, returns):
  fileName = config.UserHomeDirectory + parameter.FirstRecord.fileName
  sw = returns.AddStreamWrapper()
  sw.LoadFromFile(fileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(fileName)

def GetNominalPajak(config, params, returns):
  transaksiAPI = modman.getModule(config, 'transaksiapi') 
  rec = params.FirstRecord
  
  #hitung total penarikan sebelumnya, untuk prediksi yang kena pajak
  totalSebelum = transaksiAPI.TotalPenarikanSebelumnya(config, \
    rec.tglTransaksi, rec.nomorRekening)

  #hitung pajak
  pajakTarikDana = transaksiAPI.HitungPajakTarikDana(config, rec.jumlahTarik, \
    totalSebelum)
    
  dsPajak = returns.AddNewDatasetEx("pajak", "nominal_pajak: float;")
  recPajak = dsPajak.AddRecord()
  recPajak.nominal_pajak = pajakTarikDana 
      
  # error status
  errorStatus = 0
  errorMessage = ""
  
  # pattern untuk catch status dan error
  dsStatus = returns.AddNewDatasetEx("status", "error_status: integer; error_message: string;")
  recStatus = dsStatus.AddRecord()
  recStatus.error_status = errorStatus
  recStatus.error_message = errorMessage

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config
  recParameterForm = parameterForm.FirstRecord

  # cek penarikan terakhir dan saldo iuran minimal
  transaksiAPI = modman.getModule(config, 'transaksiapi')
  transaksiAPI.CekRentangWaktuPenarikan(config, recParameterForm.no_rekening)
  transaksiAPI.CekSaldoIuranMin(config, recParameterForm.no_rekening)
  
  #set uideflist
  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recParameterForm.no_peserta)
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  uipTransaksi = uideflist.uipTransaksi
  uipPeserta = uideflist.uipPeserta
  uipRekening = uideflist.uipRekening
  uipParameter = uideflist.uipParameter
  
  #CEK USER LOGIN (UNTUK KEPERLUAN HAK AKSES)

  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recPeserta = uipPeserta.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)
  recParameter = uipParameter.Dataset.AddRecord()
  
  #set parameter default
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'
  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value
  oParameter.Key = 'BIAYA_SKN'
  recParameter.BiayaSKN = oParameter.Numeric_Value
  oParameter.Key = 'BIAYA_RTGS'
  recParameter.BiayaRTGS = oParameter.Numeric_Value
  oParameter.Key = 'BIAYA_TUNAI'
  recParameter.BiayaTunai = oParameter.Numeric_Value
  oParameter.Key = 'BIAYA_PINDAH_BUKU'
  recParameter.BiayaPindahBuku = oParameter.Numeric_Value
  #oParameter.Key = 'PERSEN_PENARIKAN_PHK'
  #recParameter.PERSEN_PENARIKAN_PHK = oParameter.Numeric_Value
  oParameter.Key = 'MIN_JML_AKUM_IURAN_PST'
  recParameter.MIN_JML_AKUM_IURAN_PST = oParameter.Numeric_Value
  
  oParameter.Key = 'PERSEN_DENDA_NPWP'
  recParameter.PERSEN_DENDA_NPWP = oParameter.Numeric_Value
  
  oParameter.Key = 'PERSEN_BIAYA_TARIK_PHK'
  recParameter.PERSEN_BIAYA_TARIK_PHK = oParameter.Numeric_Value
  oParameter.Key = 'MIN_BIAYA_TARIK'
  recParameter.MIN_BIAYA_TARIK = oParameter.Numeric_Value

  recParameter.isHitungMode = 1

  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  #set field Data Transaksi
  recTransaksi.tgl_transaksi = config.ModLibUtils.Now()
  recTransaksi.jml_tarik = 0.0
  recTransaksi.jenis_biaya = 'S'
  recTransaksi.biaya_lain = recParameter.BiayaSKN
  
  #set nominal batas penarikan
  #ASUMSI: akumulasi iuran pemberi kerja tidak boleh ditarik
  # batas penarikan dipecah berdasarkan masing-masing iuran
  recTransaksi.batas_penarikan_pk = recTransaksi.jml_tarik_iuran_pk = recRekening.akum_iuran_pk
  recTransaksi.batas_penarikan_pst = recTransaksi.jml_tarik_iuran_pst = recRekening.akum_iuran_pst
  recTransaksi.batas_penarikan_tmb = recTransaksi.jml_tarik_iuran_tmb = recRekening.akum_iuran_tmb
    
  recTransaksi.jml_tarik = recRekening.akum_iuran_pk+recRekening.akum_iuran_pst+recRekening.akum_iuran_tmb
  
def SimpanTransaksi(config, params, returns):
  recT = params.uipTransaksi.GetRecord(0)
  recP = params.uipPeserta.GetRecord(0)
  recR = params.uipRekening.GetRecord(0) 
  recH = params.uipHitung.GetRecord(0) 
  
  config.BeginTransaction()
  try:
    #penarikan dana PHK
    
    oT = config.CreatePObject('PenarikanDanaPHK')
    oT.jenis_biaya = recT.jenis_biaya
    oT.ktr_biaya_lain = recT.ktr_biaya_lain
    
    oT.saldo_iuran_pk_awal = recR.akum_iuran_pk
    oT.saldo_iuran_pk_akhir = recR.akum_iuran_pk - recT.jml_tarik_iuran_pk
    oT.saldo_iuran_pst_awal = recR.akum_iuran_pst
    oT.saldo_iuran_pst_akhir = recR.akum_iuran_pst - recT.jml_tarik_iuran_pst
    oT.saldo_iuran_tmb_awal = recR.akum_iuran_tmb
    oT.saldo_iuran_tmb_akhir = recR.akum_iuran_tmb - recT.jml_tarik_iuran_tmb
    
    oT.jml_tarik = recH.jml_tarik
    oT.biaya_tarik = recH.biaya_tarik
    oT.pajak = recH.pajak
    oT.biaya_lain = recT.biaya_lain
    oT.dana_diterima = recH.dana_diterima
    
    oT.user_name = config.SecurityContext.UserID
    
    #field object TransaksiDPLK
    oT.mutasi_iuran_pk = -recT.jml_tarik_iuran_pk
    oT.mutasi_iuran_pst = -recT.jml_tarik_iuran_pst
    oT.mutasi_iuran_tmb = -recT.jml_tarik_iuran_tmb
    oT.mutasi_psl = 0.0
    oT.mutasi_pmb_pk = 0.0
    oT.mutasi_pmb_pst = 0.0
    oT.mutasi_pmb_tmb = 0.0
    oT.mutasi_pmb_psl = 0.0
    oT.kode_jenis_transaksi = 'W'
    
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