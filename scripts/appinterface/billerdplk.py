import sys, os
#DAFAPP_DIR = 'c:/dafapp/dplk07/'#os.environ.get("DAFAPPSERVER_ROOTDIR")
#sys.path.append(DAFAPP_DIR + "scripts/transaksi")
#sys.path.append(DAFAPP_DIR + "script_modules")
#import CekPesertaDPLK, transaksiapi, AuthorizeTransaksi


import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "scripts#transaksi.CekPesertaDPLK",
    "scripts#transaksi.transaksiapi",
    "scripts#transaksi.AuthorizeTransaksi"
  ]
)


# GLOBALS
PREFIX_BATCH = {'8901':'T','8902':'R','8903':'P'}

def DAFScriptMain(config, parameters, result):
  #import rpdb2; rpdb2.start_embedded_debugger("000")
   
  sRequest = parameters.FirstRecord.data
  request = eval(sRequest)
  trcode = request['trcode']
  if trcode == 'inq':
    reply, status, errmsg = InquiryAccount(config, request)
  elif trcode == 'trx':
    reply, status, errmsg = TransactionAccount(config, request)
  else:
    reply, status, errmsg = {}, 0, "Unknown trcode"
  
  reply['status'] = status
  reply['errmsg'] = errmsg
  sResponse = str(reply)
  result.CreateSimpleDataPacket().data = sResponse
  
  return 0
#--

def runSQL(config, sSQL):
  i = config.ExecSQL(sSQL)
  if i == -9999:
    raise 'SQL Error', config.GetDBConnErrorInfo()
  #--
#-- 

def InquiryAccount(config, request):
  # vaNumber ialah nomor peserta DPLK
  reply = {}
  try:
    vaPrefix = request['vaPrefix']
    vaNumber = request['vaNumber']
    # cek peserta dplk
    statusPeserta = CekPesertaDPLK.CekNomorPeserta(config, vaNumber)
    if not statusPeserta:
      raise 'Error Biller DPLK','Nomor peserta DPLK tidak ditemukan!'
    elif statusPeserta == 2:
      raise 'Error Biller DPLK','Peserta DPLK sudah tidak aktif!'
    elif statusPeserta == 3:
      raise 'Error Biller DPLK','Peserta DPLK berstatus suspend!'
      
    # ambil objek rekening dplk
    oRekening = config.CreatePObjImplProxy('RekeningDPLK')
    oRekening.Key = vaNumber
    
    # inquiry berdasarkan vaPrefix
    if PREFIX_BATCH[vaPrefix] == 'T':
      # iuran peserta
      amount = oRekening.iuran_pst
    elif PREFIX_BATCH[vaPrefix] == 'R':
      # registrasi, cek status biaya daftar peserta
      # ditutup by ade herman 2010-11-08
      #if oRekening.status_biaya_daftar == 'T':
      #  raise 'Error Biller DPLK','Peserta DPLK sudah melunasi biaya pendaftaran!'
      
      # ambil biaya pendaftaran
      oParameter = config.CreatePObjImplProxy('Parameter')
      oParameter.Key = 'BESAR_BIAYA_DAFTAR'
      amount = oParameter.Numeric_Value
    elif PREFIX_BATCH[vaPrefix] == 'P':
      # premi, perlu cek keanggotaan wasiat ummat
      if oRekening.status_wasiat_ummat != 'T':
        raise 'Error Biller DPLK','Peserta DPLK tidak ikut Wasiat Ummat!'
        
      # status ikut wasiat ummat, cek polis
      sSQL = "select besar_premi from RekeningWasiatUmmat where no_peserta = %s" \
        % config.ModLibUtils.QuotedStr(oRekening.no_peserta)
      rSQL = config.CreateSQL(sSQL).RawResult
      
      if rSQL.Eof:
        # data peserta Wasiat Ummat tidak ditemukan
        raise 'Error Biller DPLK','Peserta termasuk peserta Wasiat Ummat, tetapi data ' \
          'Rekening Wasiat Ummat peserta %s tidak ditemukan. Hubungi Pengelola DPLK!'
      else:
        amount = rSQL.besar_premi
    else:
      # transaksi tidak terdefinisi
      raise 'Error Biller DPLK','Inquiry transaksi DPLK tidak terdefinisi!'
    
    # reply request 
    reply['nama_rekening'] = oRekening.LNasabahDPLK.nama_lengkap
    # kode valuta fix rupiah
    reply['kode_valuta'] = '000'
    reply['kode_cabang'] = oRekening.kode_cab_daftar
    reply['amount'] = amount
    reply['allow_define_amount'] = 1
    reply['cost'] = 0
    reply['allow_define_cost'] = 1 
    
    status = 1
    errmsg = ""
  except:
    status = 0
    errmsg = str(sys.exc_info()[0]) + "." + str(sys.exc_info()[1])
  #--
  
  return reply, status, errmsg

def TransactionAccount(config, request):
  reply = {}
  mlu = config.ModLibUtils
  
  config.SendDebugMsg(str(request))
  config.BeginTransaction()
  try:
    vaNumber = request['vaAccount']
    vaPrefix = request['vaPrefix']
    dtTanggal = request['tanggal_transaksi']
    user = request['user']
    terminal = request['terminal']
    cabang = request['cabang']
  
    # buat batch dplk sesuai dengan transaksi-nya
    config.SendDebugMsg('a')
    oBatch = transaksiapi.CreateBatch(config, PREFIX_BATCH[vaPrefix], 'T', dtTanggal, \
      user, cabang, terminal)
    config.SendDebugMsg('b')  
    # buat transaksi berdasarkan vaPrefix: iuran, registrasi, premi
    if PREFIX_BATCH[vaPrefix] == 'T':
      # iuran peserta
      oTransaksi = IuranPeserta(config, request, oBatch)
      #oR = config.CreatePObjImplProxy('RekeningDPLK')
      #oR.Key = vaNumber
      #oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + oTransaksi.mutasi_iuran_pst

      config.SendDebugMsg('b')
    elif PREFIX_BATCH[vaPrefix] == 'R':
      # registrasi peserta
      oTransaksi = RegistrasiPeserta(config, request, oBatch)
    elif PREFIX_BATCH[vaPrefix] == 'P':
      # premi peserta
      oTransaksi = PremiPeserta(config, request, oBatch)
    else:
      # transaksi tidak terdefinisi
      raise 'Error Biller DPLK','Transaksi DPLK tidak terdefinisi!'

    #oTransaksi.user_id_auth = 'SYSTEM' #config.SecurityContext.user
    #oTransaksi.terminal_id_auth = terminal  #config.SecurityContext.GetSessionInfo()[1]
    #oTransaksi.tgl_otorisasi = config.Now()

    config.Commit()
    status = 1
    errmsg = ""
  except:
    status = 0
    errmsg = str(sys.exc_info()[0]) + "." + str(sys.exc_info()[1])
    config.Rollback()
  
  # reply request
  reply['refbiller'] = str(oTransaksi.ID_Transaksi)[:20]    
  config.SendDebugMsg('end')
  return reply, status, errmsg

def IuranPeserta(config, request, oBatch):
  # buat transaksi iuran peserta
  o = config.CreatePObject('IuranPeserta')
  o.tgl_transaksi = request['tanggal_transaksi']
  o.no_peserta = request['vaAccount']
  o.keterangan = request['keterangan']
  o.ID_TransactionBatch = oBatch.ID_TransactionBatch
  o.branch_code = oBatch.branch_code
  o.catatan_bayar_iuran = request['keterangan']

  o.mutasi_iuran_pst = request['mutasi']
  o.mutasi_iuran_pk = 0.0
  o.mutasi_pengembangan = o.mutasi_peralihan = 0.0

  #assign kode paket investasi current
  transaksiapi.SetPaketInvestasi(config, o)
      
  o.isCommitted = 'T'
  o.user_id = request['user']
  o.terminal_id = request['terminal']
  o.tgl_sistem = config.Now()

  # jika pindah buku
  o.isPindahBuku = request['isPinbuk']
  o.Rekening_Pindah_Buku = request['pinbukFromAccount']
  #o.Tipe_Rekening_Pindah_Buku =

  # referensi core banking
  o.Ref_CoreBanking = request['ref']

  # otorisasi transaksi iuran peserta
  
  return o

def PremiPeserta(config, request, oBatch):
  # buat transaksi premi peserta
  o = config.CreatePObject('TitipanPremi')
  o.tgl_transaksi = request['tanggal_transaksi']
  o.no_peserta = request['vaAccount']
  o.keterangan = request['keterangan']
  o.mutasi_premi = request['mutasi']
  o.ID_TransactionBatch = oBatch.ID_TransactionBatch
  o.branch_code = oBatch.branch_code
  o.isDebet = 'F'
  
  o.isCommitted = 'T'
  o.user_id = request['user']
  o.terminal_id = request['terminal']
  o.tgl_sistem = config.Now()
  
  #cek kewajiban wasiat ummat dan status kolektibilitas
  AuthorizeTransaksi.SetKolektibilitasWasiatUmmat(config, o.LRekeningDPLK, o)

  # jika pindah buku
  o.isPindahBuku = request['isPinbuk']
  o.Rekening_Pindah_Buku = request['pinbukFromAccount']
  #o.Tipe_Rekening_Pindah_Buku =

  # referensi core banking
  o.Ref_CoreBanking = request['ref']
  
  # otorisasi transaksi premi

  return o

def RegistrasiPeserta(config, request, oBatch):
  # buat transaksi registrasi peserta
  o = config.CreatePObject('IuranPendaftaran')
  o.tgl_transaksi = request['tanggal_transaksi']
  o.no_peserta = request['vaAccount']
  o.keterangan = request['keterangan']
  o.ID_TransactionBatch = oBatch.ID_TransactionBatch
  o.branch_code = oBatch.branch_code
  o.besar_biaya_daftar = request['mutasi']
  
  o.isCommitted = 'T'
  o.user_id = request['user']
  o.terminal_id = request['terminal']
  o.tgl_sistem = config.Now()
  
  # referensi core banking
  o.Ref_CoreBanking = request['ref']

  # otorisasi bayar registrasi

  return o
