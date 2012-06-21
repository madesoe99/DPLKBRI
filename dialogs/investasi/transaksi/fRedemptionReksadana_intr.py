dictModeRedempt = {0.00:'Redemption', 1.00:'Switch'}

def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Enabled = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  form.GetControlByName('pButton.btnClose').Default = 1
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.Caption = 'Lihat Register Redeem Investasi EQ'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.Caption = 'Otorisasi Register Redeem Investasi EQ'
  SetSelectorReadOnly(form)

def SetControlsForViewDoc(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  form.GetControlByName('pButton.btnOK').Cancel = 1
  form.GetControlByName('pButton.btnCancel').Visible = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnPrint').Visible = 1
  SetSelectorReadOnly(form)

def UnhideControls(form):
  #form.GetControlByName('pData.mutasi_kredit').Visible = 1
  form.GetControlByName('pRegister.tgl_otorisasi').Visible = 1
  form.GetControlByName('pRegister.user_id_auth').Visible = 1
  form.GetControlByName('pRegister.terminal_id_auth').Visible = 1

def SetSelectorReadOnly(form):
  form.GetControlByName('pSelector.LReksadana').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  #form.Caption = parameter.FirstRecord.caption

  uipRedemptionReksadana = form.GetUIPartByName('uipRedemptionReksadana')

  uipRedemptionReksadana.Edit()
  uipRedemptionReksadana.mode = parameter.FirstRecord.mode

  if (uipRedemptionReksadana.mode == 'new'):
    uipReksadana = form.GetUIPartByName('uipReksadana')
    uipRedemptionReksadana.unit_penyertaan = uipReksadana.unit_penyertaan
    uipRedemptionReksadana.nilai_redempt = uipReksadana.unit_penyertaan * uipReksadana.NAB
    if uipRedemptionReksadana.GetFieldValue('LReksadana.id_investasi'):
      SetSelectorReadOnly(form)

  if uipRedemptionReksadana.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Redeem Investasi EQ'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipRedemptionReksadana.biaya_redempt == 1.0 :
      form.GetControlByName('pData.LReksadanaSwitch').Visible = 1
      form.GetControlByName('pData.LMasterGiro').Visible = 0

    if uipRedemptionReksadana.mode == 'view':
      SetControlsForView(form)
    elif uipRedemptionReksadana.mode == 'auth':
      SetControlsForAuth(form)
    elif uipRedemptionReksadana.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Redeem Investasi EQ'

def LReksadanaAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipRedemptionReksadana = form.GetUIPartByName('uipRedemptionReksadana')
  uipRedemptionReksadana.Edit()
  uipRedemptionReksadana.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipRedemptionReksadana.GetFieldValue('LReksadana.kode_pihak_ketiga'))
  uipRedemptionReksadana.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipRedemptionReksadana.GetFieldValue('LReksadana.LPihakKetiga.nama_pihak_ketiga'))
  uipRedemptionReksadana.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipRedemptionReksadana.GetFieldValue('LReksadana.kode_paket_investasi'))
  uipRedemptionReksadana.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipRedemptionReksadana.GetFieldValue('LReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  uipRedemptionReksadana.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipRedemptionReksadana.GetFieldValue('LReksadana.kode_jns_investasi'))
  uipRedemptionReksadana.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipRedemptionReksadana.GetFieldValue('LReksadana.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipReksadana.Edit()
  uipReksadana.akum_nominal = uipRedemptionReksadana.GetFieldValue('LReksadana.akum_nominal')
  uipReksadana.unit_penyertaan = uipRedemptionReksadana.GetFieldValue('LReksadana.unit_penyertaan')
  uipReksadana.NAB = uipRedemptionReksadana.GetFieldValue('LReksadana.NAB')
  #uipReksadana.akum_piutangLR = uipRedemptionReksadana.GetFieldValue('LReksadana.akum_piutangLR')
  #uipReksadana.akum_LR = uipRedemptionReksadana.GetFieldValue('LReksadana.akum_LR')
  #uipReksadana.min_inv_awal = uipRedemptionReksadana.GetFieldValue('LReksadana.min_inv_awal')

def OnChange_Mode(sender) :
  form = sender.OwnerForm
  if sender.ItemIndex : #mode switch
    form.GetControlByName('pData.LMasterGiro').Visible = 0
    form.GetControlByName('pData.LReksadanaSwitch').Visible = 1
  else : #mode redemption
    form.GetControlByName('pData.LReksadanaSwitch').Visible = 0
    form.GetControlByName('pData.LMasterGiro').Visible = 1
    
def nilai_redemptExit(sender):
  form = sender.OwnerForm

  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipRedemptionReksadana = form.GetUIPartByName('uipRedemptionReksadana')
  uipRedemptionReksadana.Edit()
  uipRedemptionReksadana.nilai_redempt = (uipRedemptionReksadana.nilai_redempt or 0.0)
  #uipRedemptionReksadana.unit_penyertaan = uipRedemptionReksadana.nilai_redempt / uipReksadana.NAB
  if uipRedemptionReksadana.nilai_redempt != 0.0 :
    uipRedemptionReksadana.unit_penyertaan = 0.0


def UP_OnExit(sender) :
  form = sender.OwnerForm
  uipRedemptionReksadana = form.GetUIPartByName('uipRedemptionReksadana')
  if uipRedemptionReksadana.unit_penyertaan != 0.0 :
    uipRedemptionReksadana.nilai_redempt = 0.0

# ini buat apa, ya?
#def uipRedemptionReksadanaBeforePost(uipRedemptionReksadana):
#  form = uipRedemptionReksadana.OwnerForm

#  uipReksadana = form.GetUIPartByName('uipReksadana')
#  uipRedemptionReksadana.Edit()
#  if uipRedemptionReksadana.unit_penyertaan:
#    uipRedemptionReksadana.nilai_redempt = uipRedemptionReksadana.unit_penyertaan * uipReksadana.NAB
#  else:
#    uipRedemptionReksadana.nilai_redempt = 0.0
    
def checkNilaiRedempt(form, app):
  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipRedemptionReksadana = form.GetUIPartByName('uipRedemptionReksadana')

  sisaReksadana = uipReksadana.NAB * uipReksadana.unit_penyertaan - uipRedemptionReksadana.nilai_redempt
  if sisaReksadana < uipReksadana.min_inv_awal:
    if not app.ConfirmDialog('PERHATIAN:'\
      '\nSisa nominal Investasi EQ kurang dari minimum investasi awal.'
      '\nLanjutkan?.'
    ):
      form.GetControlByName('pData.unit_penyertaan').SetFocus()
      return 0

  return 1

def nilai_redemptChange(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  #checkNilaiRedempt(form, app)
  
def OnAfterLookup_Rek(sender, linkui) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipRedemptionReksadana')
  uip.no_rekening = uip.GetFieldValue('LMasterGiro.no_giro')

def OnAfterLookup_ReksaSw(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipRedemptionReksadana')
  uip.no_rekening = str(uip.GetFieldValue('LReksadanaSwitch.id_investasi'))

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRedemptionReksadana = form.GetUIPartByName('uipRedemptionReksadana')
  uipReksadana = form.GetUIPartByName('uipReksadana')

  if uipRedemptionReksadana.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipRedemptionReksadana.mode not in ['view','auth']:
      form.CommitBuffer()

      nilai_redemptExit(sender)

      #if not checkNilaiRedempt(form, app):
      #  return

      if uipRedemptionReksadana.mode == 'new':
        uipRedemptionReksadana.Edit()
        uipRedemptionReksadana.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 2
      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipRedemptionReksadana, uipReksadana)

    elif uipRedemptionReksadana.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Redeem Investasi EQ ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/redemptionreksadana_auth',\
          app.CreateValues(['id',uipRedemptionReksadana.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRedemptionReksadana = form.GetUIPartByName('uipRedemptionReksadana')

  if uipRedemptionReksadana.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Redeem Investasi EQ ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/tutupinv_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipRedemptionReksadana.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRedemptionReksadana = form.GetUIPartByName('uipRedemptionReksadana')
  uipReksadana = form.GetUIPartByName('uipReksadana')
  form.CommitBuffer()
  CetakAdvis(app, uipRedemptionReksadana, uipReksadana)
  
def CetakAdvis(app, uipRedemptionReksadana, uipReksadana):
  lHeader = ['Nama Investasi EQ', 'Pihak Ketiga', 'Paket Investasi', \
             'Mode Redeem', 'Tgl Transaksi', 'Nilai Redempt', 'Unit Penyertaan',\
             'No. Rekening Redeem', 'Investasi EQ Tujuan Switch', 'Nominal Investasi']
  sHeader = '|'.join(lHeader)
  tgl = uipRedemptionReksadana.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipRedemptionReksadana.GetFieldValue('LReksadana.nama_reksadana')),\
           '%s - %s'% (uipRedemptionReksadana.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipRedemptionReksadana.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipRedemptionReksadana.GetFieldValue('LPaketInvestasi.kode_paket_investasi')),\
           dictModeRedempt[uipRedemptionReksadana.biaya_redempt],\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.000000',uipRedemptionReksadana.nilai_redempt or 0.0),\
           app.ModLibUtils.FormatFloat(',0.000000',uipRedemptionReksadana.unit_penyertaan or 0.0),\
           str(uipRedemptionReksadana.GetFieldValue('LMasterGiro.no_giro')),\
           str(uipRedemptionReksadana.GetFieldValue('LReksadanaSwitch.nama_reksadana')),\
           app.ModLibUtils.FormatFloat(',0.00',uipReksadana.akum_nominal or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Redeem Investasi EQ'],['sHeader',sHeader],['sData',sData],['inputer',uipRedemptionReksadana.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
