import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

def UbahNominalInvestasi(config, oSaham, oHist,statNAB, Nom):
  moduleapi = modman.getModule(config, 'moduleapi')   
  TransactInv = modman.getModule(config, 'TransactInv')
  
  tgl = config.Now()
  #if  oBatch == '' :
  #  oBatch = CreateBatch(config,tgl)

  #oTransPiutangInvestasi = config.CreatePObject('TransPiutangInvestasi')
  #oTransPiutangInvestasi.LInvestasi = oSaham
  #oTransPiutangInvestasi.LTransactionBatch = oBatch
  #oTransPiutangInvestasi.isCommitted = 'T'
  #oTransPiutangInvestasi.tgl_otorisasi = tgl
  #oTransPiutangInvestasi.user_id_auth = config.SecurityContext.userid
  #oTransPiutangInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  #oTransPiutangInvestasi.nama_investasi = oSaham.nama_Saham
  #oTransPiutangInvestasi.kode_jns_investasi = oSaham.kode_jns_investasi
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

  akum_awal = oSaham.akum_nominal
  oSaham.akum_nominal = oSaham.NAB * oSaham.unit_penyertaan
  prof = oSaham.akum_nominal-akum_awal

  TransactInv = modman.getModule(config, 'TransactInv')
  oSPI = TransactInv.CreateSPINoBatch(config, oSaham.nama_Saham, oSaham, '', prof,'N',moduleapi.DateTimeTupleToFloat(config, oHist.tgl_penetapan))
  TransactInv.CreatePNINoBatch(config, oSaham.nama_Saham, oSaham, oSPI, prof,'N')
  TransactInv.CreateRincianPokok(config, oSaham, oSaham.akum_nominal-akum_awal)  
  
  #UpdatePosisiReturn(config, prof, oHist.tgl_penetapan)
  #UpdatePosisiReturnPeserta(config, prof)
   
def UpdatePosisiReturn(config, nom_return, tgl):
  strtgl = '%s/%s/%s' % (tgl[0],tgl[1],tgl[2])
  sSQL = "SELECT * FROM PosisiReturn\
  WHERE tanggal = '%s'\
  and kode_jns_investasi = 'S'" % (strtgl)
  rSQL = config.CreateSQL(sSQL).RawResult
  if not rSQL.Eof:
    sExc = "UPDATE PosisiReturn \
    SET nom_return = nom_return + %s\
    WHERE tanggal = '%s'\
    and kode_jns_investasi = 'S'" % (nom_return, strtgl)
  else:
    sExc = "INSERT INTO PosisiReturn VALUES \
    ('%s','S',%s)" % (strtgl, nom_return)
    
  config.SendDebugMsg(sExc)
  config.ExecSQL(sExc)
  
def UpdatePosisiReturnPeserta(config, nom_return):
  sExc = "update posisirek \
          set return_saham = return_saham + \
        	(%s  * (saldo_pod / (select sum(saldo_pod) from posisirek \
          where kode_paket_investasi = 'C'))) \
          where kode_paket_investasi = 'C' \
        " % (nom_return)
    
  config.SendDebugMsg(sExc)
  config.ExecSQL(sExc)
    
def OtorisasiPerubahanSaham(config, oSaham, oHist, IsSubs):
  TransactInv = modman.getModule(config, 'TransactInv')
  oHR = TransactInv.GetLastHistSaham(config, oSaham)
  oHist.TglUbah = config.Now()    
  tglAkhir = oHist.tgl_penetapan
  ye,me,de = tglAkhir[:3]
  ftglAkhir = config.ModDateTime.EncodeDate(ye,me,de)
  
  statNAB = oSaham.NAB < oHist.NAB
  oSahamNAB = oSaham.NAB
  oSaham.NAB = oHist.NAB  
  

  if IsSubs :
    UP = oSaham.unit_penyertaan - oHR.unit_penyertaan
  else :
    UP = oSaham.unit_penyertaan
  
  Nom =  (oHist.NAB - oSahamNAB)*UP
  
  if Nom != 0.0 :
    #oSaham.akum_piutangLR += Nom
    UbahNominalInvestasi(config, oSaham, oHist,statNAB, Nom)

  if int(oHist.TerminalOto) : #Proses Unrealize Hasil Saham
    #oBatch = CreateBatch(config,ftglAkhir)
    UnrealReturn(config, oSaham, oHist)

  oHist.UserOto = config.SecurityContext.UserID
  #oHist.tgl_penetapan = config.Now()
  oHist.TerminalOto = config.SecurityContext.InitIP
  
def BatalkanPerubahanSaham(config, oSaham, oHist) :
  oHist.Delete()

def UnrealReturn(config, oSaham, oHist) :
  #kenaikan /penurunan investasi
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransLRInvestasi = config.CreatePObject('KlaimLRSaham')
  oTransLRInvestasi.LInvestasi = oSaham
  oTransLRInvestasi.nama_investasi = oSaham.nama_Saham
  oTransLRInvestasi.kode_jns_investasi = oSaham.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'L' # fLoat return
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oHist.tgl_penetapan)
  
  unrealReturn = oSaham.akum_PNI
  
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
  TransactInv.CreateRincianBagiHasil(config, oSaham, unrealReturn)
  oSaham.akum_LR += unrealReturn
  TransactInv.CreatePNI(config, oSaham.nama_Saham, oSaham, oTransLRInvestasi, -unrealReturn,'L')

def RealReturn (config, oSaham, oRR, oHist ):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransLRInvestasi = config.CreatePObject('RealisasiReturnSaham')
  config.SendDebugMsg('RR1')
  oTransLRInvestasi.LInvestasi = oSaham
  oTransLRInvestasi.nama_investasi = oSaham.nama_Saham
  oTransLRInvestasi.kode_jns_investasi = oSaham.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'RRS' # realisasi return
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oRR.tgl_transaksi)
  config.SendDebugMsg('RR2')
  
  RealReturn = oRR.profit 
  
  if RealReturn > 0.0 :
    oTransLRInvestasi.mutasi_debet = 0.0
    oTransLRInvestasi.mutasi_kredit = RealReturn
  else :
    oTransLRInvestasi.mutasi_debet = -RealReturn
    oTransLRInvestasi.mutasi_kredit = 0.0
  
  oTransLRInvestasi.isCommitted = 'T'
  config.SendDebugMsg('RR3')
  tgl = moduleapi.DateTimeTupleToFloat(config, oRR.tgl_sistem)
  oTransLRInvestasi.tgl_sistem = tgl
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oRR.tgl_otorisasi)
  oTransLRInvestasi.user_id = oRR.user_id
  oTransLRInvestasi.user_id_auth = config.SecurityContext.userid
  oTransLRInvestasi.terminal_id = oRR.terminal_id
  oTransLRInvestasi.terminal_id_auth = config.SecurityContext.InitIP
  oTransLRInvestasi.LIndukTransaksiInvestasi = oRR
  config.SendDebugMsg('RR4')
  
  TransactInv = modman.getModule(config, 'TransactInv')
  #TransactInv.CreatePNI(config, oSaham.nama_Saham, oSaham, oTransLRInvestasi, -RealReturn,'U')
  TransactInv.CreateRincianBagiHasil(config, oSaham, RealReturn)
  oSaham.akum_LR += RealReturn
  oSaham.nominal_pembukaan -= (oRR.unit_penyertaan * oSaham.NAB_Transaksi)
  
  #config.SendDebugMsg('RR5')
  #tambahan SPI
  TransactInv.CreateSPINoBatch(config, oSaham.nama_Saham, oSaham, oTransLRInvestasi, -RealReturn ,'N',  tgl)
  #config.SendDebugMsg('RR6')
  TransactInv.CreatePNINoBatch(config, oSaham.nama_Saham, oSaham, oTransLRInvestasi, -RealReturn,'N', tgl)
  #config.SendDebugMsg('RR7')
  UnrealReturn(config, oSaham, oHist)
  #config.SendDebugMsg('RR8')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  moduleapi = modman.getModule(config, 'moduleapi')
  TransactInv = modman.getModule(config, 'TransactInv')
  recReksa = parameter.uipSaham.GetRecord(0)
  modeOto = recReksa.ModeOto
  
  strSQL = 'Select * from HistNABSaham \
            where id_investasi = %d and UserOto Is Null ' \
            % recReksa.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  if rSQL.Eof :
    raise Exception, '\PERINGATAN' + 'Perubahan belum dilakukan'
  Id_hist = rSQL.HistNABSahamID
    
  config.BeginTransaction()
  try :
    oHist = config.CreatePObjImplProxy('HistNABSaham')
    oHist.Key = Id_hist
    oSaham = config.CreatePObjImplProxy('Saham')
    oSaham.Key = recReksa.id_Investasi
    if oSaham.IsNull :
      raise Exception, 'PERINGATAN' + 'Investasi tidak ditemukan'
    config.SendDebugMsg('a1')
    if modeOto : 
       #oBatch = config.CreatePObjImplProxy('TransactionBatch')
       #oBatch.key = oHist.ID_TransactionBatch
       if recReksa.jenis_perubahan == 0 : #topup
          oSR = TransactInv.GetLastHistSaham(config, oSaham)
          oSR.NAB_Transaksi = recReksa.NAB
          oSR.Unit_Penyertaan = recReksa.unit_penyertaanbaru
          oSR.NAB_Awal = recReksa.NAB
          oSR.Tgl_sistem = recReksa.Tgl_Penetapan

          oSR.subscription_fee = oSR.NAB_Transaksi*oSR.Unit_Penyertaan
          
          oSaham.unit_penyertaan += recReksa.unit_penyertaanbaru
          
          if oSaham.akum_nominal != oSaham.nominal_pembukaan :
            oSaham.nominal_pembukaan += oSR.subscription_fee
            
          oSaham.NAB_Transaksi = round(oSaham.nominal_pembukaan / oSaham.unit_penyertaan,6)
       
       config.SendDebugMsg('a2')
       OtorisasiPerubahanSaham(config, oSaham, oHist, not recReksa.jenis_perubahan)
       config.SendDebugMsg('a3')
       
       if recReksa.jenis_perubahan == 2 :#redemption
          oRR = TransactInv.GetLastRedemtSaham(config, oSaham)
          oRR.NAB = recReksa.NAB
          up = recReksa.unit_penyertaanbaru
          totRedempt = oRR.NAB*up
          costRedempt = oSaham.NAB_Transaksi * up

          oRR.nominal_jual = totRedempt
          oRR.profit = totRedempt - costRedempt
          oRR.mutasi_kredit = costRedempt
          config.SendDebugMsg('a4')

          #cek status commit redemption
          if oRR.isCommitted != 'N' :
            raise Exception, 'PERINGATAN' + 'Redemption belum diotorisasi'
          oRR.isCommitted = 'T'
          
          oRR.unit_penyertaan = up
          oSaham.akum_nominal -= totRedempt
          TransactInv.CreateRincianPokok(config, oSaham, -totRedempt)
          config.SendDebugMsg('a5')
            
          #Realize return
          RealReturn (config, oSaham, oRR, oHist)
          config.SendDebugMsg('a6')
          
          oSaham.Unit_Penyertaan -= recReksa.unit_penyertaanbaru
          if moduleapi.IsApproxZero(oSaham.Unit_Penyertaan) :
            oSaham.status = 'F'

    else :
       BatalkanPerubahanSaham(config, oSaham, oHist)
    config.Commit()
  except :
    config.Rollback()
    raise


  return 1