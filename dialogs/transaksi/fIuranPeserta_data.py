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

  #set field Data Transaksi
  recTransaksi.tgl_transaksi = config.ModLibUtils.Now()
  
  #cek peserta korporat atau individu
  if recPeserta.kode_nasabah_corporate not in (None,''):
    #peserta korporat
    recTransaksi.mutasi_iuran_pk = 0.0
    recTransaksi.mutasi_iuran_pst = 0.0
    recTransaksi.mutasi_iuran_tmb = 0.0
  else:
    #peserta individu
    recTransaksi.mutasi_iuran_pk = 0.0
    recTransaksi.mutasi_iuran_pst = recRekening.iuran_pst
    recTransaksi.mutasi_iuran_tmb = 0.0

  #set parameter default
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'
  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value
  oParameter.Key = 'MIN_JML_IURAN_PK'
  recParameter.MIN_JML_IURAN_PK = oParameter.Numeric_Value
  oParameter.Key = 'MIN_JML_IURAN_PST'
  recParameter.MIN_JML_IURAN_PST = oParameter.Numeric_Value
  oParameter.Key = 'MIN_JML_IURAN_TMB'
  recParameter.MIN_JML_IURAN_TMB = oParameter.Numeric_Value
  
  #cek peserta ikut premi atau tidak
  if recRekening.rekasuransi_id not in (None,0):
    #peserta ikut asuransi
    uideflist.SetData('uipRekAsuransi','PObj:RekAsuransi#rekasuransi_id='+str(recRekening.rekasuransi_id))

def SimpanTransaksi(config, params, returns):
  recT = params.uipTransaksi.GetRecord(0)
  recP = params.uipPeserta.GetRecord(0)
  recR = params.uipRekening.GetRecord(0)   
  
  config.BeginTransaction()
  try:
    #cek apakah ada rekening asuransi
    if recR.rekasuransi_id not in (None,0):
      #bayar iuran peserta dan premi
      recA = params.uipRekAsuransi.GetRecord(0)
      #bayar premi asuransi
      oTitipanPremi = config.CreatePObject('TitipanPremi')
      oTitipanPremi.besar_premi = recA.besar_premi   
  
      #field object TransaksiRekInvDPLK
      oTitipanPremi.no_rekening = recR.no_rekening
      oTitipanPremi.tgl_transaksi = recT.tgl_transaksi
      oTitipanPremi.keterangan = recT.keterangan
      oTitipanPremi.jenis_transaksi = 'P'
    
      oTitipanPremi.isCommitted = 'F'
      oTitipanPremi.user_id = config.SecurityContext.UserID
      oTitipanPremi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      oTitipanPremi.tgl_sistem = config.ModLibUtils.Now()
      # TEMPORARY CODE
      if config.SecurityContext.UserID.upper() == 'ROOT': 
        oTitipanPremi.branch_code = '000'
      else:
        oTitipanPremi.branch_code = config.SecurityContext.GetSessionInfo()[4]
      
      #bayar iuran peserta
      oIuranPeserta = config.CreatePObject('IuranPeserta')
      oIuranPeserta.catatan_bayar_iuran = recT.GetFieldByName('LReconcile.id_detil_giro')
      
      #field object TransaksiDPLK
      oIuranPeserta.mutasi_iuran_pk = recT.mutasi_iuran_pk
      oIuranPeserta.mutasi_iuran_pst = recT.mutasi_iuran_pst
      oIuranPeserta.mutasi_iuran_tmb = recT.mutasi_iuran_tmb
      oIuranPeserta.mutasi_psl = oIuranPeserta.mutasi_pmb_pk = \
        oIuranPeserta.mutasi_pmb_pst = oIuranPeserta.mutasi_pmb_tmb = \
        oIuranPeserta.mutasi_pmb_psl = 0.0
      oIuranPeserta.kode_jenis_transaksi = 'K'
      
      #field object TransaksiRekInvDPLK
      oIuranPeserta.no_rekening = recR.no_rekening
      oIuranPeserta.tgl_transaksi = recT.tgl_transaksi
      oIuranPeserta.keterangan = recT.keterangan
      oIuranPeserta.jenis_transaksi = 'T'
    
      oIuranPeserta.isCommitted = 'F'
      oIuranPeserta.user_id = config.SecurityContext.UserID
      oIuranPeserta.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      oIuranPeserta.tgl_sistem = config.ModLibUtils.Now()
      # TEMPORARY CODE
      if config.SecurityContext.UserID.upper() == 'ROOT': 
        oIuranPeserta.branch_code = '000'
      else:
        oIuranPeserta.branch_code = config.SecurityContext.GetSessionInfo()[4]
      
      #buat detil transaksi DPLK
      oRekInv = config.CreatePObjImplProxy('RekInvDPLK')
      oRekInv.Key = recR.no_rekening
      Ls_RekeningDPLK = oRekInv.Ls_RekeningDPLK
      while not Ls_RekeningDPLK.EndOfList:
        oRekDPLK = Ls_RekeningDPLK.CurrentElement
        if oRekDPLK.is_deleted == 'F':
        
          #rekening DPLK masih aktif
          oDetilTransaksi = config.CreatePObject('DetilTransaksiDPLK')
          oDetilTransaksi.ID_Transaksi = oIuranPeserta.ID_Transaksi
          oDetilTransaksi.nomor_rekening = oRekDPLK.nomor_rekening 
          oDetilTransaksi.kode_paket_investasi = oRekDPLK.kode_paket_investasi
          
          oDetilTransaksi.mutasi_iuran_pk = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_pk  
          oDetilTransaksi.mutasi_iuran_pst = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_pst  
          oDetilTransaksi.mutasi_iuran_tmb = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_tmb
          oDetilTransaksi.mutasi_psl = oDetilTransaksi.mutasi_pmb_pk = \
            oDetilTransaksi.mutasi_pmb_pst = oDetilTransaksi.mutasi_pmb_tmb = \
            oDetilTransaksi.mutasi_pmb_psl = 0.0
        
        Ls_RekeningDPLK.Next()
      #-- 

    else:
      #bayar iuran saja 
    
      #bayar iuran peserta
      oIuranPeserta = config.CreatePObject('IuranPeserta')
      #raise BaseException,recT.GetFieldByName('LReconcile.id_detil_giro')
      oIuranPeserta.catatan_bayar_iuran = recT.GetFieldByName('LReconcile.id_detil_giro')
      
      #field object TransaksiDPLK
      oIuranPeserta.mutasi_iuran_pk = recT.mutasi_iuran_pk
      oIuranPeserta.mutasi_iuran_pst = recT.mutasi_iuran_pst
      oIuranPeserta.mutasi_iuran_tmb = recT.mutasi_iuran_tmb
      oIuranPeserta.mutasi_psl = oIuranPeserta.mutasi_pmb_pk = \
        oIuranPeserta.mutasi_pmb_pst = oIuranPeserta.mutasi_pmb_tmb = \
        oIuranPeserta.mutasi_pmb_psl = 0.0
      oIuranPeserta.kode_jenis_transaksi = 'K'
      
      #field object TransaksiRekInvDPLK
      oIuranPeserta.no_rekening = recR.no_rekening
      oIuranPeserta.tgl_transaksi = recT.tgl_transaksi
      oIuranPeserta.keterangan = recT.keterangan
      oIuranPeserta.jenis_transaksi = 'T'
    
      oIuranPeserta.isCommitted = 'F'
      oIuranPeserta.user_id = config.SecurityContext.UserID
      oIuranPeserta.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      oIuranPeserta.tgl_sistem = config.ModLibUtils.Now()
      # TEMPORARY CODE
      if config.SecurityContext.UserID.upper() == 'ROOT': 
        oIuranPeserta.branch_code = '000'
      else:
        oIuranPeserta.branch_code = config.SecurityContext.GetSessionInfo()[4]
      
      #buat detil transaksi DPLK
      oRekInv = config.CreatePObjImplProxy('RekInvDPLK')
      oRekInv.Key = recR.no_rekening
      Ls_RekeningDPLK = oRekInv.Ls_RekeningDPLK
      while not Ls_RekeningDPLK.EndOfList:
        oRekDPLK = Ls_RekeningDPLK.CurrentElement
        if oRekDPLK.is_deleted == 'F':
        
          #rekening DPLK masih aktif
          oDetilTransaksi = config.CreatePObject('DetilTransaksiDPLK')
          oDetilTransaksi.ID_Transaksi = oIuranPeserta.ID_Transaksi
          oDetilTransaksi.nomor_rekening = oRekDPLK.nomor_rekening 
          oDetilTransaksi.kode_paket_investasi = oRekDPLK.kode_paket_investasi
          
          oDetilTransaksi.mutasi_iuran_pk = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_pk  
          oDetilTransaksi.mutasi_iuran_pst = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_pst  
          oDetilTransaksi.mutasi_iuran_tmb = (oRekDPLK.pct_alokasi / 100.0) * oIuranPeserta.mutasi_iuran_tmb
          oDetilTransaksi.mutasi_psl = oDetilTransaksi.mutasi_pmb_pk = \
            oDetilTransaksi.mutasi_pmb_pst = oDetilTransaksi.mutasi_pmb_tmb = \
            oDetilTransaksi.mutasi_pmb_psl = 0.0
        
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