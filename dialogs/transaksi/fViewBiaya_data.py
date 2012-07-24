import sys
import com.ihsan.util.modman as modman

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config

  recParameterForm = parameterForm.FirstRecord
  uideflist.SetData('uipTransaksi','PObj:TransaksiDPLK#ID_Transaksi='+str(recParameterForm.id_transaksi))
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  uipTransaksi = uideflist.uipTransaksi
  uipRekening = uideflist.uipRekening
  recT = uipTransaksi.Dataset.GetRecord(0)
  recR = uipRekening.Dataset.GetRecord(0)
  
  recT.TotalMutasi = recT.mutasi_iuran_pk + recT.mutasi_iuran_pst + recT.mutasi_iuran_tmb + recT.mutasi_psl + \
  recT.mutasi_pmb_pk + recT.mutasi_pmb_pst + recT.mutasi_pmb_tmb + recT.mutasi_pmb_psl
  #set field data rekening
  recR.akum_pmb = recR.akum_pmb_pk + recR.akum_pmb_pst + recR.akum_pmb_tmb + recR.akum_pmb_psl 
  
  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recR.no_peserta)
  uipPeserta = uideflist.uipPeserta
  recPeserta = uipPeserta.Dataset.GetRecord(0)
