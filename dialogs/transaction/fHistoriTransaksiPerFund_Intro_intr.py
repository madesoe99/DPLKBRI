def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def btnOKClick(sender):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  app = form.ClientApplication

  form.CommitBuffer()

  no_rekening = uipNoData.GetFieldValue('LRekInvDPLK.no_rekening')
  kode_paket_investasi = uipNoData.GetFieldValue('LRekeningDPLK.kode_paket_investasi')
  nomor_rekening = "%s_%s" % (no_rekening, kode_paket_investasi)
  
  key = 'PObj:RekeningDPLK#NOMOR_REKENING=%s' % (nomor_rekening)
  ph = app.CreateValues(['key', key])

  #aform = app.GetFormWithData('transaction/fHistoriTransaksi','fHistoriTransaksi',0,key,'uipNasabahDPLK')
  aform = app.CreateForm('transaction/fHistoriTransaksiPerFund','fHistoriTransaksiPerFund',0,ph,None)
  SetToCenterForm(form, aform.FormObject)
  aform.Show()
  #if aform.Show() == 1:
    # eaQuitOK
  sender.ExitAction = 1
  #else:
  #  # bersihkan form
  #  uipNoData.Edit()
  #  uipNoData.no_peserta = None
  #  form.GetControlByName('pData.no_peserta').SetFocus()
  