def FormShow(form, parameter):
  uipTemplate = form.GetUIPartByName('uipTemplate')
  uipTemplate.Edit()
  
  #cek mode form
  uipTemplate.mode = parameter.FirstRecord.mode
  if uipTemplate.mode == 'view':
    form.GetPanelByName('pFilter').SetAllControlsReadOnly()
    form.GetPanelByName('gDeskripsiField').SetAllControlsReadOnly()
    form.GetControlByName('pButton.bSimpan').Enabled = 0
    form.GetControlByName('pButton.bSimpan').Default = 0
    form.GetControlByName('pButton.bCancel').Caption = '&Tutup'
    form.GetControlByName('pButton.bCancel').Default = 1
    form.Caption = 'Lihat Detil ' + form.Caption
  elif uipTemplate.mode == 'edit':
    form.Caption = 'Koreksi ' + form.Caption
  else:
    form.Caption = 'Tambah ' + form.Caption

def GridAfterPost(pclassui):
  form = pclassui.OwnerForm
  uipT = form.GetUIPartByName('uipTemplate')
  uipT.Edit()
  uipT.isGridEdited = 1

def GridAfterDelete(pclassui):
  form = pclassui.OwnerForm
  uipT = form.GetUIPartByName('uipTemplate')
  uipT.Edit()
  uipT.isGridEdited = 1

def bSimpanClick(sender):
  form = sender.OwnerForm

  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise
