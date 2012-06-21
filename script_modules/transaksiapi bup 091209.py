import string, rotor, sys
sys.path.append('c:/dafutils')
sys.path.append('c:/dafapp/dplk07/script_modules')
import batchutils
import messagelib
import com.ihsan.lib.trace as trace

def GetKasTeller(userid, host, port):
  kasteller = ''
  messagereq = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%.2f;%s;%s;%s;%s;%s;%s;%s' % (
          'GTLR', '', '', '', '', '', '', '', '', 0.0,
          userid, '', '', '', '', '', '')

  messageresp = messagelib.SendStreamMsg(messagereq, host, port)
  trace.udp_trace(messageresp)
  messageresp = messageresp.split(';')
  if len(messageresp) < 6:
    raise '90', 'Error receiving data from kiblat : ' + str(messageresp)
  else:
    kasteller = messageresp[5]

  return kasteller

#-------------------------------------------------------------------------------
## PERHITUNGAN PAJAK
#-------------------------------------------------------------------------------

def TotalPenarikanSebelumnya(config, tgl_transaksi, noPeserta):
  #jumlahkan total dana yang sudah pernah ditarik dalam 1 tahun
  y,m,d = config.ModLibUtils.DecodeDate(tgl_transaksi)
  tgl_akhir = '%s/%s/%d' % (string.zfill(str(m),2),string.zfill(str(d),2),y)
  tgl_awal = '%s/%s/%d' % ('01','01',y)
  
  sOQL = 'select from PenarikanDana [tgl_transaksi >= \'%s\' ' \
    'and tgl_transaksi <= \'%s\' and LRekeningDPLK.no_peserta = \'%s\'] ' \
    '(no_peserta, jml_tarik, self) then group by no_peserta ' \
    'columns jml_tarik sum;' % (tgl_awal, tgl_akhir, noPeserta)    

  iOQL = config.OQLEngine.CreateOQL(sOQL)
  iOQL.Active = 1 
  rOQL = iOQL.RawResult
  
  rOQL.First()
  if rOQL.Eof:
    total_sebelum = 0.0
  else:
    total_sebelum = rOQL.column1    

  return total_sebelum

def HitungPajakTarikDana(config, akena_pajak, total_sebelum):

  #ambil parameter batas dan persentase pajak tarik dana
  batas1 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas1')
  batas2 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas2')
  batas3 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas3')
  batas4 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas4')
  batas5 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas5')
  
  persenBatas1 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas1')
  persenBatas2 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas2')
  persenBatas3 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas3')
  persenBatas4 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas4')
  persenBatas5 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas5')

  akum_kena_pajak = total_sebelum+akena_pajak
  config.SendDebugMsg('akum_kena_pajak '+ str(akum_kena_pajak))
  config.SendDebugMsg('batas1 '+ str(batas1))
  config.SendDebugMsg('batas2 '+ str(batas2))
  if akum_kena_pajak <= batas1:
    config.SendDebugMsg('pjk2')
    Result = akena_pajak * (persenBatas1 / 100.0)
  elif (akum_kena_pajak > batas1) and (akum_kena_pajak <= batas2):
    config.SendDebugMsg('pjk3')
    if total_sebelum >= batas1:
      Result = akena_pajak * (persenBatas2 / 100.0)
    else:
      kena_pajak1 = batas1 - total_sebelum
      Result = (persenBatas1 / 100.0) * kena_pajak1
      Result = Result + (persenBatas2 / 100.0) * (akena_pajak - kena_pajak1)
  elif akum_kena_pajak > batas2:
    config.SendDebugMsg('pjk4')
    config.SendDebugMsg('total_sebelum '+ str(total_sebelum))
    if total_sebelum >= batas2:
      Result = (persenBatas3 / 100.0) * akena_pajak
    elif (total_sebelum >= batas1) and (total_sebelum < batas2):
      kena_pajak1 = batas2 - total_sebelum
      Result = (persenBatas2 / 100.0) * kena_pajak1
      Result = Result + (persenBatas3 / 100.0) * (akena_pajak-kena_pajak1)
    elif (total_sebelum < batas1):
      kena_pajak1 = batas1 - total_sebelum
      Result = (persenBatas1 / 100.0) * kena_pajak1
      kena_pajak2 = akena_pajak-kena_pajak1
      config.SendDebugMsg('kena_pajak1 '+ str(kena_pajak1))
      config.SendDebugMsg('Result '+ str(Result))
      config.SendDebugMsg('kena_pajak2 '+ str(kena_pajak2))
      if kena_pajak2 <= batas2:
        Result = Result + (persenBatas2 / 100.0) * kena_pajak2
        config.SendDebugMsg('Result1 '+ str(Result))
      else:
        Result = Result + (persenBatas2 / 100.0) * batas1
        config.SendDebugMsg('Result2 '+ str(Result))
        #kena_pajak3 = kena_pajak2 - batas2
        kena_pajak3 = akena_pajak - batas2
        Result = Result + kena_pajak3 * (persenBatas3 / 100.0)
        config.SendDebugMsg('kena_pajak3 '+ str(kena_pajak3))
        config.SendDebugMsg('Result3 '+ str(Result))
  config.SendDebugMsg('pjk5')

  return Result

def HitungPajakTarikDanaAsli(akena_pajak, total_sebelum):

  akum_kena_pajak = total_sebelum+akena_pajak
  if akum_kena_pajak <= 25E+6:
    Result = akena_pajak * 10 / 100
  elif (akum_kena_pajak > 25E+6) and (akum_kena_pajak <= 50E+6):
    if total_sebelum >= 25E+6:
      Result = akena_pajak * 15 / 100
    else:
      kena_pajak1 = 25E+6 - total_sebelum
      Result = 10 / 100 * kena_pajak1
      Result = Result + 15 / 100 * (akena_pajak - kena_pajak1)
  elif akum_kena_pajak > 50E+6:
    if total_sebelum >= 50E+6:
      Result = 30 / 100 * akena_pajak
    elif (total_sebelum >= 25E+6) and (total_sebelum < 50E+6):
      kena_pajak1 = 50E+6 - total_sebelum
      Result = 15 / 100 * kena_pajak1
      Result = result + 30 / 100 * (akena_pajak-kena_pajak1)
    elif (total_sebelum < 25E+6):
      kena_pajak1 = 25E+6 - total_sebelum
      result = 10 / 100 * kena_pajak1
      kena_pajak2 = akena_pajak-kena_pajak1
      if kena_pajak2 <= 50E+6:
        Result = Result + 15 / 100 * kena_pajak2
      else:
        Result = Result + 15 / 100 * 25E+6
        kena_pajak3 = kena_pajak2 - 50E+6
        Result = Result + kena_pajak3 * 30 / 100

  return Result

def HitungPajakPengambilanManfaat(config, AValue):
  
  #ambil parameter batas dan persentase pajak tarik dana
  batas1 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas1')
  batas2 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas2')
  batas3 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas3')
  batas4 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas4')
  batas5 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas5')
  
  persenBatas1 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas1')
  persenBatas2 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas2')
  persenBatas3 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas3')
  persenBatas4 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas4')
  persenBatas5 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas5')

  if AValue >= batas1: ## (0 - 25 jt)
    Result = 0
    AValue = AValue - batas1
  else:
    return 0

  if AValue >= batas1: ## (25 - 50 jt)
    Result = Result + batas1 * (persenBatas2 / 100.0)
    AValue = AValue - batas1
  else:
    return Result + AValue * (persenBatas2 / 100.0)

  if AValue >= 50E6: ## (50 - 100 jt)
    Result = Result + batas2 * (persenBatas3 / 100.0)
    AValue = AValue - batas2
  else:
    return Result + AValue * (persenBatas3 / 100.0)

  if AValue >= 100E6: ## (100 - 200 jt)
    Result = Result + batas3 * (persenBatas4 / 100.0)
    AValue = AValue - batas3
  else:
    return Result + AValue * (persenBatas4 / 100.0)

  return Result + AValue * (persenBatas5 / 100.0) ## > 200 jt

def HitungPajakPengambilanManfaatAsli(AValue):
  
  if AValue >= 25E6: ## (0 - 25 jt)
    Result = 0
    AValue = AValue - 25E6
  else:
    return 0

  if AValue >= 25E6: ## (25 - 50 jt)
    Result = Result + 25E6 * (5.0 / 100.0)
    AValue = AValue - 25E6
  else:
    return Result + AValue * (5.0 / 100.0)

  if AValue >= 50E6: ## (50 - 100 jt)
    Result = Result + 50E6 * (10.0 / 100.0)
    AValue = AValue - 50E6
  else:
    return Result + AValue * (10.0 / 100.0)

  if AValue >= 100E6: ## (100 - 200 jt)
    Result = Result + 100E6 * (15.0 / 100.0)
    AValue = AValue - 100E6
  else:
    return Result + AValue * (15.0 / 100.0)

  return Result + AValue * (25.0 / 100.0) ## > 200 jt

#-------------------------------------------------------------------------------
## PERHITUNGAN PROPORSIONAL BIAYA PENGELOLAAN / BIAYA ADMINISTRASI
#-------------------------------------------------------------------------------

def HitungProporsiBiaya(config, kode_jenis_transaksi, no_peserta, tgl_transaksi):

  #cari tanggal transaksi terakhir    
  sSQL = 'select top 1 TGL_TRANSAKSI from TRANSAKSIDPLK ' \
         'where KODE_JENIS_TRANSAKSI = \'%s\' and ' \
         'NO_PESERTA = \'%s\' and ISCOMMITTED = \'T\' ' \
         'order by TGL_TRANSAKSI desc' \
         % (kode_jenis_transaksi, no_peserta)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  if rSQL.Eof:
    #belum pernah melakukan pengambilan manfaat atau pengalihan ke DPLK lain
    #rentang hari dari tanggal registrasi
    oN = config.CreatePObjImplProxy('NasabahDPLK')
    oN.Key = no_peserta
    
    tglawal = config.ModLibUtils.EncodeDate(oN.tgl_registrasi[0], \
      oN.tgl_registrasi[1],oN.tgl_registrasi[2])
  else:
    #sudah pernah melakukan pengambilan manfaat atau pengalihan ke DPLK lain
    #rentang hari dari tanggal transaksi OUT terakhir

    tglawal = config.ModLibUtils.EncodeDate(rSQL.tgl_transaksi[0], \
      rSQL.tgl_transaksi[1],rSQL.tgl_transaksi[2])     
        
  tglakhir = config.ModLibUtils.EncodeDate(tgl_transaksi[0],tgl_transaksi[1], \
    tgl_transaksi[2])
        
  #tentukan proporsi dari rentang hari
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'JUMLAH_HARI_SETAHUN'
  
  if tglakhir - tglawal >= oP.Numeric_Value:
    #lebih dari atau lebih dari 1 tahun
    proporsi = 1.0
  else:
    #kurang dari 1 tahun
    proporsi = (tglakhir - tglawal) / oP.Numeric_Value
    
  #debug code
  #config.SendDebugMsg(str(proporsi))

  return proporsi

def HitungProporsiBiayaAdmTahunan(config, no_peserta, tgl_transaksi):

  oN = config.CreatePObjImplProxy('NasabahDPLK')
  oN.Key = no_peserta
  
  tgl_reg = oN.tgl_registrasi
  thn_registrasi = tgl_reg[0]; bln_registrasi = tgl_reg[1]
  # tahun & bulan dijalankannya proses pengenaan biaya administrasi tahunan
  thn_transaksi = tgl_transaksi[0]
  bln_transaksi = tgl_transaksi[1]

  #tentukan proporsi dari rentang bulan
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PERIODE_BIAYA_ADM'
  periode = oP.Numeric_Value
  
  if thn_registrasi < thn_transaksi:#registrasi tahun lalu    
    proporsi = 1.0
  else:# tgl_registrasi sama dg tanggal transaksi
    modbln = bln_registrasi % periode
    if modbln == 0: 
      proporsi = 1 / periode
    else:
      proporsi = (periode - modbln + 1) / periode      

  return proporsi


#-------------------------------------------------------------------------------
## PENGAMBILAN INFORMASI LOGIN APLIKASI AKUNTANSI
#-------------------------------------------------------------------------------

def GetLoginAkuntansi(config):
  ServerName = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','ServerName')
  AppName = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','AppName')
  Session_Name = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','Session_Name')
  UserID = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','UserID')    
  
  cryptedPasswd = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','Password')
  rt = rotor.newrotor(UserID, 19)
  Password = rt.decrypt(cryptedPasswd)

  return [ServerName,AppName,Session_Name,UserID,Password]

#-------------------------------------------------------------------------------
## ASSIGN PAKET INVESTASI UNTUK TIAP TRANSAKSI DPLK 'EXECUTED'
#-------------------------------------------------------------------------------

def SetPaketInvestasi(config, oTransaksi):

  #ambil current paket investasi dari rekening DPLK dan set ke Transaksi DPLK 
  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.Key = oTransaksi.no_peserta

  oTransaksi.kode_paket_investasi = oR.kode_paket_investasi

def CekKoneksiCoreBanking(config):
  sessionID = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'AppName') + \
    config.SecurityContext.UserID
  if not config.AppObject.lookuprsession(sessionID):
    raise 'Error koneksi core banking', 'User %s tidak terhubung ke core banking' % config.SecurityContext.UserID
  return sessionID

#-------------------------------------------------------------------------------
## SETOR TUNAI DPLK, KONEKSI KE CORE BANKING
#-------------------------------------------------------------------------------
'''def SetorTunaiCoreBanking(config, noBatch, noPeserta, namaLengkap, noGiro, \
  idTransaksi, nominal, keterangan):

  sessionID = CekKoneksiCoreBanking(config)
  param = config.AppObject.CreateValues(\
    ['NomorBatch', noBatch],
    ['NomorPeserta', noPeserta],
    ['NamaPeserta', namaLengkap],
    ['NomorRekeningGiro', noGiro],
    ['NomorReferensi', hex(idTransaksi)[2:]],
    ['Nominal', nominal],
    ['Keterangan', keterangan])

  try:
    #remote eksekusi creating giro core banking untuk setor tunai
    ph = config.AppObject.rexecscript(sessionID,'remote/SetorTunaiDPLK',param,1)
    if ph.FirstRecord.IsErr:
      raise '\nError Giro %s' % (noGiro), str(ph.FirstRecord.ErrMessage)
  except:
    raise
  
  return ph.FirstRecord.NoReferensi
'''

def SetorTunaiCoreBanking(config, noBatch, noPeserta, namaLengkap, noGiro, \
  idTransaksi, nominal, keterangan):
#   import rpdb2; rpdb2.start_embedded_debugger("000")  
  userid = config.SecurityContext.UserID  
  Host = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'HostCoreBanking')
  Port = int(config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'PortCoreBanking'))
  config.BeginTransaction()
  session = batchutils.begin_session(config)
  try:
    no_referensi = ''
    nokasteller = GetKasTeller(userid, Host, Port)
    batchutils.new_transaction(config, session, noBatch, nokasteller, '10', keterangan, 'IURAN DPLK '+noPeserta+'/'+namaLengkap, 'D', nominal)
    batchutils.new_transaction(config, session, noBatch, noGiro, '10', keterangan, 'IURAN DPLK '+noPeserta+'/'+namaLengkap, 'C', nominal)
    no_referensi = str(config.Now())
    batchutils.commit_session(config, session, noBatch)
    
    config.Commit()
  except:
    batchutils.rollback_session(config, session, noBatch)
    config.Rollback()
    
  return no_referensi  
#-------------------------------------------------------------------------------
## PINDAH BUKU, KONEKSI KE CORE BANKING
#-------------------------------------------------------------------------------

'''def PindahBukuCoreBanking(config, noBatch, noPeserta, namaLengkap, noGiro, \
  idTransaksi, nominal, rekeningPindahBuku, tipeRekeningPindahBuku, keterangan):

  sessionID = CekKoneksiCoreBanking(config)
  param = config.AppObject.CreateValues(\
    ['NomorBatch', noBatch],
    ['NomorPeserta', noPeserta],
    ['NamaPeserta', namaLengkap],
    ['NomorRekeningGiro', noGiro],
    ['NomorReferensi', hex(idTransaksi)[2:]],
    ['Nominal', nominal],
    ['Keterangan', keterangan],
    ['NomorRekeningDebet',rekeningPindahBuku],
    ['JenisRekeningDebet',tipeRekeningPindahBuku])

  try:
    #remote eksekusi creating giro core banking untuk pindah buku
    ph = config.AppObject.rexecscript(sessionID,'remote/PindahBukuDPLK',param,1)
    if ph.FirstRecord.IsErr:
      raise '\nError Giro %s' % (noGiro), str(ph.FirstRecord.ErrMessage)
  except:
    raise

  return ph.FirstRecord.NoReferensi'''

def PindahBukuCoreBanking(config, noBatch, noPeserta, namaLengkap, noGiro, \
  idTransaksi, nominal, rekeningPindahBuku, tipeRekeningPindahBuku, keterangan):

  userid = config.SecurityContext.UserID  
  Host = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'HostCoreBanking')
  Port = int(config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'PortCoreBanking'))
  config.BeginTransaction()
  session = batchutils.begin_session(config)
  try:
    no_referensi = ''
    batchutils.new_transaction(config, session, noBatch, rekeningPindahBuku, tipeRekeningPindahBuku, keterangan, 'IURAN DPLK '+noPeserta+'/'+namaLengkap, 'D', nominal)
    batchutils.new_transaction(config, session, noBatch, noGiro, '10', keterangan, 'IURAN DPLK '+noPeserta+'/'+namaLengkap, 'C', nominal)
    no_referensi = session
    batchutils.commit_session(config, session, noBatch)
    
    config.Commit()
  except:
    batchutils.rollback_session(config, session, noBatch)
    config.Rollback()
    
  return no_referensi  

#-------------------------------------------------------------------------------
## SETOR TUNAI DPLK PERTAMA KALI (PENDAFTARAN+IURANPERTAMA), KONEKSI KE CORE BANKING
#-------------------------------------------------------------------------------

'''def SetorTunaiPertamaCoreBanking(config, noBatch, noPeserta, namaLengkap, noGiroDaftar, \
  noGiroIuran, idTransaksiDaftar, idTransaksiIuran, nominalDaftar, nominalIuran, \
  keteranganDaftar, keteranganIuran):

  sessionID = CekKoneksiCoreBanking(config)
  param = config.AppObject.CreateValues(\
    ['NomorBatch', noBatch],
    ['NomorPeserta', noPeserta],
    ['NamaPeserta', namaLengkap],
    ['NomorRekeningGiroPendaftaran', noGiroDaftar],
    ['NomorRekeningGiroIuran', noGiroIuran],
    ['NomorReferensiPendaftaran', hex(idTransaksiDaftar)[2:]],
    ['NomorReferensiIuran', hex(idTransaksiIuran)[2:]],
    ['NominalPendaftaran', nominalDaftar],
    ['NominalIuran', nominalIuran],
    ['KeteranganPendaftaran', keteranganDaftar],
    ['KeteranganIuran', keteranganIuran])
  
  try:
    #remote eksekusi creating giro core banking untuk setor tunai
    ph = config.AppObject.rexecscript(sessionID,'remote/SetorTunaiDPLKPertama',param,1)
    if ph.FirstRecord.IsErr:
      raise '\nError Giro %s dan %s' % (noGiroDaftar,noGiroIuran), \
        str(ph.FirstRecord.ErrMessage)
  except:
    raise
  
  return [ph.FirstRecord.NoReferensiPendaftaran,ph.FirstRecord.NoReferensiIuran]
'''

def SetorTunaiPertamaCoreBanking(config, noBatch, noPeserta, namaLengkap, noGiroDaftar, \
  noGiroIuran, idTransaksiDaftar, idTransaksiIuran, nominalDaftar, nominalIuran, \
  keteranganDaftar, keteranganIuran):
#   import rpdb2; rpdb2.start_embedded_debugger("000")  
  
  userid = config.SecurityContext.UserID  
  Host = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'HostCoreBanking')
  Port = int(config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'PortCoreBanking'))
  config.BeginTransaction()
  session = batchutils.begin_session(config)
  try:
    no_referensi = ''
    nokasteller = GetKasTeller(userid, Host, Port)
    #pendaftaran
    batchutils.new_transaction(config, session, noBatch, nokasteller, '10', keteranganDaftar, noPeserta+'/'+namaLengkap, 'D', nominalDaftar)
    batchutils.new_transaction(config, session, noBatch, noGiroDaftar, '10', keteranganDaftar, noPeserta+'/'+namaLengkap, 'C', nominalDaftar)
    #iuran
    batchutils.new_transaction(config, session, noBatch, nokasteller, '10', keteranganIuran, 'IURAN DPLK '+noPeserta+'/'+namaLengkap, 'D', nominalIuran)
    batchutils.new_transaction(config, session, noBatch, noGiroIuran, '10', keteranganIuran, 'IURAN DPLK '+noPeserta+'/'+namaLengkap, 'C', nominalIuran)
    no_referensi = str(config.Now())
    batchutils.commit_session(config, session, noBatch)
    
    config.Commit()
  except:
    batchutils.rollback_session(config, session, noBatch)
    config.Rollback()
    
  return [no_referensi, no_referensi]  

#-------------------------------------------------------------------------------
## PINDAH BUKU PERTAMA KALI (PENDAFTARAN+IURANPERTAMA), KONEKSI KE CORE BANKING
#-------------------------------------------------------------------------------

'''def PindahBukuPertamaCoreBanking(config, noBatch, noPeserta, namaLengkap, noGiroDaftar, \
  noGiroIuran, idTransaksiDaftar, idTransaksiIuran, nominalDaftar, nominalIuran, \
  rekeningPindahBuku, tipeRekeningPindahBuku, keteranganDaftar, keteranganIuran):

  sessionID = CekKoneksiCoreBanking(config)
  param = config.AppObject.CreateValues(\
    ['NomorBatch', noBatch],
    ['NomorPeserta', noPeserta],
    ['NamaPeserta', namaLengkap],
    ['NomorRekeningGiroPendaftaran', noGiroDaftar],
    ['NomorRekeningGiroIuran', noGiroIuran],
    ['NomorReferensiPendaftaran', hex(idTransaksiDaftar)[2:]],
    ['NomorReferensiIuran', hex(idTransaksiIuran)[2:]],
    ['NominalPendaftaran', nominalDaftar],
    ['NominalIuran', nominalIuran],
    ['KeteranganPendaftaran', keteranganDaftar],
    ['KeteranganIuran', keteranganIuran],
    ['NomorRekeningDebet',rekeningPindahBuku],
    ['JenisRekeningDebet',tipeRekeningPindahBuku])

  try:
    #remote eksekusi creating giro core banking untuk pindah buku
    ph = config.AppObject.rexecscript(sessionID,'remote/PindahBukuDPLKPertama',param,1)
    if ph.FirstRecord.IsErr:
      raise '\nError Giro %s dan %s' % (noGiroDaftar,noGiroIuran), \
        str(ph.FirstRecord.ErrMessage)
  except:
    raise

  return [ph.FirstRecord.NoReferensiPendaftaran,ph.FirstRecord.NoReferensiIuran]
'''

def PindahBukuPertamaCoreBanking(config, noBatch, noPeserta, namaLengkap, noGiroDaftar, \
  noGiroIuran, idTransaksiDaftar, idTransaksiIuran, nominalDaftar, nominalIuran, \
  rekeningPindahBuku, tipeRekeningPindahBuku, keteranganDaftar, keteranganIuran):
  
  no_referensi = ''
  userid = config.SecurityContext.UserID  
  Host = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'HostCoreBanking')
  Port = int(config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'PortCoreBanking'))
  config.BeginTransaction()
  session = batchutils.begin_session(config)
  try:
    #pendaftaran
    batchutils.new_transaction(config, session, noBatch, rekeningPindahBuku, tipeRekeningPindahBuku, keteranganDaftar, noPeserta+'/'+namaLengkap, 'D', nominalDaftar)
    batchutils.new_transaction(config, session, noBatch, noGiroDaftar, '10', keteranganDaftar, noPeserta+'/'+namaLengkap, 'C', nominalDaftar)
    #iuran
    batchutils.new_transaction(config, session, noBatch, rekeningPindahBuku, tipeRekeningPindahBuku, keteranganIuran, 'IURAN DPLK '+noPeserta+'/'+namaLengkap, 'D', nominalIuran)
    batchutils.new_transaction(config, session, noBatch, noGiroIuran, '10', keteranganIuran, 'IURAN DPLK '+noPeserta+'/'+namaLengkap, 'C', nominalIuran)
    no_referensi = session
    batchutils.commit_session(config, session, noBatch)
    
    config.Commit()
  except:
    batchutils.rollback_session(config, session, noBatch)
    config.Rollback()
    
  return [no_referensi, no_referensi]  


#-------------------------------------------------------------------------------
## CREATE SI, KONEKSI KE CORE BANKING
#-------------------------------------------------------------------------------

def CreateSI(config, noPeserta, noRekeningDebet, noRekeningKredit, jenisSetoran, \
  nominal, floatTanggalSIPertama, floatTanggalKadaluarsa):
 
  sessionID = CekKoneksiCoreBanking(config)
  #jenisSetoran: 1 - Iuran Peserta, 2 - Premi Wasiat Ummat

  param = config.AppObject.CreateValues(\
    ['NomorPeserta', noPeserta],
    ['NomorRekeningDebet', noRekeningDebet],
    ['JenisRekeningDebet', '10'],
    ['NomorRekeningKredit', noRekeningKredit],
    ['JenisRekeningKredit', '20'],
    ['JenisSetoran', jenisSetoran],
    ['NominalSI', nominal],
    ['TanggalSIPertama', floatTanggalSIPertama],
    ['TanggalKadaluarsa', floatTanggalKadaluarsa])
      
  #remote eksekusi creating New SI core banking
  try:
    ph = config.AppObject.rexecscript(sessionID,'remote/CreateSI',param,1)
    if ph.FirstRecord.IsErr:
      raise '\nError Create Stading Instruction (SI)',str(ph.FirstRecord.ErrMessage)
  except:
    raise

  return 1

#-------------------------------------------------------------------------------
## EDIT SI, KONEKSI KE CORE BANKING
#-------------------------------------------------------------------------------

def EditSI(config, noPeserta, noRekeningDebet, noRekeningKredit, jenisRekeningKredit, \
  jenisSetoran, nominal, tanggalKadaluarsa):

  sessionID = CekKoneksiCoreBanking(config)
  #jenisSetoran: 1 - Iuran Peserta, 2 - Premi Wasiat Ummat
  
  param = config.AppObject.CreateValues(\
    ['NomorPeserta', noPeserta],
    ['NomorRekeningDebet', noRekeningDebet],
    ['NomorRekeningKredit', noRekeningKredit],
    ['JenisRekeningKredit', jenisRekeningKredit],
    ['JenisSetoran', jenisSetoran],
    ['NominalSI', nominal],
    ['TanggalKadaluarsa',tanggalKadaluarsa])

  try:
    #remote eksekusi creating giro core banking untuk pindah buku
    ph = config.AppObject.rexecscript(sessionID,'remote/EditSI',param,1)
    if ph.FirstRecord.IsErr:
      raise '\nError Edit Standing Instruction (SI)', str(ph.FirstRecord.ErrMessage)
  except:
    raise

  return 1
  
#-------------------------------------------------------------------------------
## REMOVE SI, KONEKSI KE CORE BANKING
#-------------------------------------------------------------------------------

def RemoveSI(config, noPeserta, noRekeningDebet, noRekeningKredit):

  sessionID = CekKoneksiCoreBanking(config)
  param = config.AppObject.CreateValues(\
    ['NomorPeserta', noPeserta],
    ['NomorRekeningDebet', noRekeningDebet],
    ['NomorRekeningKredit', noRekeningKredit])

  #remote eksekusi removing SI core banking
  try:
    ph = config.AppObject.rexecscript(sessionID,'remote/RemoveSI',param,1)
    if ph.FirstRecord.IsErr:
      raise '\nError Remove Stading Instruction (SI)',str(ph.FirstRecord.ErrMessage)
  except:
    raise  

  return 1

#-------------------------------------------------------------------------------
## BUAT BATCH DPLK
#-------------------------------------------------------------------------------

def CreateBatch(config, batchType, batchSubType, dtTglTransaksi, userId, kodeCabang, terminalId):
  #sesuai tanggal transaksi, account link type Single
  needCreateBatch = 1
  if batchSubType == 'T':
    # batch milik teller, hanya boleh 1 instance per tipe batch per hari
    # cari dengan SQL
    y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)
    sSQL = "select t.ID_TRANSACTIONBATCH from TRANSACTIONBATCH t \
           where t.USER_ID_OWNER = '%s' and t.TGL_USED = '%s' and \
           t.BATCH_STATUS = 'O' and t.BATCH_TYPE = '%s' and t.BATCH_SUB_TYPE = '%s'" \
           % (userId, '%s-%s-%s' % (str(y),str(m).zfill(2),str(d).zfill(2)),\
           batchType, batchSubType)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    if not rSQL.Eof:
      oTB = config.CreatePObjImplProxy('TransactionBatch')
      oTB.Key = rSQL.ID_TRANSACTIONBATCH
      needCreateBatch = 0
    else:
      # batch tidak ketemu
      needCreateBatch = 1
    
  if needCreateBatch:
    # create new batch
    oTB = config.CreatePObject('TransactionBatch')
    
    #batch type: R-Registrasi, T-Transaksi, P-Premi, I-Investasi
    oTB.batch_type = batchType
  
    #batch sub type: M-Manual, T-Teller
    oTB.batch_sub_type = batchSubType
  
    #ambil info tanggal
    y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  
    #tanggal pembuatan dan tanggap pakai disamakan
    oTB.tgl_create = oTB.tgl_used = config.ModDateTime.EncodeDate(y, m, d)
  
    #acccount link type diset 'Single' dan status batch 'Open'
    oTB.account_link_type = 'S'
    oTB.batch_status = 'O'
  
    #informasi tambahan untuk batch
    oTB.terminal_id_create = terminalId
    oTB.user_id_create = oTB.user_id_owner = userId
    oTB.branch_code = kodeCabang  
  
    #creating nomor batch
    oTB.no_batch = 'B' + oTB.batch_type + '.' + oTB.user_id_owner + '.' + \
      str(oTB.tgl_used[0]) + \
      str(string.zfill(oTB.tgl_used[1],2)) + \
      str(string.zfill(oTB.tgl_used[2],2)) + '.' + str(oTB.ID_TransactionBatch)

  return oTB
  
def GetLastTglPenarikan30(config, noPeserta):
  #ambil tanggal penarikan 30% terakhir
  sSQL = 'select top 1 TGL_TRANSAKSI from TRANSAKSIDPLK where NO_PESERTA = \'%s\' and '\
    'KODE_JENIS_TRANSAKSI = \'V\' and ISCOMMITTED = \'T\' order by TGL_TRANSAKSI desc'\
    % (noPeserta)
  rSQL = config.CreateSQL(sSQL).RawResult

  tgl_transaksi = None
  rSQL.First()
  if not rSQL.Eof:
    tgl_transaksi = rSQL.tgl_transaksi

  return tgl_transaksi

def CompareLastTglPenarikan(config, tgl_transaksi):
  # hitung rentang bulan penarikan terakhir until Now
  # tgl_transaksi != None

  tglTarikTerakhir = config.ModLibUtils.EncodeDate(tgl_transaksi[0], tgl_transaksi[1], tgl_transaksi[2])

  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'BATAS_WAKTU_PENARIKAN_NORMAL'

  if (config.Now() - tglTarikTerakhir) < oP.Numeric_Value:
    #rentang penarikan masih dalam waktu BATAS_WAKTU_PENARIKAN_NORMAL (default 6 bulan (365/2 hari))
    return 0

  return 1  

def CekRentangWaktuPenarikan(config, noPeserta):
  tgl_transaksi = GetLastTglPenarikan30(config, noPeserta)
  if tgl_transaksi:
    # tgl_transaksi != None, sudah pernah ditarik sebelumnya
    # hitung rentang bulan penarikan terakhir until Now

    if not CompareLastTglPenarikan(config, tgl_transaksi):
      raise '\nPeringatan','\nPenarikan masih dalam rentang waktu 6 bulan. '\
        'Penarikan terakhir tanggal %d-%d-%d.' % (tgl_transaksi[2], tgl_transaksi[1], tgl_transaksi[0])

def CekSaldoIuranMin(config, noPeserta):
  # cek saldo iuran
  oRekening = config.CreatePObjImplProxy('RekeningDPLK')
  oRekening.key = noPeserta

  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'MIN_JML_AKUM_IURAN_PST'
  saldo_iuran = oRekening.akum_dana_iuran_pk + oRekening.akum_dana_iuran_pst
  if saldo_iuran < oP.Numeric_Value:
    raise '\nPeringatan', '\nDana iuran peserta tidak mencukupi'

def CekBatasTarikMinPHK(config, ID_Transaksi):
  oPenarikanDanaPHK = config.CreatePObjImplProxy('PenarikanDanaPHK')
  oPenarikanDanaPHK.Key = ID_Transaksi

  oRekeningDPLK = oPenarikanDanaPHK.LRekeningDPLK

  if oPenarikanDanaPHK.jml_tarik < oRekeningDPLK.akum_dana_iuran_pk:
    raise 'Kesalahan Jumlah Penarikan Dana PHK', '\nNominal Penarikan tidak boleh kurang dari Batas Penarikan Minimal!'

def CekBatasTarikMaxPHK(config, ID_Transaksi):
  oPenarikanDanaPHK = config.CreatePObjImplProxy('PenarikanDanaPHK')
  oPenarikanDanaPHK.Key = ID_Transaksi

  oRekeningDPLK = oPenarikanDanaPHK.LRekeningDPLK
  if oPenarikanDanaPHK.jml_tarik > oRekeningDPLK.akum_dana_iuran_pk + oRekeningDPLK.akum_dana_iuran_pst:
    raise 'Kesalahan Jumlah Penarikan Dana PHK', '\nNominal Penarikan melebihi batas nominal dana yang boleh ditarik!!'
