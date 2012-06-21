import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def OtorisasiPerubahanDeposito(config, oDepo, oHist):
    
  oHist.UserOtorisasi = config.SecurityContext.UserID
  oHist.TglOtorisasi = config.Now()
  oHist.TerminalOto = config.SecurityContext.InitIP

  if oHist.TreatmentPokokAwal == '0' : #mode karakter nol bukan O
    oDepo.jenisJatuhTempo = oHist.jenisJatuhTempoPrb
    oDepo.jmlHariOnCall = oHist.jmlHariOnCallPrb
    moduleapi.AdvanceJatuhTempo(config, oDepo)
    oHist.TreatmentPokokAwal = ''
  else :
    if oDepo.no_bilyet != oHist.NoBilyetPerb :
      moduleapi.CheckNoBilyetAvl(config,oHist.NoBilyetPerb) 

    config.SendDebugMsg('ER : '+str(oHist.ER_Perb))
    oDepo.no_bilyet = oHist.NoBilyetPerb
    oDepo.kapitalisir_rollover = oHist.IsKapitalisirPrb
    oDepo.Nisbah=oHist.NisbahPerb
    oDepo.equivalent_rate=oHist.ER_Perb
    oDepo.Rekening_Deposito=oHist.RekDepoPerb
    oDepo.no_rekening=oHist.NoRekPBPerb
    oDepo.tgl_buka=moduleapi.DateTimeTupleToFloat(config, oHist.TglBukaPerb)
    oDepo.treatmentPokok=oHist.TreatmentPokokPrb

def BatalkanPerubahanDeposito(config, oDepo, oHist) :
  
  #oDepo.no_bilyet = oHist.NoBilyetAwal
  #oDepo.kapitalisir_rollover = oHist.IsKapitalisirAwal
  #oDepo.Nisbah=oHist.NisbahAwal
  #oDepo.Rekening_Deposito=oHist.RekDepoAwal
  #oDepo.no_rekening=oHist.NoRekPBAwal
  #oDepo.tgl_buka=oHist.TglBukaAwal
  #oDepo.treatmentPokok=oHist.TreatmentPokokAwal
  
  oHist.Delete()



def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  recDepo = parameter.uipDeposito.GetRecord(0)
  modeOto = recDepo.ModeOto
  
  strSQL = 'Select * from HISTPERUBAHANDEPOSITO \
            where id_investasi = %d and UserOtorisasi Is Null ' \
            % recDepo.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  if rSQL.Eof :
    raise '\PERINGATAN','Perubahan belum dilakukan'
  Id_hist = rSQL.Id_HistPerubahan 
  
    
  config.BeginTransaction()
  try :
    oHist = config.CreatePObjImplProxy('HistPerubahanDeposito')
    oHist.Key = Id_hist
  
    oDepo = config.CreatePObjImplProxy('Deposito')
    oDepo.Key = recDepo.id_Investasi  
    if oDepo.IsNull :
      raise 'PERINGATAN','Investasi tidak ditemukan'
    
    if modeOto :
       OtorisasiPerubahanDeposito(config, oDepo, oHist)
    else :
       BatalkanPerubahanDeposito(config, oDepo, oHist)
    config.Commit()
  except :
    config.Rollback()
    raise


  return 1

