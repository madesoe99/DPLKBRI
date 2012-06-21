import sys
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def ConstructReportHeader(config, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Rollover Deposito</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0; border-bottom-width:0px" bordercolor="#111111" border="1" width="1230" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="3" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3"><b>Dana Pensiun Lembaga \n')
  oFile.write('		Keuangan Muamalat</b></font><p align="center">\n')
  oFile.write('		<font size="3"><b>Rollover Deposito</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="3" style="border-style: none; border-width: medium">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('	</tr>\n')

def ConstructReportValues(config, no_bilyet, no_batch, kode_pihak_ketiga, nama_pihak_ketiga, kode_paket_investasi, tgl_transaksi, nominal, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">No. Bilyet</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ (no_bilyet or '&nbsp;') +'</font></font></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Batch Investasi</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ (no_batch or '&nbsp;') +'</font></font></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Pihak Ketiga</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  
  pihakKetiga = '%s/%s' % (kode_pihak_ketiga, nama_pihak_ketiga or '')
  
  oFile.write('		<font size="2">'+ (pihakKetiga or '&nbsp;') +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Paket Investasi</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ (kode_paket_investasi or '&nbsp;') +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Tanggal Transaksi</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  
  y, m, d = tgl_transaksi[:3]
  strTglTransaksi = '%d-%d-%d' % (d, m, y)
  
  oFile.write('		<font size="2">'+ strTglTransaksi +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Bagi Hasil</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, nominal) +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	</table>\n')

def ConstructReportTrailer(config, user_id, user_id_auth, oFile):
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0; border-bottom-width:0px" bordercolor="#111111" border="1" width="1230" id="table2" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="30%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		<font size="2">Pembuat</font></td>\n')
  oFile.write('		<td width="40%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		<font size="2">Pemeriksa</font></td>\n')
  oFile.write('		<td width="30%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		<font size="2">Otorisasi</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="30%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		&nbsp;<p>&nbsp;</p>\n')
  oFile.write('		<p>&nbsp;</p>\n')
  oFile.write('		<p>&nbsp;</td>\n')
  oFile.write('		<td width="40%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('		<td width="30%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="30%" style="border-style: none; border-width: medium" align="center">\n')
  
  oUserPembuat = config.CreatePObjImplProxy('UserApp')
  oUserPembuat.Key = user_id
  strPembuat = '....................................'
  if not oUserPembuat.IsNull:
    strPembuat = oUserPembuat.UserName or strPembuat
  
  oUserOtorisasi = config.CreatePObjImplProxy('UserApp')
  oUserOtorisasi.Key = user_id_auth
  strOtorisasi = '....................................'
  if not oUserOtorisasi.IsNull:
    strOtorisasi = oUserOtorisasi.UserName or strOtorisasi

  oFile.write('		<font size="2">('+ strPembuat +')</font></td>\n')
  oFile.write('		<font size="2">\n')
  oFile.write('		<td width="40%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		<font size="2">(....................................)</font></td>\n')
  oFile.write('		<td width="30%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		<font size="2">('+ strOtorisasi +')</font></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	</table>\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  sBaseFileName = 'rollover.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  oRolloverDeposito = config.CreatePObjImplProxy('RolloverDeposito')
  oRolloverDeposito.Key = parameter.FirstRecord.id

  ConstructReportHeader(
    config
    , oFile
  )

  ConstructReportValues(
    config
    , oRolloverDeposito.LDeposito.no_bilyet
    , oRolloverDeposito.LTransactionBatch.no_batch
    , oRolloverDeposito.LDeposito.LPihakKetiga.kode_pihak_ketiga
    , oRolloverDeposito.LDeposito.LPihakKetiga.nama_pihak_ketiga
    , oRolloverDeposito.LDeposito.kode_paket_investasi
    , oRolloverDeposito.tgl_transaksi
    , oRolloverDeposito.nominal
    , oFile
  )

  ConstructReportTrailer(
    config
    , oRolloverDeposito.user_id
    , oRolloverDeposito.user_id_auth
    , oFile
  )

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1

