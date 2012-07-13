def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  GetHistoriTransaksi(config, parameter, returnpacket)
  
  return 1

def GetHistoriTransaksi(config, parameters, returns):
    JD = 'D'
    ParamTrans = {JD+'A':'RegistrasiDeposito',
                  JD+'C':'TutupDeposito',
                  JD+'E':'BagiHasilDeposito',
                  JD+'F':'BagiHasilDeposito'} #Parameter Keterangan

    def AsDateTime(tdate):
        utils = config.ModLibUtils
        return utils.EncodeDate(tdate[0], tdate[1], tdate[2])


    # Get Parameter
    rec = parameters.FirstRecord
    Id_Investasi = rec.Id_Investasi
    TglAwal   = rec.TglAwal
    TglAkhir  = rec.TglAkhir

    # Preparing returns
    dsHist = returns.AddNewDatasetEx(
        'histori',
        ';'.join([
            'Id_TransaksiInvestasi: integer', 'TglTransaksi: datetime',
            'Kode: string',          'Keterangan: string',
            'Mutasi_Debet: float',   'Mutasi_Kredit: float',
            'Status_Otorisasi: string',
            'TglEfektif: datetime'
        ])
    )


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

    while not ds.Eof:
        id = ds.Id_TransaksiInvestasi

        recHist = dsHist.AddRecord()
        recHist.Id_TransaksiInvestasi = ds.Id_TransaksiInvestasi
        recHist.TglTransaksi = AsDateTime(ds.Tgl_Transaksi)
        recHist.TglEfektif = AsDateTime(ds.tgl_sistem)
        recHist.Kode = ds.kode_jenis_trinvestasi

        if ParamTrans.has_key(ds.kode_jns_investasi+ds.kode_jenis_trinvestasi) :
          recHist.Keterangan = ParamTrans[ds.kode_jns_investasi+ds.kode_jenis_trinvestasi]
        else :
          recHist.Keterangan = ds.Keterangan
        recHist.Mutasi_Debet = ds.Mutasi_Debet
        recHist.Mutasi_Kredit = ds.Mutasi_Kredit
        recHist.Status_Otorisasi = ds.isCommitted

        ds.Next()

    #Peran = config.SecurityContext.GetUserInfo()[7]
    #if countH != 0 and Peran.find('ALLOWEDUSER') == -1:
    #   if (countTD + countH) > 100 and (Tanggal_Akhir - Tanggal_Awal) > 3 :
    #      raise Exception, 'PERINGATAN','Data terlalu banyak tidak dapat diambil +  kurangi range tanggal'
