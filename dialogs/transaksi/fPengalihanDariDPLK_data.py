import sys

def downloadFile(config, parameter, returns):
  fileName = config.UserHomeDirectory + parameter.FirstRecord.fileName
  sw = returns.AddStreamWrapper()
  sw.LoadFromFile(fileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(fileName)

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config

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

  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 

  #set field Data Transaksi
  recTransaksi.tgl_transaksi = config.ModLibUtils.Now()
  recTransaksi.mutasi_iuran_pk = recTransaksi.mutasi_iuran_pst = \
    recTransaksi.mutasi_iuran_tmb = recTransaksi.mutasi_psl = 0.0
  recTransaksi.mutasi_pmb_pk = recTransaksi.mutasi_pmb_pst = \
    recTransaksi.mutasi_pmb_tmb = recTransaksi.mutasi_pmb_psl = 0.0

  #set parameter default
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'
  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value

def SimpanTransaksi(config, params, returns):
  recT = params.uipTransaksi.GetRecord(0)
  recP = params.uipPeserta.GetRecord(0)
  recR = params.uipRekening.GetRecord(0) 
  
  config.BeginTransaction()
  try:
    #bayar iuran peserta
    oT = config.CreatePObject('PengalihanDariDPLKLain')
    oT.kode_dp = recT.GetFieldByName('LLDP.kode_dp')
    oT.no_dplk_lain = recT.no_dplk_lain
    
    oT.saldo_iuran_pk = recT.mutasi_iuran_pk
    oT.saldo_iuran_pst = recT.mutasi_iuran_pst
    oT.saldo_iuran_tambahan = recT.mutasi_iuran_tmb
    oT.saldo_peralihan = recT.mutasi_psl
    #oT.saldo_pengembangan = ??
    
    #field object TransaksiDPLK
    oT.mutasi_iuran_pk = recT.mutasi_iuran_pk
    oT.mutasi_iuran_pst = recT.mutasi_iuran_pst
    oT.mutasi_iuran_tmb = recT.mutasi_iuran_tmb
    oT.mutasi_psl = recT.mutasi_psl
    oT.mutasi_pmb_pk = recT.mutasi_pmb_pk
    oT.mutasi_pmb_pst = recT.mutasi_pmb_pst
    oT.mutasi_pmb_tmb = recT.mutasi_pmb_tmb
    oT.mutasi_pmb_psl = recT.mutasi_pmb_psl
    oT.kode_jenis_transaksi = 'I'
    
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