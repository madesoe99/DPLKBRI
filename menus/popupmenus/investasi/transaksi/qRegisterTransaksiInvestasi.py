def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi):
  if kode_jenis_trinvestasi == 'A':
    return ['fAlokInvTambahan','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'B':
    return ['fPendapatanInvestasiTunai','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'P':
    return ['fPendapatanInvestasiPiutang','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'C':
    return ['fTutupInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'D':
    return ['fBiayaInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'F':
    return ['fRolloverInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManPiutangLRInvestasi','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManLRInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  else:
    raise 'PERINGATAN','Kode jenis transaksi investasi tidak dikenali / belum terdefinisi.'

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.GetForm('investasi/transaksi/'+formid,formid,0)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication

  formid, classname, uipart = GetFormInfoByJnsTransCode(context.GetFieldValue('TransaksiInvestasi.kode_jenis_trinvestasi'))[:3]
  key = 'PObj:%s#ID_TRANSAKSIINVESTASI=%d' % (classname, context.GetFieldValue('TransaksiInvestasi.ID'))
  mode = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(app.CreateValues(['mode',mode]))

  if mode == 'auth':
    if ea == 1:
      # otorisasi berhasil
      #app.ShowMessage('Otorisasi berhasil.')
      context.DeleteRow()
    elif ea <> 2:
      # penghapusan berhasil
      #app.ShowMessage('Penolakan register berhasil.')
      context.DeleteRow()

