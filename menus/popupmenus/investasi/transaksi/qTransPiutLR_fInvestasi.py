def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi):
  if kode_jenis_trinvestasi == 'P':
    return ['fPendapatanInvestasiPiutang_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'E':
    return ['fBagiHasilDeposito_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'C':
    return ['fTutupDeposito_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'J':
    return ['fJualObligasi_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManPiutangLRInvestasiObl','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManPiutangLRInvestasi','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManPiutangLRInvestasiRksdn','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'F':
    return ['fRolloverInvestasi_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManInvestasi','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  else:
    raise Exception, 'PERINGATAN' + 'Kode jenis transaksi investasi tidak dikenali / belum terdefinisi.'

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication

  formid, classname, uipart = \
    GetFormInfoByJnsTransCode(context.GetFieldValue('TransPiutangLRInvestasi.kode_jenis_trinvestasi'))

  key = 'PObj:%s#ID_TRANSAKSIINVESTASI=%d' % (classname, context.GetFieldValue('TransPiutangLRInvestasi.ID'))
  mode = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(
    app.CreateValues(
      ['mode',mode]
      , ['caption',sender.Caption.replace('...','')]
    )
  )

