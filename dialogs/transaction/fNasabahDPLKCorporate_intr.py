def SetControlsForView(form):
  #form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  #form.GetPanelByName('pDataRight').SetAllControlsReadOnly() 
  #form.GetPanelByName('pPerjanjian').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tutup'
  form.GetControlByName('pButton.btnCancel').Default = 1
  form.Caption = 'Lihat Detil ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipNasabahDPLKCorporate = form.GetUIPartByName('uipNasabahDPLKCorporate')

  uipNasabahDPLKCorporate.Edit()
  uipNasabahDPLKCorporate.mode = parameter.FirstRecord.mode

  if uipNasabahDPLKCorporate.mode == 'view':
    SetControlsForView(form)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication

  uipNasabahDPLKCorporate = form.GetUIPartByName('uipNasabahDPLKCorporate')

  if uipNasabahDPLKCorporate.mode <> 'view':
    form.CommitBuffer()
    form.PostResult()

    sender.ExitAction = 1
  else:
    #mode view
    sender.ExitAction = 2

