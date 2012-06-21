def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi):
  if kode_jenis_trinvestasi == 'A':
    return 'fAlokInvTambahan'
  elif kode_jenis_trinvestasi == 'B':
    return 'fPendapatanInvestasiTunai'
  elif kode_jenis_trinvestasi == 'P':
    return 'fPendapatanInvestasiPiutang'
  elif kode_jenis_trinvestasi == 'C':
    return 'fTutupInvestasi'
  elif kode_jenis_trinvestasi == 'D':
    return 'fBiayaInvestasi'
  elif kode_jenis_trinvestasi == 'F':
    return 'fRolloverInvestasi'
  elif kode_jenis_trinvestasi == 'G':
    return 'fManInvestasi'
  elif kode_jenis_trinvestasi == 'H':
    return 'fManPiutangLRInvestasi'
  elif kode_jenis_trinvestasi == 'I':
    return 'fManLRInvestasi'
  else:
    raise 'GetFormInfoByJnsTransCode Error','Kode jenis transaksi investasi tidak dikenali.'

def btnOKClick(sender):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  app = form.ClientApplication

  form.CommitBuffer()
  form.PostResult()

  formid = GetFormInfoByJnsTransCode(uipNoData.GetFieldValue('LJnsTransInvestasi.kode_jenis_trinvestasi'))
  key = 'PObj:Investasi#ID_INVESTASI=%d' % (uipNoData.GetFieldValue('LInvestasi.id_investasi'))

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,'uipInvestasi')
  ea = aform.Show(app.CreateValues(['mode','new']))

  if ea == 1:
    # eaQuitOK
    sender.ExitAction = 1
  else:
    # bersihkan form
    uipNoData.Edit()
    uipNoData.SetFieldValue('LJnsTransInvestasi.kode_jenis_trinvestasi',None)
    uipNoData.SetFieldValue('LJnsTransInvestasi.deskripsi',None)
    uipNoData.SetFieldValue('LInvestasi.id_investasi',None)
    uipNoData.SetFieldValue('LInvestasi.no_bilyet',None)
    form.GetControlByName('pData.LInvestasi').SetFocus()

