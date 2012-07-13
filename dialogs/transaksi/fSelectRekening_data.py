import com.ihsan.lib.remotequery as librq
                              
sSQLBoth = "SELECT ri.no_rekening, ns.nama_lengkap, ns.no_peserta FROM RekInvDPLK ri, NasabahDPLK ns WHERE ri.status_dplk = 'A' AND ri.no_peserta = ns.no_peserta AND ri.no_rekening='%(nomor_rekening)s' AND ns.nama_lengkap LIKE '%%%(nama_peserta)s%%' ORDER BY ri.no_rekening, ns.nama_lengkap"

sSQLRekening = "SELECT ri.no_rekening, ns.nama_lengkap, ns.no_peserta FROM RekInvDPLK ri, NasabahDPLK ns WHERE ri.status_dplk = 'A' AND ri.no_peserta = ns.no_peserta AND ri.no_rekening='%(nomor_rekening)s' ORDER BY ri.no_rekening, ns.nama_lengkap"

sSQLPeserta = "SELECT ri.no_rekening, ns.nama_lengkap, ns.no_peserta FROM RekInvDPLK ri, NasabahDPLK ns WHERE ri.status_dplk = 'A' AND ri.no_peserta = ns.no_peserta AND ns.nama_lengkap LIKE '%%%(nama_peserta)s%%' ORDER BY ri.no_rekening, ns.nama_lengkap"

def execQrySELECT(config, params, returns): # dummy handler when users click refresh / top button
  rq = librq.RQResult()
  rq.resultcode = librq.RTBLRES_NOCHANGE             
  rq.composeResult(returns)
#--

def searchRekening(config, params, returns):
  mlu = config.ModLibUtils
  rec = params.FirstRecord
  dParameterSQL = {'nomor_rekening':rec.nomorRekening,'nama_peserta':rec.namaPeserta}
  
  if "None" not in dParameterSQL.values():
    sSQL = sSQLBoth % dParameterSQL 
  elif dParameterSQL['nomor_rekening']!="None":
    sSQL = sSQLRekening % dParameterSQL
  elif dParameterSQL['nama_peserta']!="None":
    sSQL = sSQLPeserta % dParameterSQL
      
  rSQL = config.CreateSQL(sSQL).RawResult
  if not rSQL.Eof:
    #raise Exception, "Data not found"
    rq = librq.RQResult()
    rq.maxRow = 50
    rq.rawResult = rSQL
    rq.resultcode = librq.RTBLRES_NORMAL
    rq.composeResult(returns)
    
    errorStatus = 0
    errorMessage = ""
  else:
    # data not found
    errorStatus = 1
    errorMessage = "Data tidak ditemukan!"
  
  # pattern untuk catch status dan error
  ds = returns.AddNewDatasetEx("status", "has_more_data: integer; error_status: integer; error_message: string;")
  rec = ds.AddRecord()
  rec.has_more_data = not rSQL.Eof
  rec.error_status = errorStatus
  rec.error_message = errorMessage
#--
