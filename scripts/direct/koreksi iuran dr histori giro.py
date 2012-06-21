import sys, dafsys

def RunSQL(config, sSQL):
  i = config.ExecSQL(sSQL)
  if i == -9999:
    raise 'SQL Error', config.GetDBConnErrorInfo()
  
def CreateResultSet(config):
  sSQL = "select * from transaksidplk a \
          where tgl_transaksi = '08/04/2009' \
          and terminal_id = '193.6.1.103' \
          and keterangan = 'Transaksi dibuat dari Transaksi-Histori-Giro DPLK' \
          and exists \
          (select 1 \
          from historigiro hg, historigiroharian hgh \
          where hg.id_historigiroharian = hgh.id_historigiroharian \
          and tanggal_histori >= '08/04/2009' \
          and istransaksicreated = 'T' \
          and a.no_peserta = nomor_peserta \
          and a.mutasi_iuran_pst = nominal)"
  rSQL = config.CreateSQL(sSQL).RawResult
  
  return rSQL

def HapusTransaksiDPLK(config, id_transaksi):
  sSQL = "delete from transaksidplk \
          where id_transaksi = %s" % id_transaksi
  RunSQL(config, sSQL)

def Koreksi(config):
  rSQL = CreateResultSet(config)
  rSQL.First()
  i = 1
  while not rSQL.Eof:
    print str(i)+'-'+rSQL.No_Peserta
    oRek = config.CreatePObjImplProxy('RekeningDPLK')
    oRek.key = rSQL.No_Peserta
    oRek.akum_dana_iuran_pst = oRek.akum_dana_iuran_pst - rSQL.mutasi_iuran_pst
    HapusTransaksiDPLK(config, rSQL.id_transaksi)      
    i += 1
    rSQL.Next()    
  
def DoKoreksi(config):
  config.BeginTransaction()
  try:
    Koreksi(config)
    config.Commit()
  except:
    config.Rollback()
    raise str(sys.exc_info()[0]) + '.' + str(sys.exc_info()[1])
  
if __name__ == '__main__':
  config = dafsys.openConfig('c:/dafapp/dplk07/default.cfg')
  DoKoreksi(config)
