import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi,TransactInv

def CreateRincianObligasi(config, oObligasi):
  # buat satu objek rincianobligasi
  # karena dalam kasus obligasi, satu obligasi hanya mengacu ke satu paket saja (B)

  oRincianObligasi = config.CreatePObject('RincianObligasi')
  oRincianObligasi.LObligasi = oObligasi
  oRincianObligasi.kode_paket_investasi = oObligasi.kode_paket_investasi
  oRincianObligasi.Akum_Paket = oRincianObligasi.nominal = oObligasi.nominal_pembukaan
  oRincianObligasi.Akum_LR_Paket = 0.0
  oRincianObligasi.proporsi = 1


def CreateObligasi(config, oRegisterObligasi):
  oObligasi = config.CreatePObject('Obligasi')
  oObligasi.nama_obligasi = oRegisterObligasi.nama_obligasi
  oObligasi.kode_pihak_ketiga = oRegisterObligasi.kode_pihak_ketiga
  oObligasi.kode_paket_investasi = oRegisterObligasi.kode_paket_investasi
  oObligasi.kode_jns_investasi = oRegisterObligasi.kode_jns_investasi
  oObligasi.tgl_buka = moduleapi.DateTimeTupleToFloat(config, oRegisterObligasi.tgl_buka)
  
  oObligasi.nominal_pembukaan = oRegisterObligasi.harga_beli * oRegisterObligasi.harga_pari / 100.0 #oRegisterObligasi.harga_pari
  oObligasi.akum_nominal = oRegisterObligasi.harga_pari
  oObligasi.akum_LR = 0.0
  
  # penampungan untuk kupon ijarah
  oObligasi.akum_piutangLR = oRegisterObligasi.biaya
  
  oObligasi.rollover_counter = 0
  oObligasi.status = 'T'

  if oRegisterObligasi.tgl_jatuh_tempo != None :
    oObligasi.tgl_jatuh_tempo = moduleapi.DateTimeTupleToFloat(config, oRegisterObligasi.tgl_jatuh_tempo)
  else :
    oObligasi.tgl_jatuh_tempo = int(config.Now())
  oObligasi.harga_beli = oRegisterObligasi.harga_beli
  oObligasi.harga_pari = oRegisterObligasi.harga_pari
  oObligasi.nilai_wajar = 100#oRegisterObligasi.nilai_wajar
  oObligasi.jenisKupon = oRegisterObligasi.jenisKupon
  oObligasi.jenisAkad = oRegisterObligasi.jenisAkad
  oObligasi.jenis_obligasi = oRegisterObligasi.jenis_obligasi
  oObligasi.LCustodianBank = oRegisterObligasi.LCustodianBank
  oObligasi.no_rekening = oRegisterObligasi.no_rekening
  oObligasi.TreatmentObligasi = oRegisterObligasi.TreatmentObligasi

  oObligasi.LAccrual = oRegisterObligasi.LAccrual
  oObligasi.LBroker = oRegisterObligasi.LBroker
  oObligasi.LPayingAgent = oRegisterObligasi.LPayingAgent
  oObligasi.LSubJenisInv = oRegisterObligasi.LSubJenisInv
  oObligasi.ER = oRegisterObligasi.ER
  oObligasi.harga_beli_acq = oRegisterObligasi.harga_beli_acq
  oObligasi.last_coupon_date = moduleapi.DateTimeTupleToFloat(config, oRegisterObligasi.last_coupon_date)
  oObligasi.AccruedInterest = oRegisterObligasi.AccruedInterest
  oObligasi.AccruedInterestOnTax = oRegisterObligasi.AccruedInterestOnTax
  oObligasi.TaxOnCapitalGain = oRegisterObligasi.TaxOnCapitalGain
  oObligasi.TaxOnAccruedInterest = oRegisterObligasi.TaxOnAccruedInterest

  oObligasi.tgl_otorisasi = config.Now()
  oObligasi.last_update = config.Now()
  oObligasi.user_id = oRegisterObligasi.user_id
  oObligasi.user_id_auth = config.SecurityContext.userid
  oObligasi.terminal_id = oRegisterObligasi.terminal_id
  oObligasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

  # create rincian Obligasi
  CreateRincianObligasi(config, oObligasi)
  
  return oObligasi

def CreateTransPiutangInvestasi(config, oObligasi, oRegisterObligasi):
  oBeliObligasi = config.CreatePObject('BeliObligasi')
  oBeliObligasi.LInvestasi = oObligasi
  oBeliObligasi.nama_investasi = oObligasi.nama_obligasi
  oBeliObligasi.kode_jns_investasi = 'O' # obligasi
  oBeliObligasi.kode_jenis_trinvestasi = 'O' # buat investasi baru, beli obligasi
  oBeliObligasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oObligasi.tgl_buka)
  oBeliObligasi.mutasi_debet = oObligasi.nominal_pembukaan#oObligasi.akum_nominal
  oBeliObligasi.mutasi_kredit = 0.0
  oBeliObligasi.isCommitted = 'T'

  oBeliObligasi.tgl_sistem = config.Now()
  oBeliObligasi.tgl_otorisasi = config.Now()
  oBeliObligasi.user_id = oObligasi.user_id
  oBeliObligasi.user_id_auth = oObligasi.user_id_auth
  oBeliObligasi.terminal_id = oObligasi.terminal_id
  oBeliObligasi.terminal_id_auth = oObligasi.terminal_id_auth

  return oBeliObligasi

def CreatePendapatanObligasi(config, oObligasi, oRegisterObligasi, profObl):
# pendapatan (atau biaya) beli obligasi sebagai selisih dari nominal_jual

  oPendapatanObligasi = config.CreatePObject('PendapatanObligasi')
  oPendapatanObligasi.kode_jenis_trinvestasi = 'O' # pendapatan/biaya obligasi
  oPendapatanObligasi.LInvestasi = oObligasi
  oPendapatanObligasi.nama_investasi = oObligasi.nama_obligasi
  oPendapatanObligasi.kode_jns_investasi = oRegisterObligasi.kode_jns_investasi
  oPendapatanObligasi.nominal = profObl
  #oPendapatanObligasi.no_rekening = oRegisterObligasi.no_rekening

  if profObl >= 0.0:
    # pendapatan
    oPendapatanObligasi.kode_subjns_LRInvestasi = 'B-PROF' # pendapatan obligasi capital gain
    oPendapatanObligasi.mutasi_debet = 0.0
    oPendapatanObligasi.mutasi_kredit = profObl
  else:
    # biaya
    oPendapatanObligasi.kode_subjns_LRInvestasi = 'B-COST' # biaya obligasi
    oPendapatanObligasi.mutasi_debet = -profObl
    oPendapatanObligasi.mutasi_kredit = 0.0

  oPendapatanObligasi.isCommitted = 'T'
  oPendapatanObligasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oObligasi.tgl_buka)
  oPendapatanObligasi.tgl_sistem = config.Now()
  oPendapatanObligasi.tgl_otorisasi = config.Now()
  oPendapatanObligasi.user_id = oObligasi.user_id
  oPendapatanObligasi.user_id_auth = oObligasi.user_id_auth
  oPendapatanObligasi.terminal_id = oObligasi.terminal_id
  oPendapatanObligasi.terminal_id_auth = oObligasi.terminal_id_auth
  oPendapatanObligasi.no_bilyet = oObligasi.no_bilyet

  oObligasi.akum_LR += profObl

  return oPendapatanObligasi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterObligasi = config.CreatePObjImplProxy('RegisterObligasi')
  oRegisterObligasi.Key = id

  config.BeginTransaction()
  try:
    oObligasi = CreateObligasi(config, oRegisterObligasi)
    oTransPiutang = CreateTransPiutangInvestasi(config, oObligasi, oRegisterObligasi)

    # pendapatan obligasi
    nominal = oRegisterObligasi.harga_beli * oRegisterObligasi.harga_pari / 100.0
    profObl = oRegisterObligasi.harga_pari - nominal
    if not moduleapi.IsApproxZero(profObl):
      #CreatePendapatanObligasi(config, oObligasi, oRegisterObligasi, profObl)
      TransactInv.CreateSPI(config, oObligasi.nama_obligasi, oObligasi, oTransPiutang, profObl,'O')
      TransactInv.CreatePNI(config, oObligasi.nama_obligasi, oObligasi, oTransPiutang, profObl,'O')
    #if oRegisterObligasi.biaya > 0.0:
    #  CreatePendapatanObligasi(config, oObligasi, oRegisterObligasi, -oRegisterObligasi.biaya)

    oRegisterObligasi.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

