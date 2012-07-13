isOnLoad = 0

def checkDateInterval(form, dateFrom, dateUntil):
  app = form.ClientApplication

  if dateFrom > dateUntil:
    form.ShowMessage('Kesalahan Interval Tanggal Jatuh Tempo:\nTanggal awal tidak boleh lebih dari tanggal akhir.')
    return 0
    
  dateUntilDT = app.ModDateTime.EncodeDate(
    dateUntil[0]
    , dateUntil[1]
    , dateUntil[2]
  )
  if dateUntilDT > app.ModDateTime.Now():
    form.ShowMessage('Kesalahan Interval Tanggal Jatuh Tempo:\nTanggal tidak boleh lebih dari hari ini.')
    return 0

  return 1


def btnLoadClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')
  uipRolloverDeposito = form.GetUIPartByName('uipRolloverDeposito')

  if not checkDateInterval(form, uipNoData.dateFrom, uipNoData.dateUntil):
    return

  if uipRolloverDeposito.RecordCount > 0:
    if not app.ConfirmDialog('Deposito yang sudah ada akan dihapus dari daftar yang akan di-rollover.\nLanjutkan?'):
      return

  global isOnLoad
  isOnLoad = 1
  try:
    uipRolloverDeposito.Edit()
    uipRolloverDeposito.ClearData()

    uipNoData.Edit()

    # set dateUntil_tmrw, next day of dateUntil
    dayUntilTmrwDT = 1 + app.ModDateTime.EncodeDate(
      uipNoData.dateUntil[0]
      , uipNoData.dateUntil[1]
      , uipNoData.dateUntil[2]
    )
    uipNoData.dateUntil_tmrw = dayUntilTmrwDT

    res = app.ExecuteScript(
      'investasi/transaksi/loaddeposito'
      , app.CreateValues(
          ['dateFrom', uipNoData.dateFrom]
          , ['dateUntil_tmrw', uipNoData.dateUntil_tmrw]
        )
    )
    packet = res.Packet
    dsDeposito = packet.GetDatasetByName('deposito')

    nowDateTime = app.ModDateTime.Now()
    for i in range(dsDeposito.RecordCount):
      rec = dsDeposito.GetRecord(i)
      uipRolloverDeposito.Append()
      uipRolloverDeposito.SetFieldValue('LDeposito.id_investasi', rec.id_investasi)
      uipRolloverDeposito.SetFieldValue('LDeposito.no_bilyet', rec.no_bilyet)
      uipRolloverDeposito.SetFieldValue('LDeposito.kode_paket_investasi', rec.kode_paket_investasi)
      uipRolloverDeposito.SetFieldValue('LDeposito.kode_pihak_ketiga', rec.kode_pihak_ketiga)
      uipRolloverDeposito.SetFieldValue('LDeposito.akum_nominal', rec.akum_nominal)
      uipRolloverDeposito.SetFieldValue('LDeposito.akum_piutangLR', rec.akum_piutangLR)
      uipRolloverDeposito.SetFieldValue('LDeposito.akum_LR', rec.akum_LR)
      uipRolloverDeposito.SetFieldValue('LDeposito.rollover_counter', rec.rollover_counter)
      uipRolloverDeposito.SetFieldValue('LDeposito.treatmentPokok', rec.treatmentPokok)
      uipRolloverDeposito.SetFieldValue('LDeposito.kapitalisir_rollover', rec.kapitalisir_rollover)
      uipRolloverDeposito.SetFieldValue('LDeposito.nisbah', rec.nisbah)
      uipRolloverDeposito.SetFieldValue('LDeposito.tgl_jatuh_tempo', rec.tgl_jatuh_tempo)
      #uipRolloverDeposito.ID_TransactionBatch = uipNoData.GetFieldValue('LTransactionBatch.ID_TransactionBatch')

      uipRolloverDeposito.tgl_transaksi = nowDateTime
      uipRolloverDeposito.tgl_sistem = nowDateTime
      if uipRolloverDeposito.GetFieldValue('LDeposito.kapitalisir_rollover') == 'T':
        uipRolloverDeposito.proses = 'K'
      else:
        uipRolloverDeposito.proses = 'R'

      uipRolloverDeposito.SetFieldValue('__SYSFLAG', 'N')
  finally:
    isOnLoad = 0

def uipRolloverDepositoNewRecord(uipRolloverDeposito):
  global isOnLoad
  if not isOnLoad:
    uipRolloverDeposito.Delete()

def uipRolloverDepositoBeforeDelete(uipRolloverDeposito):
  raise Exception, 'Operasi Dibatalkan' + 'Data tidak boleh dihapus dari daftar.'

def gDetailsDoubleClick(sender):
  form = sender.OwnerForm
  uipRolloverDeposito = form.GetUIPartByName('uipRolloverDeposito')
  uipRolloverDeposito.Edit()
  if uipRolloverDeposito.proses == 'K':
    if uipRolloverDeposito.GetFieldValue('LDeposito.kapitalisir_rollover') == 'T':
      uipRolloverDeposito.proses = 'N'
    else:
      uipRolloverDeposito.proses = 'R'
  elif uipRolloverDeposito.proses == 'R':
    uipRolloverDeposito.proses = 'N'
  else:
    uipRolloverDeposito.proses = 'K'

def setSysFlag(form):
  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.SetFieldValue('__SYSFLAG', 'N')

  uipRolloverDeposito = form.GetUIPartByName('uipRolloverDeposito')
  uipRolloverDeposito.First()
  while not uipRolloverDeposito.Eof:
    uipRolloverDeposito.Edit()
    uipRolloverDeposito.ID_TransactionBatch = uipNoData.GetFieldValue('LTransactionBatch.ID_TransactionBatch')
    if (uipRolloverDeposito.proses == 'N') or (not uipRolloverDeposito.proses):
      # tidak akan diproses
      uipRolloverDeposito.SetFieldValue('__SYSFLAG', 'L')

    uipRolloverDeposito.Next()

def checkTransactionBatch(form):
  uipNoData = form.GetUIPartByName('uipNoData')
  if not uipNoData.GetFieldValue('LTransactionBatch.ID_TransactionBatch'):
    form.ShowMessage('Transaction Batch belum dipilih.')
    return 0

  return 1

def btnProsesClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication

  if not checkTransactionBatch(form):
    return

  if not app.ConfirmDialog('Buat register transaksi rollover?'):
    return

  setSysFlag(form)

  form.CommitBuffer()
  form.PostResult()
  
  sender.ExitAction = 1

