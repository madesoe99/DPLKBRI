import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  try:
    #checking status dplk peserta
    uiCalled = uideflist.GetPClassUIByName(auiname)
    if auiname == 'uipMaster':
      no_peserta = uiCalled.ActiveRecord.no_peserta
    else:
      no_peserta = uiCalled.ActiveRecord.GetFieldByName('LNasabahDPLK.no_peserta')
    moduleapi.IsPesertaAktif(config, no_peserta)

    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    if uideflist.uipMaster.Dataset.RecordCount > 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'Y')
  except:
    raise

  uipRegisterCIF = uideflist.uipRegisterCIF

  if uipRegisterCIF.DataSet.RecordCount > 0:
    rec = uipRegisterCIF.DataSet.GetRecord(0)
  else:
    rec = uipRegisterCIF.DataSet.AddRecord()

  rec.user_id = config.SecurityContext.userid
  rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  rec.tanggal_register = config.Now()
  
  return 0

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode
  
  #sender.ActiveInstance.jpd_id = sender.ActiveRecord.jpd_id
  #sender.ActiveInstance.jpd_id_ortu = sender.ActiveRecord.jpd_id_ortu
  
  if oData.no_referensi in ['', None]:
    raise Exception,'\nRegistrasi Error\n\nNomor referensi tidak terdefinisi.'



def FormOnGeneralProcessData(uideflist, datapacket):
  # function(uideflist: TPClassUIDefList; datapacket: TPClassUIDataPacket):boolean
  
  #dummy, s = datapacket.GetSerializationString()
  #raise Exception, s
  
  return 1