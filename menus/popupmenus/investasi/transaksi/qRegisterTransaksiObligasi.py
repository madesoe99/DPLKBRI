def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi):
  if kode_jenis_trinvestasi == 'A':
    return ['fAlokInvTambahan','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'K':
    return ['fPendapatanObligasi','PendapatanObligasi','uipPendapatanObligasi']
  elif kode_jenis_trinvestasi == 'N':
    return ['fKoreksiNilaiSukuk','PendapatanObligasi','uipPendapatanObligasi']
  elif kode_jenis_trinvestasi == 'P':
    return ['fPendapatanInvestasiPiutang','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'C':
    return ['fTutupInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'D':
    return ['fBiayaInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'F':
    return ['fRolloverInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManInvestasiObl','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManPiutangLRInvestasiObl','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManLRInvestasiObl','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'O':
    return ['fBeliObligasi','BeliObligasi','uipBeliObligasi']
  elif kode_jenis_trinvestasi == 'J':
    return ['fJualObligasi','JualObligasi','uipJualObligasi']
  #elif kode_jenis_trinvestasi == 'S':
  #  return ['fSubscribeReksadana','SubscribeReksadana','uipSubscribeReksadana']
  #elif kode_jenis_trinvestasi == 'R':
  #  return ['fRedemptionReksadana','RedemptReksadana','uipRedemptReksadana']
  else:
    raise Exception, 'PERINGATAN' + 'Kode jenis transaksi investasi tidak dikenali / belum terdefinisi.'

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
  ea = aform.Show(
    app.CreateValues(
      ['mode',mode]
      , ['caption',sender.Caption.replace('...','')]
    )
  )

  if mode == 'auth':
    if ea == 1:
      # otorisasi berhasil
      #app.ShowMessage('Otorisasi berhasil.')
      context.DeleteRow()
    elif ea <> 2:
      # penghapusan berhasil
      #app.ShowMessage('Penolakan register berhasil.')
      context.DeleteRow()

def mnuTransInvClick(sender, context):
  app = context.OwnerForm.ClientApplication

  formid = sender.StringTag
  aform = app.GetFormWithData('investasi/transaksi/'+formid, formid, 0, 'new', 'new')
  aform.Show(
    app.CreateValues(
      ['mode','new']
      , ['inv','B']
      , ['caption',sender.Caption.replace('...','')]
    )
  )

