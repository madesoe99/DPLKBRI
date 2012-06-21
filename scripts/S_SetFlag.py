import com.ihsan.foundation.pobjecthelper as phelper
import sys

def DeleteNasabahKorporat(config, parameter, returnpacket):
  IsErr = 0
  ErrMsg = ''
  
  #import rpdb2; rpdb2.start_embedded_debugger('solusi', True, True)
  config.BeginTransaction()
  try:
    rec = parameter.FirstRecord
    key = str(rec.key)
    arrRec = key.split('=')
    kode_nasabah_corporate = arrRec[1]
    
    oNasabah = config.CreatePObjImplProxy("NasabahDPLKCorporate")
    oNasabah.Key = kode_nasabah_corporate
    oNasabah.is_deleted = 1
    
    config.Commit()
  except:
    config.Rollback()
    IsErr = 1; ErrMsg = str(sys.exc_info()[1])
  
  returnpacket.CreateValues(['IsErr', IsErr], ['ErrMsg', ErrMsg])
  
  return 1
  
def DeleteNasabah(config, parameter, returnpacket):
  IsErr = 0
  ErrMsg = ''
  
  #import rpdb2; rpdb2.start_embedded_debugger('solusi', True, True)
  config.BeginTransaction()
  try:
    rec = parameter.FirstRecord
    key = str(rec.key)
    arrRec = key.split('=')
    no_peserta = arrRec[1]
    
    oNasabah = config.CreatePObjImplProxy("NasabahDPLK")
    oNasabah.Key = no_peserta
    oNasabah.is_deleted = 1
    
    config.Commit()
  except:
    config.Rollback()
    IsErr = 1; ErrMsg = str(sys.exc_info()[1])
  
  returnpacket.CreateValues(['IsErr', IsErr], ['ErrMsg', ErrMsg])
  
  return 1
  
def DeleteRekInvDPLK(config, parameter, returnpacket):
  IsErr = 0
  ErrMsg = ''
  
  #import rpdb2; rpdb2.start_embedded_debugger('solusi', True, True)
  config.BeginTransaction()
  try:
    rec = parameter.FirstRecord
    key = str(rec.key)
    arrRec = key.split('=')
    no_rekening = arrRec[1]
    
    oRekInv = config.CreatePObjImplProxy("RekInvDPLK")
    oRekInv.Key = no_rekening
    oRekInv.is_deleted = 1
    
    config.Commit()
  except:
    config.Rollback()
    IsErr = 1; ErrMsg = str(sys.exc_info()[1])
  
  returnpacket.CreateValues(['IsErr', IsErr], ['ErrMsg', ErrMsg])
  
  return 1