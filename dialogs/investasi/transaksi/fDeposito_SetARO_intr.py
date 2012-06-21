def SalinData(Source,Dest,LsField) :
  Dest.Edit()
  for FieldName in LsField :
    Dest.SetFieldValue(FieldName,Source.GetFieldValue(FieldName))
  Dest.Post()
  
def SwitchView(form, Panel, CtrlList, Visibility) :
  for Ctrl in CtrlList :
    form.GetControlByName(Panel+'.'+Ctrl).Visible = Visibility
    
def ViewMode(form, Panel, mode) :
  SwitchView(form, Panel,['jmlHariOnCall','jenisJatuhTempo'],mode)
  SwitchView(form, Panel,['treatmentPokok','kapitalisir_rollover','LMasterGiro'],not mode)

def FormShow(form, parameter):
  form.Caption = parameter.FirstRecord.caption
  pButton = form.GetPanelByName('pButton')
  uip = form.GetUIPartByName('uipDeposito')
  uip.Edit()
  uip.CreateMode = parameter.FirstRecord.mode
  pData = form.GetPanelByName('pData')
  uip.SetFieldValue('LMasterGiro.no_giro',uip.no_rekening)
  if uip.CreateMode == 'Oto' :
    if uip.IsCommited :
      raise 'PERINGATAN','Data Deposito belum mengalami perubahan apapun'
    form.SetAllControlsReadOnly()
    pButton.GetControlByName('btnClose').Visible = 1
    pButton.GetControlByName('btnOK').Caption = '&Otorisasi'
    pButton.GetControlByName('btnClose').Enabled = 1
    pButton.GetControlByName('btnOK').Enabled = 1
    pButton.GetControlByName('btnCancel').Enabled = 1
    if uip.ChangeMode == '0' :
      ViewMode(form, 'pData',1)
      form.GetControlByName('pData.treatmentPokok').ControlCaption = ''
      form.GetControlByName('pData.kapitalisir_rollover').ControlCaption = ''
    else :
      form.GetControlByName('pData.jenisJatuhTempo').ControlCaption = 'nisbah'
    if uip.kapitalisir_rollover == 'T' :
      pData.GetControlByName('LMasterGiro').Visible = 0
  else :
    if not uip.IsCommited :
      raise '\nPERINGATAN','Perubahan Deposito belum di Otorisasi'
    pButton.GetControlByName('btnCancel').Cancel = 1
    if uip.CreateMode == 'mnuUbahPeriode' :
      ViewMode(form, 'pData',1)
      OnChange_jnsjt(form.GetControlByName('pData.jenisJatuhTempo'))
      pData.GetControlByName('no_bilyet').Enabled = 0
      pData.GetControlByName('Rekening_Deposito').Enabled = 0
      uip.ChangeMode = '0'
      form.GetControlByName('pData.treatmentPokok').ControlCaption = ''
      form.GetControlByName('pData.kapitalisir_rollover').ControlCaption = ''
    else :
      ViewMode(form, 'pData',0)
      kapitalisir_rolloverChange(form.GetControlByName('pData.kapitalisir_rollover'))
      form.GetControlByName('pData.jenisJatuhTempo').ControlCaption = 'nisbah'

    SalinData(uip,form.GetUIPartByName('uipDepo_Awal'),
       ('no_bilyet','kapitalisir_rollover','equivalent_rate','Rekening_Deposito',
        'no_rekening','tgl_buka','treatmentPokok'))

def kapitalisir_rolloverChange(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipDeposito = form.GetUIPartByName('uipDeposito')

  if sender.ItemIndex == 0:
    # pindah buku
    form.GetControlByName('pData.LMasterGiro').Visible = 1
  else:
    # konfirmasi atau ARO kapitalisir
    uipDeposito.Edit()
    form.GetControlByName('pData.LMasterGiro').Visible = 0

def OnAfterLookup_Rek(sender, linkui) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipDeposito')
  uip.no_rekening = uip.GetFieldValue('LMasterGiro.no_giro')

def OnChange_jnsjt(sender) :
  form = sender.OwnerForm
  if sender.ItemIndex == 4 :
    form.GetControlByName('pData.jmlHariOnCall').Visible = 1
  else :
    form.GetControlByName('pData.jmlHariOnCall').Visible = 0
    form.GetUIPartByName('uipDeposito').jmlHariOnCall = 0

def btnCancelClick(sender) :
  form = sender.OwnerForm
  app = form.ClientApplication
  if not form.GetUIPartByName('uipDeposito').IsCommited :
    if app.ConfirmDialog('Anda yakin akan membatalkan perubahan ini ?') :
      app = form.ClientApplication
      #batalkan otorisasi
      form.GetUIPartByName('uipDeposito').Edit()
      form.GetUIPartByName('uipDeposito').ModeOto = 0
      form.CommitBuffer()
      app.ExecuteScript('investasi/transaksi/perubahandeposito_auth',
       form.GetDataPacket())
    else :
      return 0
  sender.ExitAction = 2
    
def CekKesamaan(Source,Dest,LsField) :
  for FieldName in LsField :
    if Dest.GetFieldValue(FieldName)!=Source.GetFieldValue(FieldName) :
       return 0
  return 1
  
def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipDeposito = form.GetUIPartByName('uipDeposito')

  if not form.GetControlByName('pData.LMasterGiro').Visible:
    uipDeposito.Edit()
    uipDeposito.no_rekening = ''

  form.GetUIPartByName('uipDeposito').Edit()
  form.GetUIPartByName('uipDeposito').ModeOto = 1
  form.CommitBuffer()
  if uipDeposito.CreateMode == 'Oto' :
    ConfirmMess = 'Anda yakin akan mengotorisasi perubahan ini ?'
  else : #mode ubah
    ConfirmMess = 'Anda yakin akan menyimpan perubahan ini ?'
  if app.ConfirmDialog(ConfirmMess) :
    if form.GetUIPartByName('uipDeposito').IsCommited : #form Ubah
      if not CekKesamaan(form.GetUIPartByName('uipDeposito'),form.GetUIPartByName('uipDepo_Awal'),
         ('no_bilyet','kapitalisir_rollover','Nisbah','equivalent_rate','Rekening_Deposito',
          'no_rekening','tgl_buka','treatmentPokok','jmlHariOnCall','jenisJatuhTempo')) :
        form.PostResult()
    else : #form Otorisasi
      app.ExecuteScript('investasi/transaksi/perubahandeposito_auth',
       form.GetDataPacket())

    sender.ExitAction = 1

