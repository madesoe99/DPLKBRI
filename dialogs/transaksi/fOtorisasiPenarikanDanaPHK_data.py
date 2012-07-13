import sys
import com.ihsan.util.modman as modman

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config

  recParameterForm = parameterForm.FirstRecord
  uideflist.SetData('uipTransaksi','PObj:PenarikanDanaPHK#ID_Transaksi='+str(recParameterForm.id_transaksi))
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
  
  recTransaksi.batas_penarikan_pk = recTransaksi.jml_tarik_iuran_pk = recRekening.akum_iuran_pk
  recTransaksi.batas_penarikan_pst = recTransaksi.jml_tarik_iuran_pst = recRekening.akum_iuran_pst
  recTransaksi.batas_penarikan_tmb = recTransaksi.jml_tarik_iuran_tmb = recRekening.akum_iuran_tmb
  

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
