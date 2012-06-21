import string, sys, dafsys, calendar, time

def Proses(config):
  tgl = config.FormatDateTime('mm/dd/yyyy', config.Now()+1)
  sSQL = "select * from DEPOSITO d, INVESTASI i \
          where d.ID_INVESTASI = i.ID_INVESTASI \
          and STATUS = 'T' \
          and TGL_JATUH_TEMPO < '%s'" % tgl
  print sSQL
  rSQL = config.CreateSQL(sSQL).RawResult
  rSQL.First()
  while not rSQL.Eof:
    tjt = rSQL.tgl_jatuh_tempo; tbk = rSQL.tgl_buka
    print 'no depo:', rSQL.rekening_deposito, 'tgl_buka:', config.FormatDateTime('dd/mm/yyyy', config.ModLibUtils.EncodeDate(tbk[0],tbk[1],tbk[2])), 'tgl jt lama:', config.FormatDateTime('dd/mm/yyyy', config.ModLibUtils.EncodeDate(tjt[0],tjt[1],tjt[2]))
    tgljt_baru = GetTanggalJatuhTempo(config, rSQL.tgl_buka, rSQL.jenisjatuhtempo, rSQL.jmlharioncall)
    UpdateTanggalJatuhTempo(config, rSQL.id_investasi, tgljt_baru)
    rSQL.Next()

def GetTanggalJatuhTempo(config, tgl_buka, jarak, jml_hari_oncall):
  tgljt = tgl_buka
  tgljt_dt = config.ModLibUtils.EncodeDate(tgljt[0],tgljt[1],tgljt[2])
  while tgljt_dt < config.Now():
    if jarak > 0:
      tgljt_dt = config.ModLibUtils.IncMonth(tgljt_dt, jarak)
      d_tgl_buka = tgl_buka[2]
      if d_tgl_buka > 28:
          tgljt_dt = config.ModLibUtils.DecodeDate(tgljt_dt)
          aMax = calendar.monthrange(tgljt_dt[0], tgljt_dt[1])[1]
          if d_tgl_buka > aMax:
              d_tgl_buka = aMax
          #-- if            
          tgljt_dt = config.ModLibUtils.EncodeDate(tgljt_dt[0], tgljt_dt[1], d_tgl_buka)  
          
#       print 'tgl JT:', config.FormatDateTime('dd/mm/yyyy', tgljt_dt)
    else: # deposito on call
      tgljt_dt = tgljt_dt + jml_hari_oncall
      
  print 'tgl JT baru :', config.FormatDateTime('dd/mm/yyyy', tgljt_dt)
  return config.FormatDateTime('mm/dd/yyyy', tgljt_dt)
  
def UpdateTanggalJatuhTempo(config, id_investasi, tgljt_baru):
  sSQL = "UPDATE deposito SET tgl_jatuh_tempo = '%s'\
  WHERE id_investasi = %s" % (tgljt_baru, id_investasi)
  config.BeginTransaction()
  try:
    runSQL(config, sSQL)
    config.Commit()
  except:
    config.Rollback()
    raise str(sys.exc_info()[1])
    
def runSQL(config, sSQL):
  print 'SQL:> \n', sSQL
  t1 = time.clock()
  if config.ExecSQL(sSQL) < 0:
    raise 'runSQL', config.GetDBConnErrorInfo()
  t2 = time.clock()
  
  print '>>... %.8f seconds\n' % (t2-t1)
    
#-- MAIN
if __name__ == '__main__':
  config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
  Proses(config)
    
