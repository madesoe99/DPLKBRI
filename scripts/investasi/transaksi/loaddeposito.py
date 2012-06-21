def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  strDateFrom = config.FormatDateTime('mm/dd/yyyy', parameter.FirstRecord.dateFrom)
  strDateUntil_tmrw = config.FormatDateTime('mm/dd/yyyy', parameter.FirstRecord.dateUntil_tmrw)

  returnpacket.AddDataPacketStructureEx('deposito',
    'no_bilyet:string;'\
    'kode_paket_investasi:string;'\
    'kode_pihak_ketiga:string;'\
    'akum_nominal:float;'\
    'akum_piutangLR:float;'\
    'akum_LR:float;'\
    'rollover_counter:integer;'\
    'treatmentPokok:string;'\
    'kapitalisir_rollover:string;'\
    'nisbah:float;'\
    'tgl_jatuh_tempo:datetime;'\
    'id_investasi:integer;'\
  )
  returnpacket.BuildAllStructure()
  dsDeposito = returnpacket.AddNewDataset('deposito')

  strOQL = \
    'select from Deposito '\
    '[ '\
    '  (tgl_jatuh_tempo >= \'%s\') '\
    '  and (tgl_jatuh_tempo < \'%s\') '\
    '  and (treatmentPokok = \'A\') '\
    '] '\
    '( '\
    '  no_bilyet '\
    '  , kode_paket_investasi '\
    '  , kode_pihak_ketiga '\
    '  , akum_nominal '\
    '  , akum_piutangLR '\
    '  , akum_LR '\
    '  , rollover_counter '\
    '  , treatmentPokok '\
    '  , kapitalisir_rollover '\
    '  , nisbah '\
    '  , tgl_jatuh_tempo '\
    '  , id_investasi '\
    '  , self '\
    ') '\
    'then order by id_investasi; '\
    % (strDateFrom, strDateUntil_tmrw)
  depOQL = config.OQLEngine.CreateOQL(strOQL)
  depOQL.Active = 1
  resOQL = depOQL.RawResult
  resOQL.First()
  while not resOQL.Eof:
    rec = dsDeposito.AddRecord()
    rec.no_bilyet = resOQL.no_bilyet
    rec.kode_paket_investasi = resOQL.kode_paket_investasi
    rec.kode_pihak_ketiga = resOQL.kode_pihak_ketiga
    rec.akum_nominal = resOQL.akum_nominal
    rec.akum_piutangLR = resOQL.akum_piutangLR
    rec.akum_LR = resOQL.akum_LR
    rec.rollover_counter = resOQL.rollover_counter
    rec.treatmentPokok = resOQL.treatmentPokok
    rec.kapitalisir_rollover = resOQL.kapitalisir_rollover
    rec.nisbah = resOQL.nisbah
    rec.tgl_jatuh_tempo = resOQL.tgl_jatuh_tempo
    rec.id_investasi = resOQL.id_investasi

    resOQL.Next()

  return 1
