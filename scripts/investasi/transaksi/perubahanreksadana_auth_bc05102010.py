import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

def CreateBatch(config,tgl) :
  oBatch = config.CreatePObject('TransactionBatch')
  oBatch.batch_type = 'I'
  oBatch.batch_sub_type = 'M'
  oBatch.tgl_create = tgl
  oBatch.account_link_type = 'S'
  oBatch.tgl_used = tgl
  oBatch.user_id_create = oBatch.user_id_owner = config.SecurityContext.userid
  oBatch.batch_status = 'O'
  oBatch.terminal_id_create = config.SecurityContext.GetSessionInfo()[1]
  oBatch.no_batch = 'B' + oBatch.batch_type + '.' + oBatch.user_id_owner + '.' + \
      str(oBatch.tgl_used[0]) + \
      str(oBatch.tgl_used[1]).zfill(2) + \
      str(oBatch.tgl_used[2]).zfill(2) + '.' + str(oBatch.ID_TransactionBatch)
  oUser = config.CreatePObjImplProxy('UserApp')
  oUser.Key = oBatch.user_id_owner
  oBatch.branch_code = oUser.branch_code

  return oBatch

def UbahNominalInvestasi(config, oBatch, oReksa, oHist,statNAB, Nom) :
  tgl = config.Now()
  if  oBatch == '' :
    oBatch = CreateBatch(config,tgl)

  #oTransPiutangInvestasi = config.CreatePObject('TransPiutangInvestasi')
  #oTransPiutangInvestasi.LInvestasi = oReksa
  #oTransPiutangInvestasi.LTransactionBatch = oBatch
  #oTransPiutangInvestasi.isCommitted = 'T'
  #oTransPiutangInvestasi.tgl_otorisasi = tgl
  #oTransPiutangInvestasi.user_id_auth = config.SecurityContext.userid
  #oTransPiutangInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  #oTransPiutangInvestasi.nama_investasi = oReksa.nama_reksadana
  #oTransPiutangInvestasi.kode_jns_investasi = oReksa.kode_jns_investasi
  #oTransPiutangInvestasi.kode_jenis_trinvestasi = 'N' # Perubahan NAB
  #oTransPiutangInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oHist.TglUbah)

  #if  statNAB : #NAB membesar alias positif
  #  oTransPiutangInvestasi.mutasi_debet = Nom
  #  oTransPiutangInvestasi.mutasi_kredit = 0.0
  #else :
  #  oTransPiutangInvestasi.mutasi_debet = 0.0
  #  oTransPiutangInvestasi.mutasi_kredit = -Nom

  #oTransPiutangInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oHist.TglUbah)
  #oTransPiutangInvestasi.user_id = oHist.UserPengubah
  #oTransPiutangInvestasi.terminal_id = oHist.TerminalUbah

  akum_awal = oReksa.akum_nominal
  oReksa.akum_nominal = oReksa.NAB * oReksa.unit_penyertaan
  prof = oReksa.akum_nominal-akum_awal

  moduleapi = modman.getModule(config, 'moduleapi')
  TransactInv = modman.getModule(config, 'TransactInv')
  oSPI = TransactInv.CreateSPI(config, oReksa.nama_reksadana, oReksa, '', prof,'N',oBatch,moduleapi.DateTimeTupleToFloat(config, oHist.tgl_penetapan))
  TransactInv.CreatePNI(config, oReksa.nama_reksadana, oReksa, oSPI, prof,'N')

  TransactInv.CreateRincianPokok(config, oReksa, oReksa.akum_nominal-akum_awal)
  
def OtorisasiPerubahanReksadana(config, oReksa, oHist, IsSubs, oBatch):
  TransactInv = modman.getModule(config, 'TransactInv')  
  oHR = TransactInv.GetLastHistReksadana(config, oReksa)
  oHist.TglUbah = config.Now()    
  tglAkhir = oHist.tgl_penetapan
  ye,me,de = tglAkhir[:3]
  ftglAkhir = config.ModDateTime.EncodeDate(ye,me,de)
  
  statNAB = oReksa.NAB < oHist.NAB
  oReksaNAB = oReksa.NAB
  oReksa.NAB = oHist.NAB  
  

  if IsSubs:
    UP = oReksa.unit_penyertaan - oHR.unit_penyertaan
  else :
    UP = oReksa.unit_penyertaan
  
  Nom = (oHist.NAB - oReksaNAB)*UP
  
  if Nom != 0.0 :
    #oReksa.akum_piutangLR += Nom
    UbahNominalInvestasi(config, oBatch, oReksa, oHist,statNAB, Nom)

  if int(oHist.TerminalOto) : #Proses Unrealize Hasil Reksadana
    #oBatch = CreateBatch(config,ftglAkhir)
    UnrealReturn(config, oReksa, oHist, oBatch)

  oHist.UserOto = config.SecurityContext.UserID
  #oHist.tgl_penetapan = config.Now()
  oHist.TerminalOto = config.SecurityContext.InitIP
  
def BatalkanPerubahanReksadana(config, oReksa, oHist) :
  oHist.Delete()

def UnrealReturn(config, oReksa, oHist, oBatch):
  #kenaikan /penurunan investasi
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransLRInvestasi = config.CreatePObject('KlaimLRReksadana')
  oTransLRInvestasi.LInvestasi = oReksa
  oTransLRInvestasi.nama_investasi = oReksa.nama_reksadana
  oTransLRInvestasi.LTransactionBatch = oBatch
  oTransLRInvestasi.kode_jns_investasi = oReksa.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'L' # fLoat return
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oHist.tgl_penetapan)
  
  unrealReturn = oReksa.akum_PNI
  
  if unrealReturn > 0.0 :
    oTransLRInvestasi.mutasi_debet = 0.0
    oTransLRInvestasi.mutasi_kredit = unrealReturn
  else :
    oTransLRInvestasi.mutasi_debet = -unrealReturn
    oTransLRInvestasi.mutasi_kredit = 0.0
  
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oHist.TglUbah)
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oHist.tgl_penetapan)
  oTransLRInvestasi.user_id = oHist.UserPengubah
  oTransLRInvestasi.user_id_auth = config.SecurityContext.userid
  oTransLRInvestasi.terminal_id = oHist.TerminalUbah
  oTransLRInvestasi.terminal_id_auth = config.SecurityContext.InitIP
  
  TransactInv = modman.getModule(config, 'TransactInv')
  TransactInv.CreateRincianBagiHasil(config, oReksa, unrealReturn)
  oReksa.akum_LR += unrealReturn
  TransactInv.CreatePNI(config, oReksa.nama_reksadana, oReksa, oTransLRInvestasi, -unrealReturn,'L')

def RealReturn (config, oReksa, oRR, oBatch ):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransLRInvestasi = config.CreatePObject('RealisasiReturn')
  
  oTransLRInvestasi.LInvestasi = oReksa
  oTransLRInvestasi.nama_investasi = oReksa.nama_reksadana
  oTransLRInvestasi.LTransactionBatch = oBatch
  oTransLRInvestasi.kode_jns_investasi = oReksa.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'U' # realisasi return
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oRR.tgl_transaksi)
  
  RealReturn = oRR.profit 
  
  if RealReturn > 0.0 :
    oTransLRInvestasi.mutasi_debet = 0.0
    oTransLRInvestasi.mutasi_kredit = RealReturn
  else :
    oTransLRInvestasi.mutasi_debet = -RealReturn
    oTransLRInvestasi.mutasi_kredit = 0.0
  
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oRR.tgl_sistem)
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oRR.tgl_otorisasi)
  oTransLRInvestasi.user_id = oRR.user_id
  oTransLRInvestasi.user_id_auth = config.SecurityContext.userid
  oTransLRInvestasi.terminal_id = oRR.terminal_id
  oTransLRInvestasi.terminal_id_auth = config.SecurityContext.InitIP
  oTransLRInvestasi.LIndukTransaksiInvestasi = oRR
  
  #TransactInv.CreatePNI(config, oReksa.nama_reksadana, oReksa, oTransLRInvestasi, -RealReturn,'U')
  TransactInv = modman.getModule(config, 'TransactInv')
  TransactInv.CreateRincianBagiHasil(config, oReksa, RealReturn)
  oReksa.akum_LR += RealReturn
  oReksa.nominal_pembukaan -= (oRR.unit_penyertaan * oReksa.NAB_Transaksi)
            
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  recReksa = parameter.uipReksadana.GetRecord(0)
  modeOto = recReksa.ModeOto
  TransactInv = modman.getModule(config, 'TransactInv')
  
  strSQL = 'Select * from HistNABReksadana \
            where id_investasi = %d and UserOto Is Null ' \
            % recReksa.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  if rSQL.Eof :
    raise Exception, '\PERINGATAN: Perubahan belum dilakukan'
  Id_hist = rSQL.HistNABReksadanaID
    
  config.BeginTransaction()
  try :
    oHist = config.CreatePObjImplProxy('HistNABReksadana')
    oHist.Key = Id_hist
    oReksa = config.CreatePObjImplProxy('Reksadana')
    oReksa.Key = recReksa.id_Investasi
    
    if oReksa.IsNull:
      raise Exception, 'PERINGATAN: Investasi tidak ditemukan'
    
    if modeOto: 
        oBatch = config.CreatePObjImplProxy('TransactionBatch')
        oBatch.key = oHist.ID_TransactionBatch
        if recReksa.jenis_perubahan == 0 : #topup
          oSR = TransactInv.GetLastHistReksadana(config, oReksa)
          oSR.NAB_Transaksi = recReksa.NAB
          oSR.Unit_Penyertaan = recReksa.unit_penyertaanbaru
          oSR.NAB_Awal = recReksa.NAB
          oSR.Tgl_sistem = recReksa.Tgl_Penetapan

          oSR.subscription_fee = oSR.NAB_Transaksi*oSR.Unit_Penyertaan
          
          oReksa.unit_penyertaan += recReksa.unit_penyertaanbaru
          
          if oReksa.akum_nominal != oReksa.nominal_pembukaan :
            oReksa.nominal_pembukaan += oSR.subscription_fee
            
          oReksa.NAB_Transaksi = round(oReksa.nominal_pembukaan / oReksa.unit_penyertaan,6)
        #--
        
        if recReksa.jenis_perubahan == 2 :#redemption
          oRR = TransactInv.GetLastRedemt(config, oReksa)
          oRR.NAB = recReksa.NAB
          up = recReksa.unit_penyertaanbaru
          totRedempt = oRR.NAB*up
          costRedempt = oReksa.NAB_Transaksi * up
          oReksa.Unit_Penyertaan -= recReksa.unit_penyertaanbaru
          oRR.nominal_jual = totRedempt
          oRR.profit = totRedempt - costRedempt
          oRR.mutasi_kredit = costRedempt 

          #cek status commit redemption
          if oRR.isCommitted != 'N':
            raise Exception, 'PERINGATAN: Redemption belum diotorisasi'
          oRR.isCommitted = 'T'
          
          moduleapi = modman.getModule(config, 'moduleapi')
          if moduleapi.IsApproxZero(oReksa.Unit_Penyertaan):
            oReksa.status = 'F'
            
          oRR.unit_penyertaan = up
          oReksa.akum_nominal -= costRedempt
          TransactInv.CreateRincianPokok(config, oReksa, -costRedempt)
            
          #Realize return
          RealReturn (config, oReksa, oRR, oBatch)
        #--
        
        OtorisasiPerubahanReksadana(config, oReksa, oHist, not recReksa.jenis_perubahan, oBatch)
    else :
        BatalkanPerubahanReksadana(config, oReksa, oHist)
    
    config.Commit()
  except :
    config.Rollback()
    raise

  return 1