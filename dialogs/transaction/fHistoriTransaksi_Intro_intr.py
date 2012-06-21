def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def btnOKClick(sender):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  app = form.ClientApplication

  form.CommitBuffer()

  keyvalue = uipNoData.GetFieldValue('LRekInvDPLK.no_rekening')
  key = 'PObj:RekInvDPLK#NO_REKENING=%s' % (keyvalue)
  ph = app.CreateValues(['key', key])

  #aform = app.GetFormWithData('transaction/fHistoriTransaksi','fHistoriTransaksi',0,key,'uipNasabahDPLK')
  aform = app.CreateForm('transaction/fHistoriTransaksi','fHistoriTransaksi',0,ph,None)
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

