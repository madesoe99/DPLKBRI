import com.ihsan.foundation.pobjecthelper as phelper
import sys

def doDelete(config, parameter, returnpacket) :
  #import rpdb2; rpdb2.start_embedded_debugger('solusi')
  
  status = returnpacket.CreateValues(
    ['Is_Err',0],
    ['Err_Message',''],
  )
  helper = phelper.PObjectHelper(config)
  Obj = config.AccessPObject(parameter.FirstRecord.key)
  
  if Obj.IsNull :
    raise Exception, 'WARNING' + 'Data not found'
  
  config.BeginTransaction()
  try :
    Obj = helper.GetObjectByInstance(Obj.classname,Obj)
    #if Obj.CheckForDelete() :
    Obj.Delete()
          
    #rec = helper.LoadScript('GeneralModule.S_ObjectEditor').\
    #  NonActivateData(config, Obj)
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