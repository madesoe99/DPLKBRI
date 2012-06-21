import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def uipDepositoSetData(uipDeposito):
  uideflist = uipDeposito.UIDefList
  config = uideflist.Config
  rec_inv = uipDeposito.Dataset.GetRecord(0)
  rec_inv.ChangeMode = 'D'
  strSQL = 'Select * from HISTPERUBAHANDEPOSITO \
            where id_investasi = %d and UserOtorisasi Is Null ' \
            % rec_inv.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  if rSQL.Eof :
     rec_inv.IsCommited = 1
  else :
     rec_inv.IsCommited = 0
     rec_inv.tgl_buka=moduleapi.DateTimeTupleToFloat(config, rSQL.TglBukaPerb)
     if rSQL.TreatmentPokokAwal == '0' :
       rec_inv.ChangeMode = '0'
       rec_inv.jenisJatuhTempo = rSQL.jenisJatuhTempoPrb
       rec_inv.jmlHariOnCall = rSQL.jmlHariOnCallPrb
     else :
       rec_inv.no_bilyet = rSQL.NoBilyetPerb
       rec_inv.Rekening_Deposito=rSQL.RekDepoPerb
       rec_inv.kapitalisir_rollover = rSQL.IsKapitalisirPrb
       rec_inv.equivalent_rate=rSQL.ER_Perb
       rec_inv.no_rekening=rSQL.NoRekPBPerb
       rec_inv.treatmentPokok=rSQL.TreatmentPokokPrb

     rec_inv.user_id =rSQL.UserPengubah
     rec_inv.terminal_id = rSQL.TerminalUbah

  oDeposito = config.CreatePObjImplProxy('Deposito')
  oDeposito.Key = rec_inv.id_investasi
  if moduleapi.IsInvestasiTutup(config, oDeposito):
    raise '\nPERINGATAN','Investasi sudah ditutup.'

def OnBeginProcessData (uideflist, AData) :
  config = uideflist.Config
  uDepo = AData.uipDeposito.GetRecord(0)
  uAwal = AData.uipDepo_Awal.GetRecord(0)
  Tgl = config.Now()
  #Record di histori
  #config.BeginTransaction()
  #try :
  
  oHist = config.CreatePObject('HistPerubahanDeposito')
  oHist.id_investasi=uDepo.id_investasi

  oHist.UserPengubah = config.SecurityContext.UserID
  oHist.TglUbah = Tgl
  oHist.TerminalUbah = config.SecurityContext.InitIP
  oHist.TglBukaPerb=uDepo.tgl_buka

  if uDepo.ChangeMode == 'D' :
    #Awal
    oHist.NoBilyetAwal= uAwal.no_bilyet
    oHist.IsKapitalisirAwal=uAwal.kapitalisir_rollover
    oHist.NisbahAwal=uAwal.Nisbah
    oHist.ER_Awal=uAwal.equivalent_rate
    oHist.RekDepoAwal=uAwal.Rekening_Deposito
    oHist.NoRekPBAwal=uAwal.no_rekening
    oHist.TglBukaAwal=uAwal.tgl_buka
    oHist.TreatmentPokokAwal=uAwal.treatmentPokok

    #Perubahan
    oHist.NoBilyetPerb=uDepo.no_bilyet
    oHist.IsKapitalisirPrb=uDepo.kapitalisir_rollover
    oHist.ER_Perb=uDepo.equivalent_rate
    oHist.RekDepoPerb=uDepo.Rekening_Deposito
    oHist.NoRekPBPerb=uDepo.no_rekening
    oHist.TreatmentPokokPrb=uDepo.treatmentPokok

  else : #ubah periode
    #Cek Jatuh Tempo
    if uDepo.tgl_jatuh_tempo >= int(config.Now()) + 10 :
      raise 'PERINGATAN','Deposito belum jatuh tempo'
    #Ubah Data
    oHist.jenisJatuhTempoAwal = uAwal.jenisJatuhTempo
    oHist.jenisJatuhTempoPrb = uDepo.jenisJatuhTempo
    oHist.jmlHariOnCallAwal = (uAwal.jmlHariOnCall or 0)
    oHist.jmlHariOnCallPrb = (uDepo.jmlHariOnCall or 0)
    oHist.TreatmentPokokAwal = '0'
  #  config.Commit()
  #except :
  #  config.Rollback()
  #  raise

  return 0
