import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi,TransactInv

def uipTransLRSetData(uipTrans) :
  uideflist = uipTrans.UIDefList
  config = uideflist.Config

  uipParameter = uideflist.uipParameter

  rec_inv = uideflist.uipReksadana.Dataset.AddRecord()

  uipTrans = uipTrans.Dataset.GetRecord(0)
  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = uipTrans.id_investasi
  rec_inv.user_id = uipTrans.user_id
  rec_inv.terminal_id = uipTrans.terminal_id
  rec_inv.Tgl_penetapan = uipTrans.tgl_transaksi
  rec_inv.SetFieldByName('LIndukTransaksiInvestasi.id_transaksiinvestasi',uipTrans.id_transaksiinduk)
  rec_inv.SetFieldByName('LTransactionBatch.ID_TransactionBatch',uipTrans.id_transactionbatch)
  rec_inv.Biaya = uipTrans.mutasi_debet - uipTrans.mutasi_kredit
  rec_inv.Keterangan = uipTrans.Keterangan
  
  rec_inv.nama_reksadana = oReksadana.nama_reksadana
  rec_inv.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oReksadana.kode_pihak_ketiga)
  rec_inv.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oReksadana.LPihakKetiga.nama_pihak_ketiga)
  y,m,d = oReksadana.tgl_buka[:3]
  tgl = config.ModDateTime.EncodeDate(y,m,d)
  rec_inv.tgl_buka = tgl
  

def uipReksadanaSetData(uipReksadana):
  uideflist = uipReksadana.UIDefList
  config = uideflist.Config

  uipParameter = uideflist.uipParameter
  recP = uipParameter.Dataset.AddRecord()
  #set parameter nowDate
  tglPakai = config.ModDateTime.DecodeDate(config.Now())
  recP.nowDate = '%s/%s/%d' % (str(tglPakai[1]).zfill(2), \
    str(tglPakai[2]).zfill(2),tglPakai[0])
    
  rec_inv = uipReksadana.Dataset.GetRecord(0)

  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = rec_inv.id_investasi

  rec_inv.user_id = config.SecurityContext.UserID
  rec_inv.terminal_id = config.SecurityContext.InitIP
  rec_inv.Tgl_penetapan = config.Now()

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipReksadana')
  rec = uidef.ActiveRecord
  
  oReksa = config.CreatePObjImplProxy('Reksadana')
  oReksa.key = rec.id_investasi

  oTI = config.CreatePObject('TransLRInvestasi')
  oTI.id_investasi = rec.id_investasi
  oTI.terminal_id = config.SecurityContext.InitIP
  oTI.user_id = config.SecurityContext.UserID
  oTI.Tgl_transaksi = rec.Tgl_Penetapan
  oTI.keterangan = rec.Keterangan
  oTI.nama_investasi = oReksa.nama_reksadana
  oTI.kode_jenis_trinvestasi = 'Q'
  oTI.kode_jns_investasi = oReksa.kode_jns_investasi
  oTI.mutasi_debet = rec.Biaya
  oTI.mutasi_kredit = 0.0
  oTI.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
  oTI.id_transaksiinduk = rec.GetFieldByName('LIndukTransaksiInvestasi.id_transaksiinvestasi')
  oTI.isCommitted = 'F'
  if oTI.ID_TransactionBatch in (0, None) :
    raise 'PERINGATAN','Batch Transaksi belum dipilih'

  return 1
