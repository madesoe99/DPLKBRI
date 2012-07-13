def SalinData(Source,Dest,LsField) :
  Dest.Edit()
  for FieldName in LsField :
    Dest.SetFieldValue(FieldName,Source.GetFieldValue(FieldName))
  Dest.Post()


def OnAfterLookup_Rek(sender, linkui) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipObligasi')
  uip.no_rekening = uip.GetFieldValue('LMasterGiro.no_giro')
  
def FormShow(form, parameter):
  form.Caption = parameter.FirstRecord.caption
  pButton = form.GetPanelByName('pAction')
  uip = form.GetUIPartByName('uipObligasi')
  uip.Edit()
  uip.CreateMode = parameter.FirstRecord.mode
  if uip.CreateMode == 'Oto' :
    if uip.UbahStat :
      raise Exception, 'PERINGATAN' + 'Data belum mengalami perubahan apapun'
    form.SetAllControlsReadOnly()
    pButton.GetControlByName('bClose').Visible = 1
    pButton.GetControlByName('bOK').Caption = '&Otorisasi'
    pButton.GetControlByName('bClose').Enabled = 1
    pButton.GetControlByName('bOK').Enabled = 1
    pButton.GetControlByName('bCancel').Enabled = 1

  else :
    if not uip.UbahStat :
      raise Exception, '\nPERINGATAN' + 'Perubahan belum di Otorisasi'
    pButton.GetControlByName('bCancel').Cancel = 1
    if uip.CreateMode == 'Settlement' :
      form.GetControlByName('pData.TreatmentObligasi').Visible = 0
      form.GetControlByName('pData.RateSekarang').Visible = 0
      form.GetControlByName('pData.LMasterGiro').Visible = 0
      form.GetControlByName('pData.tgl_settlement').Visible = 1
    else: # ubah
      form.GetControlByName('pData.TreatmentObligasi').Visible = 1
      form.GetControlByName('pData.RateSekarang').Visible = 1
      form.GetControlByName('pData.LMasterGiro').Visible = 1
      form.GetControlByName('pData.tgl_settlement').Visible = 0

def OnClick_Cancel (sender) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipObligasi')
  if uip.CreateMode == 'Oto' :
    if app.ConfirmDialog('Anda yakin akan membatalkan perubahan ini ?') :
      app = form.ClientApplication
      #batalkan otorisasi
      uip.Edit()
      uip.ModeOto = 0
      form.CommitBuffer()
      #app.ExecuteScript('investasi/transaksi/ubahsukuk_auth',
      # form.GetDataPacket())
      form.PostResult()
    else :
      return 0
  sender.ExitAction = 2

def OnClick_OK (sender) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipObligasi')
  uip.Edit()
  uip.ModeOto = 1
  form.CommitBuffer()

  if uip.CreateMode == 'Oto' :
    ConfirmMess = 'Anda yakin akan mengotorisasi perubahan ini ?'
  else : #mode ubah
    ConfirmMess = 'Anda yakin akan menyimpan perubahan ini ?'

  if app.ConfirmDialog(ConfirmMess) :
    form.PostResult()
  else :
    return 0
  sender.ExitAction = 1
