import sys
import com.ihsan.util.modman as modman

##DEBUG CODE
#import rpdb2;rpdb2.start_embedded_debugger('haryo',True,True)

def downloadFile(config, parameter, returns):
  fileName = config.UserHomeDirectory + parameter.FirstRecord.fileName
  sw = returns.AddStreamWrapper()
  sw.LoadFromFile(fileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(fileName)

def GetNominalPajak(config, params, returns):
  transaksiAPI = modman.getModule(config, 'transaksiapi') 
  rec = params.FirstRecord
  
  ##TANYAKAN BENTUK PAJAK PENGEMBALIAN DANA##
  #hitung pajak pengambilan manfaat
  #pajakDanaKembali = transaksiAPI.HitungPajakPengambilanManfaat(config, rec.saldoPengembalian)
  
  #hitung total penarikan sebelumnya, untuk prediksi yang kena pajak
  totalSebelum = transaksiAPI.TotalPenarikanSebelumnya(config, \
    rec.tglTransaksi, rec.nomorRekening)

  #hitung pajak
  pajakDanaKembali = transaksiAPI.HitungPajakTarikDana(config, rec.jumlahDanaKembali, \
    totalSebelum)
    
  dsPajak = returns.AddNewDatasetEx("pajak", "nominal_pajak: float;")
  recPajak = dsPajak.AddRecord()
  recPajak.nominal_pajak = pajakDanaKembali 
      
  # error status
  errorStatus = 0
  errorMessage = ""
  
  # pattern untuk catch status dan error
  dsStatus = returns.AddNewDatasetEx("status", "error_status: integer; error_message: string;")
  recStatus = dsStatus.AddRecord()
  recStatus.error_status = errorStatus
  recStatus.error_message = errorMessage
########################################

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config
  recParameterForm = parameterForm.FirstRecord

  #set uideflist
  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recParameterForm.no_peserta)
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  #checking peserta individu atau peserta korporat
  
  uipTransaksi = uideflist.uipTransaksi
  uipPeserta = uideflist.uipPeserta
  uipRekening = uideflist.uipRekening
  uipParameter = uideflist.uipParameter
  
  #CEK USER LOGIN (UNTUK KEPERLUAN HAK AKSES)

  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recPeserta = uipPeserta.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)
  recParameter = uipParameter.Dataset.AddRecord()
  
  #cek rekening investasi DPLK
  if recRekening.operation_code != 'F':
    raise Exception, "Rekening DPLK peserta berstatus Sedang Diubah. Transaksi tidak diperbolehkan!"
  
  #cek parameter default atau parameter korporat
  
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
  
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  recParameter.JUMLAH_HARI_SETAHUN = oParameter.Numeric_Value
  oParameter.Key = 'MIN_KEPESERTAAN_KEMBALI_DANA'
  recParameter.MIN_KEPESERTAAN_KEMBALI_DANA = oParameter.Numeric_Value

  oParameter.Key = 'PERSEN_CAIR_KEMBALI_DANA'
  recParameter.PERSEN_CAIR_KEMBALI_DANA = oParameter.Numeric_Value
  oParameter.Key = 'PERSEN_BIAYA_PENGELOLAAN'
  recParameter.PERSEN_BIAYA_PENGELOLAAN = oParameter.Numeric_Value
  oParameter.Key = 'BIAYA_ADM_TAHUNAN'
  recParameter.BIAYA_ADM_TAHUNAN = oParameter.Numeric_Value

  oParameter.Key = 'PERSEN_DENDA_NPWP'
  recParameter.PERSEN_DENDA_NPWP = oParameter.Numeric_Value
  
  recParameter.isHitungMode = 1
  
  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  #set field Data Transaksi
  recTransaksi.tgl_transaksi = config.ModLibUtils.Now()
  recTransaksi.jenis_biaya = 'S'
  recTransaksi.biaya_lain = recParameter.BiayaSKN
  
  #set nominal total dana manfaat
  recTransaksi.total_dana = \
    recRekening.akum_pmb + \
    recRekening.akum_iuran_pk + \
    recRekening.akum_iuran_pst + \
    recRekening.akum_iuran_tmb + \
    recRekening.akum_psl
    
  #do get proporsi biaya untuk biaya pengelolaan dan biaya administrasi
  transaksiAPI = modman.getModule(config, 'transaksiapi')
  recParameter.proporsiBiaya = transaksiAPI.HitungProporsiBiaya(config, 'C', \
    recRekening.no_rekening, recTransaksi.tgl_transaksi)
  
def SimpanTransaksi(config, params, returns):
  recT = params.uipTransaksi.GetRecord(0)
  recP = params.uipPeserta.GetRecord(0)
  recR = params.uipRekening.GetRecord(0) 
  recH = params.uipHitung.GetRecord(0) 
  
  config.BeginTransaction()
  try:
    #pindah paket investasi
    
    oT = config.CreatePObject('PengambilanManfaat')

    oT.saldo_iuran_pk = recR.akum_iuran_pk
    oT.saldo_iuran_pst = recR.akum_iuran_pst
    oT.saldo_iuran_tmb = recR.akum_iuran_tmb
    oT.saldo_psl = recR.akum_psl
    oT.saldo_pmb_pk = recR.akum_pmb_pk
    oT.saldo_pmb_pst = recR.akum_pmb_pst
    oT.saldo_pmb_tmb = recR.akum_pmb_tmb
    oT.saldo_pmb_psl = recR.akum_pmb_psl
      
    oT.saldo_jml_dana = recH.saldo_jml_dana
    
    oT.biaya_pencairan = recH.biaya_pencairan
    oT.biaya_pengelolaan = recH.biaya_pengelolaan
    oT.biaya_administrasi = recH.biaya_administrasi
    
    oT.saldo_pengembalian = recH.saldo_pengembalian
    oT.pajak = recH.pajak 
    oT.dana_stlh_pajak = recH.dana_setelah_pajak

    oT.jenis_biaya = recT.jenis_biaya
    oT.biaya_lain = recT.biaya_lain
    
    oT.dana_dikembalikan = recH.dana_dikembalikan
    
    #field object TransaksiDPLK
    #mutasi akan di set ulang saat otorisasi, untuk kalkulasi biaya
    oT.mutasi_iuran_pk = -oT.saldo_iuran_pk
    oT.mutasi_iuran_pst = -oT.saldo_iuran_pst
    oT.mutasi_iuran_tmb = -oT.saldo_iuran_tmb
    oT.mutasi_psl = -oT.saldo_psl
    oT.mutasi_pmb_pk = -oT.saldo_pmb_pk
    oT.mutasi_pmb_pst = -oT.saldo_pmb_pst
    oT.mutasi_pmb_tmb = -oT.saldo_pmb_tmb
    oT.mutasi_pmb_psl = -oT.saldo_pmb_psl
    oT.kode_jenis_transaksi = 'F'
    
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