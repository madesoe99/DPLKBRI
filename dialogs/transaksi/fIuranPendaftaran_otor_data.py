import sys
import com.ihsan.util.modman as modman

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config
  recParameterForm = parameterForm.FirstRecord
  
  #set uideflist
  uideflist.SetData('uipTransaksi','PObj:IuranPendaftaran#ID_Transaksi='+recParameterForm.id_transaksi)
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  uipPeserta = uideflist.uipPeserta
  uipRekening = uideflist.uipRekening
  
  #CEK USER LOGIN (UNTUK KEPERLUAN HAK AKSES)

  recRekening = uipRekening.Dataset.GetRecord(0) 
  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recRekening.no_peserta)
  recPeserta = uipPeserta.Dataset.GetRecord(0) 
  
  if recRekening.STATUS_BIAYA_DAFTAR == 'T': 
     raise Exception,'Peserta [ '+recRekening.no_rekening+' ] '+recPeserta.nama_lengkap+' Sudah Bayar Iuran Pendaftaran.!!' 

  #set field data rekening
  recRekening.akum_pmb = recRekening.akum_pmb_pk + recRekening.akum_pmb_pst + \
    recRekening.akum_pmb_tmb + recRekening.akum_pmb_psl 
  
