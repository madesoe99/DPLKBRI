def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def btnOKClick(sender):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  app = form.ClientApplication

  form.CommitBuffer()

  keyvalue = uipNoData.GetFieldValue('LPeserta.no_peserta')
  key = 'PObj:NasabahDPLK#NO_PESERTA=%s' % (keyvalue)

  aform = app.GetFormWithData('transaction/fEditNasabahRekening','fEditNasabahRekening',0,key,'uipMaster')
  SetToCenterForm(form, aform.FormObject)
  if aform.Show(app.CreateValues(['mode','editdoc'])) == 1:
    # eaQuitOK
    sender.ExitAction = 1
  else:
    # bersihkan form
    uipNoData.Edit()
    uipNoData.SetFieldValue('LPeserta.no_peserta',None)
    uipNoData.SetFieldValue('LPeserta.nama_lengkap',None)
    form.GetControlByName('pData.LPeserta').SetFocus()
    
def pushMessageClick(menu, app):
  app.ExecuteScript('MessagePush', None)
