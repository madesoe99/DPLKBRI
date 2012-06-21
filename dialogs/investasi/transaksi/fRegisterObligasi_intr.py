dictTreatmentSukuk = {'H':'Hold to Maturity', 'R':'Ready to Sell'}
dictKupon = {1:'Bulanan',3:'Triwulan',6:'Semester',12:'Tahunan'}
dictJenisSukuk = {'K':'Korporat','P':'Pemda','N':'Negara',None:'','R':''}

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
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  #form.Caption = 'Otorisasi Register Investasi'

def SetInvCategory(form, mode, inv):
  if mode != 'new':
    # edit, auth, or view
    uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')
    kode_paket_investasi = uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')
    nama_paket_investasi = uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi')
    kode_jns_investasi = uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.kode_jns_investasi')

  uipParameter = form.GetUIPartByName('uipParameter')
  uipParameter.Edit()
  uipParameter.inv = inv
  
  if mode != 'new':
    # edit, auth, or view
    # nilai di lrincianpaketinvestasi diisi lagi karena terhapus
    # akibat pengisian nilai uipParameter.inv
    uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')
    uipRegisterObligasi.Edit()
    uipRegisterObligasi.SetFieldValue('LRincianPaketInvestasi.kode_paket_investasi', kode_paket_investasi)
    uipRegisterObligasi.SetFieldValue('LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi', nama_paket_investasi)
    uipRegisterObligasi.SetFieldValue('LRincianPaketInvestasi.kode_jns_investasi', kode_jns_investasi)

  #if uipParameter.inv == 'A':
  #  uipParameter.strInv = 'Deposito'
  #elif uipParameter.inv == 'B':
  #  uipParameter.strInv = 'Obligasi'
  #if uipParameter.inv == 'C':
  #  uipParameter.strInv = 'Reksadana'

def FormShow(form, parameter):
  #uipParameter = form.GetUIPartByName('uipParameter')
  #SetInvCategory(form, parameter.FirstRecord.mode, parameter.FirstRecord.inv)

  uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')

  uipRegisterObligasi.Edit()
  uipRegisterObligasi.mode = parameter.FirstRecord.mode

  if uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.maks_proporsi') not in ('',None) :
    uipRegisterObligasi.maks_proporsi = uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.maks_proporsi')
    
  harga_pariUpdate(uipRegisterObligasi)

  # set caption
  form.Caption = parameter.FirstRecord.caption
  if uipRegisterObligasi.mode in ['view', 'auth']:
    if uipRegisterObligasi.mode == 'view':
      SetControlsForView(form)
    elif uipRegisterObligasi.mode == 'auth':
      SetControlsForAuth(form)
  else:
    # new
    if uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi'):
      # sudah terisi, berarti hanya ada satu paket untuk obligasi
      # set disable
      form.GetControlByName('pData.LRincianPaketInvestasi').Enabled = 0


def LRincianPaketInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')

  res = app.ExecuteScript(
   'investasi/transaksi/paketinvinfo'
   , app.CreateValues(
       ['kode_paket_investasi', uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')]
       , ['kode_jns_investasi', 'O']
     )
  )

  uipRegisterObligasi.Edit()
  uipRegisterObligasi.maks_proporsi = uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.maks_proporsi')
  uipRegisterObligasi.dpkPaket = res.FirstRecord.dpkPaket
  uipRegisterObligasi.dpkInvExisting = res.FirstRecord.dpkInvExisting
  uipRegisterObligasi.nilaiMaksProporsi = res.FirstRecord.nilaiMaksProporsi
  uipRegisterObligasi.dpkTersedia = res.FirstRecord.dpkTersedia
  uipRegisterObligasi.nominalGiro = res.FirstRecord.nominalGiro

## on update harga beli

def harga_beliUpdate(uipRegisterObligasi):
  uipRegisterObligasi.Edit()
  uipRegisterObligasi.harga_beli = (uipRegisterObligasi.harga_beli or 0.0)
  uipRegisterObligasi.harga_beli_val = uipRegisterObligasi.harga_beli * uipRegisterObligasi.harga_pari / 100.0

def harga_beliExit(sender):
  form = sender.OwnerForm
  uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')
  harga_beliUpdate(uipRegisterObligasi)

## on update nilai wajar

def nilai_wajarUpdate(uipRegisterObligasi):
  uipRegisterObligasi.Edit()
  uipRegisterObligasi.nilai_wajar = (uipRegisterObligasi.nilai_wajar or 0.0)
  uipRegisterObligasi.nilai_wajar_val = uipRegisterObligasi.nilai_wajar * uipRegisterObligasi.harga_pari / 100.0

def nilai_wajarExit(sender):
  form = sender.OwnerForm
  uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')
  nilai_wajarUpdate(uipRegisterObligasi)

## on update harga pari

def harga_pariUpdate(uipRegisterObligasi):
  uipRegisterObligasi.Edit()
  uipRegisterObligasi.harga_pari = (uipRegisterObligasi.harga_pari or 0.0)
  harga_beliUpdate(uipRegisterObligasi)
  nilai_wajarUpdate(uipRegisterObligasi)

def harga_pariExit(sender):
  form = sender.OwnerForm
  uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')
  harga_pariUpdate(uipRegisterObligasi)

def OnChange_Akad (sender) :
  form = sender.OwnerForm
  if sender.ItemIndex == 0 :
    form.GetControlByName('pDataRight.biaya').Visible = 1
  else :
    form.GetControlByName('pDataRight.biaya').Visible = 0
    form.GetUIPartByName('uipRegisterObligasi').biaya = 0

def OnAfterLookup_Rek(sender, linkui) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipRegisterObligasi')
  uip.no_rekening = uip.GetFieldValue('LMasterGiro.no_giro')


def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')
  
  if uipRegisterObligasi.mode not in ['view','auth']:
    form.CommitBuffer()

    harga_pariExit(sender)

    if uipRegisterObligasi.mode == 'new':
      uipRegisterObligasi.Edit()
      uipRegisterObligasi.__SYSFLAG = 'N'

    form.PostResult()
    sender.ExitAction = 2
    dlg = app.ConfirmDialog('Cetak advis transaksi?')
    if dlg: CetakAdvis(app, uipRegisterObligasi)

  elif uipRegisterObligasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin mengotorisasi investasi baru ini?')
    if dlg:
      # otorisasi
      app.ExecuteScript('investasi/transaksi/registerobligasi_auth',\
        app.CreateValues(['id',uipRegisterObligasi.id_registerinvestasi])\
      )
      #app.ExecuteScript('investasi/transaksi/registerinvestasi_auth',\
      #  app.CreateValues(['id',uipRegisterObligasi.id_registerinvestasi])\
      #)
      sender.ExitAction = 1
  elif uipRegisterObligasi.mode == 'view':
    sender.ExitAction = 2

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')

  if uipRegisterObligasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan register investasi baru ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/registerinvestasi_del',\
        app.CreateValues(['id',uipRegisterObligasi.id_registerinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterObligasi = form.GetUIPartByName('uipRegisterObligasi')
  form.CommitBuffer()
  CetakAdvis(app, uipRegisterObligasi)

def CetakAdvis(app, uipRegisterObligasi):
  lHeader = ['Nama Sukuk', 'Pihak Ketiga', 'Paket Investasi', \
             'Maks. Proporsi', 'Nominal Paket', 'Nilai Maks. Proporsi', \
             'Sukuk Existing', 'Dana Idle', 'Nominal Giro', 'Nominal Sukuk',\
             '% Harga Beli', 'Harga Beli', '% Nilai Wajar', 'Nilai Wajar',\
             'Treatment Sukuk', 'Tgl Pembelian', 'Tgl Jatuh Tempo', 'Kupon',\
             'Jenis Sukuk', 'Custodian Bank', 'No. Rekening']
  sHeader = '|'.join(lHeader)
  tgl_beli = uipRegisterObligasi.tgl_buka
  sTglBeli = '%s-%s-%s' % (tgl_beli[2],tgl_beli[1],tgl_beli[0])
  tgl_jt = uipRegisterObligasi.tgl_jatuh_tempo
  sTglJT = '%s-%s-%s' % (tgl_jt[2],tgl_jt[1],tgl_jt[0])
  lData = [str(uipRegisterObligasi.nama_obligasi),\
           '%s - %s'% (uipRegisterObligasi.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipRegisterObligasi.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipRegisterObligasi.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.maks_proporsi or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.dpkPaket or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.nilaiMaksProporsi or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.dpkInvExisting or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.dpkTersedia or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.nominalGiro or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.harga_pari or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00 %',uipRegisterObligasi.harga_beli or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.harga_beli_val or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00 %',uipRegisterObligasi.nilai_wajar or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipRegisterObligasi.nilai_wajar_val or 0.0),\
           dictTreatmentSukuk[uipRegisterObligasi.TreatmentObligasi],\
           str(sTglBeli),\
           str(sTglJT),\
           dictKupon[uipRegisterObligasi.jenisKupon],\
           dictJenisSukuk[uipRegisterObligasi.jenis_obligasi],\
           '%s - %s'% (uipRegisterObligasi.GetFieldValue('LCustodianBank.BankCode'),\
           uipRegisterObligasi.GetFieldValue('LCustodianBank.BankName')),\
           str(uipRegisterObligasi.no_rekening)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Register Sukuk'],['sHeader',sHeader],['sData',sData],['inputer',uipRegisterObligasi.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
