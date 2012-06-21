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
    uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')
    kode_paket_investasi = uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')
    nama_paket_investasi = uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi')
    kode_jns_investasi = uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.kode_jns_investasi')

  uipParameter = form.GetUIPartByName('uipParameter')
  uipParameter.Edit()
  uipParameter.inv = inv
  
  if mode != 'new':
    # edit, auth, or view
    # nilai di lrincianpaketinvestasi diisi lagi karena terhapus
    # akibat pengisian nilai uipParameter.inv
    uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')
    uipRegisterSaham.Edit()
    uipRegisterSaham.SetFieldValue('LRincianPaketInvestasi.kode_paket_investasi', kode_paket_investasi)
    uipRegisterSaham.SetFieldValue('LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi', nama_paket_investasi)
    uipRegisterSaham.SetFieldValue('LRincianPaketInvestasi.kode_jns_investasi', kode_jns_investasi)

  #if uipParameter.inv == 'A':
  #  uipParameter.strInv = 'Deposito'
  #elif uipParameter.inv == 'B':
  #  uipParameter.strInv = 'Saham'
  #if uipParameter.inv == 'C':
  #  uipParameter.strInv = 'Saham'

def FormShow(form, parameter):
  #uipParameter = form.GetUIPartByName('uipParameter')
  #SetInvCategory(form, parameter.FirstRecord.mode, parameter.FirstRecord.inv)

  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')

  uipRegisterSaham.Edit()
  uipRegisterSaham.mode = parameter.FirstRecord.mode

  # set caption
  form.Caption = parameter.FirstRecord.caption
  if uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.maks_proporsi') not in ('',None) :
      uipRegisterSaham.maks_proporsi = uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.maks_proporsi')
  if uipRegisterSaham.mode in ['view', 'auth']:
    if uipRegisterSaham.mode == 'view':
      SetControlsForView(form)
    elif uipRegisterSaham.mode == 'auth':
      SetControlsForAuth(form)
  else:
    # new
    if uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi'):
      # sudah terisi, berarti hanya ada satu paket untuk Saham
      # set disable
      form.GetControlByName('pData.LRincianPaketInvestasi').Enabled = 0


  #else:
  #  SetInvCategory(form, parameter.FirstRecord.inv)
  #  # uipRegisterSaham.mode == 'edit':
  #  #form.Caption = 'Koreksi Register %s' % (uipParameter.strInv)

#def LPaketInvestasiAfterLookup(sender, linkui):
#  form = sender.OwnerForm
#  app = form.ClientApplication
#  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')

#  kode_paket_investasi = uipRegisterSaham.GetFieldValue('LPaketInvestasi.kode_paket_investasi')
#  dh = app.ExecuteScript('investasi/transaksi/rincianpaketinv',\
#    app.CreateValues(['kode_paket_investasi',kode_paket_investasi])\
#  )

#  kode_jns_investasi = dh.FirstRecord.kode_jns_investasi
#  if kode_jns_investasi:
#    uipRegisterSaham.SetFieldValue('LRincianPaketInvestasi.kode_paket_investasi',kode_paket_investasi)
#    uipRegisterSaham.SetFieldValue('LRincianPaketInvestasi.kode_jns_investasi',kode_jns_investasi)
#    uipRegisterSaham.SetFieldValue('LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi',dh.FirstRecord.nama_jns_investasi)

#  uipRegisterSaham.Edit()

#def LRincianPaketInvestasiBeforeLookup(sender, linkui):
#  openlookup = 1
#  uipRegisterSaham = sender.OwnerForm.GetUIPartByName('uipRegisterSaham')
#  if uipRegisterSaham.GetFieldValue('LPaketInvestasi.kode_paket_investasi') \
#    in [None,'']:
#    sender.OwnerForm.ShowMessage('Pilih dahulu Paket Investasi!')
#    openlookup = 0
#
#  return openlookup

def LRincianPaketInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')

  res = app.ExecuteScript(
   'investasi/transaksi/paketinvinfo'
   , app.CreateValues(
       ['kode_paket_investasi', uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')]
       , ['kode_jns_investasi', 'R']
     )
  )

  uipRegisterSaham.Edit()
  uipRegisterSaham.maks_proporsi = uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.maks_proporsi')
  uipRegisterSaham.dpkPaket = res.FirstRecord.dpkPaket
  uipRegisterSaham.dpkInvExisting = res.FirstRecord.dpkInvExisting
  uipRegisterSaham.nilaiMaksProporsi = res.FirstRecord.nilaiMaksProporsi
  uipRegisterSaham.dpkTersedia = res.FirstRecord.dpkTersedia
  uipRegisterSaham.nominalGiro = res.FirstRecord.nominalGiro

  uipRegisterSaham.nominal = min(uipRegisterSaham.dpkTersedia, uipRegisterSaham.nilaiMaksProporsi)

def unit_penyertaanUpdate(uipRegisterSaham):
  uipRegisterSaham.Edit()
  if uipRegisterSaham.NAB_awal > 0.0:
    uipRegisterSaham.unit_penyertaan = (uipRegisterSaham.nominal - uipRegisterSaham.biaya) / uipRegisterSaham.NAB_awal

## on update nilai investasi (nominal)

def nominalUpdate(uipRegisterSaham):
  uipRegisterSaham.Edit()
  uipRegisterSaham.nominal = (uipRegisterSaham.nominal or 0.0)

def nominalExit(sender):
  form = sender.OwnerForm
  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')
  nominalUpdate(uipRegisterSaham)
  biayaUpdate(uipRegisterSaham)
  NAB_awalUpdate(uipRegisterSaham)
  unit_penyertaanUpdate(uipRegisterSaham)

## on update NAB_awal

def NAB_awalUpdate(uipRegisterSaham):
  uipRegisterSaham.Edit()
  uipRegisterSaham.NAB_awal = (uipRegisterSaham.NAB_awal or 0.0)

def NAB_awalExit(sender):
  form = sender.OwnerForm
  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')
  NAB_awalUpdate(uipRegisterSaham)
  nominalUpdate(uipRegisterSaham)
  biayaUpdate(uipRegisterSaham)
  unit_penyertaanUpdate(uipRegisterSaham)

## on update biaya

def biayaUpdate(uipRegisterSaham):
  uipRegisterSaham.Edit()
  uipRegisterSaham.biaya = (uipRegisterSaham.biaya or 0.0)

def biayaExit(sender):
  form = sender.OwnerForm
  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')
  biayaUpdate(uipRegisterSaham)
  nominalUpdate(uipRegisterSaham)
  NAB_awalUpdate(uipRegisterSaham)
  unit_penyertaanUpdate(uipRegisterSaham)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')
  
  if uipRegisterSaham.mode not in ['view','auth']:
    form.CommitBuffer()

    if uipRegisterSaham.mode == 'new':
      uipRegisterSaham.Edit()
      uipRegisterSaham.__SYSFLAG = 'N'

    form.PostResult()

    sender.ExitAction = 2
    dlg = app.ConfirmDialog('Cetak advis transaksi?')
    if dlg: CetakAdvis(app, uipRegisterSaham)

  elif uipRegisterSaham.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin mengotorisasi investasi baru ini?')
    if dlg:
      # otorisasi
      app.ExecuteScript('investasi/transaksi/registerSaham_auth',\
        app.CreateValues(['id',uipRegisterSaham.id_registerinvestasi])\
      )
      #app.ExecuteScript('investasi/transaksi/registerinvestasi_auth',\
      #  app.CreateValues(['id',uipRegisterSaham.id_registerinvestasi])\
      #)
      sender.ExitAction = 1
  elif uipRegisterSaham.mode == 'view':
    sender.ExitAction = 2

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')

  if uipRegisterSaham.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan register investasi baru ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/registerinvestasi_del',\
        app.CreateValues(['id',uipRegisterSaham.id_registerinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterSaham = form.GetUIPartByName('uipRegisterSaham')
  form.CommitBuffer()
  CetakAdvis(app, uipRegisterSaham)
  
def CetakAdvis(app, uipRegisterSaham):
  lHeader = ['Nama Saham', 'No. Batch', 'Manajer Investasi', 'Paket Investasi', \
             'Maks. Proporsi', 'Nominal Paket', 'Nilai Maks. Proporsi', \
             'Saham Existing', 'Dana Idle', 'Nominal Giro', \
             'Tgl Buka','Nilai Investasi']
  sHeader = '|'.join(lHeader)
  tgl_buka = uipRegisterSaham.tgl_buka
  sTglBuka = '%s-%s-%s' % (tgl_buka[2],tgl_buka[1],tgl_buka[0])
  lData = [str(uipRegisterSaham.nama_Saham),\
           str(uipRegisterSaham.GetFieldValue('LTransactionBatch.no_batch')),\
           '%s - %s'% (uipRegisterSaham.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipRegisterSaham.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipRegisterSaham.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterSaham.maks_proporsi or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterSaham.dpkPaket or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterSaham.nilaiMaksProporsi or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterSaham.dpkInvExisting or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterSaham.dpkTersedia or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterSaham.nominalGiro or 0.0),\
           str(sTglBuka),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterSaham.nominal or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Register Saham'],['sHeader',sHeader],['sData',sData],['inputer',uipRegisterSaham.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
