def FormShow(form, parameter):
  pButton = form.GetPanelByName('pButton')
  uipTrans = form.GetUIPartByName('uipTransLRInvestasi')
  if uipTrans.isCommitted == 'F' :
    form.SetAllControlsReadOnly()
    pButton.GetControlByName('btnOK').Caption = '&Otorisasi'
    pButton.GetControlByName('btnClose').Visible = 1
    pButton.GetControlByName('btnOK').Enabled = 1
    pButton.GetControlByName('btnClose').Enabled = 1
    pButton.GetControlByName('btnCancel').Enabled = 1
    

def printAdvis(form):
  app = form.ClientApplication

  res = app.ExecuteScript('investasi/report/biayareksadana',
    form.GetDataPacket()
  )

  app.DownloadItem(res.FirstRecord.filename,'v')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  pData = form.GetPanelByName('pData')
  uip = 'uipReksadana'
  if app.ConfirmDialog('Anda yakin akan menyimpan data ini ?') :
    if sender.Caption == '&Otorisasi' :
      form.GetUIPartByName(uip).Edit()
      form.GetUIPartByName(uip).ModeOto = 1
      form.CommitBuffer()
      app.ExecuteScript('investasi/transaksi/biaya_auth',
       form.GetDataPacket())
    else :
      #if app.ConfirmDialog('Cetak advis perubahan %s ?'
      #  %(JnsPerubahan[pData.GetControlByName('Jenis_Perubahan').ItemIndex])):
      #  printAdvis(form)

      form.PostResult()

    sender.ExitAction = 1
  
def btnCancelClick(sender) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = 'uipReksadana'
  if app.ConfirmDialog('Anda yakin akan membatalkan perubahan ini ?') :
      uipTrans = form.GetUIPartByName('uipTransLRInvestasi')
      if uipTrans.isCommitted != 'F' :
         sender.ExitAction = 2
         return 0
      #batalkan otorisasi
      form.GetUIPartByName(uip).Edit()
      form.GetUIPartByName(uip).ModeOto = 0
      form.CommitBuffer()
      app.ExecuteScript('investasi/transaksi/biaya_auth',
       form.GetDataPacket())
  else :
      return 0
  sender.ExitAction = 2
  
def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipReksadana = form.GetUIPartByName('uipReksadana')

  form.CommitBuffer()

  printAdvis(form)

