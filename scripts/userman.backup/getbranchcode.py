def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  strSQL = '\
    select branch_code \
    from BranchLocation'
  resSQL = config.CreateSQL(strSQL).RawResult
  
  resSQL.First()
  if resSQL.Eof:
    raise 'Branch is not found.'
    
  returnpacket.CreateValues(['branch_code',resSQL.branch_code])

  return 1
