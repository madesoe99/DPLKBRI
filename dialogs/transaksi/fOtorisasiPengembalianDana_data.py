import sys
import com.ihsan.util.modman as modman

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config

  recParameterForm = parameterForm.FirstRecord
  uideflist.SetData('uipTransaksi','PObj:PengembalianDana#ID_Transaksi='+str(recParameterForm.id_transaksi))
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  uipTransaksi = uideflist.uipTransaksi
  uipRekening = uideflist.uipRekening
  recTransaksi = uipTransaksi.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)
  
  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recRekening.no_peserta)
  uipPeserta = uideflist.uipPeserta
  recPeserta = uipPeserta.Dataset.GetRecord(0)

