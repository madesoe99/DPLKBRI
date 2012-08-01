import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver
import com.ihsan.lib.remotequery as librq

#import rpdb2; rpdb2.start_embedded_debugger('solusi', True, True)

def execQrySELECT(config, params, returns): # dummy handler when users click refresh / top button
  rq = librq.RQResult()
  rq.resultcode = librq.RTBLRES_NOCHANGE             
  rq.composeResult(returns)
#--

def searchRekeningDPLK(config, params, returns):
  mlu = config.ModLibUtils
  rec = params.FirstRecord
  dParameterSQL = {'no_peserta' : rec.no_peserta}
  
  sSQL = """
    SELECT 
      rd.No_Rekening,
      rd.Kode_Paket_Investasi, 
      rd.Pct_Alokasi,
      rd.Akum_Iuran_PK,
      rd.Akum_Iuran_PST,
      rd.Akum_Iuran_TMB,
      rd.Akum_PSL,
      rd.Akum_Pmb_PK,
      rd.Akum_Pmb_PST,
      rd.Akum_Pmb_TMB,
      rd.Akum_Pmb_PSL
    FROM 
      RekInvDPLK ri
      INNER JOIN RekeningDPLK rd ON rd.no_rekening = ri.no_rekening
    WHERE
      ri.no_peserta = '%(no_peserta)s'
    ORDER BY
      rd.no_rekening ASC, 
      rd.kode_paket_investasi ASC
    """ \
    % dParameterSQL
      
  rSQL = config.CreateSQL(sSQL).RawResult
  if not rSQL.Eof:
    #raise Exception, "Data not found"
    rq = librq.RQResult()
    rq.maxRow = 20
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

def OnSetDataEx(uideflist, params):
  config = uideflist.Config           
  lsKey = str(params.FirstRecord.key).split('=')
  
  uideflist.SetData('uipNasabahDPLK', params.FirstRecord.key)
  
  