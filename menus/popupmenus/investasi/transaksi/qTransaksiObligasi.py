def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi, clsfTransaksiInvestasi):
  if kode_jenis_trinvestasi == 'D':
    return ['fBiayaInvestasi','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'I':
    return ['fManInvestasiObl','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'G':
    return ['fManPiutangLRInvestasiObl','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
  elif kode_jenis_trinvestasi == 'H':
    return ['fManLRInvestasiObl','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'O':
    if clsfTransaksiInvestasi == 'A':
      return ['fBeliObligasi','BeliObligasi','uipBeliObligasi']
    else:
      # piutang lr investasi
      return ['fPendapatanObligasi','PendapatanObligasi','uipPendapatanObligasi']
  elif kode_jenis_trinvestasi == 'J':
    if clsfTransaksiInvestasi == 'A':
      return ['fJualObligasi','JualObligasi','uipJualObligasi']
    else:
      # piutang lr investasi
      return ['fPendapatanObligasi','PendapatanObligasi','uipPendapatanObligasi']
  elif kode_jenis_trinvestasi == 'K':
    return ['fPendapatanObligasi','PendapatanObligasi','uipPendapatanObligasi']
  elif kode_jenis_trinvestasi == 'N':
    return ['fKoreksiNilaiSukuk','PendapatanObligasi','uipPendapatanObligasi']
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

