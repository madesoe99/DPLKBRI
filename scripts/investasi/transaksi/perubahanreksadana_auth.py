import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

def UbahNominalInvestasi(config, oReksa, oHist,statNAB, Nom):
  moduleapi = modman.getModule(config, 'moduleapi')
  TransactInv = modman.getModule(config, 'TransactInv')
  
  tgl = config.Now()

  akum_awal = oReksa.akum_nominal
  oReksa.akum_nominal = oReksa.NAB * oReksa.unit_penyertaan
  prof = oReksa.akum_nominal-akum_awal

  oSPI = TransactInv.CreateSPINoBatch(config, oReksa.nama_reksadana, oReksa, '', prof,'N', moduleapi.DateTimeTupleToFloat(config, oHist.tgl_penetapan))
  TransactInv.CreatePNINoBatch(config, oReksa.nama_reksadana, oReksa, oSPI, prof,'N')

  TransactInv.CreateRincianPokok(config, oReksa, oReksa.akum_nominal-akum_awal)

def OtorisasiPerubahanReksadana(config, oReksa, oHist, IsSubs):
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
  else:
    UP = oReksa.unit_penyertaan
  
  Nom =  (oHist.NAB - oReksaNAB)*UP
  
  if Nom != 0.0 :
    UbahNominalInvestasi(config, oReksa, oHist,statNAB, Nom)

  if int(oHist.TerminalOto) : #Proses Unrealize Hasil Reksadana
    UnrealReturn(config, oReksa, oHist)

  oHist.UserOto = config.SecurityContext.UserID
  #oHist.tgl_penetapan = config.Now()
  oHist.TerminalOto = config.SecurityContext.InitIP
  
def BatalkanPerubahanReksadana(config, oReksa, oHist) :
  oHist.Delete()

def UnrealReturn(config, oReksa, oHist):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  #kenaikan /penurunan investasi
  oTransLRInvestasi = config.CreatePObject('KlaimLRReksadana')
  oTransLRInvestasi.LInvestasi = oReksa
  oTransLRInvestasi.nama_investasi = oReksa.nama_reksadana
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
  TransactInv.CreatePNINoBatch(config, oReksa.nama_reksadana, oReksa, oTransLRInvestasi, -unrealReturn,'L')

def RealReturn (config, oReksa, oRR, oHist):
  moduleapi = modman.getModule(config, 'moduleapi')
  TransactInv = modman.getModule(config, 'TransactInv')
  
  oTransLRInvestasi = config.CreatePObject('RealisasiReturn')
  oTransLRInvestasi.LInvestasi = oReksa
  oTransLRInvestasi.nama_investasi = oReksa.nama_reksadana
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
  
  TransactInv.CreateRincianBagiHasil(config, oReksa, RealReturn)
  oReksa.akum_LR += RealReturn
  oReksa.nominal_pembukaan -= (oRR.unit_penyertaan * oReksa.NAB_Transaksi)
  
  #tambahan SPI
  TransactInv = modman.getModule(config, 'TransactInv')
  TransactInv.CreateSPINoBatch(config, oReksa.nama_reksadana, oReksa, oTransLRInvestasi, -RealReturn ,'N')
  TransactInv.CreatePNINoBatch(config, oReksa.nama_reksadana, oReksa, oTransLRInvestasi, -RealReturn,'N')
  UnrealReturn(config, oReksa, oHist)

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
    oReksa.tgl_settlement = recReksa.Tgl_Penetapan
    if oReksa.IsNull :
      raise Exception, 'PERINGATAN: Investasi tidak ditemukan'
    if modeOto : 
       #oBatch = config.CreatePObjImplProxy('TransactionBatch')
       #oBatch.key = oHist.ID_TransactionBatch
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

       OtorisasiPerubahanReksadana(config, oReksa, oHist, not recReksa.jenis_perubahan)
       
       if recReksa.jenis_perubahan == 2 :#redemption
          oRR = TransactInv.GetLastRedemt(config, oReksa)
          oRR.NAB = recReksa.NAB
          up = recReksa.unit_penyertaanbaru
          totRedempt = oRR.NAB*up
          costRedempt = oReksa.NAB_Transaksi * up

          oRR.nominal_jual = totRedempt
          oRR.profit = totRedempt - costRedempt
          oRR.mutasi_kredit = costRedempt

          #cek status commit redemption
          if oRR.isCommitted != 'N' :
            raise Exception, 'PERINGATAN: Redeem belum diotorisasi'
          oRR.isCommitted = 'T'
          
          oRR.unit_penyertaan = up
          oReksa.akum_nominal -= totRedempt
          TransactInv.CreateRincianPokok(config, oReksa, -totRedempt)
            
          #Realize return
          RealReturn (config, oReksa, oRR, oHist)
          
          oReksa.Unit_Penyertaan -= recReksa.unit_penyertaanbaru
          moduleapi = modman.getModule(config, 'moduleapi')
          if moduleapi.IsApproxZero(oReksa.Unit_Penyertaan) :
            oReksa.status = 'F'

    else :
       BatalkanPerubahanReksadana(config, oReksa, oHist)
    config.Commit()
  except :
    config.Rollback()
    raise

  return 1