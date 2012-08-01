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
  
  #hitung pajak pengambilan manfaat
  pajakManfaat = transaksiAPI.HitungPajakPengambilanManfaat(config, rec.saldoManfaat)
    
  dsPajak = returns.AddNewDatasetEx("pajak", "nominal_pajak: float;")
  recPajak = dsPajak.AddRecord()
  recPajak.nominal_pajak = pajakManfaat 
      
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
  transaksiAPI = modman.getModule(config, 'transaksiapi')

  #set uideflist
  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recParameterForm.no_peserta)
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  #checking peserta individu atau peserta korporat
  
  uipTransaksi = uideflist.uipTransaksi
  uipPeserta = uideflist.uipPeserta
  uipRekening = uideflist.uipRekening
  uipParameter = uideflist.uipParameter
  uipJenisManfaat = uideflist.uipJenisManfaat
  
  #CEK USER LOGIN (UNTUK KEPERLUAN HAK AKSES)

  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recPeserta = uipPeserta.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)
  recParameter = uipParameter.Dataset.AddRecord()
  recJenisManfaat = uipJenisManfaat.Dataset.AddRecord()
  
  #cek rekening investasi DPLK
  if recRekening.operation_code != 'F':
    raise Exception, "Rekening DPLK peserta berstatus Sedang Diubah. Transaksi tidak diperbolehkan!"

  #set field untuk jenis manfaat dan keterkaitan dengan tanggal pensiun 
  recJenisManfaat.isDipercepatAllowed = 0
  recJenisManfaat.isBiasaAllowed = 0
  tglNow = config.ModLibUtils.Now()
  if tglNow < recRekening.tgl_pensiun_dipercepat:
    #belum memasuki tanggal pensiun dipercepat sekalipun
    #hanya boleh pensiun cacat atau meninggal, do nothing
    pass
  elif (tglNow >= recRekening.tgl_pensiun_dipercepat) and \
    (tglNow < recRekening.tgl_pensiun): 
    #berada diantara tgl pensiun dipercepat dan pensiun biasa
    #boleh pensiun cacat, meninggal atau dipercepat (tinggal set dipercepat)
    recJenisManfaat.isDipercepatAllowed = 1
  else:
    #bisa semua jenis manfaat pensiun
    recJenisManfaat.isDipercepatAllowed = 1
    recJenisManfaat.isBiasaAllowed = 1

  #cek parameter default atau parameter korporat
  
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

  oParameter.Key = 'PERSEN_DENDA_NPWP'
  recParameter.PERSEN_DENDA_NPWP = oParameter.Numeric_Value

  #cek parameter default atau parameter korporat
  if recPeserta.kode_nasabah_corporate not in (None,''):
    #pakai parameter korporat
    listParameterKey =[]
    dictParameterKorporat = transaksiAPI.GetParameterCorporate(config, \
      recPeserta.kode_nasabah_corporate, listParameterKey)
    
    recParameter.PERSEN_CAIR_MANFAAT_UMUM = dictParameterKorporat['PERSEN_CAIR_MANFAAT_>=1TH'][1]
    recParameter.PERSEN_CAIR_MANFAAT_KURANG_SETAHUN = dictParameterKorporat['PERSEN_CAIR_MANFAAT_<1TH'][1]
  
    recParameter.BATAS_MANFAAT_KENA_ANUITAS = dictParameterKorporat['BATAS_MANFAAT_KENA_ANUITAS'][1]
    recParameter.PERSEN_BATAS_TUNAI_MANFAAT = dictParameterKorporat['PERSEN_BATAS_TUNAI_MANFAAT'][1]
  
    recParameter.PERSEN_BIAYA_PENGELOLAAN = dictParameterKorporat['PERSEN_BIAYA_PENGELOLAAN'][1]
    recParameter.BIAYA_ADM_TAHUNAN = dictParameterKorporat['BIAYA_ADM_TAHUNAN'][1]
  else:
    #pakai parameter default aplikasi
    oParameter.Key = 'PERSEN_CAIR_MANFAAT_>=1TH'
    recParameter.PERSEN_CAIR_MANFAAT_UMUM = oParameter.Numeric_Value
    oParameter.Key = 'PERSEN_CAIR_MANFAAT_<1TH'
    recParameter.PERSEN_CAIR_MANFAAT_KURANG_SETAHUN = oParameter.Numeric_Value
  
    oParameter.Key = 'BATAS_MANFAAT_KENA_ANUITAS'
    recParameter.BATAS_MANFAAT_KENA_ANUITAS = oParameter.Numeric_Value
    oParameter.Key = 'PERSEN_BATAS_TUNAI_MANFAAT'
    recParameter.PERSEN_BATAS_TUNAI_MANFAAT = oParameter.Numeric_Value
  
    oParameter.Key = 'PERSEN_BIAYA_PENGELOLAAN'
    recParameter.PERSEN_BIAYA_PENGELOLAAN = oParameter.Numeric_Value
    oParameter.Key = 'BIAYA_ADM_TAHUNAN'
    recParameter.BIAYA_ADM_TAHUNAN = oParameter.Numeric_Value
  
  recParameter.isHitungMode = 1
  
  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  #set field Data Transaksi
  recTransaksi.tgl_transaksi = config.ModLibUtils.Now()
  recTransaksi.isCekAturanMenkeu = 1
  recTransaksi.isSkipPPh = 0
  recTransaksi.isPengalihanKurangSetahun = 0
  recTransaksi.jenis_biaya = 'S'
  recTransaksi.biaya_lain = recParameter.BiayaSKN
  
  #set kepesertaan < 1 tahun
  recTransaksi.isKepesertaanKurangSetahun = \
    (recTransaksi.tgl_transaksi - recPeserta.tgl_registrasi) < recParameter.JUMLAH_HARI_SETAHUN 

  #set nominal total dana manfaat
  recTransaksi.total_dana = \
    recRekening.akum_pmb + \
    recRekening.akum_iuran_pk + \
    recRekening.akum_iuran_pst + \
    recRekening.akum_iuran_tmb + \
    recRekening.akum_psl
    
  #set % anuitas pilihan peserta
  recTransaksi.persen_anuitas_pilihan_peserta = 0.0
    
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
    #pengambilan manfaat dana pensiun
    
    oT = config.CreatePObject('PengambilanManfaat')
    oT.jenis_biaya = recT.jenis_biaya
    oT.kode_jns_manfaat = recT.GetFieldByName('Ljenis_penerimaan_manfaat.kode_jns_manfaat')
    oT.ahliwaris_id = recT.GetFieldByName('LAhliWaris.ahliwaris_id')
    if recT.nama_anuitas not in ('',None):
      oT.nama_anuitas = recT.nama_anuitas

    oT.saldo_iuran_pk = recR.akum_iuran_pk
    oT.saldo_iuran_pst = recR.akum_iuran_pst
    oT.saldo_iuran_tmb = recR.akum_iuran_tmb
    oT.saldo_psl = recR.akum_psl
    oT.saldo_pmb_pk = recR.akum_pmb_pk
    oT.saldo_pmb_pst = recR.akum_pmb_pst
    oT.saldo_pmb_tmb = recR.akum_pmb_tmb
    oT.saldo_pmb_psl = recR.akum_pmb_psl
      
    oT.saldo_jml_dana = recH.saldo_jml_dana
    oT.saldo_peralihan_1th = recH.pengalihan_bwh1th
    
    oT.biaya_pencairan = recH.biaya_pencairan
    oT.biaya_pengelolaan = recH.biaya_pengelolaan
    oT.biaya_administrasi = recH.biaya_administrasi
    
    oT.saldo_manfaat = recH.saldo_manfaat
    oT.pajak = recH.pajak 
    oT.manfaat_stlh_pajak = recH.manfaat_setelah_pajak

    oT.manfaat_tunai = recH.manfaat_tunai
    oT.manfaat_anuitas = recH.manfaat_anuitas
    oT.manfaat_tunai_diterima = recH.manfaat_tunai_diterima
    #oT.mutasi_biaya_lain = ?
    
    oT.jenis_biaya = recT.jenis_biaya
    oT.biaya_lain = recT.biaya_lain
    
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
    oT.kode_jenis_transaksi = 'J'
    
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