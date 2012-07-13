def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi, clsfTransaksiInvestasi):
  if kode_jenis_trinvestasi == 'A':
    return ['fAlokInvTambahan','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'B':
    return ['fPendapatanInvestasiTunai','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'P':
    if clsfTransaksiInvestasi == 'C':
      return ['fPendapatanInvestasiPiutang','TransLRInvestasi','uipTransLRInvestasi']
    else:
      # piutang lr investasi
      return ['fPendapatanInvestasiPiutang_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'C':
    if clsfTransaksiInvestasi == 'A':
      return ['fTutupInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
    else:
      # piutang lr investasi
      return ['fTutupInvestasi_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'D':
    return ['fBiayaInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'F':
    if clsfTransaksiInvestasi == 'A':
      return ['fRolloverInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
    else:
      # piutang lr investasi
      return ['fRolloverInvestasi_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManPiutangLRInvestasi','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManLRInvestasi','TransLRInvestasi','uipTransLRInvestasi']
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
  aform.Show(app.CreateValues(['mode',mode]))

