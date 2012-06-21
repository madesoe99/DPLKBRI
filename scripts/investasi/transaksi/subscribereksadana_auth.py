import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi,TransactInv
import transpiutanginv_auth

# biaya subscribe
def CreateBiayaSubscribe(config, oSubscribeReksadana):
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.LInvestasi = oSubscribeReksadana.LReksadana
  oTransLRInvestasi.LTransactionBatch = oSubscribeReksadana.LTransactionBatch
  oTransLRInvestasi.kode_jns_investasi = oSubscribeReksadana.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya reksadana
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'C-SUB' # biaya subscribe reksadana
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oSubscribeReksadana.tgl_transaksi)
  oTransLRInvestasi.mutasi_debet = oSubscribeReksadana.subscription_fee
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oSubscribeReksadana.tgl_sistem)
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oSubscribeReksadana.tgl_otorisasi)
  oTransLRInvestasi.user_id = oSubscribeReksadana.user_id
  oTransLRInvestasi.user_id_auth = oSubscribeReksadana.user_id_auth
  oTransLRInvestasi.terminal_id = oSubscribeReksadana.terminal_id
  oTransLRInvestasi.terminal_id_auth = oSubscribeReksadana.terminal_id_auth
  oTransLRInvestasi.no_bilyet = oSubscribeReksadana.LReksadana.no_bilyet

  oReksadana = oSubscribeReksadana.LReksadana
  oReksadana.akum_LR -= oSubscribeReksadana.subscription_fee

def updUnitPenyertaan(config, id):
  oSubscribeReksadana = config.CreatePObjImplProxy('SubscribeReksadana')
  oSubscribeReksadana.Key = id
  #oReksadana = oSubscribeReksadana.LReksadana
  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = oSubscribeReksadana.id_investasi
  oSubscribeReksadana.nama_investasi = oReksadana.nama_reksadana

  totNABAwalSblm = oReksadana.unit_penyertaan * oReksadana.NAB_awal
  # update nilai unit penyertaan
  #oReksadana.unit_penyertaan += oSubscribeReksadana.unit_penyertaan

  #totNABAwalTmbhn = oSubscribeReksadana.unit_penyertaan * oReksadana.NAB
  # update nilai NAB awal
  #oReksadana.NAB_awal = (totNABAwalSblm + totNABAwalTmbhn) / oReksadana.unit_penyertaan
  y,m,d = oSubscribeReksadana.tgl_transaksi[:3]
  tgltrans = config.ModDateTime.EncodeDate(y,m,d)
#   if TransactInv.CheckUpdateNAB(config, tgltrans, oReksadana) :
#     raise 'PERINGATAN', 'Transaksi NAB sudah dilakukan tgl ini'
    
  oRR = TransactInv.GetLastRedemt(config, oReksadana)
  if not oRR.IsNull :
    if oRR.NAB == 0.0 and oRR.isCommitted == 'T' :
      raise 'PERINGATAN','Subscribe dan Redemption tidak boleh dilakukan bersamaan, batalkan transaksi'
  
  oSubscribeReksadana.NAB_Awal = 0.0
  oSubscribeReksadana.NAB_Transaksi = oSubscribeReksadana.NAB_Awal
  #oSubscribeReksadana.Nominal_Pembukaan = oSubscribeReksadana.nilai_subscribe
  oSubscribeReksadana.tgl_otorisasi = config.Now()
  
  oSubscribeReksadana.UP_Awal = oReksadana.unit_penyertaan
      
  if oSubscribeReksadana.nilai_subscribe == 0.0 :
    oSubscribeReksadana.tgl_sistem = oSubsribeReksadana.tgl_transaksi
    oReksadana.unit_penyertaan += oSubscribeReksadana.unit_penyertaan
  else :
    oSubscribeReksadana.unit_penyertaan = 0.0
  
  TransactInv.CreateRincianPokok(config, oReksadana, oSubscribeReksadana.nilai_subscribe)
  #if oSubscribeReksadana.subscription_fee > 0.0:
  #  CreateBiayaSubscribe(config, oSubscribeReksadana)
 

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id
  
  config.BeginTransaction()
  try:
    oTransPiutangInvestasi = transpiutanginv_auth.otorTransPiutangInvestasi(config, id)
    updUnitPenyertaan(config, id)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

