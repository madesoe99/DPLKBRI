import sys
import com.ihsan.util.modman as modman

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config

  recParameterForm = parameterForm.FirstRecord
  uideflist.SetData('uipTransaksi','PObj:PengalihanKeDPLKLain#ID_Transaksi='+str(recParameterForm.id_transaksi))
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  uipTransaksi = uideflist.uipTransaksi
  uipRekening = uideflist.uipRekening
  recTransaksi = uipTransaksi.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)
  
  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  #set field info perhitungan
  recTransaksi.saldo_iuran_tmb = recRekening.akum_iuran_tmb

  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recRekening.no_peserta)
  uipPeserta = uideflist.uipPeserta
  recPeserta = uipPeserta.Dataset.GetRecord(0)

def Form_OnGeneralProcessData(uideflist, data):
  config = uideflist.Config
  recT = data.uipTransaksi.GetRecord(0)
  try:
    #otorisasi transaksi
    OtorisasiTransaksi = modman.getModule(config,'scripts#transaksi.OtorisasiTransaksi')
    returns = OtorisasiTransaksi.ProsesOtorisasi(config, recT.ID_Transaksi, 'A')
  except:
    raise Exception, "Gagal otorisasi transaksi: "+ str(sys.exc_info()[1])

  return 0

def OtorisasiTransaksi(config, params, returns):
  recT = params.uipTransaksi.GetRecord(0)
  try:
    #otorisasi transaksi
    OtorisasiTransaksi = modman.getModule(config,'scripts#transaksi.OtorisasiTransaksi')
    returns = OtorisasiTransaksi.ProsesOtorisasi(config, recT.ID_Transaksi, 'A')

    errorStatus = 0
    errorMessage = ""
  except:
    config.Rollback()
    errorStatus = 1
    errorMessage = "Gagal otorisasi transaksi: "+ str(sys.exc_info()[1])
      
  # pattern untuk catch status dan error
  ds = returns.AddNewDatasetEx("status", "error_status: integer; error_message: string;")
  rec = ds.AddRecord()
  rec.error_status = errorStatus
  rec.error_message = errorMessage
