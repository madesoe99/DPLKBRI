import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

def SetRedemptSaham(config, oRedemptSaham):
  oSaham = oRedemptSaham.LSaham

  oRedemptSaham.isCommitted = 'T'
  #untuk redemption status sudah terotor ketika sudah di update NAB redemptnya.
  oRedemptSaham.isCommitted = 'N'
  
  oRedemptSaham.tgl_otorisasi = config.Now()
  oRedemptSaham.user_id_auth = config.SecurityContext.userid
  oRedemptSaham.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oRedemptSaham.nama_investasi = oSaham.nama_Saham
  #oRedemptSaham.profit = (oSaham.NAB - oSaham.NAB_awal) * oRedemptSaham.unit_penyertaan
  
  oRedemptSaham.NAB = 0.0
  
def CreatePendapatanSaham(config, oRedemptSaham):
# pendapatan (atau biaya) redempt Saham sebagai selisih dari NAB
# pendapatan diperoleh secara tunai, maka tidak menggunakan transpiutanglrinv

  oSaham = oRedemptSaham.LSaham

  oPendapatanSaham = config.CreatePObject('PendapatanSaham')
  oPendapatanSaham.kode_jenis_trinvestasi = 'RS' # pendapatan/biaya redempt Saham
  oPendapatanSaham.LSaham = oSaham
  oPendapatanSaham.LTransactionBatch = oRedemptSaham.LTransactionBatch
  oPendapatanSaham.kode_jns_investasi = oRedemptSaham.kode_jns_investasi
  moduleapi = modman.getModule(config, 'moduleapi')
  oPendapatanSaham.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oRedemptSaham.tgl_transaksi)
  oPendapatanSaham.nominal = oRedemptSaham.profit
  oPendapatanSaham.no_rekening = oRedemptSaham.no_rekening

  if oRedemptSaham.profit >= 0.0:
    # pendapatan
    oPendapatanSaham.kode_subjns_LRInvestasi = 'C-PROF' # pendapatan Saham
    oPendapatanSaham.mutasi_debet = 0.0
    oPendapatanSaham.mutasi_kredit = oRedemptSaham.profit
  else:
    oPendapatanSaham.kode_subjns_LRInvestasi = 'C-COST' # biaya Saham
    oPendapatanSaham.mutasi_debet = -oRedemptSaham.profit
    oPendapatanSaham.mutasi_kredit = 0.0

  oPendapatanSaham.isCommitted = 'T'
  oPendapatanSaham.nama_investasi = oSaham.nama_Saham
  moduleapi = modman.getModule(config, 'moduleapi')
  oPendapatanSaham.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oRedemptSaham.tgl_sistem)
  oPendapatanSaham.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oRedemptSaham.tgl_otorisasi)
  oPendapatanSaham.user_id = oRedemptSaham.user_id
  oPendapatanSaham.user_id_auth = oRedemptSaham.user_id_auth
  oPendapatanSaham.terminal_id = oRedemptSaham.terminal_id
  oPendapatanSaham.terminal_id_auth = oRedemptSaham.terminal_id_auth

  # update saldo laba rugi
  oSaham.akum_LR += oRedemptSaham.profit
  oSaham.akum_piutangLR -= oRedemptSaham.profit

  TransactInv = modman.getModule(config, 'TransactInv')
  TransactInv.CreateRincianBagiHasil(config, oSaham, oRedemptSaham.profit)
  
  return oPendapatanSaham

# biaya redemption
def CreateBiayaRedemption(config, oRedemptionSaham):
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.LInvestasi = oRedemptionSaham.LSaham
  oTransLRInvestasi.nama_investasi = oRedemptSaham.LSaham.nama_Saham
  oTransLRInvestasi.LTransactionBatch = oRedemptionSaham.LTransactionBatch
  oTransLRInvestasi.kode_jns_investasi = oRedemptionSaham.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya Saham
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'C-RDM' # biaya redemption Saham
  moduleapi = modman.getModule(config, 'moduleapi')
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oRedemptionSaham.tgl_transaksi)
  oTransLRInvestasi.mutasi_debet = oRedemptionSaham.biaya_redempt
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oRedemptionSaham.tgl_sistem)
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oRedemptionSaham.tgl_otorisasi)
  oTransLRInvestasi.user_id = oRedemptionSaham.user_id
  oTransLRInvestasi.user_id_auth = oRedemptionSaham.user_id_auth
  oTransLRInvestasi.terminal_id = oRedemptionSaham.terminal_id
  oTransLRInvestasi.terminal_id_auth = oRedemptionSaham.terminal_id_auth
  #oTransLRInvestasi.no_bilyet = oRedemptionSaham.LSaham.no_bilyet

  oSaham = oRedemptionSaham.LSaham
  oSaham.akum_LR -= oRedemptionSaham.biaya_redempt

def CloseInvestasi(config, oRedemptSaham):
  oSaham = oRedemptSaham.LSaham

  #oSaham.status = 'F'
  #oSaham.tgl_tutup = moduleapi.DateTimeTupleToFloat(config, oRedemptSaham.tgl_transaksi)
  #oSaham.akum_nominal = 0.0
  #oSaham.akum_piutangLR = 0.0
  oSaham.last_update = config.Now()

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id
  TransactInv = modman.getModule(config, 'TransactInv')

  oRedemptSaham = config.CreatePObjImplProxy('RedemptSaham')
  oRedemptSaham.Key = id
  
  config.BeginTransaction()
  try:
    oSaham = oRedemptSaham.LSaham
    y,m,d = oRedemptSaham.tgl_transaksi[:3]
    tgltrans = config.ModDateTime.EncodeDate(y,m,d)
    if TransactInv.CheckUpdateNAB(config, tgltrans, oSaham) :
      raise Exception, 'PERINGATAN: Transaksi NAB sudah dilakukan tgl ini'
    
    oHR = TransactInv.GetLastHistSaham(config, oSaham)
    if oHR.NAB_Transaksi == 0.0 and oHR.isCommitted == 'T' :
      raise Exception, 'PERINGATAN: Subscribe dan Redemption tidak boleh dilakukan bersamaan, batalkan transaksi'
    oRR = TransactInv.GetLastRedemt(config, oSaham)
    if not oRR.IsNull :
      if oRR.NAB == 0.0 and oRR.isCommitted == 'T' :
        raise Exception, 'PERINGATAN: Redemption tidak boleh dua kali dalam satu transaksi dilakukan bersamaan'
     
    SetRedemptSaham(config, oRedemptSaham)

    moduleapi = modman.getModule(config, 'moduleapi')
    if not moduleapi.IsApproxZero(oRedemptSaham.nilai_redempt):
      pass#CreatePendapatanSaham(config, oRedemptSaham)

    if moduleapi.IsApproxZero(oSaham.unit_penyertaan - oRedemptSaham.unit_penyertaan):
      # tutup Saham
      CloseInvestasi(config, oRedemptSaham)
      # unit_penyertaan nol
      #oSaham.unit_penyertaan = 0.0

    else:
      # akum nominal disesuaikan, dikurangi dengan nilai unit_penyertaan yang dilepas
      #oSaham.akum_nominal -= oRedemptSaham.unit_penyertaan * oSaham.NAB_awal
      
      pass
      #oSaham.akum_nominal -= oRedemptSaham.nilai_redempt
      #TransactInv.CreateRincianPokok(config, oSaham, -oRedemptSaham.nilai_redempt)
      
      # unit_penyertaan dikurangi
      #if moduleapi.IsApproxZero(oRedemptSaham.nilai_redempt) :
      
      #oSaham.unit_penyertaan -= oRedemptSaham.unit_penyertaan
      
      #else : 
      #  oRedemptSaham.unit_penyertaan = 0.0
    
    #if oRedemptSaham.biaya_redempt > 0.0:
    #  CreateBiayaRedemption(config, oRedemptSaham)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1