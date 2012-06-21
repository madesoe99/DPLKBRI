import sys
import os

def ConstructHeader(config, params, oFile):
  oFile.write('<html>')
  oFile.write('')
  oFile.write('<head>')
  oFile.write('<meta http-equiv="Content-Language" content="en-us">')
  oFile.write('<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">')
  oFile.write('<title>Rincian transaksi giro DPLK</title>')
  oFile.write('<style>')
  oFile.write('<!--')
  oFile.write('body         { font-family: courier new; font-size: 8pt }')
  oFile.write('table        { font-size: 8pt }')
  oFile.write('th           { font-size: 8pt }')
  oFile.write('-->')
  oFile.write('</style>')
  oFile.write('</head>')
  oFile.write('')
  oFile.write('<body>')
  oFile.write('')
  oFile.write('<p><b><font size="4">Rincian</font><font size="4"> transaksi giro DPLK</font></b></p>')

  oGiro = config.CreatePObjImplProxy('MasterGiro')
  oGiro.Key = params.FirstRecord.GetFieldByName('giroDPLK.acc_giro')
  tgl = params.FirstRecord.tanggal
  oFile.write('<p><font size="2">No giro: %s <br>' % (oGiro.no_giro))
  oFile.write('Tanggal transaksi: %s</font></p>' % (config.FormatDateTime("dd mmm yyyy", tgl)) )
  oFile.write('<table border="1" width="100%" id="table1">')
  oFile.write('	<tr>')
  oFile.write('		<td width="146" align="center"><b>KIBLAT batch</b></td>')
  oFile.write('		<td align="center"><b>No urut</b></td>')
  oFile.write('		<td align="center"><b>Keterangan</b></td>')
  oFile.write('		<td align="center"><b>No_peserta</b></td>')
  oFile.write('		<td align="center"><b>Debet</b></td>')
  oFile.write('		<td align="center"><b>Kredit</b></td>')
  oFile.write('		<td align="center"><b>Settl_flag</b></td>')
  oFile.write('		<td align="center"><b>Keterangan Flag</b></td>')
  oFile.write('	</tr>')

def safeStr(libutils, sValue):
  if sValue == None:
    return '&nbsp;'
  else:
    return str(sValue)

def ConstructContent(config, sqlRes, oFile):
  libutils = config.ModLibUtils
  while not sqlRes.Eof:
    oFile.write('<tr>')
    oFile.write('<td>%s</td>' % (safeStr(libutils, sqlRes.nomor_batch_corebanking)))
    oFile.write('<td>%s</td>' % (safeStr(libutils, sqlRes.nomor_urut)) )
    oFile.write('<td>%s</td>' % (safeStr(libutils, sqlRes.keterangan)) )
    oFile.write('<td>%s</td>' % (safeStr(libutils, sqlRes.nomor_peserta)) )
    if sqlRes.kode_mnemonic == 'C':
      oFile.write('<td>%s</td>' % (safeStr(libutils, None )) )
      oFile.write('<td align="right">%s</td>' % (safeStr(libutils, config.FormatFloat(",0.00", sqlRes.nominal) )) )
    else:
      oFile.write('<td align="right">%s</td>' % (safeStr(libutils, config.FormatFloat(",0.00", sqlRes.nominal) )) )
      oFile.write('<td>%s</td>' % (safeStr(libutils, None )) )   		
    oFile.write('<td>%s</td>' % (safeStr(libutils, sqlRes.IsTransaksiCreated)) )
    oFile.write('<td>%s</td>' % (safeStr(libutils, GetFlagDescription(config, sqlRes))) )
    oFile.write('</tr>')
    sqlRes.Next()

def GetFlagDescription(config, sqlRes):
  description = ''
  if sqlRes.IsTransaksiCreated == 'F':
    if sqlRes.kode_mnemonic <> 'C':
      description = 'Transaksi debet'
    elif sqlRes.nomor_peserta in [None, '', ' ']:
      description = 'Nomor peserta kosong'
    elif sqlRes.transaksi_peserta == 1:
      description = 'Transaksi dr aplikasi DPLK baru'
    else:
      description = CekRekening(config, sqlRes.nomor_peserta)

  return description
    
def CekRekening(config, no_peserta):
  description = ''
  oRek = config.CreatePObjImplProxy('RekeningDPLK')
  oRek.key = no_peserta
  if oRek.IsNull:
    description = 'Rekening tidak terdaftar'
  else:
    if oRek.Status_DPLK <> 'A':
      description = 'Rekening tidak aktif'
    elif oRek.tgl_pensiun <= config.Now():
      description = 'Peserta sudah masuk usia pensiun'
  
  return description


def ConstructTail(config, oFile):
  oFile.write('</table></body>')
  oFile.write('</html>')

def WriteToFile(config, params, sqlRes, oFile):
  ConstructHeader(config, params, oFile)
  ConstructContent(config, sqlRes, oFile)
  ConstructTail(config, oFile)

def createReport(config, params, returns):
  # prepare data
  tgl = params.FirstRecord.tanggal
  #tgl = config.ModLibUtils.EncodeDate(tgl[0], tgl[1], tgl[2])
  
  sSQL = \
    "SELECT nomor_batch_corebanking, nomor_urut, transaksi_peserta,\
    keterangan, nomor_peserta, kode_mnemonic, nominal, istransaksicreated \
    FROM historigiro a, historigiroharian b WHERE \
    a.id_historigiroharian = b.id_historigiroharian \
    AND b.tanggal_histori = %s AND b.acc_giro = %s \
    ORDER BY nomor_urut" % \
    ( \
      config.FormatDateTimeForQuery(tgl), \
      config.ModLibUtils.QuotedStr(params.FirstRecord.GetFieldByName("giroDPLK.acc_giro")) \
    )
    
  sqlStat = config.CreateSQL(sSQL)
  sqlRes = sqlStat.RawResult

  # prepare file
  sBaseFileName = 'histori_giro.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')
  
  # generate report
  WriteToFile(config, params, sqlRes, oFile)
  oFile.close()
  
  # pack as stream
  sw = returns.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

  return 1
