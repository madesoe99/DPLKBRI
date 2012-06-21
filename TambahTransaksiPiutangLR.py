##------------------------------------------------------------------------------
##TambahTransaksiPiutangLR.py
##------------------------------------------------------------------------------
##Menambah Transaksi Piutang LR Investasi yang kurang
##------------------------------------------------------------------------------
import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import dafsys, moduleapi, TransactInv
CONFIG_DEFAULT_FILE = 'c:/dafapp/dplk07/testinv.cfg'
CONFIG_FOLDER = 'c:/dafapp/dplk07/'
FORMAT_DATE_DB = 'MM/DD/YYYY'

def StrToDate(strDate, format) :
  # Pemeriksaan Format Tanggal
  if format == 'YYYY-MM-DD' :
    if strDate[4] != '-' or strDate[7] != '-' :
       raise 'ERROR','Format tanggal salah YYYY-MM-DD (untuk tanggal awal dan akhir)'
    d = int(strDate[8:])
    m = int(strDate[5:7])
    y = int(strDate[:4])
    dtTgl = config.ModLibUtils.EncodeDate(y,m,d)
  return dtTgl
  
    
  
def InsertTransPiutangLRInvestasi(config, nom, oInv) :
  oPLRI = config.CreatePObject('TransPiutangLRInvestasi')
  oPLRI.kode_jenis_trinvestasi = 'M' # Kode Migrasi
  oPLRI.LInvestasi = oInv
  #oPendapatanReksadana.LTransactionBatch = oBatch
  oPLRI.kode_jns_investasi = oInv.kode_jns_investasi 
  oPLRI.tgl_transaksi = config.ModDateTime.EncodeDate(2009,12,31)
  oPLRI.mutasi_debet = nom
  oPLRI.mutasi_kredit = 0.0
  oPLRI.isCommitted = 'T'
  oPLRI.nama_investasi = 'PIUTANG TAHUN 2009'
  oPLRI.tgl_sistem = config.Now()
  oPLRI.tgl_otorisasi = config.Now()
  oPLRI.user_id = 'IMPORT MASSAL KOR'
  oPLRI.user_id_auth = 'IMPORT MASSAL KOR'
  oPLRI.terminal_id = '127.0.0.1'
  oPLRI.terminal_id_auth = '127.0.0.1'
  
  oPLRI = config.CreatePObject('TransPiutangLRInvestasi')
  oPLRI.kode_jenis_trinvestasi = 'M' # Kode Migrasi
  oPLRI.LInvestasi = oInv
  #oPendapatanReksadana.LTransactionBatch = oBatch
  oPLRI.kode_jns_investasi = oInv.kode_jns_investasi 
  oPLRI.tgl_transaksi = config.ModDateTime.EncodeDate(2010,01,01)     
  oPLRI.mutasi_debet = 0.0
  oPLRI.mutasi_kredit = nom    
  oPLRI.isCommitted = 'T'
  oPLRI.nama_investasi = 'PIUTANG TAHUN 2010'
  oPLRI.tgl_sistem = config.Now()
  oPLRI.tgl_otorisasi = config.Now()
  oPLRI.user_id = 'IMPORT MASSAL KOR'
  oPLRI.user_id_auth = 'IMPORT MASSAL KOR'
  oPLRI.terminal_id = '127.0.0.1'
  oPLRI.terminal_id_auth = '127.0.0.1'

  return 1

def MainFlow(config) :
    config.BeginTransaction()
    try :
      oInv = config.CreatePObjImplProxy('Investasi')
      oInv.key = 115
      InsertTransPiutangLRInvestasi(config, 44981722,oInv)
      oInv = config.CreatePObjImplProxy('Investasi')
      oInv.key = 83
      InsertTransPiutangLRInvestasi(config, 475351710,oInv)
      config.Commit()
    except :
      config.Rollback()
      raise
#main function
if len(sys.argv) < 3:
      raise 'argument error', 'TambahTransaksiPiutangLR.py <Config File>'
#
CONFIG_FILE = CONFIG_FOLDER + sys.argv[2]
config = dafsys.OpenConfig(CONFIG_FILE)
print 'Configuration File : %s' % CONFIG_FILE
MainFlow(config)
    
