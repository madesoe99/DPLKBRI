def FormShow(form, parameter):
  uipRegisterWasiatUmmat = form.GetUIPartByName('uipRegisterWasiatUmmat')
  uipRegisterWasiatUmmat.Edit()
  uipRegisterWasiatUmmat.tgl_akseptasi = form.ClientApplication.ModDateTime.Now()
  uipRegisterWasiatUmmat.registernr_id = parameter.FirstRecord.registernr_id

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterWasiatUmmat = form.GetUIPartByName('uipRegisterWasiatUmmat')

  form.CommitBuffer()

  app.ExecuteScript('transaction/authorize_regnsbrek',\
    app.CreateValues(\
      ['id',uipRegisterWasiatUmmat.registernr_id],\
      ['no_polis',uipRegisterWasiatUmmat.no_polis],\
      ['besar_premi',uipRegisterWasiatUmmat.besar_premi],\
      ['manfaat_asuransi',uipRegisterWasiatUmmat.manfaat_asuransi],\
      ['tgl_akseptasi',uipRegisterWasiatUmmat.tgl_akseptasi]\
    )\
  )

