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
  form.Caption = 'Lihat Register Redemption Saham'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.Caption = 'Otorisasi Register Redemption Saham'
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
  form.GetControlByName('pSelector.LSaham').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  #form.Caption = parameter.FirstRecord.caption

  uipRedemptionSaham = form.GetUIPartByName('uipRedemptionSaham')

  uipRedemptionSaham.Edit()
  uipRedemptionSaham.mode = parameter.FirstRecord.mode

  if (uipRedemptionSaham.mode == 'new'):
    uipSaham = form.GetUIPartByName('uipSaham')
    uipRedemptionSaham.unit_penyertaan = uipSaham.unit_penyertaan
    uipRedemptionSaham.nilai_redempt = uipSaham.unit_penyertaan * uipSaham.NAB
    if uipRedemptionSaham.GetFieldValue('LSaham.id_investasi'):
      SetSelectorReadOnly(form)

  if uipRedemptionSaham.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Redemption Saham'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    #if uipRedemptionSaham.biaya_redempt == 1.0 :
    #  form.GetControlByName('pData.LSahamSwitch').Visible = 1
    #  form.GetControlByName('pData.LMasterGiro').Visible = 0

    if uipRedemptionSaham.mode == 'view':
      SetControlsForView(form)
    elif uipRedemptionSaham.mode == 'auth':
      SetControlsForAuth(form)
    elif uipRedemptionSaham.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Redemption Saham'

def LSahamAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipRedemptionSaham = form.GetUIPartByName('uipRedemptionSaham')
  uipRedemptionSaham.Edit()
  uipRedemptionSaham.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipRedemptionSaham.GetFieldValue('LSaham.kode_pihak_ketiga'))
  uipRedemptionSaham.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipRedemptionSaham.GetFieldValue('LSaham.LPihakKetiga.nama_pihak_ketiga'))
  uipRedemptionSaham.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipRedemptionSaham.GetFieldValue('LSaham.kode_paket_investasi'))
  uipRedemptionSaham.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipRedemptionSaham.GetFieldValue('LSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  uipRedemptionSaham.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipRedemptionSaham.GetFieldValue('LSaham.kode_jns_investasi'))
  uipRedemptionSaham.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipRedemptionSaham.GetFieldValue('LSaham.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipSaham = form.GetUIPartByName('uipSaham')
  uipSaham.Edit()
  uipSaham.akum_nominal = uipRedemptionSaham.GetFieldValue('LSaham.akum_nominal')
  uipSaham.unit_penyertaan = uipRedemptionSaham.GetFieldValue('LSaham.unit_penyertaan')
  uipSaham.NAB = uipRedemptionSaham.GetFieldValue('LSaham.NAB')
  #uipSaham.akum_piutangLR = uipRedemptionSaham.GetFieldValue('LSaham.akum_piutangLR')
  #uipSaham.akum_LR = uipRedemptionSaham.GetFieldValue('LSaham.akum_LR')
  #uipSaham.min_inv_awal = uipRedemptionSaham.GetFieldValue('LSaham.min_inv_awal')

def OnChange_Mode(sender) :
  form = sender.OwnerForm
  if sender.ItemIndex : #mode switch
    form.GetControlByName('pData.LMasterGiro').Visible = 0
    form.GetControlByName('pData.LSahamSwitch').Visible = 1
  else : #mode redemption
    form.GetControlByName('pData.LSahamSwitch').Visible = 0
    form.GetControlByName('pData.LMasterGiro').Visible = 1
    
def nilai_redemptExit(sender):
  form = sender.OwnerForm

  uipSaham = form.GetUIPartByName('uipSaham')
  uipRedemptionSaham = form.GetUIPartByName('uipRedemptionSaham')
  uipRedemptionSaham.Edit()
  uipRedemptionSaham.nilai_redempt = (uipRedemptionSaham.nilai_redempt or 0.0)
  #uipRedemptionSaham.unit_penyertaan = uipRedemptionSaham.nilai_redempt / uipSaham.NAB
  if uipRedemptionSaham.nilai_redempt != 0.0 :
    uipRedemptionSaham.unit_penyertaan = 0.0


def UP_OnExit(sender) :
  form = sender.OwnerForm
  uipRedemptionSaham = form.GetUIPartByName('uipRedemptionSaham')
  if uipRedemptionSaham.unit_penyertaan != 0.0 :
    uipRedemptionSaham.nilai_redempt = 0.0

# ini buat apa, ya?
#def uipRedemptionSahamBeforePost(uipRedemptionSaham):
#  form = uipRedemptionSaham.OwnerForm

#  uipSaham = form.GetUIPartByName('uipSaham')
#  uipRedemptionSaham.Edit()
#  if uipRedemptionSaham.unit_penyertaan:
#    uipRedemptionSaham.nilai_redempt = uipRedemptionSaham.unit_penyertaan * uipSaham.NAB
#  else:
#    uipRedemptionSaham.nilai_redempt = 0.0
    
def checkNilaiRedempt(form, app):
  uipSaham = form.GetUIPartByName('uipSaham')
  uipRedemptionSaham = form.GetUIPartByName('uipRedemptionSaham')

  sisaSaham = uipSaham.NAB * uipSaham.unit_penyertaan - uipRedemptionSaham.nilai_redempt
  if sisaSaham < uipSaham.min_inv_awal:
    if not app.ConfirmDialog('PERHATIAN:'\
      '\nSisa nominal Saham kurang dari minimum investasi awal.'
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
  uip = form.GetUIPartByName('uipRedemptionSaham')
  uip.no_rekening = uip.GetFieldValue('LMasterGiro.no_giro')

def OnAfterLookup_ReksaSw(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipRedemptionSaham')
  uip.no_rekening = str(uip.GetFieldValue('LSahamSwitch.id_investasi'))

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRedemptionSaham = form.GetUIPartByName('uipRedemptionSaham')
  uipSaham = form.GetUIPartByName('uipSaham')

  if uipRedemptionSaham.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipRedemptionSaham.mode not in ['view','auth']:
      form.CommitBuffer()

      nilai_redemptExit(sender)

      #if not checkNilaiRedempt(form, app):
      #  return

      if uipRedemptionSaham.mode == 'new':
        uipRedemptionSaham.Edit()
        uipRedemptionSaham.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 2
      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipRedemptionSaham, uipSaham)

    elif uipRedemptionSaham.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Redemption Saham ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/redemptionSaham_auth',\
          app.CreateValues(['id',uipRedemptionSaham.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRedemptionSaham = form.GetUIPartByName('uipRedemptionSaham')

  if uipRedemptionSaham.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Redemption Saham ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/tutupinv_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipRedemptionSaham.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRedemptionSaham = form.GetUIPartByName('uipRedemptionSaham')
  uipSaham = form.GetUIPartByName('uipSaham')
  form.CommitBuffer()
  CetakAdvis(app, uipRedemptionSaham, uipSaham)
  
def CetakAdvis(app, uipRedemptionSaham, uipSaham):
  lHeader = ['Nama Saham', 'Pihak Ketiga', 'Paket Investasi', \
              'Tgl Transaksi', 'Nilai Redempt', 'Unit Penyertaan',\
             'No. Rekening Redempt', 'Nominal Investasi']
  sHeader = '|'.join(lHeader)
  tgl = uipRedemptionSaham.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipRedemptionSaham.GetFieldValue('LSaham.nama_Saham')),\
           '%s - %s'% (uipRedemptionSaham.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipRedemptionSaham.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipRedemptionSaham.GetFieldValue('LPaketInvestasi.kode_paket_investasi')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.000000',uipRedemptionSaham.nilai_redempt or 0.0),\
           app.ModLibUtils.FormatFloat(',0.000000',uipRedemptionSaham.unit_penyertaan or 0.0),\
           str(uipRedemptionSaham.GetFieldValue('LMasterGiro.no_giro')),\
           app.ModLibUtils.FormatFloat(',0.00',uipSaham.akum_nominal or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Redemption Saham'],['sHeader',sHeader],['sData',sData],['inputer',uipRedemptionSaham.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
