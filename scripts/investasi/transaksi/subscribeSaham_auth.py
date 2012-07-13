import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')
#transpiutanginv_auth = modman.getModule(config, 'transpiutanginv_auth')

# biaya subscribe
def CreateBiayaSubscribe(config, oSubscribeSaham):
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.LInvestasi = oSubscribeSaham.LSaham
  oTransLRInvestasi.LTransactionBatch = oSubscribeSaham.LTransactionBatch
  oTransLRInvestasi.kode_jns_investasi = oSubscribeSaham.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya Saham
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'C-SUB' # biaya subscribe Saham
  moduleapi = modman.getModule(config, 'moduleapi')
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oSubscribeSaham.tgl_transaksi)
  oTransLRInvestasi.mutasi_debet = oSubscribeSaham.subscription_fee
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oSubscribeSaham.tgl_sistem)
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oSubscribeSaham.tgl_otorisasi)
  oTransLRInvestasi.user_id = oSubscribeSaham.user_id
  oTransLRInvestasi.user_id_auth = oSubscribeSaham.user_id_auth
  oTransLRInvestasi.terminal_id = oSubscribeSaham.terminal_id
  oTransLRInvestasi.terminal_id_auth = oSubscribeSaham.terminal_id_auth
  oTransLRInvestasi.no_bilyet = oSubscribeSaham.LSaham.no_bilyet

  oSaham = oSubscribeSaham.LSaham
  oSaham.akum_LR -= oSubscribeSaham.subscription_fee

def updUnitPenyertaan(config, id):
  oSubscribeSaham = config.CreatePObjImplProxy('SubscribeSaham')
  oSubscribeSaham.Key = id
  #oSaham = oSubscribeSaham.LSaham
  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.Key = oSubscribeSaham.id_investasi
  oSubscribeSaham.nama_investasi = oSaham.nama_Saham

  totNABAwalSblm = oSaham.unit_penyertaan * oSaham.NAB_awal
  # update nilai unit penyertaan
  #oSaham.unit_penyertaan += oSubscribeSaham.unit_penyertaan

  #totNABAwalTmbhn = oSubscribeSaham.unit_penyertaan * oSaham.NAB
  # update nilai NAB awal
  #oSaham.NAB_awal = (totNABAwalSblm + totNABAwalTmbhn) / oSaham.unit_penyertaan
  y,m,d = oSubscribeSaham.tgl_transaksi[:3]
  tgltrans = config.ModDateTime.EncodeDate(y,m,d)
#   if TransactInv.CheckUpdateNAB(config, tgltrans, oSaham) :
#     raise Exception, 'PERINGATAN: Transaksi NAB sudah dilakukan tgl ini'

  TransactInv = modman.getModule(config, 'TransactInv')
  oRR = TransactInv.GetLastRedemtSaham(config, oSaham)
  if not oRR.IsNull :
    if oRR.NAB == 0.0 and oRR.isCommitted == 'T' :
      raise Exception, 'PERINGATAN: Subscribe dan Redemption tidak boleh dilakukan bersamaan, batalkan transaksi'
  
  oSubscribeSaham.NAB_Awal = 0.0
  oSubscribeSaham.NAB_Transaksi = oSubscribeSaham.NAB_Awal
  #oSubscribeSaham.Nominal_Pembukaan = oSubscribeSaham.nilai_subscribe
  oSubscribeSaham.tgl_otorisasi = config.Now()
  
  oSubscribeSaham.UP_Awal = oSaham.unit_penyertaan
      
  if oSubscribeSaham.nilai_subscribe == 0.0 :
    oSubscribeSaham.tgl_sistem = oSubsribeSaham.tgl_transaksi
    oSaham.unit_penyertaan += oSubscribeSaham.unit_penyertaan
  else :
    oSubscribeSaham.unit_penyertaan = 0.0
  
  TransactInv = modman.getModule(config, 'TransactInv')
  TransactInv.CreateRincianPokok(config, oSaham, oSubscribeSaham.nilai_subscribe)
  #if oSubscribeSaham.subscription_fee > 0.0:
  #  CreateBiayaSubscribe(config, oSubscribeSaham)
 

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id
  
  config.BeginTransaction()
  try:
    transpiutanginv_auth = modman.getModule(config, 'transpiutanginv_auth')
    oTransPiutangInvestasi = transpiutanginv_auth.otorTransPiutangInvestasi(config, id)
    updUnitPenyertaan(config, id)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

