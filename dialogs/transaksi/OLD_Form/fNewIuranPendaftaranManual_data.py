import string, sys

def FormBeginSetData(uideflist, uipNasabah, key):
  config = uideflist.config

  keepGoingProcess = 1
  #checking status iuran/biaya daftar nasabah
  try:
    #ambil no_peserta
    noPeserta = string.split(key,'=')[1]

    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = noPeserta
    
    if oR.status_biaya_daftar == 'T':
      #peserta sudah membayar biaya/iuran pendaftaran
      keepGoingProcess = 0
      raise '\nPeringatan','\nPeserta sudah membayar biaya/iuran pendaftaran.'
  except:
    raise
    
  return keepGoingProcess
  
def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipTransaksi = uideflist.uipTransaksi
  uipParameter = uideflist.uipParameter

  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recParameter = uipParameter.Dataset.AddRecord()

  #set nilai default iuran pendaftaran
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'BESAR_BIAYA_DAFTAR'
  
  #set field Data Transaksi
  recTransaksi.DefaultIuranPendaftaran = oParameter.Numeric_Value
  recTransaksi.besar_biaya_daftar = recTransaksi.DefaultIuranPendaftaran
  
  #set parameter default
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'
  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value

  return 0
  
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)
  recN = data.uipNasabah.GetRecord(0)
  
  try:
    o = config.CreatePObject('IuranPendaftaran')

    tgl_transaksi = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
    o.tgl_transaksi = config.ModDateTime.EncodeDate(tgl_transaksi[0], \
        tgl_transaksi[1], tgl_transaksi[2])

    o.no_peserta = recN.no_peserta
    o.keterangan = rec.keterangan
    o.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
    o.branch_code = rec.TB_BranchCode
    o.besar_biaya_daftar = rec.besar_biaya_daftar

    #assign nilai yang tidak tercantum di form
    o.isCommitted = 'F'
    o.user_id = config.SecurityContext.UserID
    o.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    o.tgl_sistem = config.Now()
    
  except:
    raise '\nProses Error', str(sys.exc_info()[1])
  
  return 0
