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
  
  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recPeserta = uipPeserta.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)

  if recRekening.status_asuransi == 'F' or recRekening.rekasuransi_id in (None,0): 
     raise Exception,'Peserta [ '+recRekening.no_rekening+' ] '+recPeserta.nama_lengkap+' Tidak mengikuti asuransi.!!'

  uideflist.SetData('uipAsuransi','PObj:RekAsuransi#rekasuransi_id='+str(recRekening.rekasuransi_id))
  recAsuransi = uideflist.uipAsuransi.Dataset.GetRecord(0)

  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  #set field Data Transaksi
  recTransaksi.tgl_transaksi = config.ModLibUtils.Now()
  recTransaksi.besar_premi = recAsuransi.besar_premi
  recTransaksi.no_rekening = recRekening.no_rekening
    
def SimpanTransaksi(config, params, returns):
  status = returns.CreateValues(
     ['IsErr',0],
     ['ErrMessage',''],
  )
  recT = params.uipTransaksi.GetRecord(0)  
  config.BeginTransaction()
  try:
    #Titipa premi
    oT = config.CreatePObject('TitipanPremi')
    oT.besar_premi = recT.besar_premi   

    #field object TransaksiRekInvDPLK
    oT.no_rekening = recT.no_rekening
    oT.tgl_transaksi = recT.tgl_transaksi
    oT.keterangan = recT.keterangan
    oT.jenis_transaksi = 'P'
  
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
