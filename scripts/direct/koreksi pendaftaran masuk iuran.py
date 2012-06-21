import sys, dafsys

def RunSQL(config, sSQL):
  i = config.ExecSQL(sSQL)
  if i == -9999:
    raise 'SQL Error', config.GetDBConnErrorInfo()
  
def CreateResultSet(config):
  sSQL = "select * from transaksidplk a \
          where tgl_transaksi >= '07/07/2009' \
          and tgl_transaksi < '08/01/2009' \
          and keterangan = 'Transaksi dibuat dari Transaksi-Histori-Giro DPLK' \
          and exists \
          (select 1 \
          from historigiro hg, historigiroharian hgh \
          where hg.id_historigiroharian = hgh.id_historigiroharian \
          and tanggal_histori >= '07/07/2009' \
          and tanggal_histori < '08/01/2009' \
          and hg.acc_giro = 11206 \
          and istransaksicreated = 'T' \
          and a.no_peserta = nomor_peserta \
          and a.mutasi_iuran_pst = nominal)\
          and a.mutasi_iuran_pst = 10000"
          
  rSQL = config.CreateSQL(sSQL).RawResult
  
  return rSQL

def HapusTransaksiDPLK(config, id_transaksi):
  sSQL = "delete from transaksidplk \
          where id_transaksi = %s" % id_transaksi
  RunSQL(config, sSQL)
  
def CreateTransaksiPremi(config):
  rSQL = CreateResultSet(config)
  rSQL.First()
  i = 1
  while not rSQL.Eof:
    print str(i)+'-'+rSQL.No_Peserta
    oTransaksi = config.CreatePObject('IuranPendaftaran')        
    oTransaksi.ID_TransactionBatch = rSQL.ID_TransactionBatch
    oTransaksi.no_peserta = rSQL.No_Peserta
    oTransaksi.branch_code = rSQL.branch_code    
    oTransaksi.user_id = oTransaksi.user_id_auth = rSQL.user_id
    oTransaksi.terminal_id = oTransaksi.terminal_id_auth = rSQL.terminal_id
    y,m,d = rSQL.tgl_transaksi[:3]
    oTransaksi.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)
    y1,m1,d1 = rSQL.tgl_sistem[:3]
    oTransaksi.tgl_sistem = oTransaksi.tgl_otorisasi = config.ModLibUtils.EncodeDate(y1,m1,d1)
    oTransaksi.keterangan = rSQL.keterangan
    oTransaksi.IsCommitted = 'T'
    oTransaksi.besar_biaya_daftar = rSQL.mutasi_iuran_pst
    
    oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
    oRekeningDPLK.key = oTransaksi.no_peserta     
    
    ResetRekeningDPLK(oTransaksi, oRekeningDPLK)
    HapusTransaksiDPLK(config, rSQL.id_transaksi)
    
    i += 1
    rSQL.Next()    
  
def ResetRekeningDPLK(oTransaksi, oRekeningDPLK):
    oRekeningDPLK.akum_dana_iuran_pst = oRekeningDPLK.akum_dana_iuran_pst - oTransaksi.besar_biaya_daftar
    oRekeningDPLK.status_biaya_daftar = 'T'
    
def DoKoreksi(config):
  config.BeginTransaction()
  try:
    CreateTransaksiPremi(config)
    config.Commit()
  except:
    config.Rollback()
    raise str(sys.exc_info()[0]) + '.' + str(sys.exc_info()[1])
  
if __name__ == '__main__':
  config = dafsys.openConfig('c:/dafapp/dplk07/default.cfg')
  DoKoreksi(config)
