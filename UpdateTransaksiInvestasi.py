##------------------------------------------------------------------------------
##UpdateTransaksiInvestasi.py
##------------------------------------------------------------------------------
##Mengupdate transaksi investasi yang salah nilainya
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
  
    
def ProcessObligasi(config, oObligasi) :
  strSQL = '\
      select id_transaksiinvestasi,mutasi_debet,mutasi_kredit  \
      from transaksiinvestasi \
      where clsftransaksiinvestasi = \'A\' and \
        ID_TRansactionBatch is null and id_investasi = %s ' % (oObligasi.id_investasi)
  rSQL = config.CreateSQL(strSQL).RawResult
  while not rSQL.Eof :
    if (rSQL.mutasi_debet-rSQL.mutasi_kredit) != oObligasi.nominal_pembukaan : 
      #Membuat transaksi SPI dan PNI
      oBeliObligasi = config.CreatePObjImplProxy('BeliObligasi')
      oBeliObligasi.key = rSQL.id_transaksiinvestasi
      nominal = (rSQL.mutasi_debet-rSQL.mutasi_kredit)- oObligasi.nominal_pembukaan
      TransactInv.CreateSPI(config, oObligasi.nama_obligasi, oObligasi, oBeliObligasi, nominal,'O')
      TransactInv.CreatePNI(config, oObligasi.nama_obligasi, oObligasi, oBeliObligasi, nominal,'O')
      
      #kurangi transaksi piutang investasi
      oBeliObligasi.mutasi_kredit = nominal
    rSQL.Next()
  
  strSQL = '\
      select id_transaksiinvestasi,mutasi_debet,mutasi_kredit  \
      from transaksiinvestasi \
      where clsftransaksiinvestasi = \'B\' and \
        ID_TRansactionBatch is null and id_investasi = %s ' % (oObligasi.id_investasi)
  rSQL = config.CreateSQL(strSQL).RawResult
  while not rSQL.Eof :
    if rSQL.mutasi_debet == 0.0 and rSQL.mutasi_kredit == 0.0 :
      return 1
    if rSQL.mutasi_debet == nominal :
      oPiutLR = config.CreatePObjImplProxy('TransPiutangLRInvestasi')
      oPiutLR.key = rSQL.id_transaksiinvestasi
      oPiutLR.mutasi_kredit = oPiutLR.mutasi_debet
    else :
      raise 'PERINGATAN','Data Salah'
    rSQL.Next()
  return 1
  
def ProcessReksadana(config, oReksadana) :
  #proses piutang investasi
  strSQL = '\
      select id_transaksiinvestasi,mutasi_debet,mutasi_kredit  \
      from transaksiinvestasi \
      where clsftransaksiinvestasi = \'A\' and \
        ID_TRansactionBatch is null and id_investasi = %s ' %(oReksadana.id_investasi)
  rSQL = config.CreateSQL(strSQL).RawResult
  while not rSQL.Eof :
    if (rSQL.mutasi_debet-rSQL.mutasi_kredit) != oReksadana.nominal_pembukaan : 
      #Membuat transaksi SPI saja
      oSR = config.CreatePObjImplProxy('SubscribeReksadana')
      oSR.key = rSQL.id_transaksiinvestasi
      nominal = oReksadana.akum_nominal - oReksadana.nominal_pembukaan
      TransactInv.CreateSPI(config, oReksadana.nama_reksadana, oReksadana, oSR, nominal,'S')
      
      #kurangi transaksi piutang investasi
      oSR.mutasi_kredit = nominal
    rSQL.Next()
  
  #proses piutang lr investasi yang diubah menjadi KlaimLRReksadana.
  strSQL = '\
      select id_transaksiinvestasi,mutasi_debet,mutasi_kredit  \
      from transaksiinvestasi \
      where clsftransaksiinvestasi = \'B\' and \
        ID_TRansactionBatch is null and id_investasi = %s ' %(oReksadana.id_investasi)
        
  rSQL = config.CreateSQL(strSQL).RawResult
  while not rSQL.Eof :
    oPLRI = config.CreatePObjImplProxy('TransPiutangLRInvestasi')
    oPLRI.key = rSQL.id_transaksiinvestasi
    nominal = oReksadana.akum_piutangLR
    #Membuat transaksi KlaimLRReksadana
    oPendapatanReksadana = config.CreatePObject('KlaimLRReksadana')
    oPendapatanReksadana.kode_jenis_trinvestasi = 'L' # UnReal Return
    oPendapatanReksadana.LInvestasi = oReksadana
    #oPendapatanReksadana.LTransactionBatch = oBatch
    oPendapatanReksadana.kode_jns_investasi = oReksadana.kode_jns_investasi 
    oPendapatanReksadana.tgl_transaksi = config.Now()
     
    if nominal > 0.0 :
      # pendapatan
      oPendapatanReksadana.kode_subjns_LRInvestasi = 'C-PROF' # pendapatan reksadana
      oPendapatanReksadana.mutasi_debet = 0.0
      oPendapatanReksadana.mutasi_kredit = nominal
      oPLRI.mutasi_kredit = nominal
    else:
      oPendapatanReksadana.kode_subjns_LRInvestasi = 'C-COST' # biaya reksadana
      oPendapatanReksadana.mutasi_debet = -nominal
      oPendapatanReksadana.mutasi_kredit = 0.0
      oPLRI.mutasi_debet = -nominal
    
    oPendapatanReksadana.isCommitted = 'T'
    oPendapatanReksadana.nama_investasi = oReksadana.nama_reksadana
    oPendapatanReksadana.tgl_sistem = config.Now()
    oPendapatanReksadana.tgl_otorisasi = config.Now()
    oPendapatanReksadana.user_id = 'IMPORT MASSAL KOR'
    oPendapatanReksadana.user_id_auth = 'IMPORT MASSAL KOR'
    oPendapatanReksadana.terminal_id = '127.0.0.1'
    oPendapatanReksadana.terminal_id_auth = '127.0.0.1'
      
    #kurangi transaksi piutang investasi
    oReksadana.akum_piutangLR -= nominal
    oReksadana.akum_lr += nominal
    rSQL.Next()

  return 1

def MainFlow(config) :
    strSQL = '\
      select id_investasi,kode_jns_investasi  \
      from investasi \
      where kode_jns_investasi in (\'R\',\'O\') and \
        User_ID_AUTH = \'IMPORT MASSAL\' '
    rSQLID = config.CreateSQL(strSQL).RawResult
    
    config.BeginTransaction()
    try :
      while not rSQLID.Eof :
        oInv = config.CreatePObjImplProxy('Investasi')
        oInv.key = rSQLID.id_investasi
        oInv = oInv.CastToLowestDescendant()
        if rSQLID.kode_jns_investasi == 'O' : #obligasi
          ProcessObligasi(config,oInv)
        else : #reksadana
          ProcessReksadana(config,oInv)
        rSQLID.Next()
      config.Commit()
    except :
      config.Rollback()
      raise
#main function
if len(sys.argv) < 3:
      raise 'argument error', 'UpdateTransaksiInvestasi.py <Config File>'
#
CONFIG_FILE = CONFIG_FOLDER + sys.argv[2]
config = dafsys.OpenConfig(CONFIG_FILE)
print 'Configuration File : %s' % CONFIG_FILE
MainFlow(config)
    
