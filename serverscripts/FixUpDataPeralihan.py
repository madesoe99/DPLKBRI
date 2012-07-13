import dafsys
import sys

def _fixupPeralihanDPLK(config):
  
  qTrans = config.CreateSQL("SELECT * FROM transaksidplk \
    WHERE (kode_jenis_transaksi IN ('I', 'O', 'P')) AND \
    (mutasi_iuran_pst <> 0 OR mutasi_iuran_pk <> 0 OR mutasi_pengembangan <> 0)")
  qResult = qTrans.RawResult
  while not qResult.Eof:
    id_transaksi = qResult.id_transaksi
    no_peserta = qResult.no_peserta
    tgl_transaksi = qResult.tgl_transaksi
    print "Proses transaksi pengalihan DPLK/DPPK/DPK atas nama ", no_peserta, \
      " tanggal: ", tgl_transaksi[2], tgl_transaksi[1], tgl_transaksi[0]
    mutasi_iuran_pst = qResult.mutasi_iuran_pst
    mutasi_iuran_pk = qResult.mutasi_iuran_pk
    mutasi_pengembangan = qResult.mutasi_pengembangan
    
    iRes = config.ExecSQL("UPDATE transaksidplk \
      SET mutasi_peralihan = mutasi_peralihan + mutasi_iuran_pst + mutasi_iuran_pk \
      + mutasi_pengembangan, mutasi_iuran_pst = 0, mutasi_iuran_pk = 0, mutasi_pengembangan = 0 \
      WHERE id_transaksi = %d " % (id_transaksi) 
    )
    if iRes < 0:
      raise Exception, 'DB Error' +  config.GetDBConnErrorInfo()
    oRekening = config.CreatePObjImplProxy("rekeningdplk")
    oRekening.key = no_peserta
    oRekening.akum_dana_iuran_pst = oRekening.akum_dana_iuran_pst - mutasi_iuran_pst
    oRekening.akum_dana_iuran_pk = oRekening.akum_dana_iuran_pk - mutasi_iuran_pk
    oRekening.akum_dana_pengembangan = oRekening.akum_dana_pengembangan - mutasi_pengembangan
    oRekening.akum_dana_peralihan = oRekening.akum_dana_peralihan + mutasi_iuran_pst + \
      mutasi_iuran_pk + mutasi_pengembangan
    config.FlushUpdates()
    qResult.Next()

def fixupPeralihanDPLK(config, errMsg):
  config.BeginTransaction()
  try:
    _fixupPeralihanDPLK(config)
    errMsg[0] = ""
    config.Commit()
    return 1
  except:
    errMsg[0] = str(sys.exc_info()[0]) + ":" + str(sys.exc_info()[1])
    config.Rollback()
    return 0

cfg = dafsys.OpenConfig("c:\\dafapp\\dplk07\\default.cfg")
sErr = [""]
if fixupPeralihanDPLK(cfg, sErr) == 0:
  print "error: ", sErr[0]
else:
  print "perbaikan data peralihan dari DPLK lain sukses !"


