import sys
sys.path.append('c:/dafapp/dplk07/scripts/report')

import AdvisTransaksi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  classTransaksi = parameter.FirstRecord.classtransaksi

  #buat dulu objek HistoriPindahPaketInvestasi
  oH = config.CreatePObjImplProxy('HistoriPindahPaketInvestasi')
  oH.Key = parameter.FirstRecord.idHistori
  
  #cari ID_Transaksi biaya adm transaksi pindah paket yang tanggal histori dan 
  #no peserta sama dengan data di objek HistoriPindahPaketInvestasi
  sSQL = 'select ID_Transaksi from TransaksiDPLK where \
    kode_jenis_transaksi = \'X\' and isPindahPaket = \'T\' and no_peserta = \'%s\' and \
    tgl_transaksi = \'%s\' and kode_paket_investasi = \'%s\'' \
    % (oH.no_peserta, '%d-%d-%d' % (oH.tanggal_histori[0],oH.tanggal_histori[1],\
    oH.tanggal_histori[2]), oH.kode_paket_investasi)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  #debug code
  config.SendDebugMsg(sSQL)
  
  #harus ketemu 1 result
  rSQL.First()
  if not rSQL.Eof:
    idTransaksi = rSQL.ID_Transaksi
  
  sBaseFileName = AdvisTransaksi.CreateAdvis(config, classTransaksi, idTransaksi)
  
  #return packet
  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1
