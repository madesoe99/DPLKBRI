import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

def SetRedemptReksadana(config, oRedemptReksadana):
  oReksadana = oRedemptReksadana.LReksadana

  oRedemptReksadana.isCommitted = 'T'
  #untuk redemption status sudah terotor ketika sudah di update NAB redemptnya.
  oRedemptReksadana.isCommitted = 'N'
  
  oRedemptReksadana.tgl_otorisasi = config.Now()
  oRedemptReksadana.user_id_auth = config.SecurityContext.userid
  oRedemptReksadana.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oRedemptReksadana.nama_investasi = oReksadana.nama_reksadana
  #oRedemptReksadana.profit = (oReksadana.NAB - oReksadana.NAB_awal) * oRedemptReksadana.unit_penyertaan
  
  oRedemptReksadana.NAB = 0.0
  
def CreatePendapatanReksadana(config, oRedemptReksadana):
# pendapatan (atau biaya) redempt reksadana sebagai selisih dari NAB
# pendapatan diperoleh secara tunai, maka tidak menggunakan transpiutanglrinv

  oReksadana = oRedemptReksadana.LReksadana

  oPendapatanReksadana = config.CreatePObject('PendapatanReksadana')
  oPendapatanReksadana.kode_jenis_trinvestasi = 'R' # pendapatan/biaya redempt reksadana
  oPendapatanReksadana.LReksadana = oReksadana
  oPendapatanReksadana.LTransactionBatch = oRedemptReksadana.LTransactionBatch
  oPendapatanReksadana.kode_jns_investasi = oRedemptReksadana.kode_jns_investasi
  moduleapi = modman.getModule(config, 'moduleapi')
  oPendapatanReksadana.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oRedemptReksadana.tgl_transaksi)
  oPendapatanReksadana.nominal = oRedemptReksadana.profit
  oPendapatanReksadana.no_rekening = oRedemptReksadana.no_rekening

  if oRedemptReksadana.profit >= 0.0:
    # pendapatan
    oPendapatanReksadana.kode_subjns_LRInvestasi = 'C-PROF' # pendapatan reksadana
    oPendapatanReksadana.mutasi_debet = 0.0
    oPendapatanReksadana.mutasi_kredit = oRedemptReksadana.profit
  else:
    oPendapatanReksadana.kode_subjns_LRInvestasi = 'C-COST' # biaya reksadana
    oPendapatanReksadana.mutasi_debet = -oRedemptReksadana.profit
    oPendapatanReksadana.mutasi_kredit = 0.0

  oPendapatanReksadana.isCommitted = 'T'
  oPendapatanReksadana.nama_investasi = oReksadana.nama_reksadana
  oPendapatanReksadana.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oRedemptReksadana.tgl_sistem)
  oPendapatanReksadana.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oRedemptReksadana.tgl_otorisasi)
  oPendapatanReksadana.user_id = oRedemptReksadana.user_id
  oPendapatanReksadana.user_id_auth = oRedemptReksadana.user_id_auth
  oPendapatanReksadana.terminal_id = oRedemptReksadana.terminal_id
  oPendapatanReksadana.terminal_id_auth = oRedemptReksadana.terminal_id_auth

  # update saldo laba rugi
  oReksadana.akum_LR += oRedemptReksadana.profit
  oReksadana.akum_piutangLR -= oRedemptReksadana.profit

  TransactInv = modman.getModule(config, 'TransactInv')
  TransactInv.CreateRincianBagiHasil(config, oReksadana, oRedemptReksadana.profit)
  
  return oPendapatanReksadana

# biaya redemption
def CreateBiayaRedemption(config, oRedemptionReksadana):
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.LInvestasi = oRedemptionReksadana.LReksadana
  oTransLRInvestasi.nama_investasi = oRedemptReksadana.LReksadana.nama_reksadana
  oTransLRInvestasi.LTransactionBatch = oRedemptionReksadana.LTransactionBatch
  oTransLRInvestasi.kode_jns_investasi = oRedemptionReksadana.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya reksadana
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'C-RDM' # biaya redemption reksadana
  moduleapi = modman.getModule(config, 'moduleapi')
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oRedemptionReksadana.tgl_transaksi)
  oTransLRInvestasi.mutasi_debet = oRedemptionReksadana.biaya_redempt
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oRedemptionReksadana.tgl_sistem)
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oRedemptionReksadana.tgl_otorisasi)
  oTransLRInvestasi.user_id = oRedemptionReksadana.user_id
  oTransLRInvestasi.user_id_auth = oRedemptionReksadana.user_id_auth
  oTransLRInvestasi.terminal_id = oRedemptionReksadana.terminal_id
  oTransLRInvestasi.terminal_id_auth = oRedemptionReksadana.terminal_id_auth
  #oTransLRInvestasi.no_bilyet = oRedemptionReksadana.LReksadana.no_bilyet

  oReksadana = oRedemptionReksadana.LReksadana
  oReksadana.akum_LR -= oRedemptionReksadana.biaya_redempt

def CloseInvestasi(config, oRedemptReksadana):
  oReksadana = oRedemptReksadana.LReksadana

  #oReksadana.status = 'F'
  #oReksadana.tgl_tutup = moduleapi.DateTimeTupleToFloat(config, oRedemptReksadana.tgl_transaksi)
  #oReksadana.akum_nominal = 0.0
  #oReksadana.akum_piutangLR = 0.0
  oReksadana.last_update = config.Now()

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id
  moduleapi = modman.getModule(config, 'moduleapi')
  TransactInv = modman.getModule(config, 'TransactInv')

  oRedemptReksadana = config.CreatePObjImplProxy('RedemptReksadana')
  oRedemptReksadana.Key = id
  
  config.BeginTransaction()
  try:
    oReksadana = oRedemptReksadana.LReksadana
    y,m,d = oRedemptReksadana.tgl_transaksi[:3]
    tgltrans = config.ModDateTime.EncodeDate(y,m,d)
    if TransactInv.CheckUpdateNAB(config, tgltrans, oReksadana) :
      raise Exception, 'PERINGATAN' +  'Transaksi NAB sudah dilakukan tgl ini'
    
    oHR = TransactInv.GetLastHistReksadana(config, oReksadana)
    if oHR.NAB_Transaksi == 0.0 and oHR.isCommitted == 'T' :
      raise Exception, 'PERINGATAN','Subscribe dan Redemption tidak boleh dilakukan bersamaan +  batalkan transaksi'
    oRR = TransactInv.GetLastRedemt(config, oReksadana)
    if not oRR.IsNull :
      if oRR.NAB == 0.0 and oRR.isCommitted == 'T' :
        raise Exception, 'PERINGATAN' + 'Redemption tidak boleh dua kali dalam satu transaksi dilakukan bersamaan'
     
    SetRedemptReksadana(config, oRedemptReksadana)

    if not moduleapi.IsApproxZero(oRedemptReksadana.nilai_redempt):
      pass#CreatePendapatanReksadana(config, oRedemptReksadana)

    if moduleapi.IsApproxZero(oReksadana.unit_penyertaan - oRedemptReksadana.unit_penyertaan):
      # tutup reksadana
      CloseInvestasi(config, oRedemptReksadana)
      # unit_penyertaan nol
      #oReksadana.unit_penyertaan = 0.0

    else:
      # akum nominal disesuaikan, dikurangi dengan nilai unit_penyertaan yang dilepas
      #oReksadana.akum_nominal -= oRedemptReksadana.unit_penyertaan * oReksadana.NAB_awal
      
      pass
      #oReksadana.akum_nominal -= oRedemptReksadana.nilai_redempt
      #TransactInv.CreateRincianPokok(config, oReksadana, -oRedemptReksadana.nilai_redempt)
      
      # unit_penyertaan dikurangi
      #if moduleapi.IsApproxZero(oRedemptReksadana.nilai_redempt) :
      
      #oReksadana.unit_penyertaan -= oRedemptReksadana.unit_penyertaan
      
      #else : 
      #  oRedemptReksadana.unit_penyertaan = 0.0
    
    #if oRedemptReksadana.biaya_redempt > 0.0:
    #  CreateBiayaRedemption(config, oRedemptReksadana)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

