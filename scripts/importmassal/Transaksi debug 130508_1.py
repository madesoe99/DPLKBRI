#
# Fungsi BeforeCreateObject merupakan KONVENSI, 
# harus ada di setiap script import massal
#

import time, sys
sys.path.append('c:/Python23/Lib/site-packages')
import rpdb2

sys.path.append('c:/dafapp/dplk07/scripts/transaksi')
sys.path.append('c:/dafapp/dplk07/script_modules')

import AuthorizeTransaksi, kakasapi

def BeforeCreateObject(config, targetClassName, data):
  rpdb2.start_embedded_debugger("0102")

  returnValue = 1
  
  #UNTUK SEMUA JENIS TRANSAKSI APAPUN, CEK BATCH YANG DIPAKAI
  oTB = config.CreatePObjImplProxy('TransactionBatch')
  oTB.Key = data.GetFieldByName('IDTransactionBatch')
  
  if oTB.IsNull or oTB.batch_status == 'C':
    #batch tidak ditemukan atau batch sudah berstatus tutup
    kakasapi.Logging(config, targetClassName, \
      'Batch dengan ID=%s tidak ditemukan / sudah berstatus tutup.' \
      % (str(data.GetFieldByName('IDTransactionBatch'))))
    returnValue = 0
    
  #UNTUK SEMUA JENIS TRANSAKSI APAPUN, PERIKSA STATUS REKENING / PESERTA
  noPeserta = data.GetFieldByName('NoPeserta') 
  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.Key = noPeserta
  
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
  
  if returnValue:
    #tidak ada permasalahan dengan batch dan status peserta, cek transaksinya
    
    if targetClassName == 'IuranPeserta':
      #cek jenis batch yang dipakai
      if oTB.batch_type != 'T':
        #yang dipakai BUKAN batch transaksi
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
        if oR.status_wasiat_ummat == 'F':
          #peserta tidak ikut wasiat ummat
          kakasapi.Logging(config, targetClassName, \
            'Peserta %s bukan peserta wasiat ummat.' % (noPeserta))
          returnValue = 0  
        else:
          #ikut menjadi peserta wasiat ummat, cek nilai titipan premi
          oRWU = oR.Ls_RekeningWasiatUmmat.Elements[0]
          if data.GetFieldByName('MutasiPremi') < oRWU.besar_premi:
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

    else:
      #error, classname tidak terdefinisi
      #lebih baik log untuk data yang ini, tergantung konfigurasi import massal
      pass

  return returnValue

def ProcessingImport(config, obj, data):  
  #cek berdasarkan classname obj untuk mengetahui jenis transaksinya
  className = obj.ClassName
  
  if className == 'IuranPeserta':
    #transaksi iuran peserta
    obj.mutasi_pengembangan = obj.mutasi_peralihan = 0.0
    obj.catatan_bayar_iuran = 'Iuran peserta hasil impor massal tgl %s' \
      % (time.asctime(time.localtime()))
      
    #tanggal dan branch code mengikuti tanggal pakai dan branch code Transaction batch
    oTB = config.CreatePObjImplProxy('TransactionBatch')
    oTB.Key = data.GetFieldByName('IDTransactioBatch')
    
    obj.tgl_transaksi = oTB.tgl_used
    obj.branch_code = oTB.branch_code  
  
  elif className == 'TitipanPremi':
    #transaksi titipan premi
    obj.isDebet = 'F'
  
  elif className == 'IuranPendaftaran':
    #transaksi pembayaran pendaftaran
    obj.LRekeningDPLK.Status_Biaya_Daftar = 'T'

  else:
    #error, classname tidak terdefinisi
    #lebih baik log untuk data yang ini, tergantung konfigurasi import massal
    pass
    
  #tanggal dan branch code mengikuti tanggal pakai dan branch code Transaction batch
  oTB = obj.LTransactionBatch
  
  y,m,d = oTB.tgl_used[:3]
  obj.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)
  
  if className != 'IuranPendaftaran':
    obj.branch_code = oTB.branch_code  
  
  #assign properti common
  obj.isCommitted = 'F'
  obj.user_id = config.SecurityContext.UserID
  obj.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  obj.tgl_sistem = config.Now()
  
  #autorisasi transaksi
  AuthorizeTransaksi.AuthorizeOperation(config, className, obj.ID_Transaksi, 'A')
