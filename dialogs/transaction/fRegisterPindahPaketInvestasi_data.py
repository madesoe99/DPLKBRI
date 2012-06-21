import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

#sys.path.append('c:/dafapp/dplk/script_modules/')
#import moduleapi

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')
#import rpdb2; rpdb2.start_embedded_debugger("000")

def FormBeginSetData(uideflist, uipMaster, key):
  config = uideflist.config

  #inisialisasi
  keepGoingProcess = 1

  #checking riwayat pindah paket investasi rekening peserta selama periode pindah paket
  try:
    #ambil no_rekening
    idStr = string.split(key,'#')[1]
    keyName, keyVal = string.split(idStr,'=')
    if keyName == 'REGISTERCIF_ID':
      #registercif_id = string.split(key,'=')[1]
      oRegisterCIF = config.CreatePObjImplProxy('RegisterCIF')
      oRegisterCIF.Key = keyVal
      noRekening = oRegisterCIF.no_rekening
    elif keyName == 'NO_REKENING':
      noRekening = keyVal
    else:
      raise Exception, '\n\nKesalahan Proses Pindah Paket\nKey %s tidak terdefinisi.' % (str(key))

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
    #oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
    #oNasabahDPLK.Key = noPeserta
    #y, m, d = oNasabahDPLK.tgl_registrasi[:3]
    #dtTglRegistrasi = config.ModLibUtils.EncodeDate(y, m, d)
    '''if (config.Now() - dtTglRegistrasi) < minMasaKepesertaan:
      #masa kepesertaan belum mencukupi untuk boleh pindah paket
      #prosesi pindah paket tidak boleh dilanjutkan
      raise '\nPERINGATAN!','Peserta belum mencapai masa kepesertaan minimum.'
      keepGoingProcess = 0'''

    ## Tambahan By ade herman 2011-07-25
    yearNow = config.FormatDateTime('yyyy', config.Now())
    #config.SendDebugMsg('year...... : '+str(yearNow))
    ## end By ade herman

    #ambil pindah paket terakhir
    #sSQL = 'select top %d hppi.TANGGAL_HISTORI from HISTORIPINDAHPAKETINVESTASI hppi ' \
    #  'where hppi.NO_PESERTA = \'%s\' '\
    #  '  and datepart(year,hppi.tanggal_histori) = \'%s\' '\
    #  'order by hppi.TANGGAL_HISTORI DESC' \
    #  % (maksPindahPaket, noPeserta, yearNow)
    
    sSQL = \
      '''select hppi.TANGGAL_HISTORI from HISTORIPINDAHPAKETINVESTASI hppi
      where hppi.no_rekening = \'%s\'
      and datepart(year,hppi.tanggal_histori) = \'%s\'
      order by hppi.TANGGAL_HISTORI DESC'''\
      % (noRekening, yearNow)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    #config.SendDebugMsg('rSQL : '+ sSQL )
    
    #secara otomatis bila maksPindahPaket == 0 maka rSQL akan Eof
    if not rSQL.Eof: # and rSQL.RecordCount == maksPindahPaket:
      #hasil SQL tidak kosong dan record ada sejumlah maksPindahPaket
      #ambil tanggal histori terakhir (di record pertama)
      rSQL.First()
      dtTglTerakhir = config.ModLibUtils.EncodeDate(rSQL.tanggal_histori[0],\
        rSQL.tanggal_histori[1],rSQL.tanggal_histori[2])

      #config.SendDebugMsg('Masukkkkkkkkkk')
      if config.ModLibUtils.Now() - dtTglTerakhir < periodePindahPaket:
         raise Exception,'\n\nPERINGATAN!\nPeriode Pindah Paket Investasi '\
            ' tidak di perkenankan, karena belum genap 1 bulan (31 hari)'
         keepGoingProcess = 0


      ## Sementara di tutup By ade herman 2011-07-25
      #if maksPindahPaket > 1:
        #maksimal pindah paket investasi boleh lebih dari 1 kali

        #ambil tanggal histori sebelumnya (di record terakhir sesuai restriksi 'TOP')
      #  i = 2
      #  while not rSQL.Eof and i <= maksPindahPaket:
      #    if i == maksPindahPaket:
            #sudah sampe ke record yang terakhir
      #      dtTglSebelumnya = config.ModLibUtils.EncodeDate(rSQL.tanggal_histori[0],\
      #        rSQL.tanggal_histori[1],rSQL.tanggal_histori[2])
      #    else:
            #skip, untuk sampe ke record terakhir
       #     rSQL.Next()

          #inkremen i
       #   i += 1

        #cek rentang kedua tanggal histori
       # if dtTglTerakhir - dtTglSebelumnya < periodePindahPaket:
          #rentang masih kurang dari periode pindah paket yang dibolehkan
          #prosesi pindah paket tidak boleh dilanjutkan
        #  raise '\nPERINGATAN!','Peserta sudah melakukan Pindah Paket Investasi '\
        #    'sebanyak %d dalam satu periode. Tidak diperkenankan untuk pindah paket '\
        #    'investasi lagi sampai periode baru berikutnya.' % (maksPindahPaket)
        #  keepGoingProcess = 0
      #else:
        #maksimal pindah paket investasi hanya boleh 1 kali selama periode
        #cek rentang tanggal sekarang dengan tanggal histori terakhir pindah paket
       # if config.ModLibUtils.Now() - dtTglTerakhir < periodePindahPaket:
       #   raise '\nPERINGATAN!','Peserta sudah melakukan Pindah Paket Investasi '\
       #     'sebanyak %d dalam satu periode. Tidak diperkenankan untuk pindah paket '\
       #     'investasi lagi sampai periode baru berikutnya.' % (maksPindahPaket)
       #   keepGoingProcess = 0
          
      ## End by Ade herman 2011-07-25

    sSQL = "SELECT * FROM paketinvestasi"
    rSQL = config.CreateSQL(sSQL).RawResult
    while not rSQL.Eof:
      recTmpPI = uideflist.uipTmpPaket.Dataset.AddRecord()
      recTmpPI.kode_pi = rSQL.kode_paket_investasi
      recTmpPI.nama_pi = rSQL.nama_paket_investasi
      rSQL.Next()

  except:
    raise Exception, str(sys.exc_info()[1])

  return keepGoingProcess

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  try:
    #checking status dplk peserta
    uiCalled = uideflist.GetPClassUIByName(auiname)
    rec = uiCalled.ActiveRecord
    if auiname == 'uipMaster':
      no_peserta = uiCalled.ActiveRecord.no_peserta
    else:
      no_peserta = uiCalled.ActiveRecord.GetFieldByName('LNasabahDPLK.no_peserta')
      
    moduleapi.IsPesertaAktif(config, no_peserta)

    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    if uideflist.uipMaster.Dataset.RecordCount > 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'P')
  except:
    raise Exception, str(sys.exc_info()[1])

  #set TanggalPakai untuk OQL batch transaksi
  recP = uideflist.uipParameter.Dataset.AddRecord()
  tglPakai = time.localtime()[:3]
  recP.TanggalPakai = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])
    
def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config

  if oData.no_referensi in ['', None]:
    raise Exception,'\n\nRegistrasi Error\nNomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()
  
def saveRegisterPPI(config, params, returns):
  uipRegisterCIF = params.uipRegisterCIF.GetRecord(0)
  uipPaketInvest = None
  if params.uipRekDPLK_New.RecordCount > 0:
    uipPaketInvest = params.uipRekDPLK_New
  
  success = False; msgreturn = ''
  config.BeginTransaction()
  try:
    oM = config.CreatePObject("RegisterPindahPaketInvestasi")
    oM.keterangan = uipRegisterCIF.keterangan
    oM.no_peserta = uipRegisterCIF.GetFieldByName("LNasabahDPLK.no_peserta")
    oM.no_rekening = uipRegisterCIF.GetFieldByName("LRekeningDPLK.no_rekening")
    oM.no_referensi = uipRegisterCIF.no_referensi
    oM.tanggal_register = config.Now()
    oM.terminal_id = uipRegisterCIF.terminal_id
    oM.user_id = uipRegisterCIF.user_id
    
    for i in range(0, uipPaketInvest.RecordCount):
      oInvest = uipPaketInvest.GetRecord(i)
                                           
      oD = config.CreatePObject("RegPindahPaketDetil")
      oD.LRegPindahPaket = oM
      oD.kode_paket_investasi = oInvest.GetFieldByName("LPaketInvestasi.kode_paket_investasi")
      oD.proporsi = oInvest.pct_alokasi
  
    config.Commit()
    success = True
    msgreturn = 'Registrasi pindah paket investasi telah disimpan...'
  except:
    config.Rollback()
    msgreturn = 'Proses tidak dapat dilanjutkan\n%s' % str(sys.exc_info()[1])
    #raise Exception, str(sys.exc_info()[1])
  
  returns.CreateValues(['success', success], ['msgreturn', msgreturn])
