#
# Fungsi BeforeCreateObject merupakan KONVENSI, 
# harus ada di setiap script import massal
#

import time, string
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#kakasapi = modman.getModule(config, 'kakasapi')

def BeforeCreateObject(config, targetClassName, data):
  moduleapi = modman.getModule(config, 'moduleapi')
  kakasapi = modman.getModule(config, 'kakasapi')
  
  return 1
  returnValue = 1
  
  if targetClassName == 'Deposito':
    #Investasi
    kakasapi.Logging(config, targetClassName, \
            'Peserta Masuk SUKSES' )
    pass
    
  elif targetClassName == 'Obligasi':
    #cek nomor peserta sudah ada atau belum   
    #peserta = config.CreatePObjImplProxy('NasabahDPLK')
    #peserta.Key = data.GetFieldByName('NomorPeserta')
    rSQL = config.CreateSQL('select no_peserta from NasabahDPLK where no_peserta = \
      \'%s\'' % (data.GetFieldByName('NomorPeserta'))).RawResult

    #if not peserta.IsNull:
    if not rSQL.Eof:
      #peserta sudah ada
      kakasapi.Logging(config, targetClassName, \
        'Nomor Peserta %s sudah ada.' % (data.GetFieldByName('NomorPeserta')))
      returnValue = 0

  elif targetClassName == 'Reksadana':
    no_peserta = data.GetFieldByName('NoPeserta')

    # cek apakah peserta yang akan diproses sudah ada
    try:
      moduleapi.IsNasabahAvail(config, no_peserta)
    except:
      kakasapi.Logging(config, targetClassName, \
        'Nomor Peserta %s tidak ada!' % (no_peserta))
      returnValue = 0

    # cek apakah peserta yang akan diproses berstatus aktif
    if returnValue:
      try:
        moduleapi.IsPesertaAktif(config, no_peserta)
      except:
        kakasapi.Logging(config, targetClassName, \
          'Peserta %s tidak aktif!' % (no_peserta))
        returnValue = 0

      #cek usia peserta
      if returnValue:
        oR = config.CreatePObjImplProxy('RekeningDPLK')
        oR.Key = no_peserta
        if oR.status_wasiat_ummat == 'T':
          # update rekening wasiat umat (besar premi & manfaat asuransi) -- ita 06 july 2009
          besar_premi = data.GetFieldByName('BesarPremi')
          manfaat_asuransi = data.GetFieldByName('ManfaatAsuransi')
          y,m,d = config.ModLibUtils.DecodeDate(data.GetFieldByName('TanggalAkseptasi'))
          tgl_akseptasi = string.zfill(m, 2) + '/' + string.zfill(d, 2) + '/' + str(y)
          sSQL = "UPDATE RekeningWasiatUmmat \
          SET Besar_Premi = %s, Manfaat_Asuransi = %s, \
          Tgl_Akseptasi = '%s' \
          WHERE No_Peserta = '%s'" % (besar_premi, manfaat_asuransi, tgl_akseptasi, no_peserta)
          config.SendDebugMsg(sSQL)
          config.ExecSQL(sSQL)

          kakasapi.Logging(config, targetClassName, \
            'Peserta %s sudah terdaftar akseptasi wasiat ummat!' % (no_peserta))
          returnValue = 0 
          
        elif moduleapi.GetUsiaPeserta(config, no_peserta) > 55.0:
          #peserta wasiat ummat hanya boleh dibawah 55 tahun
          kakasapi.Logging(config, targetClassName, \
            'Peserta %s lebih dari 55 tahun!' % (no_peserta))
          returnValue = 0

        #cek otoritas user terhadap cabang peserta
        if returnValue:
          try:
            moduleapi.CheckRegCIFRestr(config, no_peserta)
          except:
            kakasapi.Logging(config, targetClassName, \
              'Anda tidak diperkenankan mengoreksi peserta %s!' % (no_peserta))
            returnValue = 0

          #cek apabila ada register CIF lainnya
          if returnValue:
            try:
              moduleapi.CheckRegisterCIFUniq(config, no_peserta, 'U')
            except:
              kakasapi.Logging(config, targetClassName, \
                'Peserta %s sedang dikoreksi dengan jenis koreksi yang sama!' % (no_peserta))
              returnValue = 0

              if returnValue:
                besar_premi = data.GetFieldByName('BesarPremi')
                manfaat_asuransi = data.GetFieldByName('ManfaatAsuransi')
                if not besar_premi \
                  or moduleapi.IsApproxZero(besar_premi) \
                  or (besar_premi < 0.0):
                  kakasapi.Logging(config, targetClassName, \
                    'Besar premi untuk peserta %s harus lebih dari nol!' % (no_peserta))
                  returnValue = 0
                elif not manfaat_asuransi \
                  or moduleapi.IsApproxZero(manfaat_asuransi) \
                  or (manfaat_asuransi < 0.0):
                  kakasapi.Logging(config, targetClassName, \
                    'Manfaat asuransi untuk peserta %s harus lebih dari nol!' % (no_peserta))
                  returnValue = 0

  else:
    #error, classname tidak terdefinisi
    #lebih baik log untuk data yang ini, tergantung konfigurasi import massal
    pass

  return returnValue

def ProcessingImport(config, obj, data):  
  #cek berdasarkan classname obj untuk mengetahui jenis transaksinya
  moduleapi = modman.getModule(config, 'moduleapi')
  
  className = obj.ClassName
  obj.user_id = config.SecurityContext.UserId
  obj.terminal_id = config.SecurityContext.InitIP
  obj.user_id_auth = 'IMPORT MASSAL'
  obj.tgl_otorisasi = config.Now()
  obj.last_update = config.Now()
    
  if className == 'Deposito':
    #input massal Data Deposito
    config.SendDebugMsg('bilyet#'+str(data.GetFieldByName('Nomor_Bilyet')))
    if data.GetFieldByName('Nomor_Bilyet') not in ('','None') :
      moduleapi.CheckNoBilyetAvl(config, data.GetFieldByName('Nomor_Bilyet'))
    InsertDeposito(config,obj,data)

  elif className == 'Obligasi':
    #input massal obligasi
    InsertObligasi(config,obj,data)

  elif className == 'Reksadana':
    #input massal reksadana
    InsertReksadana(config,obj,data)
    
  else :
    #error, classname tidak terdefinisi
    #lebih baik log untuk data yang ini, tergantung konfigurasi import massal
    pass

def InsertDeposito (config,oD, data) :
    #create objek Deposito
    config.SendDebugMsg('InsertDeposito')
    oD.Rekening_Deposito = data.GetFieldByName('Rekening_Deposito')
    if oD.Rekening_Deposito.find('e')!= -1 and oD.Rekening_Deposito.find('+') != -1:
      raise Exception, '' + 'Data Rekening Deposito dan no bilyet harus berupa teks' 
    
    oD.no_bilyet = data.GetFieldByName('Nomor_Bilyet')
    if oD.no_bilyet == 'None' :
      oD.no_bilyet = None
    oD.akum_nominal = data.GetFieldByName('Nominal_Akumulasi')
    config.SendDebugMsg('InsertDeposito1')
    oD.akum_LR = data.GetFieldByName('akumulasi_LabaRugi')
    config.SendDebugMsg('InsertDeposito2')
    oD.status = data.GetFieldByName('status')
    oD.tgl_buka = data.GetFieldByName('tanggal_buka')
    oD.tgl_tutup = data.GetFieldByName('tanggal_tutup')
    oD.nominal_pembukaan = data.GetFieldByName('Nominal_Awal')
    config.SendDebugMsg('InsertDeposito3')
    if len(data.GetFieldByName('KodePihakKetiga')) > 8 :
      raise Exception, '' + 'Isilah kode pihak ketiga sesuai kode di master pihak ketiga'
    oD.kode_pihak_ketiga = data.GetFieldByName('KodePihakKetiga')
    config.SendDebugMsg('InsertDeposito4')
    oD.jenisJatuhTempo = data.GetFieldByName('jangka_waktu')
    oD.nisbah = data.GetFieldByName('Nisbah') 
    config.SendDebugMsg('InsertDeposito5')
    
    oD.tgl_jatuh_tempo = data.GetFieldByName('tgl_Jatuh_Tempo')
    config.SendDebugMsg('InsertDeposito6')
    oD.kapitalisir_rollover = data.GetFieldByName('jenis_bagi_hasil')
    if oD.treatmentPokok == 'A' :
      oD.ARO = 'T'
    config.SendDebugMsg('InsertDeposito8')
    oD.treatmentPokok = data.GetFieldByName('pokok_saat_jatuh_tempo')
    oD.jmlHariOnCall = data.GetFieldByName('JumlahOnCall')
    if data.GetFieldByName('rekening_bagi_hasil').find('.') != -1 :
      raise Exception, '' + 'Data Rekening bagi hasil harus berupa teks' 
    
    oD.no_rekening = data.GetFieldByName('rekening_bagi_hasil')
    if oD.no_rekening == 'None' :
      oD.no_rekening = None
    config.SendDebugMsg('no_bilyet='+oD.no_bilyet)  
    if data.GetFieldByName('Proporsi_Paket_A') != 'None' :
      config.SendDebugMsg('PA='+data.GetFieldByName('Proporsi_Paket_A'))  
      PA = float(data.GetFieldByName('Proporsi_Paket_A'))
    else :
      PA = 0.0
    if data.GetFieldByName('Proporsi_Paket_B') != 'None' :
      PB = float(data.GetFieldByName('Proporsi_Paket_B'))
      config.SendDebugMsg('PB='+data.GetFieldByName('Proporsi_Paket_B'))  
    else :
      PB = 0.0
  
    if data.GetFieldByName('Proporsi_Paket_C') != 'None' :
      PC = float(data.GetFieldByName('Proporsi_Paket_C'))
      config.SendDebugMsg('PC='+data.GetFieldByName('Proporsi_Paket_C'))  
    else :
      PC = 0.0
      
    if PA + PB + PC != 100 :
       raise Exception, 'ERROR' + 'Proporsi total harus 100%'
    
    if PA != 0.0 :
      oRD = config.CreatePObject('RincianDeposito')
      oRD.Akum_Paket = oD.akum_nominal * PA /100
      #oRD.Akum_LR_Paket = oD.akum_LR * PA / 100
      oRD.LDeposito = oD
      oRD.kode_paket_investasi = 'A'
    if PB != 0.0 :
      oRD = config.CreatePObject('RincianDeposito')
      oRD.Akum_Paket = oD.akum_nominal * PB /100
      #oRD.Akum_LR_Paket = oD.akum_LR * PB /100
      oRD.LDeposito = oD
      oRD.kode_paket_investasi = 'B'
    if PC != 0.0 :
      oRD = config.CreatePObject('RincianDeposito')
      oRD.Akum_Paket = oD.akum_nominal * PC /100
      #oRD.Akum_LR_Paket = oD.akum_LR * PC /100
      oRD.LDeposito = oD
      oRD.kode_paket_investasi = 'C'

def InsertObligasi(config,oO,data) :
    #create objek Obligasi
    
    oO.nama_obligasi = data.GetFieldByName('NamaSukuk')
    oO.akum_nominal = data.GetFieldByName('Nominal_Akumulasi')
    oO.akum_LR = data.GetFieldByName('akumulasi_LabaRugi')
    oO.status = data.GetFieldByName('status')
    oO.tgl_buka = data.GetFieldByName('tanggal_buka')
    oO.tgl_tutup = data.GetFieldByName('tanggal_tutup')
    oO.nominal_pembukaan = data.GetFieldByName('Nominal_Awal')
    if len(data.GetFieldByName('KodeEmiten')) > 8 :
      raise Exception, '' + 'Isilah kode Emiten sesuai kode master pihak ketiga'
    oO.kode_pihak_ketiga = data.GetFieldByName('KodeEmiten')
    oO.TreatmentObligasi = data.GetFieldByName('TreatmentSukuk')[:1]
    oO.tgl_jatuh_tempo = data.GetFieldByName('tgl_jatuh_tempo')
    oO.jenisAkad = data.GetFieldByName('jenisakad')
    if data.GetFieldByName('jenisakad') == 'I' : 
      oO.akum_piutangLR = data.GetFieldByName('PersenAkadIjarah')
    oO.BankCode = data.GetFieldByName('KodeBank')
    if oO.BankCode == 'None' :
      oO.BankCode = None
    if data.GetFieldByName('NoRekening').find('.') != -1 :
      raise Exception, '' + 'Data Rekening bagi hasil harus berupa teks'
    oO.no_rekening = data.GetFieldByName('NoRekening')
    if oO.no_rekening == 'None' :
      oO.no_rekening = None
    
    oRD = config.CreatePObject('RincianObligasi')
    oRD.Akum_Paket = oO.akum_nominal
    #oRD.Akum_LR_Paket = oO.akum_LR
    oRD.LObligasi = oO
    oRD.kode_paket_investasi = 'B'
  
def InsertReksadana(config,oR, data) :
    #create objek Reksadana
    config.SendDebugMsg('InsertReksadana')
    oR.nama_reksadana = data.GetFieldByName('NamaReksadana')
    config.SendDebugMsg('oR.nama_reksadana='+oR.nama_reksadana)
    if len(data.GetFieldByName('ManajerInvestasi')) > 8 :
      raise Exception, '' + 'input kode Manajer Investasi seperti di master Pihak Ketiga'
    oR.kode_pihak_ketiga = data.GetFieldByName('ManajerInvestasi')
    config.SendDebugMsg('InsertReksadana1')
    oR.kode_jns_reksadana = data.GetFieldByName('JenisReksadana')
    oR.unit_penyertaan = data.GetFieldByName('UP')
    config.SendDebugMsg('InsertReksadana2')
    oR.nominal_pembukaan = data.GetFieldByName('NilaiInvestasi')
    config.SendDebugMsg('InsertReksadana3')
    oR.NAB_awal = data.GetFieldByName('NABSubscribe')
    config.SendDebugMsg('InsertReksadana4')
    #oR.NAB = data.GetFieldByName('NABRedempt')
    oR.NAB_Transaksi = data.GetFieldByName('NAB_Rata')
    config.SendDebugMsg('InsertReksadana5')
    oR.NAB = data.GetFieldByName('NAB_Sekarang')
    config.SendDebugMsg('InsertReksadana6')
    oR.last_update = data.GetFieldByName('TglPenetapanNAB')
    config.SendDebugMsg('InsertReksadana7')
    oR.status = data.GetFieldByName('status')
    oR.tgl_buka = data.GetFieldByName('tanggal_buka')
    
    oR.akum_nominal = data.GetFieldByName('NilaiPasar')
    oR.akum_piutangLR = data.GetFieldByName('ReturnUnRealize')
    oR.akum_LR = data.GetFieldByName('ReturnRealize')
    
    #oR.no_rekening = data.GetFieldByName('rekening_pencairan')
    
    oRD = config.CreatePObject('RincianReksadana')
    oRD.Akum_Paket = oR.akum_nominal
    oRD.Akum_LR_Paket = 0.0#oD.akum_LR
    oRD.LReksadana = oR
    oRD.kode_paket_investasi = 'C'
    
    oHistNABReksadana = config.CreatePObject('HistNABReksadana')
    oHistNABReksadana.id_investasi = oR.id_investasi
    oHistNABReksadana.TerminalUbah = config.SecurityContext.InitIP
    oHistNABReksadana.UserPengubah = config.SecurityContext.UserID
    oHistNABReksadana.Tgl_Penetapan = data.GetFieldByName('TglPenetapanNAB')
    oHistNABReksadana.NAB = oR.NAB
    oHistNABReksadana.TerminalOto = config.SecurityContext.InitIP
    oHistNABReksadana.unit_penyertaan = oR.unit_penyertaan
    oHistNABReksadana.UserOto = 'IMPORT MASSAL'
    oHistNABReksadana.TerminalOto = config.SecurityContext.InitIP
    oHistNABReksadana.TglUbah = config.Now()

