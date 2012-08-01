import sys
import com.ihsan.util.modman as modman

def Form_OnSetDataEx(uideflist, parameterForm):
  config = uideflist.config

  recParameterForm = parameterForm.FirstRecord
  uideflist.SetData('uipTransaksi','PObj:IuranPeserta#ID_Transaksi='+str(recParameterForm.id_transaksi))
  uideflist.SetData('uipRekening','PObj:RekInvDPLK#no_rekening='+recParameterForm.no_rekening)
  
  uipTransaksi = uideflist.uipTransaksi
  uipRekening = uideflist.uipRekening
  recTransaksi = uipTransaksi.Dataset.GetRecord(0)
  recRekening = uipRekening.Dataset.GetRecord(0)
  
  uideflist.SetData('uipPeserta','PObj:NasabahDPLK#no_peserta='+recRekening.no_peserta)
  uipPeserta = uideflist.uipPeserta
  recPeserta = uipPeserta.Dataset.GetRecord(0)
  
  if recTransaksi.catatan_bayar_iuran not in (None,''):
    DRG = config.CreatePObjImplProxy('DetilRiwayatGiro')
    DRG.key = recTransaksi.catatan_bayar_iuran
    recTransaksi.SetFieldByName('LReconcile.rekening_sumber',DRG.rekening_sumber) 
    recTransaksi.SetFieldByName('LReconcile.nominal',DRG.nominal) 

