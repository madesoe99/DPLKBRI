def UpdateProcess(config, namaTabel, updatedField, condition, flag):
  config.BeginTransaction()
  try:
    res = config.ExecSQL('update %s set %s where (%s) and %s' \
      % (namaTabel, updatedField, condition, flag))
    if res < 0:
      message = 'Data sedang diperbarui pengguna lain.'
    elif res == 0:
      message = 'Data sudah terbarukan, tidak perlu diperbarui lagi.'
    else:
      #update berhasil
      config.Commit()
      message = 'Koreksi/perubahan berhasil.'    
  except:
    config.Rollback()
    raise

  return [res, message]

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  namaTabel = parameter.FirstRecord.namatabel
  updatedField = parameter.FirstRecord.updatedfield
  condition = parameter.FirstRecord.condition
  flag = parameter.FirstRecord.flag
  
  result = UpdateProcess(config, namaTabel, updatedField, condition, flag)
  
  returnpacket.CreateValues(\
    ['status', result[0]],\
    ['message', result[1]]\
  )

  return 1
