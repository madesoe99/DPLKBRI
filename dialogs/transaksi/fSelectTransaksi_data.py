import com.ihsan.lib.remotequery as librq
                              
def execQrySELECT(config, params, returns): # dummy handler when users click refresh / top button
  rq = librq.RQResult()
  rq.resultcode = librq.RTBLRES_NOCHANGE             
  rq.composeResult(returns)
#--

def Form_OnSetDataEx(uideflist, params):
  config = uideflist.config
  uipFilter = uideflist.uipFilter

  recFilter = uipFilter.Dataset.AddRecord()
  recFilter.cbAllCabang = 0
  recFilter.cbAllTransaksi = 0
  recFilter.cbStatusOtorisasi = 'A'
  #recFilter.Metode = 'A'
  recFilter.eAwalTanggal = config.ModLibUtils.Now()
  recFilter.eHinggaTanggal = config.ModLibUtils.Now()
    
  return 0
#--

def searchTransaksi(config, params, returns):
  mlu = config.ModLibUtils
  rec = params.FirstRecord
  dParameterSQL = {'nomor_rekening':rec.nomorRekening,'nama_peserta':rec.namaPeserta}
  
  sSQL = \
  "SELECT \
  FROM \
    TransaksiDPLK \
  WHERE \
    (1=%d OR ) AND "
      
  rSQL = config.CreateSQL(sSQL).RawResult
  if not rSQL.Eof:
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