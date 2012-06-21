def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def btnOKClick(sender):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  app = form.ClientApplication

  form.CommitBuffer()
  form.PostResult()

  key = 'PObj:RekeningDPLK#NO_PESERTA=%s' % (uipNoData.GetFieldValue('LPeserta.no_peserta'))

  formid = 'fRegisterWasiatUmmat'
  aform = app.GetFormWithData('transaction/'+formid,formid,0,key,'uipMaster')
  #SetToCenterForm(form, aform.FormObject)
  ea = aform.Show(app.CreateValues(['mode','new']))

  if ea == 1:
    # eaQuitOK
    sender.ExitAction = 1
  else:
    # bersihkan form
    uipNoData.Edit()
    uipNoData.SetFieldValue('LPeserta.no_peserta',None)
    uipNoData.SetFieldValue('LPeserta.nama_lengkap',None)
    form.GetControlByName('pData.LPeserta').SetFocus()

