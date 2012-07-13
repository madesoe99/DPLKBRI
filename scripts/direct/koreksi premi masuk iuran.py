import sys, dafsys

def RunSQL(config, sSQL):
  i = config.ExecSQL(sSQL)
  if i == -9999:
    raise Exception, 'SQL Error' +  config.GetDBConnErrorInfo()
  
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
          and hg.acc_giro = 11210 \
          and istransaksicreated = 'T' \
          and a.no_peserta = nomor_peserta \
          and a.mutasi_iuran_pst = nominal)"
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
    oTransaksi = config.CreatePObject('TitipanPremi')        
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
    oTransaksi.isDebet = 'F'
    oTransaksi.mutasi_premi = rSQL.mutasi_iuran_pst
    
    oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
    oRekeningDPLK.key = oTransaksi.no_peserta 
    SetKolektibilitasWasiatUmmat(config, oRekeningDPLK, oTransaksi)
    ResetAkumDanaRekeningDPLK(oTransaksi, oRekeningDPLK)
    HapusTransaksiDPLK(config, rSQL.id_transaksi)
    
    i += 1
    rSQL.Next()    
  
def GetRekeningWasiatUmmat(config, no_peserta):
  strSQL = \
    'select rekeningwasiatummat_id '\
    'from RekeningWasiatUmmat '\
    'where no_peserta = \'%s\'; '\
    % (no_peserta)
  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()
  if resSQL.Eof:
    return None
    
  oRekeningWasiatUmmat = config.CreatePObjImplProxy('RekeningWasiatUmmat')
  oRekeningWasiatUmmat.Key = resSQL.rekeningwasiatummat_id 
 
  return oRekeningWasiatUmmat

def SetKolektibilitasWasiatUmmat(config, oRekeningDPLK, oTransaksi):
  oRWU = GetRekeningWasiatUmmat(config, oRekeningDPLK.no_peserta)
  if oRWU <> None:
      selisihNominal = oTransaksi.mutasi_premi - oRWU.besar_premi

      if selisihNominal > 0.0:
        if oRekeningDPLK.kewajiban_wasiat_ummat > 0.0:
          sisaKewajiban = oRekeningDPLK.kewajiban_wasiat_ummat - selisihNominal
          if sisaKewajiban > 0.0:
            oRekeningDPLK.kewajiban_wasiat_ummat = sisaKewajiban          
          else: 
            oRekeningDPLK.kewajiban_wasiat_ummat = 0.0

      if oRekeningDPLK.kewajiban_wasiat_ummat > 0.0:
        oRekeningDPLK.collectivity_wasiat_ummat = 'F'
      else:
        oRekeningDPLK.collectivity_wasiat_ummat = 'T'

def ResetAkumDanaRekeningDPLK(oTransaksi, oRekeningDPLK):
    oRekeningDPLK.akum_dana_iuran_pst = oRekeningDPLK.akum_dana_iuran_pst - oTransaksi.mutasi_premi
    
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
