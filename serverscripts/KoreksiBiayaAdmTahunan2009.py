import string, sys, dafsys
sys.path.append('c:/dafapp/dplk07/script_modules')
import transaksiapi

def DoKoreksi(config):
  config.BeginTransaction()
  try:
    sSQL = "select a.no_peserta, mutasi_iuran_pk, mutasi_iuran_pst, \
            mutasi_pengembangan, mutasi_peralihan\
            from transaksidplk a, nasabahdplk b\
            where a.no_peserta = b.no_peserta\
            and kode_jenis_transaksi = 'D'\
            and tgl_transaksi = '12/31/2009'\
            and tgl_registrasi >= '02/01/2009'\
            and tgl_registrasi < '07/01/2009'"
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First(); i = 1
    while not rSQL.Eof:
      print 'data ke-',i,': ',rSQL.no_peserta
      CreateTransaksiReverse(config, rSQL)
      CreateTransaksiBiaya(config, rSQL)
      rSQL.Next(); i += 1
    config.Commit()
  except:
    config.Rollback()
    raise 'Error', str(sys.exc_info()[1])

def CreateTransaksiReverse(config, rSQL):
  o = config.CreatePObject('TransaksiDPLKManual')
  o.tgl_transaksi = '02/22/2010'
  o.no_peserta = rSQL.no_peserta
  o.kode_transaksi_manual = 'M'
  o.keterangan = 'KOREKSI BIAYA PENGELOLAAN 2009'
  o.mutasi_iuran_pk = -rSQL.mutasi_iuran_pk
  o.mutasi_iuran_pst = -rSQL.mutasi_iuran_pst
  o.mutasi_pengembangan = -rSQL.mutasi_pengembangan
  o.mutasi_peralihan = -rSQL.mutasi_iuran_pk
  o.ID_TransactionBatch = 170291 
  o.branch_code = '311'
  o.user_id = 'ADE HERMAN'
  o.terminal_id = '193.6.1.105'
  o.tgl_sistem = config.Now()   
  transaksiapi.SetPaketInvestasi(config, o)
  
  o.isCommitted = 'T'
  o.user_id_auth = 'ADE HERMAN'
  o.terminal_id_auth = '193.6.1.105'
  o.tgl_otorisasi = config.Now()      

  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.Key = o.no_peserta
  oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk + o.mutasi_iuran_pk
  oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + o.mutasi_iuran_pst
  oR.akum_dana_pengembangan = oR.akum_dana_pengembangan + o.mutasi_pengembangan
  oR.akum_dana_peralihan = oR.akum_dana_peralihan + o.mutasi_peralihan     

def CreateTransaksiBiaya(config, rSQL):
  o = config.CreatePObject('TransaksiDPLKManual')
  o.tgl_transaksi = '02/22/2010'
  o.no_peserta = rSQL.no_peserta
  o.kode_transaksi_manual = 'M'
  o.keterangan = 'KOREKSI BIAYA PENGELOLAAN 2009'
  o.mutasi_iuran_pk = 0
  o.mutasi_iuran_pst = 0
  o.mutasi_pengembangan = -9000
  o.mutasi_peralihan = 0
  o.ID_TransactionBatch = 170291 
  o.branch_code = '311'
  o.user_id = 'ADE HERMAN'
  o.terminal_id = '193.6.1.105'
  o.tgl_sistem = config.Now()   
  transaksiapi.SetPaketInvestasi(config, o)
  
  o.isCommitted = 'T'
  o.user_id_auth = 'ADE HERMAN'
  o.terminal_id_auth = '193.6.1.105'
  o.tgl_otorisasi = config.Now()      

  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.Key = o.no_peserta
  oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk + o.mutasi_iuran_pk
  oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + o.mutasi_iuran_pst
  oR.akum_dana_pengembangan = oR.akum_dana_pengembangan + o.mutasi_pengembangan
  oR.akum_dana_peralihan = oR.akum_dana_peralihan + o.mutasi_peralihan     
    
config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
DoKoreksi(config)
    
