dictJangkaWaktu = {1:'1 Bulan',3:'3 Bulan',6:'6 Bulan',12:'12 Bulan',0:'On Call'}
dictTreatmentPokok = {'A':'ARO','K':'Konfirmasi','P':'Pindah Buku'} 
dictBagiHasil = {'F':'Pindah Buku','T':'Kapitalisir'}

def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('gRincianInvestasi').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  form.GetControlByName('pButton.btnCancel').Visible = 0

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('gRincianInvestasi').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1

def SetInvCategory(form, mode, inv):
  if mode != 'new':
    # edit, auth, or view
    uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
    kode_paket_investasi = uipRegisterDeposito.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')
    nama_paket_investasi = uipRegisterDeposito.GetFieldValue('LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi')
    kode_jns_investasi = uipRegisterDeposito.GetFieldValue('LRincianPaketInvestasi.kode_jns_investasi')

  uipParameter = form.GetUIPartByName('uipParameter')
  uipParameter.Edit()
  uipParameter.inv = inv
  
  if mode != 'new':
    # edit, auth, or view
    # nilai di lrincianpaketinvestasi diisi lagi karena terhapus
    # akibat pengisian nilai uipParameter.inv
    uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
    uipRegisterDeposito.Edit()
    uipRegisterDeposito.SetFieldValue('LRincianPaketInvestasi.kode_paket_investasi', kode_paket_investasi)
    uipRegisterDeposito.SetFieldValue('LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi', nama_paket_investasi)
    uipRegisterDeposito.SetFieldValue('LRincianPaketInvestasi.kode_jns_investasi', kode_jns_investasi)

def FormShow(form, parameter):
  #uipParameter = form.GetUIPartByName('uipParameter')
  #SetInvCategory(form, parameter.FirstRecord.mode, parameter.FirstRecord.inv)

  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')

  uipRegisterDeposito.Edit()
  uipRegisterDeposito.mode = parameter.FirstRecord.mode

  # set caption
  form.Caption = parameter.FirstRecord.caption

  if uipRegisterDeposito.mode in ['view', 'auth']:
    if uipRegisterDeposito.mode == 'view':
      SetControlsForView(form)
    elif uipRegisterDeposito.mode == 'auth':
      SetControlsForAuth(form)

  jenisJatuhTempoChange(form.GetControlByName('pDataRight.jenisJatuhTempo'))
  #treatmentPokokChange(form.GetControlByName('pDataRight.treatmentPokok'))
  kapitalisir_rolloverChange(form.GetControlByName('pDataRight.kapitalisir_rollover'))

def jenisJatuhTempoChange(sender):
  form = sender.OwnerForm
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')

  uipRegisterDeposito.Edit()
    
  if sender.ItemIndex == 4:
    # deposito on call
    uipRegisterDeposito.SetFieldValue('LSubJenisInv.kode_subjns_LRInvestasi','DOC')
    uipRegisterDeposito.SetFieldValue('LSubJenisInv.deskripsi','Deposito On Call')
    form.GetControlByName('pDataRight.jmlHariOnCall').Visible = 1
  else:
    uipRegisterDeposito.SetFieldValue('LSubJenisInv.kode_subjns_LRInvestasi','TDP')
    uipRegisterDeposito.SetFieldValue('LSubJenisInv.deskripsi','Time Deposit')
    form.GetControlByName('pDataRight.jmlHariOnCall').Visible = 0
    uipRegisterDeposito.jmlHariOnCall = None

def treatmentPokokChange(sender):
  pass
##  form = sender.OwnerForm
##  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
##  kapitalisir_rolloverCtrl = form.GetControlByName('pDataRight.kapitalisir_rollover')
##
##  if sender.ItemIndex == 2:
##    # pindah buku
##    uipRegisterDeposito.Edit()
##    uipRegisterDeposito.kapitalisir_rollover = 'F'
##    form.GetControlByName('pDataRight.kapitalisir_rollover').Visible = 0
##  else:
##    form.GetControlByName('pDataRight.kapitalisir_rollover').Visible = 1
##
##  if ((sender.ItemIndex == 0) and not kapitalisir_rolloverCtrl.Checked) \
##    or (sender.ItemIndex == 2):
##    # ARO non kapitalisir
##    # atau Pindah Buku
##    form.GetControlByName('pDataRight.no_rekening').Visible = 1
##  else:
##    # konfirmasi atau ARO kapitalisir
##    uipRegisterDeposito.Edit()
##    uipRegisterDeposito.no_rekening = ''
##    form.GetControlByName('pDataRight.no_rekening').Visible = 0

def kapitalisir_rolloverChange(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')

  if sender.ItemIndex == 0:
    # pindah buku
    #form.GetControlByName('pDataRight.no_rekening').Visible = 1
    form.GetControlByName('pDataRight.LMasterGiro').Visible = 1
  else:
    # kapitalisir
    uipRegisterDeposito.Edit()
    #uipRegisterDeposito.no_rekening = ''
    #form.GetControlByName('pDataRight.no_rekening').Visible = 0
    uipRegisterDeposito.SetFieldValue('LMasterGiro.acc_giro', None)
    uipRegisterDeposito.SetFieldValue('LMasterGiro.no_giro', None)
    form.GetControlByName('pDataRight.LMasterGiro').Visible = 0

    #formObj = app.CreateForm('investasi/transaksi/fInputNomorRekening', 'fInputNomorRekening', 0, None, None)
    #formObj.ShowForm()
    #no_giro = formObj.Show()
    #if no_giro:
    #  uipRegisterDeposito.Edit()
    #  uipRegisterDeposito.no_rekening = no_giro
    #else:
    #  pass

##  treatmentPokokCtrl = form.GetControlByName('pDataRight.treatmentPokok')
##
##  if ((treatmentPokokCtrl.ItemIndex == 0) and not sender.Checked) \
##    or (treatmentPokokCtrl.ItemIndex == 2):
##    # ARO non kapitalisir
##    # atau Pindah Buku
##    form.GetControlByName('pDataRight.no_rekening').Visible = 1
##  else:
##    # konfirmasi atau ARO kapitalisir
##    uipRegisterDeposito.Edit()
##    uipRegisterDeposito.no_rekening = ''
##    form.GetControlByName('pDataRight.no_rekening').Visible = 0

def LSecTypeAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
  uipRegisterDeposito.Edit()
  if uipRegisterDeposito.GetFieldValue('LSubJenisInv.kode_subjns_LRInvestasi') == 'DOC':
    form.GetControlByName('pDataRight.jenisJatuhTempo').ItemIndex = 4
    form.GetControlByName('pDataRight.jmlHariOnCall').Visible = 1
  else:
    form.GetControlByName('pDataRight.jmlHariOnCall').Visible = 0
    form.GetControlByName('pDataRight.jenisJatuhTempo').ItemIndex = 0
    uipRegisterDeposito.jmlHariOnCall = None

def LRincianPaketInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRincianRegisterDeposito = form.GetUIPartByName('uipRincianRegisterDeposito')
  
  kode_paket_investasi = uipRincianRegisterDeposito.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')

  res = app.ExecuteScript(
   'investasi/transaksi/paketinvinfo'
   , app.CreateValues(
       ['kode_paket_investasi', kode_paket_investasi]
       , ['kode_jns_investasi', 'D']
     )
  )

  uipRincianRegisterDeposito.Edit()
  uipRincianRegisterDeposito.dpkPaket = res.FirstRecord.dpkPaket
  uipRincianRegisterDeposito.dpkInvExisting = res.FirstRecord.dpkInvExisting
  uipRincianRegisterDeposito.dpkTersedia = res.FirstRecord.dpkTersedia
  uipRincianRegisterDeposito.nilaiMaksProporsi = res.FirstRecord.nilaiMaksProporsi
  uipRincianRegisterDeposito.nominalGiro = res.FirstRecord.nominalGiro

  minTersedia = min(
    uipRincianRegisterDeposito.dpkTersedia
    , uipRincianRegisterDeposito.nilaiMaksProporsi
    #, uipRincianRegisterDeposito.nominalGiro
  )
  if minTersedia <= 0.0:
    #raise 'Kesalahan Paket Investasi', '\nDana paket investasi %s tidak tersedia.' % (kode_paket_investasi)
    app.ShowMessage('Dana paket investasi %s tidak tersedia.' % (kode_paket_investasi))
  else:
    uipRincianRegisterDeposito.nominal = minTersedia

def uipRRDBeforePost(uipRRD):
  form = uipRRD.OwnerForm

  uipRRD.nominal = uipRRD.nominal or 0.0
#   if uipRRD.nominal > min(uipRRD.dpkTersedia, uipRRD.nilaiMaksProporsi, uipRRD.nominalGiro):
  if uipRRD.nominal > min(uipRRD.dpkTersedia, uipRRD.nilaiMaksProporsi):
    raise 'Kesalahan Nominal Pembukaan', '\nNominal pembukaan melebihi nilai yang tersedia.'

def HitungNominalTotal(uipRegisterDeposito, uipRRD):
  uipRegisterDeposito.Edit()
  uipRegisterDeposito.nominal = 0.0

  uipRRD.First()
  while not uipRRD.Eof:
    uipRegisterDeposito.Edit()
    uipRegisterDeposito.nominal += uipRRD.nominal or 0.0

    uipRRD.Next()

def uipRRDAfterPost(uipRRD):
  form = uipRRD.OwnerForm

  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
  HitungNominalTotal(uipRegisterDeposito, uipRRD)

def uipRRDAfterDelete(uipRRD):
  form = uipRRD.OwnerForm

  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
  HitungNominalTotal(uipRegisterDeposito, uipRRD)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
  
  if uipRegisterDeposito.mode not in ['view','auth']:
    form.CommitBuffer()

    if uipRegisterDeposito.mode == 'new':
      uipRegisterDeposito.Edit()
      uipRegisterDeposito.__SYSFLAG = 'N'

    form.PostResult()
    sender.ExitAction = 2
    dlg = app.ConfirmDialog('Cetak advis transaksi?')
    if dlg: CetakAdvis(app, uipRegisterDeposito)

  elif uipRegisterDeposito.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin mengotorisasi investasi baru ini?')
    if dlg:
      # otorisasi
      app.ExecuteScript('investasi/transaksi/registerdeposito_auth',\
        app.CreateValues(['id',uipRegisterDeposito.id_registerinvestasi])\
      )
      sender.ExitAction = 1
  elif uipRegisterDeposito.mode == 'view':
    sender.ExitAction = 2

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')

  if uipRegisterDeposito.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan register investasi baru ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/registerinvestasi_del',\
        app.CreateValues(['id',uipRegisterDeposito.id_registerinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterDeposito = form.GetUIPartByName('uipRegisterDeposito')
  form.CommitBuffer()
  CetakAdvis(app, uipRegisterDeposito)

def CetakAdvis(app, uipRegisterDeposito):
  lHeader = ['Rekening Deposito', 'No. Bilyet', 'Pihak Ketiga',\
             'Rate', 'Tgl Buka', 'Jangka Waktu', 'Jatuh Tempo On Call',\
             'Pokok Saat Jatuh Tempo', 'Bagi Hasil', 'Rekening Tujuan', \
             'Nominal Pembukaan']
  sHeader = '|'.join(lHeader)
  tgl = uipRegisterDeposito.tgl_buka
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipRegisterDeposito.rekening_deposito),\
           str(uipRegisterDeposito.no_bilyet),\
           '%s - %s' % (uipRegisterDeposito.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'), \
           uipRegisterDeposito.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           app.ModLibUtils.FormatFloat(',0.00 %',uipRegisterDeposito.equivalent_rate or 0.0),\
           str(sTgl),\
           dictJangkaWaktu[uipRegisterDeposito.jenisJatuhTempo],\
           app.ModLibUtils.FormatFloat('0',uipRegisterDeposito.jmlHariOnCall or 0),\
           dictTreatmentPokok[uipRegisterDeposito.treatmentPokok],\
           dictBagiHasil[uipRegisterDeposito.kapitalisir_rollover],\
           str(uipRegisterDeposito.GetFieldValue('LMasterGiro.no_giro')),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterDeposito.nominal or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Registrasi Deposito'],['sHeader',sHeader],['sData',sData],['inputer',uipRegisterDeposito.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
