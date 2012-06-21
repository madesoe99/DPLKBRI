import sys
import com.ihsan.util.modman as modman

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  sBaseFileName = 'bagi_hasil.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  bagihasil.ConstructReportHeader(
    config
    , oFile
  )

  bagihasil = modman.getModule(config, 'bagihasil')
  bagihasil.ConstructReportValues(
    config
    , parameter.FirstRecord.no_bilyet
    , parameter.FirstRecord.no_batch
    , parameter.FirstRecord.kode_pihak_ketiga
    , parameter.FirstRecord.nama_pihak_ketiga
    , parameter.FirstRecord.kode_paket_investasi
    , config.ModDateTime.DecodeDate(parameter.FirstRecord.tgl_transaksi)
    , parameter.FirstRecord.nominal
    , oFile
  )

  bagihasil.ConstructReportTrailer(
    config
    , parameter.FirstRecord.user_id
    , None
    , oFile
  )

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1
