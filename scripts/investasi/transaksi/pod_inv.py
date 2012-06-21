import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def ARODeposito(config, strNow) :
  strSQL = \
    'select i.id_investasi, tgl_jatuh_tempo '\
    'from Deposito d, Investasi i '\
    'where d.id_investasi = i.id_investasi '\
    '  and i.status = \'T\' '\
    '  and (d.treatmentPokok in (\'A\')) '\
    '  and datediff(day, tgl_jatuh_tempo, \'%s\') >= 0 '\
    % (strNow)

  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  while not rSQL.Eof :
    oDeposito = config.CreatePObjImplProxy('Deposito')
    oDeposito.Key = rSQL.id_investasi
    
    moduleapi = modman.getModule(config, 'moduleapi')
    moduleapi.AdvanceJatuhTempo(config, oDeposito)
    
    oDeposito.last_update = config.Now()
    
    rSQL.Next()

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  TglNow = config.Now()
  strNow = config.FormatDateTime('yyyy-mm-dd', TglNow)
  config.BeginTransaction()
  try :
    ARODeposito(config, strNow)
    config.Commit()
  except :
    config.Rollback()
    raise
  return 1
