import sys
import com.ihsan.util.modman as modman

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config
  recParameterForm = parameterForm.FirstRecord
  
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
  
  if recRekening.STATUS_BIAYA_DAFTAR == 'T': 
     raise Exception,'Peserta [ '+recRekening.no_rekening+' ] '+recPeserta.nama_lengkap+' Sudah Bayar Iuran Pendaftaran.!!'
  #set parameter default
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'BESAR_BIAYA_DAFTAR'
  recParameter.BESAR_BIAYA_DAFTAR = oParameter.Numeric_Value

  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  #set field Data Transaksi
  recTransaksi.tgl_transaksi = config.ModLibUtils.Now()
  recTransaksi.besar_biaya_daftar = recParameter.BESAR_BIAYA_DAFTAR
  recTransaksi.no_rekening = recRekening.no_rekening
    
def SimpanTransaksi(config, params, returns):
  status = returns.CreateValues(
     ['IsErr',0],
     ['ErrMessage',''],
  )
  recT = params.uipTransaksi.GetRecord(0)  
  config.BeginTransaction()
  try:
    #penarikan dana PHK    
    oT = config.CreatePObject('IuranPendaftaran')
    oT.besar_biaya_daftar = recT.besar_biaya_daftar   

    #field object TransaksiRekInvDPLK
    oT.no_rekening = recT.no_rekening
    oT.tgl_transaksi = recT.tgl_transaksi
    oT.keterangan = recT.keterangan
    oT.jenis_transaksi = 'D'
  
    oT.isCommitted = 'F'
    oT.user_id = config.SecurityContext.UserID
    oT.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    oT.tgl_sistem = config.ModLibUtils.Now()
    # TEMPORARY CODE
    if config.SecurityContext.UserID.upper() == 'ROOT': 
      oT.branch_code = '000'
    else:
      oT.branch_code = config.SecurityContext.GetSessionInfo()[4]
    
    config.Commit()
  except:
    config.Rollback()
    status.IsErr = 1
    status.ErrMessage = str(sys.exc_info()[1])
