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

def FormBeginSetData(uideflist, uipMaster, key):
  config = uideflist.config
  
  #inisialisasi
  keepGoingProcess = 1

  #checking riwayat pindah paket investasi peserta selama periode pindah paket
  try:
    #ambil no_peserta
    idStr = string.split(key,'#')[1]
    keyName, keyVal = string.split(idStr,'=')
    #config.SendDebugMsg(key)
    if keyName == 'REGISTERCIF_ID':
      #registercif_id = string.split(key,'=')[1]
      oRegisterCIF = config.CreatePObjImplProxy('RegisterCIF')
      oRegisterCIF.Key = keyVal
      noPeserta = oRegisterCIF.no_peserta
      noRekening = oRegisterCIF.no_rekening      
      
      #pobjconst = "PObj:RekInvDPLK#NO_REKENING=%s" % noRekening
      #uideflist.SetData('uipMaster', pobjconst)
    elif keyName == 'NO_REKENING':
      noRekening = keyVal
      #if uideflist.uipMaster.Dataset.RecordCount > 0:
        #rec = uideflist.uipMaster.Dataset.GetRecord(0)
        #noPeserta = rec.no_peserta
      #else:
        #raise Exception, '\n\n\PERINGATAN!\nData lama tidak ditemukan...'
        #pass
    else:
      raise Exception, '\n\nKesalahan Proses Pindah Paket\nKey %s tidak terdefinisi.' % (str(keyName))
    
    #ambil parameter pindah paket investasi (periode dan maks pindah)
    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'PERIODE_PINDAH_PAKET_INVESTASI'
    periodePindahPaket = int(oP.Numeric_Value)
    
    ## Sementara di tutup BY ade herman 2011-07-25
    ## Karena tidak ada batasan dalam 1 tahun takwim
    #oP.Key = 'MAKS_PINDAH_PAKET_INVESTASI'
    maksPindahPaket = 0 #int(oP.Numeric_Value)
    ##  End 2011-07-25
    
    oP.Key = 'MIN_KEPESERTAAN_PINDAH_PAKET'
    minMasaKepesertaan = int(oP.Numeric_Value)

    # periksa masa kepesertaan minimum untuk boleh pindah paket
    oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
    oNasabahDPLK.Key = noPeserta
    y, m, d = oNasabahDPLK.tgl_registrasi[:3]
    dtTglRegistrasi = config.ModLibUtils.EncodeDate(y, m, d)
    '''if (config.Now() - dtTglRegistrasi) < minMasaKepesertaan:
      #masa kepesertaan belum mencukupi untuk boleh pindah paket
      #prosesi pindah paket tidak boleh dilanjutkan
      raise '\nPERINGATAN!','Peserta belum mencapai masa kepesertaan minimum.'
      keepGoingProcess = 0'''

    ## Tambahan By ade herman 2011-07-25
    yearNow = config.FormatDateTime('yyyy', config.Now())
    config.SendDebugMsg('year...... : '+str(yearNow))
    ## end By ade herman

    #ambil pindah paket terakhir
    #sSQL = 'select top %d hppi.TANGGAL_HISTORI from HISTORIPINDAHPAKETINVESTASI hppi ' \
    #  'where hppi.NO_PESERTA = \'%s\' '\
    #  '  and datepart(year,hppi.tanggal_histori) = \'%s\' '\
    #  'order by hppi.TANGGAL_HISTORI DESC' \
    #  % (maksPindahPaket, noPeserta, yearNow)
    
    sSQL = 'select hppi.TANGGAL_HISTORI from HISTORIPINDAHPAKETINVESTASI hppi ' \
      'where hppi.no_rekening = \'%s\' '\
      '  and datepart(year,hppi.tanggal_histori) = \'%s\' '\
      'order by hppi.TANGGAL_HISTORI DESC' \
      % ( noRekening, yearNow)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    config.SendDebugMsg('rSQL : '+ sSQL )
    
    #secara otomatis bila maksPindahPaket == 0 maka rSQL akan Eof
    if not rSQL.Eof:
      rSQL.First()
      dtTglTerakhir = config.ModLibUtils.EncodeDate(rSQL.tanggal_histori[0],\
        rSQL.tanggal_histori[1],rSQL.tanggal_histori[2])

      config.SendDebugMsg('Masukkkkkkkkkk')
      if config.ModLibUtils.Now() - dtTglTerakhir < periodePindahPaket:
         raise Exception,'\n\n\nPERINGATAN!\nPeriode Pindah Paket Investasi '\
            ' tidak di perkenankan, karena belum genap 1 bulan (31 hari)'
         keepGoingProcess = 0
         
    recP = uideflist.uipParameter.Dataset.AddRecord()
    tglPakai = time.localtime()[:3]
    recP.TanggalPakai = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
      string.zfill(str(tglPakai[2]),2),tglPakai[0])
      
    config.SendDebugMsg('end')

  except:
    raise

  return keepGoingProcess

def FormOnEndSetData(uideflist, uiname, pobjconst):
  # procedure(uideflist: TPClassUIDefList; uiname, pobjconst: string)
  config = uideflist.Config

  config.SendDebugMsg('FormEndSetData1')
  '''try:
    #checking status dplk peserta
    config.SendDebugMsg(auiname)
    uiCalled = uideflist.GetPClassUIByName(auiname)
    rec = uiCalled.ActiveRecord
    no_peserta = uiCalled.ActiveRecord.no_peserta
      
    moduleapi.IsPesertaAktif(config, no_peserta)
                   
    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    if uideflist.uipMaster.Dataset.RecordCount > 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'P')
  except:
    raise'''

  #set TanggalPakai untuk OQL batch transaksi
  recP = uideflist.uipParameter.Dataset.AddRecord()
  tglPakai = time.localtime()[:3]
  recP.TanggalPakai = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])
  config.SendDebugMsg('FormEndSetData2')
    
def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config

  if oData.no_referensi in ['', None]:
    raise Exception,'\n\nRegistrasi Error\nNomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()
