id = None

def FormShow(form, parameter):
  global id
  
  id = parameter.FirstRecord.id


def jenisJatuhTempoChange(sender):
  form = sender.OwnerForm
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')

  if sender.ItemIndex == 4:
    # deposito on call
    form.GetControlByName('pDataRight.jmlHariOnCall').Visible = 1
  else:
    form.GetControlByName('pDataRight.jmlHariOnCall').Visible = 0
    uipRegisterDeposito.Edit()
    uipRegisterDeposito.jmlHariOnCall = None

def treatmentPokokChange(sender):
  pass


def btnOKClick(sender):
  global id
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
  uipRegisterDeposito.Edit()
  uipRegisterDeposito.id_investasi = id
  form.CommitBuffer()
  form.PostResult()
  sender.ExitAction = 2

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')

  if uipRegisterDeposito.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan register investasi baru ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/registerinvestasi_del',\
        app.CreateValues(['id',uipRegisterDeposito.id_registerinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

