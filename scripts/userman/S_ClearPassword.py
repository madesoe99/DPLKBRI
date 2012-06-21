import sys
import com.ihsan.util.base88enc as b88enc
import random

def DAFScriptMain(config, parameter, returnpacket):
  result_def = 'IsErr: integer; ErrMessage: string; DefPassword: string'
  return_record = returnpacket.CreateDataPacketStructure(result_def)
  
  IsErr = 0
  ErrMessage = ''
  config.BeginTransaction()
  try:
    dataset = parameter.GetDataset(0)
    record = dataset.GetRecord(0)
    userconst = record.data
    user = config.AccessPObject(userconst)
    
    newpwd = genPassword()
    b88 = b88enc.base88()
    user.encpassword = b88.convertFromString(newpwd)
    user.isgenpassword = "T"
    return_record.DefPassword = newpwd
    config.Commit()
  except:
    IsErr = 1
    ErrMessage = str(sys.exc_info()[1])
    config.Rollback()
    
    
  return_record.IsErr = IsErr
  return_record.ErrMessage = 'Server side error : ' + ErrMessage
  
  return 1

def genPassword():
  s = ""
  for i in range(4):
    s = s + chr(random.randint(ord('a'), ord('z')))
  s = s + str(random.randint(11, 99))
  return s
#--
  