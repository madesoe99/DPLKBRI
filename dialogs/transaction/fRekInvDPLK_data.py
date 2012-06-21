def setSaldoTotal(uideflist):
  uipRekInvDPLK = uideflist.uipRekInvDPLK
  rec = uipRekInvDPLK.Dataset.GetRecord(0)

  rec.saldo_total = \
    (rec.akum_iuran_pk or 0.0) \
    + (rec.akum_iuran_pst or 0.0) \
    + (rec.akum_pmb_pk or 0.0)

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  uipRekInvDPLK = uideflist.uipRekInvDPLK
  recRekInvDPLK = uipRekInvDPLK.Dataset.GetRecord(0)

  # hitung saldo total
  setSaldoTotal(uideflist)

  #cek apakah peserta Asuransi
  '''
  recRWU = uipRWU.Dataset.AddRecord()
  if recRekInvDPLK.GetFieldByName('status_asuransi') == 'T':
    #peserta Wasiat Ummat, set field uipRekeningWU, pake SQL biar gampang
    sSQL = 'select NO_POLIS,TGL_AKSEPTASI,TGL_BERAKHIR,BESAR_PREMI, MANFAAT_ASURANSI '\
      'from REKASURANSI where NO_PESERTA = \'%s\'' % (recRekInvDPLK.no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    if not rSQL.Eof:
      recRWU.no_polis = rSQL.no_polis
      if rSQL.tgl_akseptasi != None:
        recRWU.tgl_akseptasi = config.ModLibUtils.EncodeDate(rSQL.tgl_akseptasi[0],\
          rSQL.tgl_akseptasi[1],rSQL.tgl_akseptasi[2])
      if rSQL.tgl_berakhir != None:
        recRWU.tgl_berakhir = config.ModLibUtils.EncodeDate(rSQL.tgl_berakhir[0],\
          rSQL.tgl_berakhir[1],rSQL.tgl_berakhir[2])
      recRWU.besar_premi = rSQL.besar_premi
      recRWU.manfaat_asuransi = rSQL.manfaat_asuransi
  else:
    #bukan peserta
    recRWU.no_polis = 'Bukan peserta'
  '''
  
  '''
  #cek apakah peserta Auto Debet
  uipRAD = uideflist.uipRekeningAD
  recRAD = uipRAD.Dataset.AddRecord()
  if recRekInvDPLK.GetFieldByName('status_autodebet') == 'T':

    #peserta auto debet, set field uipRekeningAD, pake SQL biar gampang
    sSQL = 'select NO_REKENING,NAMA_REKENING,TANGGAL_AUTODEBET '\
      'from REKENINGAUTODEBET where NO_PESERTA = \'%s\'' % (recRekInvDPLK.no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult

    if not rSQL.Eof:
      recRAD.no_rekening = rSQL.no_rekening
      recRAD.nama_rekening = rSQL.nama_rekening
      recRAD.tanggal_autodebet = rSQL.tanggal_autodebet
  else:
    #bukan peserta
    recRAD.no_rekening = 'Tidak ikut Autodebet'
  '''
    
  '''
  #cek apakah sudah ikut anuitas
  uipRA = uideflist.uipRekeningA
  recRA = uipRA.Dataset.AddRecord()
  if recRekInvDPLK.GetFieldByName('status_anuitas') == 'T':

    #peserta auto debet, set field uipRekeningAD, pake SQL biar gampang
    sSQL = 'select NO_REKENING,NAMA_ASURANSI,NO_POLIS_ANUITAS,TGL_PEMBELIAN_ANUITAS '\
      'from REKENINGANUITAS where NO_PESERTA = \'%s\'' % (recRekInvDPLK.no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult

    if not rSQL.Eof:
      recRA.no_rekening = rSQL.no_rekening
      recRA.nama_asuransi = rSQL.nama_asuransi
      recRA.no_polis_anuitas = rSQL.no_polis_anuitas
      recRA.tgl_pembelian_anuitas = config.ModLibUtils.EncodeDate(rSQL.tgl_pembelian_anuitas[0],\
        rSQL.tgl_pembelian_anuitas[1],rSQL.tgl_pembelian_anuitas[2])
  else:
    #bukan peserta
    recRA.no_rekening = 'Bukan peserta'
  '''

  return 0
