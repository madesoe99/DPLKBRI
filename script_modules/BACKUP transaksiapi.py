#import string, rotor, sys
import string, sys
#sys.path.append('c:/dafutils')
#sys.path.append('c:/dafapp/dplk/script_modules')

import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# import batchutils
import com.ihsan.lib.trace as trace

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
      config.SendDebugMsg('result : '+str(Result))
    else:
      kena_pajak1 = batas1 - total_sebelum
      config.SendDebugMsg('kena_pajak1 : '+str(kena_pajak1))
      Result = (persenBatas1 / 100.0) * kena_pajak1
      config.SendDebugMsg('result-01 : '+str(Result))
      Result = Result + (persenBatas2 / 100.0) * (akena_pajak - kena_pajak1)
      config.SendDebugMsg('result-02 : '+str(Result))
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
#   import rpdb2; rpdb2.start_embedded_debugger("000")  
  
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

  Result = 0
  
  if batas1 > 0:
    if AValue >= batas1: 
      Result = batas1 * (persenBatas1 / 100.0)
      AValue = AValue - batas1
      if batas2 > 0:
        if AValue >= (batas2 - batas1): 
          Result = Result + (batas2 - batas1) * (persenBatas2 / 100.0)
          AValue = AValue - (batas2 - batas1) 
          if batas3 > 0:
            if AValue >= (batas3 - batas2):
              Result = Result + (batas3 - batas2) * (persenBatas3 / 100.0)
              AValue = AValue - (batas3 - batas2)
              if batas4 > 0:
                if AValue >= (batas4 - batas3):
                  Result = Result + (batas4 - batas3) * (persenBatas4 / 100.0)
                  AValue = AValue - (batas4 - batas3)
                  if batas5 > 0:
                    Result = Result + AValue * (persenBatas5 / 100.0)
                else:
                  Result = Result + AValue * (persenBatas4 / 100.0)                
            else:
              Result = Result + AValue * (persenBatas3 / 100.0)
        else:
          Result = Result + AValue * (persenBatas2 / 100.0)  
    else:
      Result = AValue * (persenBatas1 / 100.0)


  return Result
  
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
    config.SendDebugMsg('tglawal-01='+str(oN.tgl_registrasi[0])+str(oN.tgl_registrasi[1])+str(oN.tgl_registrasi[2]))
    tglawal = config.ModLibUtils.EncodeDate(oN.tgl_registrasi[0], \
      oN.tgl_registrasi[1],oN.tgl_registrasi[2])
  else:
    #sudah pernah melakukan pengambilan manfaat atau pengalihan ke DPLK lain
    #rentang hari dari tanggal transaksi OUT terakhir
    config.SendDebugMsg('tglawal-02='+str(rSQL.tgl_transaksi[0])+str(rSQL.tgl_transaksi[1])+str(rSQL.tgl_transaksi[2]))
    tglawal = config.ModLibUtils.EncodeDate(rSQL.tgl_transaksi[0], \
      rSQL.tgl_transaksi[1],rSQL.tgl_transaksi[2])     
        
  tglakhir = config.ModLibUtils.EncodeDate(tgl_transaksi[0],tgl_transaksi[1], \
    tgl_transaksi[2])
    
  config.SendDebugMsg('tglakhir='+str(tgl_transaksi[0])+str(tgl_transaksi[1])+str(tgl_transaksi[2]))
        
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


def HitungProporsiBiayaBulanan(config, kode_jenis_transaksi, no_peserta, tgl_transaksi):

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
    config.SendDebugMsg('tglawal-01='+str(oN.tgl_registrasi[0])+str(oN.tgl_registrasi[1])+str(oN.tgl_registrasi[2]))
    tglawal = config.ModLibUtils.EncodeDate(oN.tgl_registrasi[0], \
      oN.tgl_registrasi[1],oN.tgl_registrasi[2])
  else:
    #sudah pernah di kenakan biaya pengelolaan tahunan
    #rentang hari dari tanggal transaksi OUT terakhir
    config.SendDebugMsg('tglawal-02='+str(rSQL.tgl_transaksi[0])+str(rSQL.tgl_transaksi[1])+str(rSQL.tgl_transaksi[2]))
    tglawal = config.ModLibUtils.EncodeDate(rSQL.tgl_transaksi[0], \
      rSQL.tgl_transaksi[1],rSQL.tgl_transaksi[2])


  tglakhir = config.ModLibUtils.EncodeDate(tgl_transaksi[0],tgl_transaksi[1], \
    tgl_transaksi[2])

  config.SendDebugMsg('tglakhir='+str(tgl_transaksi[0])+str(tgl_transaksi[1])+str(tgl_transaksi[2]))

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
    selbln = bln_transaksi - bln_registrasi
     
    if (selbln < 6): # biaya adm juni atau desember yg registrasinya setelah juni
      if modbln == 0: 
        proporsi = 1 / periode
      else:
        proporsi = (periode - modbln + 1) / periode
    else: # biaya adm desember dan registrasi sebelum juni
      proporsi = 1.0
        
  return proporsi

def HitungProporsiBiayaAdmTahunanSemesteran(config, no_peserta, tgl_transaksi):

  oN = config.CreatePObjImplProxy('NasabahDPLK')
  oN.Key = no_peserta

  config.SendDebugMsg('Biaya Semesteran.....')
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
    proporsi = 6 #1.0
  else:# tgl_registrasi sama dg tanggal transaksi
    modbln = bln_registrasi % periode
    selbln = bln_transaksi - bln_registrasi

    if (selbln <= 6): # biaya adm juni atau desember yg registrasinya setelah juni
      selbln = (bln_transaksi - bln_registrasi) + 1
      proporsi = selbln
    #else: # biaya adm desember dan registrasi sebelum juni
     # proporsi = 1.0

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
  #rt = rotor.newrotor(UserID, 19)
  #Password = rt.decrypt(cryptedPasswd)
  Password = ''

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
    raise Exception, 'Error koneksi core banking' +  'User %s tidak terhubung ke core banking' % config.SecurityContext.UserID
  return sessionID

#-------------------------------------------------------------------------------
## PINDAH BUKU, KONEKSI KE CORE BANKING
#-------------------------------------------------------------------------------

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
      raise Exception, '\nPeringatan' + '\nPenarikan masih dalam rentang waktu 6 bulan. '\
        'Penarikan terakhir tanggal %d-%d-%d.' % (tgl_transaksi[2], tgl_transaksi[1], tgl_transaksi[0])

def CekSaldoIuranMin(config, noPeserta):
  # cek saldo iuran
  oRekening = config.CreatePObjImplProxy('RekeningDPLK')
  oRekening.key = noPeserta

  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'MIN_JML_AKUM_IURAN_PST'
  saldo_iuran = oRekening.akum_dana_iuran_pk + oRekening.akum_dana_iuran_pst
  if saldo_iuran < oP.Numeric_Value:
    raise Exception, '\nPeringatan' +  '\nDana iuran peserta tidak mencukupi'

def CekBatasTarikMinPHK(config, ID_Transaksi):
  oPenarikanDanaPHK = config.CreatePObjImplProxy('PenarikanDanaPHK')
  oPenarikanDanaPHK.Key = ID_Transaksi

  oRekeningDPLK = oPenarikanDanaPHK.LRekeningDPLK

  if oPenarikanDanaPHK.jml_tarik < oRekeningDPLK.akum_dana_iuran_pk:
    raise Exception, 'Kesalahan Jumlah Penarikan Dana PHK' +  '\nNominal Penarikan tidak boleh kurang dari Batas Penarikan Minimal!'

def CekBatasTarikMaxPHK(config, ID_Transaksi):
  oPenarikanDanaPHK = config.CreatePObjImplProxy('PenarikanDanaPHK')
  oPenarikanDanaPHK.Key = ID_Transaksi

  oRekeningDPLK = oPenarikanDanaPHK.LRekeningDPLK
  if oPenarikanDanaPHK.jml_tarik > oRekeningDPLK.akum_dana_iuran_pk + oRekeningDPLK.akum_dana_iuran_pst:
    raise Exception, 'Kesalahan Jumlah Penarikan Dana PHK' +  '\nNominal Penarikan melebihi batas nominal dana yang boleh ditarik!!'