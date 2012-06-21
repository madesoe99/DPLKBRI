import sys

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  filename = 'c:/dafapp/dplk/userhome/histtransinv.txt'
  status = returnpacket.CreateValues(['Is_Err',0],['Err_Message',''],['filename',''])
  try:
    fHandle = open(filename,'w')  
    try:
      textreport = GetHistoriTransaksi(config, parameter, returnpacket)
      fHandle.write(textreport)
      config.SendDebugMsg(textreport)
    finally:
      fHandle.close()
      
    sw = returnpacket.AddStreamWrapper()
    sw.LoadFromFile(filename)
    sw.Name = "upload"
    sw.MIMEType = "txt"
      
  except:
    status.Is_Err = 1
    status.Err_Message = str(sys.exc_info()[1])
  
  return 1

def GetNamaJenisTransaksi(config, kode):
  nama = ''
  sSQL = "select nama from namajnstransinv where kode_jenis_trinvestasi = '%s'" % kode
  rSQL = config.CreateSQL(sSQL).RawResult
  if not rSQL.Eof: nama = rSQL.nama
  
  return nama
  
def GetHistoriTransaksi(config, parameters, returns):

    # Get Parameter
    rec = parameters.FirstRecord
    Id_Investasi = rec.Id_Investasi
    TglAwal   = rec.TglAwal
    TglAkhir  = rec.TglAkhir

    # Preparing returns
    def AsString(tdate):
        return str(tdate[0]) + '/' + str(tdate[1]) + '/' + str(tdate[2])

    s = ' \
        SELECT FROM TransaksiInvestasi \
        [ \
          Id_Investasi = :Id_Investasi and \
          tgl_transaksi >= :TglAwal and \
          tgl_transaksi < :TglAkhir \
        ] \
        ( \
          Id_TransaksiInvestasi, \
          tgl_transaksi, \
          kode_jenis_trinvestasi, \
          Keterangan, \
          Mutasi_Debet, \
          Mutasi_Kredit, \
          LTransactionBatch.no_batch,\
          tgl_sistem,\
          isCommitted, \
          kode_jns_investasi, \
          Self \
        ) \
        THEN ORDER BY ASC Tgl_Transaksi, ASC Id_TransaksiInvestasi;'

    oql = config.OQLEngine.CreateOQL(s)
    oql.SetParameterValueByName('Id_Investasi', Id_Investasi)
    oql.SetParameterValueByName('TglAwal', TglAwal)
    oql.SetParameterValueByName('TglAkhir', TglAkhir + 1)
    oql.ApplyParamValues()

    config.SendDebugMsg(oql.SQLText)
    oql.active = 1
    ds  = oql.rawresult
    header = 'ID|Tgl Transaksi|Tgl Sistem|Kode Jenis Investasi|Keterangan|Debet|Kredit|No Batch|Status Otorisasi\n' 
    textreport = ''
    while not ds.Eof:
        id = ds.Id_TransaksiInvestasi
        ket = GetNamaJenisTransaksi(config, ds.kode_jenis_trinvestasi)
          
        curtxt = '%s|%s|%s|%s|%s|%s|%s|%s|%s\n' % (id, AsString(ds.Tgl_Transaksi),\
        AsString(ds.tgl_sistem),ds.kode_jenis_trinvestasi,\
        ket,ds.Mutasi_Debet,ds.Mutasi_Kredit,ds.No_Batch,ds.isCommitted)

        textreport = textreport + curtxt

        ds.Next()

    return header + textreport
