#import sys
#sys.path.append('c:/dafapp/dplk07/script_modules')


def HitungSRR(config, no_peserta, kode_paket, day_count):
  strSQL = 'select max(Id_HistoriSRR) as Id_SRR from HistoriSRR h \
            where no_peserta = \'%s\' ' % no_peserta
  resSQL = config.CreateSQL(strSQL).RawResult
  res = ()
  if not resSQL.Eof :
    oHSRR = config.CreatePObjImplProxy('HistoriSRR')
    oHSRR.key = resSQL.Id_SRR
    oCalcRincian = oHSRR.LSRRCalcRincian
    tgl_akhir = oCalcRincian.LSRRCalc.tgl_akhir_hitung
    TotSaldo = oHSRR.srr * day_count
    sSQL = 'select * from transaksiDPLK \
            where no_peserta = \'%s\' \
            and tgl_transaksi > \'%s-%s-%s 23:59:59\' \
            and isCommitted = \'T\' ' % (no_peserta,tgl_akhir[0],tgl_akhir[1],tgl_akhir[2],)
            
    rSQL = config.CreateSQL(sSQL).RawResult
    while not rSQL.Eof :
      TotSaldo += (day_count - rSQL.tgl_transaksi[2] + 1) * ((rSQL.MUTASI_IURAN_PK or 0.0) + (rSQL.MUTASI_IURAN_PST or 0.0) + \
          (rSQL.MUTASI_PENGEMBANGAN or 0.0) + (rSQL.MUTASI_PERALIHAN or 0.0))
      
      rSQL.Next()
    SRR_Peserta = TotSaldo/day_count 
    res = ( tgl_akhir,
            oCalcRincian.total_srr,
            0,
            SRR_Peserta,
            oHSRR.srr
            )        
  return res

def AmbilInfoNasabah(config, no_peserta):
  oNas = config.CreatePObjImplProxy('NasabahDPLK')
  oNas.Key = no_peserta
  
  oRek = oNas.LRekeningDPLK
  res = (oNas.nama_lengkap,
         oNas.tempat_lahir,
         oNas.tanggal_lahir,
         oNas.no_identitas_diri,
         oNas.jenis_kelamin,
         oNas.kode_propinsi,
         oNas.LDaerahAsal.nama_propinsi,
         oRek.kode_paket_investasi,
         oRek.LPaketInvestasi.nama_paket_investasi)    
  return res

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  no_peserta = parameter.FirstRecord.no_peserta
  y,m,d = config.ModDateTime.DecodeDate(config.Now())
  tgl_transaksi_awal = config.ModDateTime.EncodeDate(y,m,1)
  
  try:
    NasabahInfo = AmbilInfoNasabah(config,no_peserta)
    
    SRRInfo = HitungSRR(config,no_peserta,NasabahInfo[7], d)
    y,m,d = SRRInfo[0][:3]
    tgl_transaksi_awal = config.ModDateTime.EncodeDate(y,m,d) + 1
  except:
    raise
  

  returnpacket.CreateValues(
    ['no_peserta',no_peserta],
    ['nama_lengkap',NasabahInfo[0]],
    ['tempat_lahir',NasabahInfo[1]],
    ['tanggal_lahir',NasabahInfo[2]],
    ['no_identitas_diri',NasabahInfo[3]],
    ['jenis_kelamin',NasabahInfo[4]],
    ['kode_propinsi',NasabahInfo[5]],
    ['nama_propinsi',NasabahInfo[6]],
    ['tgl_transaksi_awal',tgl_transaksi_awal],
    ['kode_paket',NasabahInfo[7]],
    ['nama_paket',NasabahInfo[8]],
    ['SRR_paket',SRRInfo[1]],
    ['distribusi_inv',SRRInfo[2]],
    ['SRR_peserta',SRRInfo[3]],
    ['SRR_bln_lalu',SRRInfo[4]]
    )

  return 1
