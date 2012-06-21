def FormShow(form, parameter):
  uipRegisterWasiatUmmat = form.GetUIPartByName('uipRegisterWasiatUmmat')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterWasiatUmmat = form.GetUIPartByName('uipRegisterWasiatUmmat')

  app.ExecuteScript('transaction/registercif_auth',\
    app.CreateValues(\
      ['id',uipRegisterWasiatUmmat.registercif_id]\
    )\
  )

