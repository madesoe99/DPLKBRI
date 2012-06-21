import sys
import com.ihsan.util.dbutil as dbutil

def DAFScriptMain(config, parameter, returnpacket): 
  result_def = 'IsErr: integer; ErrMessage: string'
  return_record = returnpacket.CreateDataPacketStructure(result_def)
  
  IsErr = 0
  ErrMessage = ''
  config.BeginTransaction()
  try:
    lockall_sql = "UPDATE UserApp SET login_count = 0 AND islocked = 'T' WHERE user_id <> 'admin' "
    dbutil.runSQL(config, lockall_sql)

    config.Commit()
  except:
    IsErr = 1
    ErrMessage = str(sys.exc_info()[1])
    config.Rollback()
    
  return_record.IsErr = IsErr
  return_record.ErrMessage = 'Server side error : ' + ErrMessage
  
  return 1
