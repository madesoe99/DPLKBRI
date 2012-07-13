def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi, clsfTransaksiInvestasi):
  if kode_jenis_trinvestasi == 'D':
    return ['fBiayaInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManLRInvestasiSaham','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManInvestasiSaham','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManPiutangLRInvestasiSaham','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'SS':
    return ['fSubscribeSaham','SubscribeSaham','uipSubscribeSaham']
  elif kode_jenis_trinvestasi == 'RS':
    if clsfTransaksiInvestasi == 'A':
      return ['fRedemptionSaham','RedemptSaham','uipRedemptionSaham']
    else:
      # lr investasi
      return ['fPendapatanSaham','PendapatanSaham','uipPendapatanSaham']
  elif kode_jenis_trinvestasi == 'BS':
    if clsfTransaksiInvestasi == 'C':
      return ['fBagiHasilSaham','BagiHasilSaham','uipBagiHasilSaham']
    else:
      # piutang investasi
      return ['fBagiHasilSaham_PiutInv','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'RRS':
    return ['fRealisasiReturnSaham', 'RealisasiReturnSaham', 'uipRealisasiReturnSaham']
  else:
    raise Exception, 'PERINGATAN' + 'Kode jenis transaksi investasi tidak dikenali / belum terdefinisi.'

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication

  formid, classname, uipart = \
    GetFormInfoByJnsTransCode(
      context.GetFieldValue('TransaksiInvestasi.kode_jenis_trinvestasi'),\
      context.GetFieldValue('TransaksiInvestasi.clsfTransaksiInvestasi')
    )[:3]
  key = 'PObj:%s#ID_TRANSAKSIINVESTASI=%d' % (classname, context.GetFieldValue('TransaksiInvestasi.ID'))
  mode = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(
    app.CreateValues(
      ['mode',mode]
      , ['caption',sender.Caption.replace('...','')]
    )
  )

