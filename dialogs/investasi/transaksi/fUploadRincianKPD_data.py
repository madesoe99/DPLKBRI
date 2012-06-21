import pyFlexcel
import com.ihsan.fileutils as fileutils
import sys

def ResetDataRincian(config, tanggal):
  sSQL = "DELETE FROM RINCIANKPD \
  WHERE tanggal_upload = '%s'" % tanggal
  config.ExecSQL(sSQL)

def ProsesUpload(config, params, returns):
    Is_Err = 0
    Err_Msg = ''
    config.BeginTransaction()
    try:
      recT = params.FirstRecord
      id_investasi = recT.id_investasi
      config.SendDebugMsg('aa')
      sw = params.GetStreamWrapperByName("fileupload")
      if sw == None:
        raise "Stream not found"

      sourceFilename  = config.UserHomeDirectory + fileutils.ExtractFileName(recT.filename)
      
      sw.SaveToFile(sourceFilename)

      config.SendDebugMsg('bb')
      
      book = pyFlexcel.Open(sourceFilename)
      i = 2 #baris mulai data
      config.SendDebugMsg('dd')
      kode_kpd = str(book.GetCellValue(i, 1) or '').strip().split('.')[0]
      tanggal = str(book.GetCellValue(i, 2) or '').strip().split('.')[0]
      ResetDataRincian(config, tanggal)
      
      while str(book.GetCellValue(i, 1) or '').strip().split('.')[0] != '':
        oRincian = config.CreatePObject('RincianKPD')
        oRincian.id_investasi = id_investasi
        oRincian.kode_KPD = str(book.GetCellValue(i, 1) or '').strip().split('.')[0]
        oRincian.tanggal_upload = str(book.GetCellValue(i, 2) or '').strip().split('.')[0]
        oRincian.kode_saham = str(book.GetCellValue(i, 3) or '').strip().split('.')[0]
        oRincian.nama_saham = str(book.GetCellValue(i, 4) or '').strip().split('.')[0]
        oRincian.sektoral = str(book.GetCellValue(i, 5) or 0)
        oRincian.sec_ISIN = str(book.GetCellValue(i, 6) or '').strip().split('.')[0]
        oRincian.holding = float(book.GetCellValue(i, 7) or 0.0)
        oRincian.market_price = float(book.GetCellValue(i, 8) or 0.0)
        oRincian.accrued_interest = float(book.GetCellValue(i, 9) or 0.0)
        
        i += 1

      config.Commit()
    except:
      config.Rollback()
      Is_Err = 1
      Err_Msg = str(sys.exc_info()[1])

    returns.CreateValues(
      ['Is_Err', Is_Err]
      , ['Err_Msg', Err_Msg]
    )

