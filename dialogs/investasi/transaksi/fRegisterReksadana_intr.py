def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  #form.GetControlByName('pButton.btnOK').Enabled = 0
  #form.GetControlByName('pButton.btnOK').Default = 0
  #form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Visible = 0
  #form.GetControlByName('pButton.btnCancel').Enabled = 0
  #form.GetControlByName('pButton.btnCancel').Cancel = 0
  #form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  #form.GetControlByName('pButton.btnClose').Default = 1
  #form.GetControlByName('pButton.btnClose').Visible = 1
  #form.GetControlByName('pButton.btnClose').Cancel = 1
  #form.Caption = 'Lihat Register Investasi'

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  #form.Caption = 'Otorisasi Register Investasi'

def SetInvCategory(form, mode, inv):
  if mode != 'new':
    # edit, auth, or view
    uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')
    kode_paket_investasi = uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')
    nama_paket_investasi = uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi')
    kode_jns_investasi = uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.kode_jns_investasi')

  uipParameter = form.GetUIPartByName('uipParameter')
  uipParameter.Edit()
  uipParameter.inv = inv
  
  if mode != 'new':
    # edit, auth, or view
    # nilai di lrincianpaketinvestasi diisi lagi karena terhapus
    # akibat pengisian nilai uipParameter.inv
    uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')
    uipRegisterReksadana.Edit()
    uipRegisterReksadana.SetFieldValue('LRincianPaketInvestasi.kode_paket_investasi', kode_paket_investasi)
    uipRegisterReksadana.SetFieldValue('LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi', nama_paket_investasi)
    uipRegisterReksadana.SetFieldValue('LRincianPaketInvestasi.kode_jns_investasi', kode_jns_investasi)

  #if uipParameter.inv == 'A':
  #  uipParameter.strInv = 'Deposito'
  #elif uipParameter.inv == 'B':
  #  uipParameter.strInv = 'Reksadana'
  #if uipParameter.inv == 'C':
  #  uipParameter.strInv = 'Reksadana'

def FormShow(form, parameter):
  #uipParameter = form.GetUIPartByName('uipParameter')
  #SetInvCategory(form, parameter.FirstRecord.mode, parameter.FirstRecord.inv)

  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')

  uipRegisterReksadana.Edit()
  uipRegisterReksadana.mode = parameter.FirstRecord.mode

  # set caption
  form.Caption = parameter.FirstRecord.caption
  if uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.maks_proporsi') not in ('',None) :
      uipRegisterReksadana.maks_proporsi = uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.maks_proporsi')
  if uipRegisterReksadana.mode in ['view', 'auth']:
    if uipRegisterReksadana.mode == 'view':
      SetControlsForView(form)
    elif uipRegisterReksadana.mode == 'auth':
      SetControlsForAuth(form)
  else:
    # new
    if uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi'):
      form.GetControlByName('pData.LRincianPaketInvestasi').Enabled = 0


def LSecTypeAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')
  uipRegisterReksadana.Edit()
  if uipRegisterReksadana.GetFieldValue('LSubJenisInv.kode_subjns_LRInvestasi') == 'RKS':
    form.GetControlByName('pData.LJenisReksadana').Visible = 1
  else:
    form.GetControlByName('pData.LJenisReksadana').Visible = 0
    uipRegisterReksadana.ClearLink('LJenisReksadana')

def LRincianPaketInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')

  res = app.ExecuteScript(
   'investasi/transaksi/paketinvinfo'
   , app.CreateValues(
       ['kode_paket_investasi', uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')]
       , ['kode_jns_investasi', 'R']
     )
  )

  uipRegisterReksadana.Edit()
  uipRegisterReksadana.maks_proporsi = uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.maks_proporsi')
  uipRegisterReksadana.dpkPaket = res.FirstRecord.dpkPaket
  uipRegisterReksadana.dpkInvExisting = res.FirstRecord.dpkInvExisting
  uipRegisterReksadana.nilaiMaksProporsi = res.FirstRecord.nilaiMaksProporsi
  uipRegisterReksadana.dpkTersedia = res.FirstRecord.dpkTersedia
  uipRegisterReksadana.nominalGiro = res.FirstRecord.nominalGiro

  uipRegisterReksadana.nominal = min(uipRegisterReksadana.dpkTersedia, uipRegisterReksadana.nilaiMaksProporsi)

def unit_penyertaanUpdate(uipRegisterReksadana):
  uipRegisterReksadana.Edit()
  if uipRegisterReksadana.NAB_awal > 0.0:
    uipRegisterReksadana.unit_penyertaan = (uipRegisterReksadana.nominal - uipRegisterReksadana.biaya) / uipRegisterReksadana.NAB_awal

## on update nilai investasi (nominal)

def nominalUpdate(uipRegisterReksadana):
  uipRegisterReksadana.Edit()
  uipRegisterReksadana.nominal = (uipRegisterReksadana.nominal or 0.0)

def nominalExit(sender):
  form = sender.OwnerForm
  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')
  nominalUpdate(uipRegisterReksadana)
  biayaUpdate(uipRegisterReksadana)
  NAB_awalUpdate(uipRegisterReksadana)
  unit_penyertaanUpdate(uipRegisterReksadana)

## on update NAB_awal

def NAB_awalUpdate(uipRegisterReksadana):
  uipRegisterReksadana.Edit()
  uipRegisterReksadana.NAB_awal = (uipRegisterReksadana.NAB_awal or 0.0)

def NAB_awalExit(sender):
  form = sender.OwnerForm
  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')
  NAB_awalUpdate(uipRegisterReksadana)
  nominalUpdate(uipRegisterReksadana)
  biayaUpdate(uipRegisterReksadana)
  unit_penyertaanUpdate(uipRegisterReksadana)

## on update biaya

def biayaUpdate(uipRegisterReksadana):
  uipRegisterReksadana.Edit()
  uipRegisterReksadana.biaya = (uipRegisterReksadana.biaya or 0.0)

def biayaExit(sender):
  form = sender.OwnerForm
  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')
  biayaUpdate(uipRegisterReksadana)
  nominalUpdate(uipRegisterReksadana)
  NAB_awalUpdate(uipRegisterReksadana)
  unit_penyertaanUpdate(uipRegisterReksadana)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')
  
  if uipRegisterReksadana.mode not in ['view','auth']:
    form.CommitBuffer()

    if uipRegisterReksadana.mode == 'new':
      uipRegisterReksadana.Edit()
      uipRegisterReksadana.__SYSFLAG = 'N'

    form.PostResult()

    sender.ExitAction = 2
    dlg = app.ConfirmDialog('Cetak advis transaksi?')
    if dlg: CetakAdvis(app, uipRegisterReksadana)

  elif uipRegisterReksadana.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin mengotorisasi investasi baru ini?')
    if dlg:
      # otorisasi
      app.ExecuteScript('investasi/transaksi/registerreksadana_auth',\
        app.CreateValues(['id',uipRegisterReksadana.id_registerinvestasi])\
      )
      #app.ExecuteScript('investasi/transaksi/registerinvestasi_auth',\
      #  app.CreateValues(['id',uipRegisterReksadana.id_registerinvestasi])\
      #)
      sender.ExitAction = 1
  elif uipRegisterReksadana.mode == 'view':
    sender.ExitAction = 2

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')

  if uipRegisterReksadana.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan register investasi baru ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/registerinvestasi_del',\
        app.CreateValues(['id',uipRegisterReksadana.id_registerinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterReksadana = form.GetUIPartByName('uipRegisterReksadana')
  form.CommitBuffer()
  CetakAdvis(app, uipRegisterReksadana)
  
def CetakAdvis(app, uipRegisterReksadana):
  lHeader = ['Nama Investasi', 'Manajer Investasi', 'Paket Investasi', \
             'Maks. Proporsi', 'Nominal Paket', 'Nilai Maks. Proporsi', \
             'Investasi Existing', 'Dana Idle', 'Nominal Giro', \
             'Tgl Buka','Nilai Investasi']
  sHeader = '|'.join(lHeader)
  tgl_buka = uipRegisterReksadana.tgl_buka
  sTglBuka = '%s-%s-%s' % (tgl_buka[2],tgl_buka[1],tgl_buka[0])
  lData = [str(uipRegisterReksadana.nama_reksadana),\
           '%s - %s'% (uipRegisterReksadana.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipRegisterReksadana.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipRegisterReksadana.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterReksadana.maks_proporsi or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterReksadana.dpkPaket or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterReksadana.nilaiMaksProporsi or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterReksadana.dpkInvExisting or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterReksadana.dpkTersedia or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterReksadana.nominalGiro or 0.0),\
           str(sTglBuka),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterReksadana.nominal or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Register Investasi EQ'],['sHeader',sHeader],['sData',sData],['inputer',uipRegisterReksadana.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
