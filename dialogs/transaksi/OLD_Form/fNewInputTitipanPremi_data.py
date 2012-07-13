import string, sys

def FormBeginSetData(uideflist, uipNasabah, key):
  config = uideflist.config

  keepGoingProcess = 1
  #checking status kepesertaan wasiat ummat
  try:
    #ambil no_peserta
    noPeserta = string.split(key,'=')[1]

    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = noPeserta

    if oR.status_wasiat_ummat == 'F':
      #peserta tidak ikut Wasiat Ummat
      keepGoingProcess = 0
      raise Exception, '\nPeringatan' + '\nPeserta tidak terdaftar sebagai peserta Wasiat Ummat.'
  except:
    raise

  return keepGoingProcess

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipTransaksi = uideflist.uipTransaksi
  uipNasabah = uideflist.uipNasabah

  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recNasabah = uipNasabah.Dataset.GetRecord(0)

  #set kolektibilitas dan kewajiban wasiat ummat
  recNasabah.KolektibilitasPremi = \
    recNasabah.GetFieldByName('LRekeningDPLK.collectivity_wasiat_ummat')
  recNasabah.KewajibanWasiatUmmat = \
    recNasabah.GetFieldByName('LRekeningDPLK.kewajiban_wasiat_ummat')

  #set field uipRekeningWU, pake SQL saja biar gampang
  sSQL = 'select no_polis,tgl_akseptasi,tgl_berakhir,besar_premi ' \
    'from RekeningWasiatUmmat where no_peserta = \'%s\'' % (recNasabah.no_peserta)
  rSQL = config.CreateSQL(sSQL).RawResult

  if not rSQL.Eof:
    #data peserta Wasiat Ummat pasti ditemukan (checking sudah di awal)
    uipRWU = uideflist.uipRekeningWU
    recRWU = uipRWU.Dataset.AddRecord()
    
    recRWU.no_polis = rSQL.no_polis
    recRWU.tgl_akseptasi = rSQL.tgl_akseptasi
    recRWU.tgl_berakhir = rSQL.tgl_berakhir
    recRWU.besar_premi = rSQL.besar_premi

    #set field panel Data Transaksi, samakan dengan besar premi
    #(+ kewajiban premi bila ada)
    recTransaksi.mutasi_premi = recRWU.besar_premi + recNasabah.KewajibanWasiatUmmat

  #setting parameter Default
  uipParameter = uideflist.uipParameter
  recParameter = uipParameter.Dataset.AddRecord()
  
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'
  
  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value

  return 0
  
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)
  recN = data.uipNasabah.GetRecord(0)
  
  try:
    o = config.CreatePObject('TitipanPremi')

    tgl_transaksi = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
    o.tgl_transaksi = config.ModDateTime.EncodeDate(tgl_transaksi[0], \
        tgl_transaksi[1], tgl_transaksi[2])

    o.no_peserta = recN.no_peserta
    o.keterangan = rec.keterangan
    o.mutasi_premi = rec.mutasi_premi
    o.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
    o.branch_code = rec.TB_BranchCode

    #assign nilai yang tidak tercantum di form
    o.isDebet = 'F'
    
    o.isCommitted = 'F'
    o.user_id = config.SecurityContext.UserID
    o.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    o.tgl_sistem = config.Now()
  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0
