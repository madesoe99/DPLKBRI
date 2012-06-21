import sys
sys.path.append('c:/dafapp/dplk/script_modules')
import moduleapi,TransactInv

def uipSahamSetData(uipSaham):
  uideflist = uipSaham.UIDefList
  config = uideflist.Config

  uipParameter = uideflist.uipParameter
  recP = uipParameter.Dataset.AddRecord()
  #set parameter nowDate
  tglPakai = config.ModDateTime.DecodeDate(config.Now())
  recP.nowDate = '%s/%s/%d' % (str(tglPakai[1]).zfill(2), \
    str(tglPakai[2]).zfill(2),tglPakai[0])
    
  rec_inv = uipSaham.Dataset.GetRecord(0)

  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.Key = rec_inv.id_investasi

  rec_inv.NAB_lama = oSaham.NAB
  rec_inv.user_id = config.SecurityContext.UserID
  rec_inv.terminal_id = config.SecurityContext.InitIP
  rec_inv.Tgl_penetapan = config.Now() - 1
  rec_inv.unit_penyertaanbaru = oSaham.unit_penyertaan
  rec_inv.jenis_perubahan = 1
  rec_inv.modeOto = 1
  rec_inv.ProsesHasilSaham = 1
  
  strSQL = 'Select * from HISTNABSaham \
            where id_investasi = %d and UserOto Is Null ' \
            % rec_inv.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  if rSQL.Eof :
     rec_inv.IsCommited = 1
  else :
     rec_inv.IsCommited = 0
     y,m,d = rSQL.Tgl_Penetapan[:3]
     tgl = config.ModDateTime.EncodeDate(y,m,d)
     rec_inv.Tgl_penetapan = tgl
     rec_inv.NAB = rSQL.NAB
     rec_inv.unit_penyertaanbaru = rSQL.unit_penyertaan
     rec_inv.ProsesHasilSaham = int(rSQL.TerminalOto)
     oBatch = config.CreatePObjImplProxy('TransactionBatch')
     oBatch.key = rSQL.ID_TransactionBatch
     rec_inv.SetFieldByName('LTransactionBatch.ID_TransactionBatch',oBatch.key)
     rec_inv.SetFieldByName('LTransactionBatch.no_batch',oBatch.no_batch)

  if moduleapi.IsInvestasiTutup(config, oSaham):
    raise '\nPERINGATAN','Investasi sudah ditutup.'

  oSR = TransactInv.GetLastHistSaham(config, oSaham)
  rec_inv.NomSubscribe = oSR.mutasi_debet
  rec_inv.NABSubs = oSR.NAB_Awal
  if oSR.IsCommitted != 'T' :
    raise '\nPERINGATAN','Subscribe Saham belum di otorisasi'

  oRR = TransactInv.GetLastRedemtSaham(config, oSaham)
  if not oRR.IsNull :
    rec_inv.NomRedempt = oRR.nilai_redempt
    rec_inv.NABRedempt = oRR.NAB
    rec_inv.UPRedempt = oRR.unit_penyertaan
    if oRR.IsCommitted not in ('N','T') :
      raise '\nPERINGATAN','Redemption Saham belum diotorisasi'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipSaham')
  rec = uidef.ActiveRecord
  
  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.key = rec.id_investasi
#   if TransactInv.CheckUpdateNAB(config, rec.Tgl_Penetapan, oSaham) :
#       raise 'PERINGATAN', 'Transaksi Update NAB sudah dilakukan hari ini'

  strSQL = 'Select * from RedemptSaham r, transaksiinvestasi t \
            where t.id_transaksiinvestasi=r.id_transaksiinvestasi \
            and biaya_redempt = 1.0 and no_rekening = \'%s\' order by r.id_transaksiinvestasi desc' \
            % rec.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  if not rSQL.Eof and rec.jenis_perubahan == 1 :
    y,m,d = rSQL.tgl_transaksi[:3]
    if int(rec.Tgl_Penetapan) >= config.ModDateTime.EncodeDate(y,m,d) and \
      not TransactInv.CheckUpdateNABSaham(config, rSQL.tgl_transaksi, oSaham) :
      raise 'PERINGATAN','ada transaksi switch tgl :%s-%s-%s, subscribe dahulu tgl tersebut' % (d,m,y)

  oHistNABSaham = config.CreatePObject('HistNABSaham')
  oHistNABSaham.id_investasi = rec.id_investasi
  oHistNABSaham.TerminalUbah = config.SecurityContext.InitIP
  oHistNABSaham.UserPengubah = config.SecurityContext.UserID
  oHistNABSaham.Tgl_Penetapan = rec.Tgl_Penetapan
  oHistNABSaham.NAB = rec.NAB
  oHistNABSaham.TerminalOto = str(rec.ProsesHasilSaham)
  oHistNABSaham.unit_penyertaan = rec.unit_penyertaanbaru
  oHistNABSaham.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
  if oHistNABSaham.ID_TransactionBatch in (0, None) :
    raise 'PERINGATAN','Batch Transaksi belum dipilih'

  if rec.jenis_perubahan != 1 and \
  not TransactInv.CheckUpdateUPSaham(config, rec.Tgl_Penetapan, oSaham, rec.jenis_perubahan) :
      raise 'PERINGATAN','Tanggal transaksi NAB dan update UP (TOP UP/ Redempt) tidak sama'
  oSaham.NAB = rec.NAB_lama

  return 1
