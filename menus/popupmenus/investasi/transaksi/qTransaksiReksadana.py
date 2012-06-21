def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi, clsfTransaksiInvestasi):
  if kode_jenis_trinvestasi == 'D':
    return ['fBiayaInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManLRInvestasiRksdn','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManInvestasiRksdn','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManPiutangLRInvestasiRksdn','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'S':
    return ['fSubscribeReksadana','SubscribeReksadana','uipSubscribeReksadana']
  elif kode_jenis_trinvestasi == 'R':
    if clsfTransaksiInvestasi == 'A':
      return ['fRedemptionReksadana','RedemptReksadana','uipRedemptionReksadana']
    else:
      # lr investasi
      return ['fPendapatanReksadana','PendapatanReksadana','uipPendapatanReksadana']
  elif kode_jenis_trinvestasi == 'L':
    if clsfTransaksiInvestasi == 'C':
      return ['fBagiHasilReksadana','BagiHasilReksadana','uipBagiHasilReksadana']
    else:
      # piutang investasi
      return ['fBagiHasilReksadana_PiutInv','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'U':
    return ['fRealisasiReturn', 'RealisasiReturn', 'uipRealisasiReturn']
  else:
    raise 'PERINGATAN','Kode jenis transaksi investasi tidak dikenali / belum terdefinisi.'

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

