def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi):
  if kode_jenis_trinvestasi == 'A':
    return ['fAlokInvTambahan','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'C':
    return ['fTutupDeposito','TutupDeposito','uipTutupDeposito']
  elif kode_jenis_trinvestasi == 'F':
    return ['fRolloverInvestasi','RolloverDeposito','uipRolloverDeposito']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManInvestasiRksdn','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManInvestasiObl','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'O':
    return ['fBeliObligasi','BeliObligasi','uipBeliObligasi']
  elif kode_jenis_trinvestasi == 'J':
    return ['fJualObligasi','JualObligasi','uipJualObligasi']
  elif kode_jenis_trinvestasi == 'S':
    return ['fSubscribeReksadana','SubscribeReksadana','uipSubscribeReksadana']
  elif kode_jenis_trinvestasi == 'R':
    return ['fRedemptionReksadana','RedemptReksadana','uipRedemptionReksadana']
  elif kode_jenis_trinvestasi == 'L':
    return ['fBagiHasilReksadana_PiutInv','TransPiutangInvestasi','uipTransPiutangInvestasi']
  else:
    raise 'PERINGATAN','Kode jenis transaksi investasi tidak dikenali / belum terdefinisi.'

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication

  formid, classname, uipart = \
    GetFormInfoByJnsTransCode(context.GetFieldValue('TransPiutangInvestasi.kode_jenis_trinvestasi'))

  key = 'PObj:%s#ID_TRANSAKSIINVESTASI=%d' % (classname, context.GetFieldValue('TransPiutangInvestasi.ID'))
  mode = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(
    app.CreateValues(
      ['mode',mode]
      , ['caption', sender.Caption.replace('...','')]
    )
  )

