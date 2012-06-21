def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnCancel').Visible = 0
  form.GetControlByName('pButton.btnOK').Caption = '&Close'

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

  if uipRegisterCIF.mode == 'view':
    SetControlsForView(form)
  else:
    uipRegisterCIF.user_id = app.UserID

    dh = app.ExecuteScript('getsessioninfo',app.CreateValues(['id',1]))
    uipRegisterCIF.terminal_id = dh.FirstRecord.sessioninfo

    if uipRegisterCIF.mode == 'new':
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.GetFieldValue('LNasabahDPLK.nama_lengkap'))
      uipRegisterCIF.SetFieldValue('LPaketInvestasi.kode_paket_investasi',uipMaster.GetFieldValue('LPaketInvestasi.kode_paket_investasi'))
      uipRegisterCIF.SetFieldValue('LPaketInvestasi.nama_paket_investasi',uipMaster.GetFieldValue('LPaketInvestasi.nama_paket_investasi'))

      uipRegisterCIF.SetFieldValue('LNasabahDPLK.LRekeningDPLK.LPaketInvestasi.kode_paket_investasi',uipMaster.GetFieldValue('LPaketInvestasi.kode_paket_investasi'))
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.LRekeningDPLK.LPaketInvestasi.nama_paket_investasi',uipMaster.GetFieldValue('LPaketInvestasi.nama_paket_investasi'))
    else:
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624

  kode_paket_investasi = uipRegisterCIF.GetFieldValue('LNasabahDPLK.LRekeningDPLK.LPaketInvestasi.kode_paket_investasi')
  nama_paket_investasi = uipRegisterCIF.GetFieldValue('LNasabahDPLK.LRekeningDPLK.LPaketInvestasi.nama_paket_investasi')

  uipRegisterCIF.SetFieldValue('LPaketInvestasi_lama.kode_paket_investasi',kode_paket_investasi)
  uipRegisterCIF.SetFieldValue('LPaketInvestasi_lama.nama_paket_investasi',nama_paket_investasi)

def btnOKClick(sender):
  form = sender.OwnerForm
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode <> 'view':
    form.CommitBuffer()
    form.PostResult()

    sender.ExitAction = 1
  else:
    sender.ExitAction = 2

