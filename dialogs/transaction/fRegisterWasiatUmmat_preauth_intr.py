def FormShow(form, parameter):
  uipRegisterAsuransi = form.GetUIPartByName('uipRegisterAsuransi')
  if uipRegisterAsuransi.jenis_transaksi == 'R':
    uipRegisterAsuransi.Edit()
    uipRegisterAsuransi.tgl_akseptasi = form.ClientApplication.ModDateTime.Now()
    uipRegisterAsuransi.besar_premi = 0.0
    uipRegisterAsuransi.manfaat_asuransi = 0.0

    form.GetControlByName('pRegister.alasan_berhenti').Visible = 0
    form.GetControlByName('pOtorisasi.kolektibilitas_premi').Visible = 0
    form.GetControlByName('pOtorisasi.kolektibilitas_premi').ControlCaption = ''
    form.GetControlByName('pOtorisasi.tunggakan_premi').Visible = 0
    form.GetControlByName('pOtorisasi.kolektibilitas_premi').Enabled = 0
    form.GetControlByName('pOtorisasi.tunggakan_premi').Enabled = 0
  else:
    form.GetPanelByName('pOtorisasi').SetAllControlsReadOnly()
    form.Caption = 'Pra Otorisasi Penutupan Asuransi'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterAsuransi = form.GetUIPartByName('uipRegisterAsuransi')
  form.CommitBuffer()
  
  #checking no polis
  if uipRegisterAsuransi.no_polis in ['', None] \
    and (uipRegisterAsuransi.jenis_transaksi == 'R'):
    form.ShowMessage('Nomor Polis masih kosong. Mohon untuk diisi.')
    return

  #checking nominal besar premi dan manfaat asuransi
  uipP = form.GetUIPartByName('uipParameter')
  if uipRegisterAsuransi.besar_premi in [0,'',None] or \
    uipRegisterAsuransi.besar_premi < uipP.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Nominal Besar Premi masih kosong atau 0! Mohon untuk diisi.')
    return
    
  if uipRegisterAsuransi.manfaat_asuransi in ['',None] or \
    uipRegisterAsuransi.manfaat_asuransi < uipP.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Nominal Manfaat Asuransi masih kosong atau 0! Mohon untuk diisi.')
    return

  try:
    if uipRegisterAsuransi.jenis_transaksi == 'R':
      app.ExecuteScript('transaction/registercif_auth',\
        app.CreateValues(\
          ['id',uipRegisterAsuransi.registercif_id],\
          ['no_polis',uipRegisterAsuransi.no_polis],\
          ['besar_premi',uipRegisterAsuransi.besar_premi],\
          ['manfaat_asuransi',uipRegisterAsuransi.manfaat_asuransi],\
          ['tgl_akseptasi',uipRegisterAsuransi.tgl_akseptasi]\
        )\
      )
    else:
      app.ExecuteScript('transaction/registercif_auth',\
        app.CreateValues(\
          ['id',uipRegisterAsuransi.registercif_id]\
        )\
      )
  except:
    raise

  sender.ExitAction = 1

