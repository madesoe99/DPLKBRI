import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi,TransactInv

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

  rec_inv.NAB_lama = oReksadana.NAB
  rec_inv.user_id = config.SecurityContext.UserID
  rec_inv.terminal_id = config.SecurityContext.InitIP
  rec_inv.Tgl_penetapan = config.Now() - 1
  rec_inv.unit_penyertaanbaru = oReksadana.unit_penyertaan
  rec_inv.jenis_perubahan = 1
  rec_inv.modeOto = 1
  rec_inv.ProsesHasilReksadana = 1
  
  strSQL = 'Select * from HISTNABREKSADANA \
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
     rec_inv.ProsesHasilReksadana = int(rSQL.TerminalOto)

  if moduleapi.IsInvestasiTutup(config, oReksadana):
    raise Exception, '\nPERINGATAN' + 'Investasi sudah ditutup.'

  oSR = TransactInv.GetLastHistReksadana(config, oReksadana)
  rec_inv.NomSubscribe = oSR.mutasi_debet
  rec_inv.NABSubs = oSR.NAB_Awal
  if oSR.IsCommitted != 'T' :
    raise Exception, '\nPERINGATAN' + 'Subscribe Investasi EQ belum di otorisasi'

  oRR = TransactInv.GetLastRedemt(config, oReksadana)
  if not oRR.IsNull :
    rec_inv.NomRedempt = oRR.nilai_redempt
    rec_inv.NABRedempt = oRR.NAB
    rec_inv.UPRedempt = oRR.unit_penyertaan
    if oRR.IsCommitted not in ('N','T') :
      raise Exception, '\nPERINGATAN' + 'Redeem Investasi EQ belum diotorisasi'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipReksadana')
  rec = uidef.ActiveRecord
  
  oReksa = config.CreatePObjImplProxy('Reksadana')
  oReksa.key = rec.id_investasi
#   if TransactInv.CheckUpdateNAB(config, rec.Tgl_Penetapan, oReksa) :
#       raise Exception, 'PERINGATAN' +  'Transaksi Update NAB sudah dilakukan hari ini'

  strSQL = 'Select * from RedemptREKSADANA r, transaksiinvestasi t \
            where t.id_transaksiinvestasi=r.id_transaksiinvestasi \
            and biaya_redempt = 1.0 and no_rekening = \'%s\' order by r.id_transaksiinvestasi desc' \
            % rec.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  if not rSQL.Eof and rec.jenis_perubahan == 1 :
    y,m,d = rSQL.tgl_transaksi[:3]
    if int(rec.Tgl_Penetapan) >= config.ModDateTime.EncodeDate(y,m,d) and \
      not TransactInv.CheckUpdateNAB(config, rSQL.tgl_transaksi, oReksa) :
      raise Exception, 'PERINGATAN','ada transaksi switch tgl :%s-%s-%s, subscribe dahulu tgl tersebut' % (d,m + y)

  oHistNABReksadana = config.CreatePObject('HistNABReksadana')
  oHistNABReksadana.id_investasi = rec.id_investasi
  oHistNABReksadana.TerminalUbah = config.SecurityContext.InitIP
  oHistNABReksadana.UserPengubah = config.SecurityContext.UserID
  oHistNABReksadana.Tgl_Penetapan = rec.Tgl_Penetapan
  oHistNABReksadana.NAB = rec.NAB
  oHistNABReksadana.TerminalOto = str(rec.ProsesHasilReksadana)
  oHistNABReksadana.unit_penyertaan = rec.unit_penyertaanbaru

  if rec.jenis_perubahan != 1 and \
  not TransactInv.CheckUpdateUPReksa(config, rec.Tgl_Penetapan, oReksa, rec.jenis_perubahan) :
      raise Exception, 'PERINGATAN' + 'Tanggal transaksi NAB dan update UP (TOP UP/ Redeem) tidak sama'
  oReksa.NAB = rec.NAB_lama

  return 1
