#
# Fungsi BeforeCreateObject merupakan KONVENSI, 
# harus ada di setiap script import massal
#

import time, sys
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')
sys.path.append('c:/dafapp/dplk07/script_modules')

import AuthorizeTransaksi, kakasapi, moduleapi

def BeforeCreateObject(config, targetClassName, data):
  returnValue = 1
  
  #UNTUK SEMUA JENIS TRANSAKSI APAPUN, CEK BATCH YANG DIPAKAI
  oTB = config.CreatePObjImplProxy('TransactionBatch')
  config.SendDebugMsg('id tb: %s' % str(data.GetFieldByName('IDTransactionBatch')))
  oTB.Key = data.GetFieldByName('IDTransactionBatch')
  config.SendDebugMsg('oTB id tb: %s' % str(oTB.ID_TransactionBatch))

  config.SendDebugMsg('bco1')
  if oTB.IsNull or oTB.batch_status == 'C':
    config.SendDebugMsg('Batch tidak ditemukan / sudah berstatus tutup.')
    #batch tidak ditemukan atau batch sudah berstatus tutup
    kakasapi.Logging(config, targetClassName, \
      'Batch dengan ID=%s tidak ditemukan / sudah berstatus tutup.' \
      % (str(data.GetFieldByName('IDTransactionBatch'))))
    returnValue = 0
    
  config.SendDebugMsg('bco2')
  #UNTUK SEMUA JENIS TRANSAKSI APAPUN, PERIKSA STATUS REKENING / PESERTA
  noPeserta = data.GetFieldByName('NoPeserta')
  config.SendDebugMsg('bco3')
  oR = config.CreatePObjImplProxy('RekeningDPLK')
  config.SendDebugMsg('bco4')
  oR.Key = noPeserta
  config.SendDebugMsg(str(oR.IsNull))

  #config.SendDebugMsg(str(oR.No_Peserta))
  #config.SendDebugMsg(str(targetClassName))
  #config.SendDebugMsg(str(oR.Status_Biaya_Daftar))
  #config.SendDebugMsg(str(oR.Status_DPLK))
  #config.SendDebugMsg(str(time.localtime()[:3]))
  #config.SendDebugMsg(str(oR.tgl_pensiun[:3]))
  if oR.Status_Biaya_Daftar == 'F' and targetClassName != 'IuranPendaftaran':
    #belum membayar biaya pendaftaran, untuk selain transaksi yang berniat untuk 
    #mambayar biaya pendaftaran
    kakasapi.Logging(config, targetClassName, \
      'Peserta %s belum membayar biaya pendaftaran.' % (noPeserta))
    returnValue = 0  
  elif oR.Status_DPLK in ['N','S']:
    #status peserta sudah tidak aktif / suspend
    kakasapi.Logging(config, targetClassName, \
      'Peserta %s sudah tidak aktif.' % (noPeserta))
    returnValue = 0  
  elif time.localtime()[:3] > oR.tgl_pensiun[:3]:
    #peserta sudah memasuki tanggal pensiun
    kakasapi.Logging(config, targetClassName, \
      'Peserta %s sudah memasuki usia pensiun sejak %d-%d-%d.' \
      % (noPeserta,oR.tgl_pensiun[2],oR.tgl_pensiun[1],oR.tgl_pensiun[0]))
    returnValue = 0  
  config.SendDebugMsg('bco5')  
  if returnValue:
    #tidak ada permasalahan dengan batch dan status peserta, cek transaksinya
    
    if targetClassName == 'IuranPeserta':
      #cek jenis batch yang dipakai
      if oTB.batch_type != 'T':
        #yang dipakai BUKAN batch transaksi
        config.SendDebugMsg('Batch yang dipakai BUKAN batch transaksi.')
        kakasapi.Logging(config, targetClassName, \
          'batch id %d bernomor nomor %s bukan batch jenis TRANSAKSI.' \
          % (oTB.ID_TransactionBatch,oTB.no_batch))
        returnValue = 0        
      else:
        #sudah benar memakai batch transaksi
        
        #SEMUA PENGECEKAN SEMENTARA DITIADAKAN
        #cek nilai iuran peserta dan nilai iuran PK (bila ikut keanggotaan peserta korporat)
        #if data.GetFieldByName('MutasiIuranPeserta') < oR.iuran_pst:
        #  #iuran peserta kurang dari besar iuran peserta default
        #  kakasapi.Logging(config, targetClassName, \
        #    'Iuran peserta %s: Rp %f, kurang dari seharusnya (Rp %f).' \
        #    % (noPeserta,data.GetFieldByName('MutasiIuranPeserta'),oR.iuran_pst))
        #  returnValue = 0
          
        #if data.GetFieldByName('MutasiIuranPemberiKerja') not in [None,0]:
        #  #iuran pemberi kerja tidak kosong, cek keanggotaan peserta korporat
        #  if oR.LNasabahDPLK.kode_nasabah_corporate in [None,'']:
        #    #bukan anggota peserta korporat
        #    kakasapi.Logging(config, targetClassName, \
        #      'Peserta %s bukan anggota peserta korporat manapun.' % (noPeserta))
        #    returnValue = 0
        #  else:
        #    #peserta anggota korporat tertentu, cek besaran iuran PK
        #    if data.GetFieldByName('MutasiIuranPemberiKerja') < oR.iuran_pk:
        #      kakasapi.Logging(config, targetClassName, \
        #        'Iuran Pemberi Kerja peserta %s: Rp %f, kurang dari seharusnya (Rp %f).' \
        #        % (noPeserta,data.GetFieldByName('MutasiIuranPeserta'),oR.iuran_pst))
        #      returnValue = 0
        pass
            
    elif targetClassName == 'TitipanPremi':
      #cek jenis batch yang dipakai
      if oTB.batch_type != 'P':
        #yang dipakai BUKAN batch premi
        kakasapi.Logging(config, targetClassName, \
          'batch id %d bernomor nomor %s bukan batch jenis PREMI.' \
          % (oTB.ID_TransactionBatch,oTB.no_batch))
        returnValue = 0
      else:
        #cek kepesertaan wasiat ummat
        config.SendDebugMsg('bco6')
        if oR.status_wasiat_ummat == 'F':
          #peserta tidak ikut wasiat ummat
          kakasapi.Logging(config, targetClassName, \
            'Peserta %s bukan peserta wasiat ummat.' % (noPeserta))
          returnValue = 0
        else:
          #ikut menjadi peserta wasiat ummat, cek nilai titipan premi
          oRWU = moduleapi.GetRekeningWasiatUmmat(config, noPeserta)
          if not oRWU:
            #peserta tidak memiliki rekening wasiat ummat
            kakasapi.Logging(config, targetClassName, \
              'Peserta %s tidak memiliki rekening wasiat ummat.' % (noPeserta))
            returnValue = 0
          else:
            pass
            #oR.Ls_RekeningWasiatUmmat.Elements[0]
            #oRWU = oR.Ls_RekeningWasiatUmmat.Elements[0]
#             if data.GetFieldByName('MutasiPremi') < oRWU.besar_premi:
#             if (oRWU.besar_premi - data.GetFieldByName('MutasiPremi')) > moduleapi.zero_approx:
            if (oRWU.besar_premi - data.GetFieldByName('MutasiPremi')) > moduleapi.GetToleransiByrPremi(config):
              kakasapi.Logging(config, targetClassName, \
                'Titipan premi peserta %s: Rp %f, kurang \
                dari seharusnya (Rp %f).' % (noPeserta, data.GetFieldByName('MutasiPremi'),\
                oRWU.besar_premi))
              returnValue = 0

    elif targetClassName == 'IuranPendaftaran':
      #cek jenis batch yang dipakai
      if oTB.batch_type != 'R':
        #yang dipakai BUKAN batch registrasi
        kakasapi.Logging(config, targetClassName, \
          'batch id %d bernomor nomor %s bukan batch jenis REGISTRASI.' \
          % (oTB.ID_TransactionBatch,oTB.no_batch))
        returnValue = 0        
      else:
        #cek apakah peserta sudah membayar biaya pendaftaran
        if oR.Status_Biaya_Daftar == 'T':
          kakasapi.Logging(config, targetClassName, \
            'Peserta %s sudah membayar biaya pendaftaran.' % (noPeserta))
          returnValue = 0
      pass  

    elif targetClassName == 'PengalihanDariDPLKLain':
      #cek jenis batch yang dipakai
      if oTB.batch_type != 'T':
        #yang dipakai BUKAN batch transaksi
        kakasapi.Logging(config, targetClassName, \
          'batch id %d bernomor nomor %s bukan batch jenis TRANSAKSI.' \
          % (oTB.ID_TransactionBatch,oTB.no_batch))
        returnValue = 0        
      else:
        #cek apakah jenis kode dp terdefinisi
        kode_dp = data.GetFieldByName('KodeDP')
        oLDP = config.CreatePObjImplProxy('LDP')
        oLDP.Key = kode_dp
        if oLDP.IsNull:
          kakasapi.Logging(config, targetClassName, \
            'Kode DP %s tidak terdefinisi.' % (kode_dp))
          returnValue = 0
        #else:
        #  #cek apakah jenis dp dari ldp yang dipilih sesuai dengan transaksi pengalihannya
  
      pass  

    else:
      #error, classname tidak terdefinisi
      #lebih baik log untuk data yang ini, tergantung konfigurasi import massal
      pass

  return returnValue

def SetObjAndAuthorize(config, obj, className):
  #tanggal dan branch code mengikuti tanggal pakai dan branch code Transaction batch
  config.SendDebugMsg('SetObjAndAuthorize1')
  config.SendDebugMsg('id transaksi: %s' % str(obj.ID_Transaksi))
  oTB = obj.LTransactionBatch

  config.SendDebugMsg('SetObjAndAuthorize2')
  y,m,d = oTB.tgl_used[:3]
  obj.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)

  config.SendDebugMsg('SetObjAndAuthorize3')
  if className != 'IuranPendaftaran':
    obj.branch_code = oTB.branch_code  

  config.SendDebugMsg('SetObjAndAuthorize4')
  #assign properti common
  obj.isCommitted = 'F'
  obj.user_id = config.SecurityContext.UserID
  obj.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  obj.tgl_sistem = config.Now()

  config.SendDebugMsg('SetObjAndAuthorize5')
  #autorisasi transaksi
  AuthorizeTransaksi.AuthorizeOperationNonTrans(config, className, obj.ID_Transaksi, 'A')
  config.SendDebugMsg('SetObjAndAuthorize6')

def ProcessingImport(config, obj, data):  
  #cek berdasarkan classname obj untuk mengetahui jenis transaksinya
  config.SendDebugMsg('ProcessingImport start')
  className = obj.ClassName

  if className == 'IuranPeserta':
    config.SendDebugMsg('IuranPeserta')
    #transaksi iuran peserta
    config.SendDebugMsg(data.GetFieldByName('NoPeserta'))
    obj.mutasi_pengembangan = obj.mutasi_peralihan = 0.0
    if obj.mutasi_iuran_pk == None: obj.mutasi_iuran_pk = 0.0 #add by ita 21 June 2010
    config.SendDebugMsg('IuranPeserta1')
    obj.catatan_bayar_iuran = 'Iuran peserta hasil impor massal tgl %s' \
      % (time.asctime(time.localtime()))

    config.SendDebugMsg('IuranPeserta2')
    #tanggal dan branch code mengikuti tanggal pakai dan branch code Transaction batch
    #oTB = config.CreatePObjImplProxy('TransactionBatch')
    #oTB.Key = data.GetFieldByName('IDTransactionBatch')

    #y,m,d = oTB.tgl_used[:3]
    #obj.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)
    #obj.branch_code = oTB.branch_code  
  
  elif className == 'TitipanPremi':
    #transaksi titipan premi
    obj.isDebet = 'F'

  elif className == 'IuranPendaftaran':
    #transaksi pembayaran pendaftaran
    obj.LRekeningDPLK.Status_Biaya_Daftar = 'T'

#   elif className == 'PengalihanDariDPLKLain':
#     jenis_dp = obj.LLDP.jenis_dp
#     if jenis_dp == 'B':
#       #transaksi pengalihan dari DPLK lain
#       obj.saldo_iuran_pk = 0.0
# 
#       obj.mutasi_iuran_pk = 0.0
#       obj.mutasi_iuran_pst = obj.saldo_iuran_pk + obj.saldo_iuran_pst 
#       obj.mutasi_pengembangan = obj.saldo_pengembangan
#       obj.mutasi_peralihan = obj.saldo_peralihan
# 
#     elif jenis_dp in ['A', 'C']:
#       #transaksi pengalihan dari DPK atau DPPK lain
# 
#       if jenis_dp == 'A':
#         # DPPK
#         obj.kode_jenis_transaksi = 'O'
#       else:
#         # jenis_dp == 'C'
#         # DPK
#         obj.kode_jenis_transaksi = 'P'
# 
#       obj.mutasi_iuran_pk = obj.mutasi_iuran_pst = obj.mutasi_pengembangan = 0.0
#       obj.mutasi_peralihan = obj.saldo_iuran_pk + obj.saldo_iuran_pst + \
#         obj.saldo_pengembangan + obj.saldo_peralihan
#     else:
#       #error, jenis_dp tidak terdefinisi
#       raise Exception, 'Kesalahan Jenis DP' + 'Jenis DP %s tidak terdefinisi.' % (jenis_dp)
# 
#       #kakasapi.Logging(config, className, \
#       #  'Jenis DP %s tidak terdefinisi.' % (jenis_dp))

  else:
    #error, classname tidak terdefinisi
    #lebih baik log untuk data yang ini, tergantung konfigurasi import massal
    pass

  config.SendDebugMsg('proc last')
  SetObjAndAuthorize(config, obj, className)

def ImportPengalihanDPLK(config, obj, data):
  if obj.LLDP.jenis_dp != 'B':
    raise Exception, 'Kesalahan Kode DP' + 'Kode DP %s bukan Lembaga Dana Pensiun yang termasuk DPLK.' % (obj.kode_dp)

  #transaksi pengalihan dari DPLK lain
  obj.saldo_iuran_pk = 0.0

  obj.mutasi_iuran_pk = 0.0
  obj.mutasi_iuran_pst = obj.saldo_iuran_pk + obj.saldo_iuran_pst 
  obj.mutasi_pengembangan = obj.saldo_pengembangan
  obj.mutasi_peralihan = obj.saldo_peralihan

  SetObjAndAuthorize(config, obj, obj.ClassName)

def ImportPengalihanDPPK(config, obj, data):
  if obj.LLDP.jenis_dp != 'A':
    raise Exception, 'Kesalahan Kode DP' + 'Kode DP %s bukan Lembaga Dana Pensiun yang termasuk DPPK.' % (obj.kode_dp)

  # DPPK
  obj.kode_jenis_transaksi = 'O'

  #transaksi pengalihan dari DPPK lain
  obj.mutasi_iuran_pk = obj.mutasi_iuran_pst = obj.mutasi_pengembangan = 0.0
  obj.mutasi_peralihan = obj.saldo_iuran_pk + obj.saldo_iuran_pst + \
    obj.saldo_pengembangan + obj.saldo_peralihan

  SetObjAndAuthorize(config, obj, obj.ClassName)

def ImportPengalihanDPK(config, obj, data):
  if obj.LLDP.jenis_dp != 'C':
    raise Exception, 'Kesalahan Kode DP' + 'Kode DP %s bukan Lembaga Dana Pensiun yang termasuk DPK.' % (obj.kode_dp)

  # DPPK
  obj.kode_jenis_transaksi = 'P'

  #transaksi pengalihan dari DPK lain
  obj.mutasi_iuran_pk = obj.mutasi_iuran_pst = obj.mutasi_pengembangan = 0.0
  obj.mutasi_peralihan = obj.saldo_iuran_pk + obj.saldo_iuran_pst + \
    obj.saldo_pengembangan + obj.saldo_peralihan

  SetObjAndAuthorize(config, obj, obj.ClassName)
