import string, sys, time
sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')
sys.path.append('c:/dafapp/dplk07/scripts/report')

import transaksiapi, AuthorizeTransaksi, SlipTransaksiTeller, moduleapi

def FormEndSetData(uideflist, uiname, objdata):
#   import rpdb2; rpdb2.start_embedded_debugger("000")
  config = uideflist.config
  uipUserInfo = uideflist.uipUserInfo
  uipTransaksi = uideflist.uipTransaksi
  uipNasabah = uideflist.uipNasabah
  uipParameter = uideflist.uipParameter
  
  oUser = config.CreatePObjImplProxy('UserApp')
  oUser.Key = config.SecurityContext.UserID

  userID = oUser.user_id
  groupID = config.SecurityContext.GetUserInfo()[2]
  #tglPakai = time.localtime()[:3]
  tglPakai = config.ModLibUtils.DecodeDate(config.ModLibUtils.Now())

  recUserInfo = uipUserInfo.Dataset.AddRecord()
  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recNasabah = uipNasabah.Dataset.GetRecord(0)
  recParameter = uipParameter.Dataset.AddRecord()
  
  #inisialisasi, status awal untuk user ADMINISTRATOR
  recUserInfo.TanggalPakai = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])
  recUserInfo.isTeller = 0
  recUserInfo.BranchCode = ''
  recUserInfo.UserIDOwner = ''

  #cek user apakah termasuk group teller atau Admin SAJA
  if string.upper(userID) == 'ROOT' or \
    string.upper(str(groupID)) == 'ADMIN' or oUser.NoLimitLocation == 'T':
    #user root atau admin: nothing to do, value like inisialization before
    pass
  #elif string.upper(str(groupID)) == 'TELLER':
  elif moduleapi.IsUserTeller(config, config.SecurityContext.userID):
    #user 'teller'
    recUserInfo.isTeller = 1
    recUserInfo.UserIDOwner = userID
    recUserInfo.BranchCode = config.SecurityContext.GetUserInfo()[4]
  config.SendDebugMsg('FormEndSetData4')

  #set iuran peserta, status wasiat umat, kolektibilitas, kewajiban wasiat ummat
  recNasabah.IuranPk = 0.0#recNasabah.GetFieldByName('LRekeningDPLK.iuran_pk')
  recNasabah.IuranPeserta = 0.0#recNasabah.GetFieldByName('LRekeningDPLK.iuran_pst')
  '''recNasabah.isWasiatUmmat = recNasabah.GetFieldByName('LRekeningDPLK.status_wasiat_ummat')
  if recNasabah.isWasiatUmmat == 'T':
    recNasabah.KolektibilitasPremi = \
      recNasabah.GetFieldByName('LRekeningDPLK.collectivity_wasiat_ummat')
    recNasabah.KewajibanWasiatUmmat = \
      recNasabah.GetFieldByName('LRekeningDPLK.kewajiban_wasiat_ummat')'''


  config.SendDebugMsg('FormEndSetData5')
  #set field Data Transaksi
  recTransaksi.IuranPeserta = recNasabah.IuranPeserta
  recTransaksi.IuranPemberiKerja = recNasabah.IuranPk
  recTransaksi.IuranTambahan = 0.0

  #cek apakah peserta Wasiat Ummat
  uipRWU = uideflist.uipRekeningWU
  recRWU = uipRWU.Dataset.AddRecord()
  if recNasabah.isWasiatUmmat == 'T':
    #set field uipRekeningWU, pake SQL saja biar gampang
    sSQL = 'select no_polis,tgl_akseptasi,tgl_berakhir,besar_premi ' \
      'from RekeningWasiatUmmat where no_peserta = \'%s\'' % (recNasabah.no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult

    if rSQL.Eof:
      #data peserta Wasiat Ummat tidak ditemukan
      raise Exception, '\nError','\nPeserta termasuk peserta Wasiat Ummat +  tetapi data ' \
        'Rekening Wasiat Ummat \npeserta %s tidak ditemukan!' \
        % (recNasabah.no_peserta)
    else:
      recRWU.no_polis = rSQL.no_polis
      recRWU.tgl_akseptasi = config.ModLibUtils.EncodeDate(rSQL.tgl_akseptasi[0],\
        rSQL.tgl_akseptasi[1],rSQL.tgl_akseptasi[2])
      if rSQL.tgl_berakhir != None:
        recRWU.tgl_berakhir = config.ModLibUtils.EncodeDate(rSQL.tgl_berakhir[0],\
          rSQL.tgl_berakhir[1],rSQL.tgl_berakhir[2])
      recRWU.besar_premi = rSQL.besar_premi

    #set titipan premi (tambahkan kewajiban premi bila tagihan tidak lancar)
    recTransaksi.titipan_premi = recRWU.besar_premi + recNasabah.KewajibanWasiatUmmat

    #cek pengguna ialah TELLER, untuk setting batch premi bila nasabah peserta Wasiat Ummat
    if recUserInfo.isTeller:
      #set langsung batch premi (tanpa harus lookup)
      tglPakai = '%d/%d/%d' % (tglPakai[0],tglPakai[1],tglPakai[2])
      sSQL = 'select t.ID_TRANSACTIONBATCH, t.NO_BATCH, t.TGL_USED, ' \
             't.BRANCH_CODE, t.BATCH_TYPE from dbo.TRANSACTIONBATCH t ' \
             'where t.USER_ID_OWNER = \'%s\' and t.TGL_USED = \'%s\' and ' \
             't.BATCH_STATUS = \'O\' and t.BATCH_TYPE = \'P\'' % (userID, tglPakai)
      rSQL = config.CreateSQL(sSQL).RawResult

      uipBD = uideflist.uipBatchDefined
      recBD = uipBD.Dataset.AddRecord()
      rSQL.First()
      if rSQL.Eof:
        #batch transaksi tidak ditemukan
        recBD.isBatchPremiExist = 0
      else:
        #batch premi ditemukan, flag batch premi exist
        recBD.isBatchPremiExist = 1
        
        #lansung assign untuk TB_Premi transaksi
        recTransaksi.SetFieldByName('TB_Premi.ID_TransactionBatch',rSQL.ID_TransactionBatch)
        recTransaksi.SetFieldByName('TB_Premi.no_batch',rSQL.no_batch)
        recTransaksi.SetFieldByName('TB_Premi.batch_type',rSQL.batch_type)
        recTransaksi.SetFieldByName('TB_Premi.branch_code',rSQL.branch_code)
        recTransaksi.SetFieldByName('TB_Premi.tgl_used',config.ModLibUtils.EncodeDate(rSQL.tgl_used[0], \
          rSQL.tgl_used[1],rSQL.tgl_used[2]))

  else:
    #bukan peserta wasiat umat
    recRWU.no_polis = 'Bukan peserta'

  #set parameter default
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'
  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value
  
  #set flag hanya membayar titipan premi saja
  recTransaksi.isOnlyTitipanPremi = 0

  return 0
  
def FormGeneralProcessData(uideflist, data):
#   import rpdb2; rpdb2.start_embedded_debugger("000")
  config = uideflist.Config
  config.SendDebugMsg('FormGeneralProcessData')
  rec = data.uipTransaksi.GetRecord(0)
  recN = data.uipNasabah.GetRecord(0)
  
  try:
    isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
      'NeedLoginCoreBanking')

    if isNeedLoginCoreBanking == 'T':
      y,m,d = time.localtime()[:3]
      oCBB = config.CreatePObjImplProxy('CoreBankingBatch')
      oCBB.SetKey('User_ID',config.SecurityContext.UserID)
      oCBB.SetKey('Tanggal',d)
      oCBB.SetKey('Bulan',m)
      oCBB.SetKey('Tahun',y)

    flagSetorPremiJuga = 0
    #cek isOnlyTitipanPremi
    if rec.isOnlyTitipanPremi:
      #hanya membayar titipan premi tanpa iuran peserta

      #preparing objek titipan premi
      o = config.CreatePObject('TitipanPremi')
      rec.HiddenIDTitipanPremi = o.ID_Transaksi
      
      o.isDebet = 'F'
      o.keterangan = 'hanya premi saat iuran peserta %s' % (recN.no_peserta)
      o.no_peserta = recN.no_peserta
      o.mutasi_premi = rec.titipan_premi
      o.ID_TransactionBatch = rec.GetFieldByName('TB_Premi.ID_TransactionBatch')
      o.isPindahBuku = rec.isPindahBuku
      
      #cek kewajiban wasiat ummat dan status kolektibilitas
      AuthorizeTransaksi.SetKolektibilitasWasiatUmmat(config, o.LRekeningDPLK, o)

      if isNeedLoginCoreBanking == 'T':
        if rec.isPindahBuku == 'F':
          o.Ref_CoreBanking = 'ST'

        else:
          #pindah buku premi
          o.Rekening_Pindah_Buku = rec.Rekening_Pindah_Buku
          o.Tipe_Rekening_Pindah_Buku = rec.Tipe_Rekening_Pindah_Buku
          o.Ref_CoreBanking = 'PB'
    else:
      #membayar iuran peserta (dan titipan premi kalau ada)
      sSQL = "SELECT r.kode_paket_investasi, r.proporsi, \
      p.nav, r.no_peserta \
      FROM REKENINGDPLK r, PAKETINVESTASI p\
      WHERE r.kode_paket_investasi = p.kode_paket_investasi \
      and r.nomor_rekening = '%s'\
      and r.status_dplk = 'A'" % (recN.no_peserta)
      rSQL = config.CreateSQL(sSQL).RawResult
      rSQL.First()
      while not rSQL.Eof:
        o = config.CreatePObject('IuranPeserta')
        rec.HiddenIDIuranPeserta = o.ID_Transaksi   
        o.no_peserta = rSQL.no_peserta
        o.keterangan = rec.keterangan
        o.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
        o.catatan_bayar_iuran = rec.catatan_bayar_iuran
        o.isPindahBuku = rec.isPindahBuku
      
        o.kode_paket_investasi = rSQL.kode_paket_investasi
        
        proporsi = rSQL.proporsi or 0.0
        o.mutasi_iuran_pst = rec.IuranPeserta * proporsi / 100
        o.mutasi_iuran_pk = rec.IuranPemberiKerja * proporsi / 100
        o.mutasi_iuran_tambahan = rec.IuranTambahan * proporsi / 100
        o.mutasi_pengembangan = o.mutasi_peralihan = o.mutasi_pengembangan_pst = o.mutasi_pengembangan_pk = o.mutasi_pengembangan_tambahan = o.mutasi_pengembangan_psl = 0.0
        
        o.nav_transaksi = rSQL.nav
        
        o.unit_iuran_pst = o.mutasi_iuran_pst / o.nav_transaksi
        o.unit_iuran_pk = o.mutasi_iuran_pk / o.nav_transaksi
        o.unit_iuran_tambahan = o.mutasi_iuran_tambahan / o.nav_transaksi
        o.unit_iuran_psl = 0
        
        o.tgl_transaksi = rec.tgl_transaksi
        o.branch_code = rec.TB_BranchCode
        o.isCommitted = 'F'
        o.user_id = config.SecurityContext.UserID
        o.terminal_id = config.SecurityContext.GetSessionInfo()[1]
        o.tgl_sistem = config.Now()
        #cek kepesertaan wasiat ummat: titipan premi
        #TUTUP DULU KODE PREMI
  #       if recN.isWasiatUmmat == 'T':
  #         o.titipan_premi = rec.titipan_premi
  #         if o.titipan_premi > 0.0:
  #           o.ID_BatchPremi = rec.GetFieldByName('TB_Premi.ID_TransactionBatch')
  #           
  #           #flag setor premi juga
  #           flagSetorPremiJuga = 1
  #           
  #           #langsung buatin objek TitipanPremi juga
  #           oPremi = config.CreatePObject('TitipanPremi')
  #           
  #           #saving id transaksi titipan premi, untuk kebutuhan print slip transaksi teller
  #           rec.HiddenIDTitipanPremi = oPremi.ID_Transaksi
  #       
  #           oPremi.isDebet = 'F'
  #           oPremi.keterangan = 'premi saat iuran peserta %s' % (recN.no_peserta)
  #           oPremi.no_peserta = recN.no_peserta
  #           oPremi.mutasi_premi = rec.titipan_premi
  #           oPremi.ID_TransactionBatch = rec.GetFieldByName('TB_Premi.ID_TransactionBatch')
  #           oPremi.isPindahBuku = rec.isPindahBuku
  #           
  #           oPremi.tgl_transaksi = rec.tgl_transaksi
  #           oPremi.branch_code = rec.TB_BranchCode
  #           oPremi.isCommitted = 'F'
  #           oPremi.user_id = config.SecurityContext.UserID
  #           oPremi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  #           oPremi.tgl_sistem = config.Now()
  # 
  #           #cek kewajiban wasiat ummat dan status kolektibilitas
  #           AuthorizeTransaksi.SetKolektibilitasWasiatUmmat(config, oPremi.LRekeningDPLK, oPremi)
  
        #setor giro iuran (giro paket) di CoreBanking
        oPI = config.CreatePObjImplProxy('PaketInvestasi')
        oPI.Key = o.kode_paket_investasi
        # giro_paket = oPI.no_giro
        giro_paket = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING','GiroPenampungan')
        
        if isNeedLoginCoreBanking == 'T':
          if rec.isPindahBuku == 'F':
            if flagSetorPremiJuga:
                oPremi.Ref_CoreBanking = 'SP'
                o.Ref_CoreBanking = 'SP'
            else:
              o.Ref_CoreBanking = 'SI'
  
          else:
            #pindah buku iuran
            o.Rekening_Pindah_Buku = rec.Rekening_Pindah_Buku
            o.Tipe_Rekening_Pindah_Buku = rec.Tipe_Rekening_Pindah_Buku
            
            #cek setor premi juga
            if flagSetorPremiJuga:
              oPremi.Ref_CoreBanking = 'PP'
              o.Ref_CoreBanking = 'PP'
            else:
              o.Ref_CoreBanking = 'PI'
              
        rSQL.Next()
        
        
#     #assign nilai yang tidak tercantum di form
#     o.tgl_transaksi = rec.tgl_transaksi
#     o.branch_code = rec.TB_BranchCode
#     o.isCommitted = 'F'
#     o.user_id = config.SecurityContext.UserID
#     o.terminal_id = config.SecurityContext.GetSessionInfo()[1]
#     o.tgl_sistem = config.Now()
    
    #KHUSUS IURAN PESERTA, TIDAK BISA LANGSUNG OTORISASI
    #DIPROSES LEWAT REKONSILISASI CORE BANKING DAN DPLK LIABILITIES
    #AuthorizeTransaksi.AuthorizeOperation(config, 'IuranPeserta', \
    #  o.ID_Transaksi, 'A')
    
  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0
  
def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  config.SendDebugMsg('FormEndProcessData')
  recT = datapacket.uipTransaksi.GetRecord(0)
  
  uideflist.PrepareReturnDataset()
  recP = uideflist.uipParameter.Dataset.AddRecord()
  
  #cek kasus
  if recT.isOnlyTitipanPremi:
    #hanya bayar titipan premi

    #cek hidden id titipan premi
    if recT.HiddenIDTitipanPremi not in [None,0]:
      recP.FileSlipPremi = SlipTransaksiTeller.CreateSlip(config, \
        'TitipanPremi', recT.HiddenIDTitipanPremi, 0)
  else:
    #bisa bayar iuran doang atau bayar sekaligus iuran peserta dan titipan premi

    #cek hidden id iuran peserta
    if recT.HiddenIDIuranPeserta not in [None, 0]:
      recP.FileSlipIuran = SlipTransaksiTeller.CreateSlip(config, \
        'IuranPeserta', recT.HiddenIDIuranPeserta, 0)

  return 4
  
def downloadFile(config, parameter, returns):
  fileName = config.UserHomeDirectory + parameter.FirstRecord.fileName
  sw = returns.AddStreamWrapper()
  sw.LoadFromFile(fileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(fileName)

