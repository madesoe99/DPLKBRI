import sys, time, string
#sys.path.append('c:/dafapp/dplk07/script_modules/')
#import moduleapi
#import rpdb2; rpdb2.start_embedded_debugger("000")

import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

modman.loadStdModules(globals(),
  [
    "moduleapi"
  ]
)

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  try:
    uiCalled = uideflist.GetPClassUIByName(auiname)
    rec = uiCalled.ActiveRecord
    if auiname == 'uipMaster':
      no_peserta = uiCalled.ActiveRecord.no_peserta
      no_rekening = uiCalled.ActiveRecord.no_rekening
    else:
      no_peserta = uiCalled.ActiveRecord.GetFieldByName('LNasabahDPLK.no_peserta')
      no_rekening = uiCalled.ActiveRecord.GetFieldByName('LRekeningDPLK.no_rekening')
      
      keyRekInvDPLK = "PObj:RekInvDPLK#no_rekening=%s" % no_rekening
      uideflist.SetData('uipMaster', keyRekInvDPLK)
    
    moduleapi.IsPesertaAktif(config, no_peserta)
    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    
    uipRegisterCIF = uideflist.GetPClassUIByName("uipRegisterCIF")
    if uipRegisterCIF.DataSet.RecordCount == 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'P', no_rekening)
      
    """ambil parameter pindah paket investasi (periode dan maks pindah)"""
    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'PERIODE_PINDAH_PAKET_INVESTASI'
    periodePindahPaket = int(oP.Numeric_Value)

    """batasan pindah paket investasi"""    
    oP.Key = 'MAKS_PINDAH_PAKET_INVESTASI'
    maksPindahPaket = int(oP.Numeric_Value)
    
    """minimum kepesertaan pindah paket"""
    oP.Key = 'MIN_KEPESERTAAN_PINDAH_PAKET'
    minMasaKepesertaan = int(oP.Numeric_Value)

    """periksa masa kepesertaan minimum untuk boleh pindah paket"""
    oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
    oNasabahDPLK.Key = no_peserta
    y, m, d = oNasabahDPLK.tgl_registrasi[:3]
    dtTglRegistrasi = config.ModLibUtils.EncodeDate(y, m, d)
    if (config.Now() - dtTglRegistrasi) < minMasaKepesertaan:
      raise Exception,'\n\nPERINGATAN!\nPeserta belum mencapai masa kepesertaan minimum.'

    yearNow = config.FormatDateTime('yyyy', config.Now())

    sSQL = """
      SELECT hppi.TANGGAL_HISTORI
      FROM   HISTORIPINDAHPAKETINVESTASI hppi
      WHERE  hppi.no_rekening = '%s'
             AND DATEPART(year,hppi.tanggal_histori) = '%s'
      ORDER BY hppi.TANGGAL_HISTORI DESC
    """ % (no_rekening, yearNow)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    if maksPindahPaket > 0:
      if not rSQL.Eof:
        rSQL.First()
        dtTglTerakhir = config.ModLibUtils.EncodeDate(rSQL.tanggal_histori[0],\
          rSQL.tanggal_histori[1],rSQL.tanggal_histori[2])
  
        if config.ModLibUtils.Now() - dtTglTerakhir < periodePindahPaket:
           raise Exception, """
             \nPERINGATAN!
             Periode Pindah Paket Investasi tidak di perkenankan, 
             karena belum genap 1 bulan (31 hari)"""      

    if auiname == 'uipMaster':
      sSQL = "SELECT * FROM paketinvestasi"
      rSQL = config.CreateSQL(sSQL).RawResult
      while not rSQL.Eof:
        recTmpPI = uideflist.uipTmpPaket.Dataset.AddRecord()
        recTmpPI.kode_pi = rSQL.kode_paket_investasi
        recTmpPI.nama_pi = rSQL.nama_paket_investasi
        rSQL.Next()

  except:
    raise Exception, str(sys.exc_info()[1])

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config

  if oData.no_referensi in ['', None]:
    raise Exception,'\n\nRegistrasi Error\nNomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()
