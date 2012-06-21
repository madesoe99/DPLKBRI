#
# Fungsi BeforeCreateObject merupakan KONVENSI, 
# harus ada di setiap script import massal
#

import time, sys, string
sys.path.append('c:/dafapp/dplk07/scripts/transaction')
sys.path.append('c:/dafapp/dplk07/script_modules')

import registercif_auth, moduleapi, kakasapi

def BeforeCreateObject(config, targetClassName, data):
  returnValue = 1
  
  if targetClassName == 'AhliWaris':
    #cek status rekening / peserta DPLK
    pass
    
  elif targetClassName == 'RegisterNasabahRekening':
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

  elif targetClassName == 'RekeningWasiatUmmat':
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
  className = obj.ClassName

  if className == 'AhliWaris':
    #input massal ahli waris
    pass

  elif className == 'RegisterNasabahRekening':
    #registrasi nasabah baru

    #create objek NasabahDPLK
    oN = config.CreatePObject('NasabahDPLK')
    oN.no_peserta = data.GetFieldByName('NomorPeserta')

    oN.tgl_registrasi = data.GetFieldByName('TanggalRegistrasi')

    oN.no_referensi = data.GetFieldByName('NomorReferensi')
    oN.no_identitas_diri = data.GetFieldByName('NoIdentitasDiri')
    oN.nama_lengkap = data.GetFieldByName('NamaLengkap')
    oN.tanggal_lahir = data.GetFieldByName('TanggalLahir')
    oN.tempat_lahir = data.GetFieldByName('TempatLahir')
    oN.jenis_kelamin = data.GetFieldByName('JenisKelamin')

    oN.NPWP = data.GetFieldByName('NPWP')
    oN.pekerjaan = data.GetFieldByName('Pekerjaan')

    #oN.alamat_kantor_jalan = data.GetFieldByName('AlamatKantorJalan')
    #oN.alamat_kantor_kelurahan = data.GetFieldByName('AlamatKantorKelurahan')
    #oN.alamat_kantor_kecamatan = data.GetFieldByName('AlamatKantorKecamatan')
    #oN.alamat_kantor_kota = data.GetFieldByName('AlamatKantorKota')
    #oN.alamat_kantor_propinsi = data.GetFieldByName('AlamatKantorPropinsi')
    #oN.alamat_kantor_kode_pos = data.GetFieldByName('AlamatKantorKodePos')
    #oN.alamat_kantor_telepon = data.GetFieldByName('AlamatKantorTelepon')
    #oN.alamat_kantor_telepon2 = data.GetFieldByName('AlamatKantorTelepon2')
    
    oN.nama_perusahaan = data.GetFieldByName('NamaPerusahaan')
    oN.kode_jenis_usaha = data.GetFieldByName('KodeJenisUsaha')
    oN.kode_pemilikan = data.GetFieldByName('KodeKepemilikan')
    oN.kode_propinsi= data.GetFieldByName('DaerahAsal')
    oN.kode_kelompok = data.GetFieldByName('KodeKelompok')
    oN.kode_nasabah_corporate = data.GetFieldByName('KodeKorporat')
    oN.kode_dp = data.GetFieldByName('KodeDPLain')
  
    oN.alamat_jalan = data.GetFieldByName('AlamatJalan')
    oN.alamat_jalan2 = data.GetFieldByName('AlamatJalanLanjutan')
    oN.alamat_rtrw = data.GetFieldByName('AlamatRTRW')
    oN.alamat_kelurahan = data.GetFieldByName('AlamatKelurahan')
    oN.alamat_kecamatan = data.GetFieldByName('AlamatKecamatan')
    oN.alamat_kota = data.GetFieldByName('AlamatKota')
    oN.alamat_propinsi = data.GetFieldByName('AlamatPropinsi')
    oN.alamat_kode_pos = data.GetFieldByName('AlamatKodePos')
    oN.alamat_telepon = data.GetFieldByName('AlamatTelepon1')
    oN.alamat_telepon2 = data.GetFieldByName('AlamatTelepon2')
    oN.alamat_email = data.GetFieldByName('AlamatEmail')
  
    oN.alamat_surat_jalan = data.GetFieldByName('AlamatSuratJalan')
    oN.alamat_surat_jalan2 = data.GetFieldByName('AlamatSuratJalanLanjutan')
    oN.alamat_surat_rtrw = data.GetFieldByName('AlamatSuratRTRW')
    oN.alamat_surat_kelurahan = data.GetFieldByName('AlamatSuratKelurahan')
    oN.alamat_surat_kecamatan = data.GetFieldByName('AlamatSuratKecamatan')
    oN.alamat_surat_kota = data.GetFieldByName('AlamatSuratKota')
    oN.alamat_surat_propinsi = data.GetFieldByName('AlamatSuratPropinsi')
    oN.alamat_surat_kode_pos = data.GetFieldByName('AlamatSuratKodePos')
    oN.alamat_surat_telepon = data.GetFieldByName('AlamatSuratTelepon1')
    oN.alamat_surat_telepon = data.GetFieldByName('AlamatSuratTelepon2')
  
    oN.isPesertaPengalihan = data.GetFieldByName('PesertaPengalihan')
    oN.keterangan = data.GetFieldByName('Keterangan')

    oN.terminal_id = data.GetFieldByName('TerminalInput')
    oN.isCommitted = 'T'

    #create objek RekeningDPLK
    oR = config.CreatePObject('RekeningDPLK')
    oR.no_peserta = data.GetFieldByName('NomorPeserta')
    
    oR.akum_dana_pengembangan = oR.akum_dana_peralihan = \
      oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pst = \
      oR.nilai_bayar_anuitas = oR.SRR_AKHIR = 0.0
    
    oR.iuran_pk = data.GetFieldByName('NominalIuranPemberiKerja')
    oR.iuran_pst = data.GetFieldByName('NominalIuranPeserta')
  
    oR.status_anuitas = oR.status_autodebet = oR.status_wasiat_ummat = 'F'
    
    oR.STATUS_BIAYA_DAFTAR = data.GetFieldByName('StatusBiayaDaftar')
    oR.STATUS_DPLK = 'A'
    oR.sumber_dana = data.GetFieldByName('SumberDana')
  
    oR.usia_pensiun = data.GetFieldByName('UsiaPensiun')
    y,m,d = config.ModLibUtils.DecodeDate(data.GetFieldByName('TanggalLahir'))
    tupleTanggalLahir = (y,m,d,0,0,0,0)
    tgl_pensiun = moduleapi.AddYearToDateTuple(config, \
      tupleTanggalLahir, \
      data.GetFieldByName('UsiaPensiun')) 
    tgl_pensiun_dipercepat = moduleapi.AddYearToDateTuple(config, \
      tupleTanggalLahir, \
      int(data.GetFieldByName('UsiaPensiun')) - 10) 
    oR.tgl_pensiun = moduleapi.DateTimeTupleToFloat(config, tgl_pensiun)
    oR.tgl_pensiun_dipercepat = moduleapi.DateTimeTupleToFloat(config, tgl_pensiun_dipercepat)

    #oR.WASIAT_UMMAT = oRegisterNasabahRekening.WASIAT_UMMAT

    oR.kirim_statemen = data.GetFieldByName('KirimStatement')
    oR.kode_cab_daftar = data.GetFieldByName('CabangPendaftaran')
    oR.kode_paket_investasi = data.GetFieldByName('PaketInvestasi')

    oR.keterangan = data.GetFieldByName('Keterangan')

    #common field antara NasabahDPLK dan RekeningDPLK
    oN.user_id = oR.user_id = data.GetFieldByName('UserPenginput')
    oN.auth_user_id = oR.auth_user_id = config.SecurityContext.UserID
    oN.last_terminal_id = oR.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
    oN.last_update = oR.last_update = config.ModLibUtils.Now()
    oN.operation_code = oR.operation_code = 'F'

    CreateDetailAkumPengembangan(config, oR.no_peserta, oR.kode_paket_investasi)
    
    #langsung hapus objek RegisterNasabahRekening
    obj.Delete()

  elif className == 'RekeningWasiatUmmat':
    no_peserta = data.GetFieldByName('NoPeserta')
    oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
    oRekeningDPLK.Key = no_peserta

    obj.user_id = config.SecurityContext.UserID
    obj.auth_user_id = config.SecurityContext.UserID

    #set tanggal berakhir wasiat ummat = tgl pensiun peserta
    y,m,d = oRekeningDPLK.tgl_pensiun[:3] 
    obj.tgl_berakhir = config.ModLibUtils.EncodeDate(y,m,d)

    #inisialisasi kolektibilitas dan kewajiban wasiat ummat
    oRekeningDPLK.collectivity_wasiat_ummat = 'T'
    oRekeningDPLK.kewajiban_wasiat_ummat = 0.0

    # set status wasiat ummat
    oRekeningDPLK.status_wasiat_ummat = 'T'

#     #cek peserta apakah ikut autodebet
#     if oRekeningDPLK.status_autodebet == 'T':
#       #peserta ikut autodebet, daftarkan SI juga untuk premi bulanannya
# 
#       #cek status login ke CoreBanking  
#       isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
#         'NeedLoginCoreBanking')
#       if isNeedLoginCoreBanking == 'T':   
#         #pasang status autodebet di CoreBanking
#         
#         #ambil info rekening autodebet
#         oRekeningDPLK.Ls_RekeningAutoDebet.First()
#         oRekeningAutoDebet = \
#           oRekeningDPLK.Ls_RekeningAutoDebet.CurrentElement
#               
#         #setting untuk tanggal autodebet
#         #tanggal pensiun sebagai tanggal kadaluarsa
#         y1,m1,d1 = oRekeningAutoDebet.LRekeningDPLK.tgl_pensiun[:3]
#         
#         #tanggal SI pertama
#         y0,m0,d = time.localtime()[:3]
#         d0 = oRekeningAutoDebet.tanggal_autodebet
#         if d > d0:
#           #tanggal autodebet bulan ini sudah lewat, ambil tanggal autodebet bulan depan
#           dtNextMonth = config.ModLibUtils.IncMonth(config.ModLibUtils.Now(),1)
#           y0,m0 = config.ModLibUtils.DecodeDate(dtNextMonth)[:2]
#                   
#         #remote eksekusi creating New SI premi core banking
#         #transaksiapi.CreateSI(config, oRekeningAutoDebet.no_peserta, \
#         #  oRekeningAutoDebet.no_rekening, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', \
#         #  'GiroPremi'), '2', obj.besar_premi, \
#         #  config.ModLibUtils.EncodeDate(y0,m0,d0), \
#         #  config.ModLibUtils.EncodeDate(y1,m1,d1))
    
  else:
    #error, classname tidak terdefinisi
    #lebih baik log untuk data yang ini, tergantung konfigurasi import massal
    pass

  #assign properti common
  #(belum ada properti common yang perlu diubah)

  #autorisasi CIF (perlu mengubah script registercif_auth supaya bisa diimport)
  #registercif_auth.

def CreateDetailAkumPengembangan(config, no_peserta, kode_paket_investasi):
    sSQL = 'SELECT kode_jns_investasi \
    FROM RINCIANPAKETINVESTASI\
    WHERE kode_paket_investasi = \'%s\' ' % (kode_paket_investasi)
    rSQL = config.CreateSQL(sSQL).RawResult
    while not rSQL.Eof:
        sSQL = 'INSERT INTO DETAILAKUMPENGEMBANGAN \
		(no_peserta, kode_paket_investasi, kode_jns_investasi, Nilai_Akumulasi) \
		VALUES (\'%s\',\'%s\',\'%s\',%f) ' % \
		(no_peserta, kode_paket_investasi, rSQL.kode_jns_investasi, 0)
        config.ExecSQL(sSQL)
	rSQL.Next()
