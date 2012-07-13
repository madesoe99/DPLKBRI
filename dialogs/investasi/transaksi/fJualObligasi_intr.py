dictJenisSukuk = {'K':'Korporat','P':'Pemda','N':'Negara',None:'','R':''}

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
  form.Caption = 'Lihat Register Jual Obligasi'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Jual Obligasi'
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
  form.GetControlByName('pSelector.LObligasi').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  #form.Caption = parameter.FirstRecord.caption

  uipJualObligasi = form.GetUIPartByName('uipJualObligasi')

  uipJualObligasi.Edit()
  uipJualObligasi.mode = parameter.FirstRecord.mode

  if (uipJualObligasi.mode == 'new'):
    if uipJualObligasi.GetFieldValue('LObligasi.id_investasi'):
      SetSelectorReadOnly(form)

      uipObligasi = form.GetUIPartByName('uipObligasi')
      uipJualObligasi.nominal_jual = uipObligasi.akum_nominal
      uipJualObligasi.PersenJual = 100.0
      # set nilai no_rekening sebagai default pencairan
      uipJualObligasi.no_rekening = uipObligasi.no_rekening
  uipJualObligasi.SetFieldValue('LMasterGiro.no_giro',uipJualObligasi.no_rekening)
  if uipJualObligasi.mode == 'viewdoc':
    #form.Caption = 'Lihat Transaksi Jual Obligasi'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipJualObligasi.mode == 'view':
      SetControlsForView(form)
    elif uipJualObligasi.mode == 'auth':
      SetControlsForAuth(form)
    elif uipJualObligasi.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Jual Obligasi'

def OnAfterLookup_Rek(sender, linkui) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipJualObligasi')
  uip.no_rekening = uip.GetFieldValue('LMasterGiro.no_giro')

def LObligasiAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipJualObligasi = form.GetUIPartByName('uipJualObligasi')
  uipJualObligasi.Edit()
  uipJualObligasi.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipJualObligasi.GetFieldValue('LObligasi.kode_pihak_ketiga'))
  uipJualObligasi.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipJualObligasi.GetFieldValue('LObligasi.LPihakKetiga.nama_pihak_ketiga'))
  uipJualObligasi.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipJualObligasi.GetFieldValue('LObligasi.kode_paket_investasi'))
  uipJualObligasi.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipJualObligasi.GetFieldValue('LObligasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  uipJualObligasi.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipJualObligasi.GetFieldValue('LObligasi.kode_jns_investasi'))
  uipJualObligasi.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipJualObligasi.GetFieldValue('LObligasi.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipObligasi = form.GetUIPartByName('uipObligasi')
  uipObligasi.Edit()
  uipObligasi.akum_nominal = uipJualObligasi.GetFieldValue('LObligasi.akum_nominal')
  uipObligasi.jenis_obligasi = uipJualObligasi.GetFieldValue('LObligasi.jenis_obligasi')
  uipObligasi.tgl_jatuh_tempo = uipJualObligasi.GetFieldValue('LObligasi.tgl_jatuh_tempo')
  uipObligasi.no_rekening = uipJualObligasi.GetFieldValue('LObligasi.no_rekening')
  uipJualObligasi.no_rekening = uipJualObligasi.GetFieldValue('LObligasi.no_rekening')

## on update harga pari

def nominal_jualUpdate(uipJualObligasi, uipObligasi):
  uipJualObligasi.Edit()
  uipJualObligasi.profit = (uipJualObligasi.nominal_jual or 0.0) - (uipObligasi.akum_nominal or 0.0)

def nominal_jualExit(sender):
  form = sender.OwnerForm
  uipJualObligasi = form.GetUIPartByName('uipJualObligasi')
  uipObligasi = form.GetUIPartByName('uipObligasi')
  nominal_jualUpdate(uipJualObligasi, uipObligasi)
  uipJualObligasi.PersenJual = (uipJualObligasi.nominal_jual/uipObligasi.akum_nominal) * 100

def Persen_OnExit (sender) :
  form = sender.OwnerForm
  uipJualObligasi = form.GetUIPartByName('uipJualObligasi')
  uipObligasi = form.GetUIPartByName('uipObligasi')
  uipJualObligasi.nominal_jual = uipJualObligasi.PersenJual*uipObligasi.akum_nominal / 100
  nominal_jualUpdate(uipJualObligasi, uipObligasi)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipJualObligasi = form.GetUIPartByName('uipJualObligasi')
  uipObligasi = form.GetUIPartByName('uipObligasi')
  if uipJualObligasi.no_rekening in ('',None) or uipJualObligasi.pembeli in ('',None) :
    raise Exception, 'PERINGATAN' + 'Nama Pembeli dan no rekening pencairan HARUS DIISI'
  if uipJualObligasi.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipJualObligasi.mode not in ['view','auth']:
      form.CommitBuffer()

      nominal_jualExit(sender)

      if uipJualObligasi.mode == 'new':
        uipJualObligasi.Edit()
        uipJualObligasi.__SYSFLAG = 'N'

      form.PostResult()
      sender.ExitAction = 2

      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipJualObligasi, uipObligasi)

    elif uipJualObligasi.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui penjualan obligasi ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/jualobligasi_auth',\
          app.CreateValues(['id',uipJualObligasi.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipJualObligasi = form.GetUIPartByName('uipJualObligasi')

  if uipJualObligasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan penjualan investasi ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/tutupinv_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipJualObligasi.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipJualObligasi = form.GetUIPartByName('uipJualObligasi')
  uipObligasi = form.GetUIPartByName('uipObligasi')
  form.CommitBuffer()
  CetakAdvis(app, uipJualObligasi, uipObligasi)
  
def CetakAdvis(app, uipJualObligasi, uipObligasi):
  lHeader = ['Nama Investasi', 'Pihak Ketiga', 'Paket Investasi', \
             'Tgl Transaksi', 'Persen Jual', 'Harga Jual', 'Profit', 'No. Rekening', \
             'Pembeli', 'Nominal', 'Tgl Jatuh Tempo']
  sHeader = '|'.join(lHeader)
  tgl = uipJualObligasi.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  tglJT = uipObligasi.tgl_jatuh_tempo
  sTglJT = '%s-%s-%s' % (tglJT[2],tglJT[1],tglJT[0])
  lData = [str(uipJualObligasi.GetFieldValue('LObligasi.nama_obligasi')),\
           '%s - %s'% (uipJualObligasi.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipJualObligasi.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipJualObligasi.GetFieldValue('LPaketInvestasi.kode_paket_investasi')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.00 %',uipJualObligasi.persenJual or 0),\
           app.ModLibUtils.FormatFloat(',0.00',uipJualObligasi.nominal_jual or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipJualObligasi.profit or 0.0),\
           str(uipJualObligasi.no_rekening),\
           str(uipJualObligasi.pembeli),\
           app.ModLibUtils.FormatFloat(',0.00',uipObligasi.akum_nominal or 0.0),\
           str(sTglJT)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Jual Investasi FIX'],['sHeader',sHeader],['sData',sData],['inputer',uipJualObligasi.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
