def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi):
  if kode_jenis_trinvestasi == 'B':
    return ['fPendapatanInvestasiTunai','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'P':
    return ['fPendapatanInvestasiPiutang','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'D':
    return ['fBiayaInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManLRInvestasiRksdn','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManLRInvestasiObl','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManLRInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'R':
    return ['fPendapatanReksadana','PendapatanReksadana','uipPendapatanReksadana']
  elif kode_jenis_trinvestasi == 'L':
    return ['fBagiHasilReksadana','BagiHasilReksadana','uipBagiHasilReksadana']
  elif kode_jenis_trinvestasi == 'E':
    return ['fBagiHasilDeposito','BagiHasilDeposito','uipBagiHasilDeposito']
  elif kode_jenis_trinvestasi in ['J', 'K', 'O']:
    return ['fPendapatanObligasi','PendapatanObligasi','uipPendapatanObligasi']
  elif kode_jenis_trinvestasi == 'U':
    return ['fRealisasiReturn','RealisasiReturn','uipRealisasiReturn']
  else:
    raise Exception, 'PERINGATAN' + 'Kode jenis transaksi investasi tidak dikenali / belum terdefinisi.'

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication

  formid, classname, uipart = \
    GetFormInfoByJnsTransCode(context.GetFieldValue('TransLRInvestasi.kode_jenis_trinvestasi'))

  key = 'PObj:%s#ID_TRANSAKSIINVESTASI=%d' % (classname, context.GetFieldValue('TransLRInvestasi.ID'))
  mode = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(
    app.CreateValues(
      ['mode',mode]
      , ['caption',sender.Caption.replace('...','')]
    )
  )

