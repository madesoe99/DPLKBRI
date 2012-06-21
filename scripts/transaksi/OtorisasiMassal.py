import string, sys
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')
sys.path.append('c:/dafapp/dplk07/script_modules')
import AuthorizeTransaksi, transaksiapi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  rec = parameter.FirstRecord
  kode_cbg = rec.kode_cbg
  tgl_awal = rec.tgl_awal
  tgl_akhir = rec.tgl_akhir
  try:
    sSQL = 'SELECT ID_Transaksi, No_Peserta, Kode_Jenis_Transaksi \
    FROM TransaksiDPLK \
    WHERE branch_code = \'%s\' AND \
    Flag_Pilih = \'Y\' AND \
    IsCommitted = \'F\' AND \
    tgl_transaksi >= \'%s\' AND tgl_transaksi <= \'%s\' ' \
    % (kode_cbg, tgl_awal, tgl_akhir)
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    while not rSQL.Eof:
	JenisTransaksi = rSQL.kode_jenis_transaksi
	if JenisTransaksi in ['I','O','P']:
	    tab = 'PengalihanDariDPLKLain'
	elif JenisTransaksi == 'H':
	    tab = 'PengalihanKeDPLKLain'
	elif JenisTransaksi == 'V':
	    tab = 'PenarikanDanaNormal'
	    transaksiapi.CekRentangWaktuPenarikan(config, rSQL.no_peserta)
	    transaksiapi.CekSaldoIuranMin(config, rSQL.no_peserta)
	elif JenisTransaksi == 'W':
	    tab = 'PenarikanDanaPHK'  
	    transaksiapi.CekBatasTarikMinPHK(config, rSQL.ID_Transaksi)
	    transaksiapi.CekBatasTarikMaxPHK(config, rSQL.ID_Transaksi)
	elif JenisTransaksi == 'J':
	    tab = 'PengambilanManfaat'
	elif JenisTransaksi == 'M':
	    tab = 'TransaksiDPLKManual'
	elif JenisTransaksi == 'K':
	    tab = 'IuranPeserta'
	    
	config.SendDebugMsg(tab)
	try:
	    dh = AuthorizeTransaksi.AuthorizeOperation(config, tab, rSQL.ID_Transaksi, 'A')
	except:
	    raise '\nProses Error', str(sys.exc_info()[1])
		
	rSQL.Next()
	
  except:
    raise

  return 1
