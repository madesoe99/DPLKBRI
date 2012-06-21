import sys
import com.ihsan.util.modman as modman

def ConstructReportHeader(config, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Koreksi NAB</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0; border-bottom-width:0px" bordercolor="#111111" border="1" width="1230" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="3" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3"><b>Dana Pensiun Lembaga \n')
  oFile.write('		Keuangan Muamalat</b></font><p align="center">\n')
  oFile.write('		<font size="3"><b>Koreksi NAB</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="3" style="border-style: none; border-width: medium">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('	</tr>\n')

def ConstructReportValues(config, oReksadana, NAB, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">ID Reksadana</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ str(oReksadana.id_investasi) +'</font></font></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Nama Reksadana</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ (oReksadana.nama_reksadana or '&nbsp;') +'</font></font></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Pihak Ketiga</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')

  oPihakKetiga = config.CreatePObjImplProxy('PihakKetiga')
  oPihakKetiga.Key = oReksadana.kode_pihak_ketiga
  nama_pihak_ketiga = ''
  if not oPihakKetiga.IsNull:
    nama_pihak_ketiga = oPihakKetiga.nama_pihak_ketiga

  oFile.write('		<font size="2">'+ (nama_pihak_ketiga or '&nbsp;') +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Paket Investasi</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ (oReksadana.kode_paket_investasi or '&nbsp;') +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Custodian Bank</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  
  oCustodianBank = config.CreatePObjImplProxy('CustodianBank')
  oCustodianBank.Key = oReksadana.BankCode
  custodian_bank = ''
  if not oCustodianBank.IsNull:
    custodian_bank = oCustodianBank.BankName

  oFile.write('		<font size="2">'+ (custodian_bank or '&nbsp;') +'</font></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">Tanggal Koreksi NAB</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ config.FormatDateTime('d-m-yyyy', config.Now()) +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">NAB Pembelian</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, oReksadana.NAB_awal) +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">NAB Sebelumnya</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, oReksadana.NAB) +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">NAB Baru</td>\n')
  oFile.write('		<td width="1%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">:</td>\n')
  oFile.write('		<td width="84%" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, NAB) +'</font></td>\n')
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

def ConstructReportTrailer(config, user_id, oFile):
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

  oFile.write('		<font size="2">('+ strPembuat +')</font></td>\n')
  oFile.write('		<font size="2">\n')
  oFile.write('		<td width="40%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		<font size="2">(....................................)</font></td>\n')
  oFile.write('		<td width="30%" style="border-style: none; border-width: medium" align="center">\n')
  oFile.write('		<font size="2">(....................................)</font></td>\n')
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

  sBaseFileName = 'koreksi_nab.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  uipReksadana = parameter.GetDatasetByName('uipReksadana')
  rec = uipReksadana.GetRecord(0)

  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = rec.id_investasi

  ConstructReportHeader(
    config
    , oFile
  )

  ConstructReportValues(
    config
    , oReksadana
    , rec.NAB
    , oFile
  )

  ConstructReportTrailer(
    config
    , config.SecurityContext.UserID
    , oFile
  )

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1

