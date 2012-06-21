import com.ihsan.foundation.pobjecthelper as phelper
import sys

def doDelete(config, parameter, returnpacket) :
  #import rpdb2; rpdb2.start_embedded_debugger('solusi')
  
  config.BeginTransaction()
  try :
    status = returnpacket.CreateValues(
      ['Is_Err',0],
      ['Err_Message',''],
    )
    
    oJP = config.CreatePObjImplProxy("JenisPekerjaan")
    oJP.Key = parameter.FirstRecord.key.split("=")[1]

    if oJP.IsNull :
      raise Exception,'\n\nWARNING\nData not found'
  
    oJP.Ls_JenisPekerjaanDetail.DeleteAllPObjs()
    oJP.Delete()
          
    config.Commit()
  except :
    config.Rollback()
    status.Is_Err = 1
    status.Err_Message = str(sys.exc_info()[1])

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  doDelete(config, parameter, returnpacket)

  return 1