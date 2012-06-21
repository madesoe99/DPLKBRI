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
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Lihat Register Tutup Deposito'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Tutup Investasi'
  SetSelectorReadOnly(form)

def SetControlsForViewDoc(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  form.GetControlByName('pButton.btnOK').Cancel = 1
  form.GetControlByName('pButton.btnCancel').Visible = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  SetSelectorReadOnly(form)

def UnhideControls(form):
  #form.GetControlByName('pData.mutasi_kredit').Visible = 1
  form.GetControlByName('pRegister.tgl_otorisasi').Visible = 1
  form.GetControlByName('pRegister.user_id_auth').Visible = 1
  form.GetControlByName('pRegister.terminal_id_auth').Visible = 1

def SetSelectorReadOnly(form):
  form.GetControlByName('pSelector.LDeposito').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

#def SetInvCateg(form, kode_jns_investasi):
#  uipTutupDeposito = form.GetUIPartByName('uipTutupDeposito')

#  uipTutupDeposito.Edit()
#  uipTutupDeposito.kode_jns_investasi = kode_jns_investasi

##def SetCtrlByJatuhTempo(form):
##  app = form.ClientApplication
##  uipDeposito = form.GetUIPartByName('uipDeposito')
##  uipTutupDeposito = form.GetUIPartByName('uipTutupDeposito')
##
##  toDay = app.ModDateTime.CutDate(app.ModDateTime.Now())
##  jatuhTempoDT = app.ModDateTime.EncodeDate(
##    uipDeposito.tgl_jatuh_tempo[0]
##    , uipDeposito.tgl_jatuh_tempo[1]
##    , uipDeposito.tgl_jatuh_tempo[2]
##  )
##
##  uipTutupDeposito.Edit()
##  uipTutupDeposito.penalti = 0.0
##  uipTutupDeposito.akom_bagi_hasil = 0.0
##
##  if toDay >= jatuhTempoDT:
##    # sudah jatuh tempo, tidak ada penalti
##    form.GetControlByName('pData.penalti').Visible = 0
##    form.GetControlByName('pData.akom_bagi_hasil').Visible = 0
##    uipTutupDeposito.isPenalti = 'F'
##  else:
##    form.GetControlByName('pData.penalti').Visible = 1
##    form.GetControlByName('pData.akom_bagi_hasil').Visible = 1
##    uipTutupDeposito.isPenalti = 'T'
##
##def SetCtrlByIsPenalti(form):
##  app = form.ClientApplication
##  uipTutupDeposito = form.GetUIPartByName('uipTutupDeposito')
##
##  if uipTutupDeposito.isPenalti == 'T':
##    form.GetControlByName('pData.penalti').Visible = 1
##    form.GetControlByName('pData.akom_bagi_hasil').Visible = 1
##  else:
##    form.GetControlByName('pData.penalti').Visible = 0
##    form.GetControlByName('pData.akom_bagi_hasil').Visible = 0

def FormShow(form, parameter):
  app = form.ClientApplication

  # set caption
  #form.Caption = parameter.FirstRecord.caption

  uipTutupDeposito = form.GetUIPartByName('uipTutupDeposito')
  uipDeposito = form.GetUIPartByName('uipDeposito')

  uipTutupDeposito.Edit()
  uipTutupDeposito.mode = parameter.FirstRecord.mode

  if uipTutupDeposito.mode == 'new':
    if uipTutupDeposito.GetFieldValue('LDeposito.id_investasi'):
      SetSelectorReadOnly(form)
      
      # set nilai no_rekening sebagai default pencairan
      uipTutupDeposito.no_rekening = uipDeposito.no_rekening
      
      #SetCtrlByJatuhTempo(form)

    #else:
    #  SetInvCateg(form, parameter.FirstRecord.inv)
  #else:
  #  SetCtrlByIsPenalti(form)

  if uipTutupDeposito.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Tutup Deposito'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipTutupDeposito.mode == 'view':
      SetControlsForView(form)
    elif uipTutupDeposito.mode == 'auth':
      SetControlsForAuth(form)
    elif uipTutupDeposito.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Tutup Deposito'

def OnAfterLookup_Rek(sender, linkui) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTutup = form.GetUIPartByName('uipTutupDeposito')
  uipTutup.no_rekening = uipTutup.GetFieldValue('LMasterGiro.no_giro')
  
def LDepositoAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication

  uipTutupDeposito = form.GetUIPartByName('uipTutupDeposito')
  uipTutupDeposito.Edit()
  uipTutupDeposito.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipTutupDeposito.GetFieldValue('LDeposito.kode_pihak_ketiga'))
  uipTutupDeposito.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipTutupDeposito.GetFieldValue('LDeposito.LPihakKetiga.nama_pihak_ketiga'))
  #uipTutupDeposito.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipTutupDeposito.GetFieldValue('LDeposito.kode_paket_investasi'))
  #uipTutupDeposito.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipTutupDeposito.GetFieldValue('LDeposito.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipDeposito = form.GetUIPartByName('uipDeposito')
  uipDeposito.Edit()
  uipDeposito.akum_nominal = uipTutupDeposito.GetFieldValue('LDeposito.akum_nominal')
  uipDeposito.akum_piutangLR = uipTutupDeposito.GetFieldValue('LDeposito.akum_piutangLR')
  uipDeposito.akum_LR = uipTutupDeposito.GetFieldValue('LDeposito.akum_LR')
  uipDeposito.no_rekening = uipTutupDeposito.GetFieldValue('LDeposito.no_rekening')
  #uipDeposito.tgl_jatuh_tempo = uipTutupDeposito.GetFieldValue('LDeposito.tgl_jatuh_tempo')
  uipTutupDeposito.no_rekening = uipTutupDeposito.GetFieldValue('LDeposito.no_rekening')

  #SetCtrlByJatuhTempo(form)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTutupDeposito = form.GetUIPartByName('uipTutupDeposito')
  uipDeposito = form.GetUIPartByName('uipDeposito')
  
  if uipTutupDeposito.no_rekening in ('',None) :
    raise 'PERINGATAN','nomor rekening tujuan harus diisi'
  if uipTutupDeposito.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipTutupDeposito.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipTutupDeposito.mode == 'new':
        uipTutupDeposito.Edit()
        uipTutupDeposito.__SYSFLAG = 'N'

      form.PostResult()
      sender.ExitAction = 2
      
      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipTutupDeposito, uipDeposito)

    elif uipTutupDeposito.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Penutupan Deposito ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/tutupdeposito_auth',\
          app.CreateValues(['id',uipTutupDeposito.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTutupDeposito = form.GetUIPartByName('uipTutupDeposito')

  if uipTutupDeposito.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Penutupan Deposito ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/tutupinv_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipTutupDeposito.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTutupDeposito = form.GetUIPartByName('uipTutupDeposito')
  uipDeposito = form.GetUIPartByName('uipDeposito')
  form.CommitBuffer()
  CetakAdvis(app, uipTutupDeposito, uipDeposito)

def CetakAdvis(app, uipTutupDeposito, uipDeposito):
  lHeader = ['No. Bilyet', 'Rekening Deposito', 'Pihak Ketiga','Tgl Transaksi', \
             'Rekening Tujuan', 'Nominal Akhir']
  sHeader = '|'.join(lHeader)
  tgl = uipTutupDeposito.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])

  lData = [str(uipTutupDeposito.GetFieldValue('LDeposito.no_bilyet')),\
           str(uipTutupDeposito.GetFieldValue('LDeposito.rekening_deposito')),\
           '%s - %s'% (uipTutupDeposito.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipTutupDeposito.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(sTgl),\
           str(uipTutupDeposito.no_rekening),\
           app.ModLibUtils.FormatFloat(',0.00',uipDeposito.akum_nominal or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Tutup Deposito'],['sHeader',sHeader],['sData',sData],['inputer',uipTutupDeposito.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
