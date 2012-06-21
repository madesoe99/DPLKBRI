import sys
import com.ihsan.util.modman as modman

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config

  recParameterForm = parameterForm.FirstRecord
  uideflist.SetData('uipTransaksi','PObj:PenarikanDanaNormal#ID_Transaksi='+str(recParameterForm.id_transaksi))
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  uipTransaksi = uideflist.uipTransaksi
  uipRekening = uideflist.uipRekening
  recTransaksi = uipTransaksi.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)
  
  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  #set field data transaksi
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PERSEN_PENARIKAN_NORMAL'
  oParameter.Numeric_Value
  
  recTransaksi.batas_penarikan_pk = 0.0
  recTransaksi.batas_penarikan_pst = oParameter.Numeric_Value / 100 * \
    recRekening.akum_iuran_pst
  recTransaksi.batas_penarikan_tmb = oParameter.Numeric_Value / 100 * \
    recRekening.akum_iuran_tmb
  
  recTransaksi.jml_tarik_iuran_pk = recTransaksi.saldo_iuran_pk_awal - \
    recTransaksi.saldo_iuran_pk_akhir
  recTransaksi.jml_tarik_iuran_pst = recTransaksi.saldo_iuran_pst_awal - \
    recTransaksi.saldo_iuran_pst_akhir
  recTransaksi.jml_tarik_iuran_tmb = recTransaksi.saldo_iuran_tmb_awal - \
    recTransaksi.saldo_iuran_tmb_akhir

  #set field info perhitungan
  recTransaksi.saldo_iuran_pk = recRekening.akum_iuran_pk
  recTransaksi.saldo_iuran_pst = recRekening.akum_iuran_pst
  recTransaksi.saldo_iuran_tmb = recRekening.akum_iuran_tmb
  recTransaksi.saldo_pmb = recRekening.akum_pmb
  recTransaksi.saldo_psl = recRekening.akum_psl
  recTransaksi.saldo_jml_dana = recTransaksi.saldo_iuran_pk + \
    recTransaksi.saldo_iuran_pst + recTransaksi.saldo_iuran_tmb + \
    recTransaksi.saldo_pmb + recTransaksi.saldo_psl

  recTransaksi.saldo_iuran_awal = recTransaksi.saldo_iuran_pk + \
    recTransaksi.saldo_iuran_pst + recTransaksi.saldo_iuran_tmb
  recTransaksi.saldo_iuran_akhir = recTransaksi.saldo_iuran_awal - \
    recTransaksi.jml_tarik

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
