def FormShow(form, parameter):
  uipRegisterWasiatUmmat = form.GetUIPartByName('uipRegisterWasiatUmmat')
  if uipRegisterWasiatUmmat.jenis_transaksi == 'R':
    uipRegisterWasiatUmmat.Edit()
    uipRegisterWasiatUmmat.tgl_akseptasi = form.ClientApplication.ModDateTime.Now()
    uipRegisterWasiatUmmat.besar_premi = 0.0
    uipRegisterWasiatUmmat.manfaat_asuransi = 0.0

    form.GetControlByName('pRegister.alasan_berhenti').Visible = 0
    form.GetControlByName('pOtorisasi.kolektibilitas_premi').Visible = 0
    form.GetControlByName('pOtorisasi.kolektibilitas_premi').ControlCaption = ''
    form.GetControlByName('pOtorisasi.tunggakan_premi').Visible = 0
    form.GetControlByName('pOtorisasi.kolektibilitas_premi').Enabled = 0
    form.GetControlByName('pOtorisasi.tunggakan_premi').Enabled = 0
  else:
    form.GetPanelByName('pOtorisasi').SetAllControlsReadOnly()
    form.Caption = 'Pra Otorisasi Penutupan Wasiat Ummat'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterWasiatUmmat = form.GetUIPartByName('uipRegisterWasiatUmmat')

  #checking no polis
  if (not uipRegisterWasiatUmmat.no_polis) \
    and (uipRegisterWasiatUmmat.jenis_transaksi == 'R'):
    form.ShowMessage('Nomor Polis masih kosong. Mohon untuk diisi.')
    return

  #checking nominal besar premi dan manfaat asuransi
  uipP = form.GetUIPartByName('uipParameter')
  if uipRegisterWasiatUmmat.besar_premi in ['',None] or \
    uipRegisterWasiatUmmat.besar_premi < uipP.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Nominal Besar Premi masih kosong atau 0! Mohon untuk diisi.')
    return
  elif uipRegisterWasiatUmmat.manfaat_asuransi in ['',None] or \
    uipRegisterWasiatUmmat.manfaat_asuransi < uipP.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Nominal Manfaat Asuransi masih kosong atau 0! Mohon untuk diisi.')
    return

  form.CommitBuffer()
  try:
    if uipRegisterWasiatUmmat.jenis_transaksi == 'R':
      app.ExecuteScript('transaction/registercif_auth',\
        app.CreateValues(\
          ['id',uipRegisterWasiatUmmat.registercif_id],\
          ['no_polis',uipRegisterWasiatUmmat.no_polis],\
          ['besar_premi',uipRegisterWasiatUmmat.besar_premi],\
          ['manfaat_asuransi',uipRegisterWasiatUmmat.manfaat_asuransi],\
          ['tgl_akseptasi',uipRegisterWasiatUmmat.tgl_akseptasi]\
        )\
      )
    else:
      app.ExecuteScript('transaction/registercif_auth',\
        app.CreateValues(\
          ['id',uipRegisterWasiatUmmat.registercif_id]\
        )\
      )
  except:
    raise

  sender.ExitAction = 1

