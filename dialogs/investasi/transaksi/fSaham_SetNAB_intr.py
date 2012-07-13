dictJenisPerubahan = {0:'Subscribe Baru',1:'NAB',2:'Redempt Saham'}
dictProsesHasilSaham = {0:'Tidak Proses',1:'Proses Hasil Saham'}

def FormShow(form, parameter):
  pButton = form.GetPanelByName('pButton')
  form.Caption = parameter.FirstRecord.caption
  uipReksa =   form.GetUIPartByName('uipSaham')
  OtoStatus = uipReksa.IsCommited
  uipReksa.Edit()
  uipReksa.Mode = parameter.FirstRecord.mode
  pData = form.GetPanelByName('pData')
  pPrint = form.GetPanelByName('pPrint')
  pData.GetControlByName('ProsesHasilSaham').Visible = 1
  if uipReksa.Mode == 'mnuOtoNAB' :
    if OtoStatus :
      raise Exception, '\nPERINGATAN' + 'Data belum mengalami perubahan apapun'
    form.SetAllControlsReadOnly()
    pButton.GetControlByName('btnClose').Visible = 1
    pButton.GetControlByName('btnOK').Caption = '&Otorisasi'
    pButton.GetControlByName('btnClose').Enabled = 1
    pButton.GetControlByName('btnOK').Enabled = 1
    pButton.GetControlByName('btnCancel').Enabled = 1
    pPrint.GetControlByName('btnPrint').Visible = 1
    pPrint.GetControlByName('btnPrint').Enabled = 1
    pData.GetControlByName('ProsesHasilSaham').Visible = 1
    if uipReksa.NABSubs == 0.0 : #disertai Update Subscribe
        uipReksa.jenis_perubahan = 0
    elif uipReksa.NABRedempt == 0.0 : #disertai perubahan redempt
        uipReksa.jenis_perubahan = 2

  else :
    pButton.GetControlByName('btnCancel').Cancel = 1
    if uipReksa.Mode == 'mnuKoreksiNAB' :
      if not OtoStatus :
        raise Exception, '\nPERINGATAN' + 'Perubahan Data belum di otorisasi'
      if uipReksa.NABSubs == 0.0 : #disertai Update Subscribe
        uipReksa.jenis_perubahan = 0
        pData.GetControlByName('NomSubscribe').visible = 1
        pData.GetControlByName('unit_penyertaanbaru').ControlCaption = 'UP Subscribe'
      elif uipReksa.NABRedempt == 0.0 : #disertai perubahan redempt
        uipReksa.jenis_perubahan = 2
        uipReksa.NomSubscribe = uipReksa.NomRedempt
        pData.GetControlByName('NomSubscribe').visible = 1
        pData.GetControlByName('NomSubscribe').ControlCaption = 'Nom Redempt'
        pData.GetControlByName('unit_penyertaanbaru').ControlCaption = 'UP Redempt'
        uipReksa.unit_penyertaanbaru = uipReksa.UPRedempt
      else : #hanya perubahan NAB
        pData.GetControlByName('unit_penyertaanbaru').ReadOnly = 1
        uipReksa.unit_penyertaanbaru = uipReksa.unit_penyertaan
  pData.GetControlByName('ProsesHasilSaham').Enabled = 0

def printAdvis(form):
  app = form.ClientApplication

  res = app.ExecuteScript('investasi/report/koreksinab',
    form.GetDataPacket()
  )

  app.DownloadItem(res.FirstRecord.filename,'v')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  pData = form.GetPanelByName('pData')
  uip = 'uipSaham'
  if app.ConfirmDialog('Anda yakin akan menyimpan data ini ?') :
    if sender.Caption == '&Otorisasi' :
      form.GetUIPartByName(uip).Edit()
      form.GetUIPartByName(uip).ModeOto = 1
      form.CommitBuffer()
      app.ExecuteScript('investasi/transaksi/perubahanSaham_auth', form.GetDataPacket())
      sender.ExitAction = 2
    else :
      #if app.ConfirmDialog('Cetak advis perubahan %s ?'
      #  %(JnsPerubahan[pData.GetControlByName('Jenis_Perubahan').ItemIndex])):
      #  printAdvis(form)
      form.PostResult()

      sender.ExitAction = 2
      
      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, form.GetUIPartByName('uipSaham'))



def btnCancelClick(sender) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = 'uipSaham'
  if form.GetUIPartByName(uip).Mode == 'mnuOtoNAB' :
    if app.ConfirmDialog('Anda yakin akan membatalkan perubahan ini ?') :
      #batalkan otorisasi
      form.GetUIPartByName(uip).Edit()
      form.GetUIPartByName(uip).ModeOto = 0
      form.CommitBuffer()
      app.ExecuteScript('investasi/transaksi/perubahanSaham_auth',
       form.GetDataPacket())
    else :
      return 0
  sender.ExitAction = 2
  
def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipSaham = form.GetUIPartByName('uipSaham')

  form.CommitBuffer()

  #printAdvis(form)
  CetakAdvis(app, uipSaham)


def CetakAdvis(app, uipSaham):
  lHeader = ['Nama Saham', 'Manajer Investasi', 'Paket Investasi', 'Tgl Buka',\
             'Nilai Investasi', 'Jenis Perubahan', 'No. Batch', 'UP Total', 'NAB',\
             'Proses Hasil Saham', 'Tgl Penetapan']
  sHeader = '|'.join(lHeader)
  tgl_buka = uipSaham.tgl_buka
  sTglBuka = '%s-%s-%s' % (tgl_buka[2],tgl_buka[1],tgl_buka[0])
  tgl_penetapan = uipSaham.tgl_penetapan
  sTglPenetapan = '%s-%s-%s' % (tgl_penetapan[2],tgl_penetapan[1],tgl_penetapan[0])
  lData = [str(uipSaham.nama_Saham),\
           '%s - %s'% (uipSaham.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipSaham.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipSaham.GetFieldValue('LRincianPaketInvestasi.kode_paket_investasi')),\
           str(sTglBuka),\
           app.ModLibUtils.FormatFloat(',0.0000',uipSaham.akum_nominal or 0.0),\
           dictJenisPerubahan[uipSaham.jenis_perubahan],\
           str(uipSaham.GetFieldValue('LTransactionBatch.no_batch')),\
           app.ModLibUtils.FormatFloat(',0.0000',uipSaham.unit_penyertaan or 0.0),\
           app.ModLibUtils.FormatFloat(',0.0000',uipSaham.NAB or 0.0),\
           dictProsesHasilSaham[uipSaham.ProsesHasilSaham],\
           str(sTglPenetapan)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Koreksi NAB dan UP'],['sHeader',sHeader],['sData',sData],['inputer',uipSaham.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
