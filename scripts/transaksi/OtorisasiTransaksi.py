import sys
import com.ihsan.util.modman as modman

#DEBUG MODE
#import rpdb2;rpdb2.start_embedded_debugger('haryo',True,True)

def SetKolektibilitasAsuransi(config, oRekInv, oTransaksi):
  #ambil info besar premi di rekening asuransi
  registerCIF_Auth = modman.getModule(config, 'scripts#transaction.registercif_auth')
  oRekAsuransi = registerCIF_Auth.GetRekAsuransiByRekInv(config, oRekInv)

  if oRekAsuransi != None:
    selisihNominal = oTransaksi.besar_premi - oRekAsuransi.besar_premi
  
    if selisihNominal > 0.0:
      #ada kelebihan nominal dari besar premi yang dibayarkan
      #cek nominal kewajiban asuransi
      if oRekInv.kewajiban_asuransi > 0.0:
        #masih ada sisa kewajiban sebelumnya
        sisaKewajiban = oRekInv.kewajiban_asuransi - selisihNominal
  
        #cek sisa kewajiban
        if sisaKewajiban > 0.0:
          #masih ada sisa yang belum terlunasi, jadikan sbg kewajiban yang baru
          oRekInv.kewajiban_asuransi = sisaKewajiban          
        else: 
          #sisa terlunasi semua, jika ada kelebihan dianggap sbg kelebihan
          #bayar premi peserta
          oRekInv.kewajiban_asuransi = 0.0
  
      #else: tidak ada sisa kewajiban sebelumnya, selisihNominal dianggap
      #kelebihan bayar premi peserta 
  
    if oRekInv.kewajiban_asuransi > 0.0:
      #masih ada sisa kewajiban yang belum dilunasi 
      oRekInv.collectivity_asuransi = 'F'
    else:
      #sisa kewajiban premi sudah dilunasi
      oRekInv.collectivity_asuransi = 'T'

  return 1

def CreateBiayaTransaksi(config, classJenisBiaya, oTransaksi, nominalBiaya):
  oBiaya = config.CreatePObject(classJenisBiaya)

  if classJenisBiaya == 'BiayaAdmTransaksi':
    oTransaksi.ID_Transaksi_BAdmTrans = oBiaya.ID_Transaksi
    #tidak ada biaya transaksi untuk pindah paket investasi
  elif classJenisBiaya == 'BiayaPengelolaanDana':
    oTransaksi.ID_Transaksi_BPeng = oBiaya.ID_Transaksi
    oBiaya.saldo_yang_dibebani = oTransaksi.saldo_jml_dana
  elif classJenisBiaya == 'BiayaAdmTahunan':
    oTransaksi.ID_Transaksi_BAdmThn = oBiaya.ID_Transaksi
  else:
    raise Exception, "ID: Jenis Biaya Transaksi tidak terdefinisi!"

  #field TransaksiDPLK
  #field TransaksiRekInvDPLK
  oBiaya.LRekeningDPLK = oTransaksi.LRekeningDPLK
  oBiaya.branch_code = oTransaksi.branch_code
  oBiaya.keterangan = '%s %s peserta %s' % \
    (classJenisBiaya, \
    oTransaksi.LJenisTransaksiDPLK.nama_transaksi, \
    oBiaya.LRekeningDPLK.LNasabahDPLK.no_peserta)
  
  oBiaya.isCommitted = 'T'
  oBiaya.user_id = oTransaksi.user_id
  oBiaya.user_id_auth = config.SecurityContext.UserID
  oBiaya.terminal_id = oTransaksi.terminal_id
  oBiaya.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  
  oBiaya.tgl_transaksi = config.ModLibUtils.EncodeDate(oTransaksi.tgl_transaksi[0],\
    oTransaksi.tgl_transaksi[1],oTransaksi.tgl_transaksi[2]) + \
    config.ModLibUtils.EncodeTime(oTransaksi.tgl_transaksi[3],oTransaksi.tgl_transaksi[4],\
    oTransaksi.tgl_transaksi[5],oTransaksi.tgl_transaksi[6])
  oBiaya.tgl_sistem = oBiaya.tgl_otorisasi = config.ModLibUtils.Now()

  #do charge biaya
  moduleAPI = modman.getModule(config, 'moduleapi')
  moduleAPI.ProsesChargeBiaya(config, oBiaya, nominalBiaya)
  
  return oBiaya

def UpdateUnit(config,oRekDPLK,oDetilTransaksi):
  sSQL = "SELECT * FROM PAKETINVESTASI WHERE kode_paket_investasi='%s' " % oRekDPLK.kode_paket_investasi
  PI = config.CreateSQL(sSQL).RawResult
  
  nav_c = PI.nav_custody
  oDetilTransaksi.nav_custody = nav_c

  akumIuran = oDetilTransaksi.mutasi_iuran_pk + \
              oDetilTransaksi.mutasi_iuran_pst + \
              oDetilTransaksi.mutasi_iuran_tmb
  
  h_unit = float(akumIuran) / float(nav_c)
  unit = "%.4f" % h_unit
  
  return unit
  #raise Exception, h_unit

def ApproveOperation(config, oTransaksi): 
  oTransaksi = oTransaksi.CastToLowestDescendant()
  oRekInv = oTransaksi.LRekeningDPLK
  
  if oTransaksi.IsA("IuranPendaftaran"):
    #set status iuran pendaftaran rekening investasi DPLK
    oRekInv.status_biaya_daftar = 'T'
  #--end Iuran Pendaftaran

  elif oTransaksi.IsA("TitipanPremi"):
    #operasi yang terkait dengan premi
    SetKolektibilitasAsuransi(config, oRekInv, oTransaksi)
  #--end titipan premi

  elif oTransaksi.IsA("IuranPeserta"):
    #tambahkan mutasi dana di RekeningInvDPLK
    oRekInv.akum_iuran_pk += oTransaksi.mutasi_iuran_pk
    oRekInv.akum_iuran_pst += oTransaksi.mutasi_iuran_pst
    oRekInv.akum_iuran_tmb += oTransaksi.mutasi_iuran_tmb
    
    #tambahkan mutasi dana dan unit di tiap RekeningDPLK terkait investasi
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      
      oRekDPLK.akum_iuran_pk += oDetilTransaksi.mutasi_iuran_pk
      oRekDPLK.akum_iuran_pst += oDetilTransaksi.mutasi_iuran_pst
      oRekDPLK.akum_iuran_tmb += oDetilTransaksi.mutasi_iuran_tmb
      
      Unit = UpdateUnit(config, oRekDPLK,oDetilTransaksi)
      oRekDPLK.jml_unit = float(unit)

      Ls_DetilTransaksi.Next()
    #--
  #--end IuranPeserta
  
  elif oTransaksi.IsA("PenarikanDanaNormal"):
    #buat transaksi biaya transaksi (biaya tarik dana)
    oBiayaAdmTransaksi = CreateBiayaTransaksi(config, 'BiayaAdmTransaksi', oTransaksi, \
      oTransaksi.biaya_tarik)
    oBiayaAdmTransaksi.isPindahPaket = 'F'

    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'PRESISI_ANGKA_FLOAT'

    #cek apakah perlu set ulang mutasi bila penarikan ternyata mencapai 100%
    if oRekInv.akum_iuran_pk + oTransaksi.mutasi_iuran_pk + \
      oBiayaAdmTransaksi.mutasi_iuran_pk < oP.Numeric_Value:
      #saldo akum iuran PK berpotensi minus, set ulang mutasi iuran PK 
      oTransaksi.mutasi_iuran_pk = -oRekInv.akum_iuran_pk
      oRekInv.akum_iuran_pk = 0.0
      potensiMinus_PK = 1
    else:
      oRekInv.akum_iuran_pk += oTransaksi.mutasi_iuran_pk
      potensiMinus_PK = 0

    if oRekInv.akum_iuran_pst + oTransaksi.mutasi_iuran_pst + \
      oBiayaAdmTransaksi.mutasi_iuran_pst < oP.Numeric_Value:
      #saldo akum iuran PST berpotensi minus, set ulang mutasi iuran PST
      oTransaksi.mutasi_iuran_pst = -oRekInv.akum_iuran_pst
      oRekInv.akum_iuran_pst = 0.0
      potensiMinus_PST = 1
    else: 
      oRekInv.akum_iuran_pst += oTransaksi.mutasi_iuran_pst
      potensiMinus_PST = 0

    if oRekInv.akum_iuran_tmb + oTransaksi.mutasi_iuran_tmb + \
      oBiayaAdmTransaksi.mutasi_iuran_tmb < oP.Numeric_Value:
      #saldo akum iuran TMB berpotensi minus, set ulang mutasi iuran TMB
      oTransaksi.mutasi_iuran_tmb = -oRekInv.akum_iuran_tmb
      oRekInv.akum_iuran_pst = 0.0
      potensiMinus_TMB = 1
    else: 
      oRekInv.akum_iuran_tmb += oTransaksi.mutasi_iuran_tmb
      potensiMinus_TMB = 0

    #tambahkan mutasi dana dan unit di tiap RekeningDPLK terkait investasi
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening

      if potensiMinus_PK:
        oDetilTransaksi.mutasi_iuran_pk = -oRekDPLK.akum_iuran_pk
        oRekDPLK.akum_iuran_pk = 0.0
      else:
        oRekDPLK.akum_iuran_pk += oDetilTransaksi.mutasi_iuran_pk
      
      if potensiMinus_PST:
        oDetilTransaksi.mutasi_iuran_pst = -oRekDPLK.akum_iuran_pst
        oRekDPLK.akum_iuran_pst = 0.0
      else:
        oRekDPLK.akum_iuran_pst += oDetilTransaksi.mutasi_iuran_pst
      
      if potensiMinus_TMB:
        oDetilTransaksi.mutasi_iuran_tmb = -oRekDPLK.akum_iuran_tmb
        oRekDPLK.akum_iuran_tmb = 0.0
      else:
        oRekDPLK.akum_iuran_tmb += oDetilTransaksi.mutasi_iuran_tmb
      
      Ls_DetilTransaksi.Next()
    #--
  #--end PenarikanDanaNormal
    
  elif oTransaksi.IsA("PenarikanDanaPHK"):
    #buat transaksi biaya transaksi (biaya tarik dana)
    oBiayaAdmTransaksi = CreateBiayaTransaksi(config, 'BiayaAdmTransaksi', oTransaksi, \
      oTransaksi.biaya_tarik)
    oBiayaAdmTransaksi.isPindahPaket = 'F'

    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'PRESISI_ANGKA_FLOAT'

    #cek apakah perlu set ulang mutasi bila penarikan ternyata mencapai 100%
    if oRekInv.akum_iuran_pk + oTransaksi.mutasi_iuran_pk + \
      oBiayaAdmTransaksi.mutasi_iuran_pk < oP.Numeric_Value:
      #saldo akum iuran PK berpotensi minus, set ulang mutasi iuran PK 
      oTransaksi.mutasi_iuran_pk = -oRekInv.akum_iuran_pk
      oRekInv.akum_iuran_pk = 0.0
      potensiMinus_PK = 1
    else:
      oRekInv.akum_iuran_pk += oTransaksi.mutasi_iuran_pk
      potensiMinus_PK = 0

    if oRekInv.akum_iuran_pst + oTransaksi.mutasi_iuran_pst + \
      oBiayaAdmTransaksi.mutasi_iuran_pst < oP.Numeric_Value:
      #saldo akum iuran PST berpotensi minus, set ulang mutasi iuran PST
      oTransaksi.mutasi_iuran_pst = -oRekInv.akum_iuran_pst
      oRekInv.akum_iuran_pst = 0.0
      potensiMinus_PST = 1
    else: 
      oRekInv.akum_iuran_pst += oTransaksi.mutasi_iuran_pst
      potensiMinus_PST = 0

    if oRekInv.akum_iuran_tmb + oTransaksi.mutasi_iuran_tmb + \
      oBiayaAdmTransaksi.mutasi_iuran_tmb < oP.Numeric_Value:
      #saldo akum iuran TMB berpotensi minus, set ulang mutasi iuran TMB
      oTransaksi.mutasi_iuran_tmb = -oRekInv.akum_iuran_tmb
      oRekInv.akum_iuran_pst = 0.0
      potensiMinus_TMB = 1
    else: 
      oRekInv.akum_iuran_tmb += oTransaksi.mutasi_iuran_tmb
      potensiMinus_TMB = 0

    #tambahkan mutasi dana dan unit di tiap RekeningDPLK terkait investasi
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening

      if potensiMinus_PK:
        oDetilTransaksi.mutasi_iuran_pk = -oRekDPLK.akum_iuran_pk
        oRekDPLK.akum_iuran_pk = 0.0
      else:
        oRekDPLK.akum_iuran_pk += oDetilTransaksi.mutasi_iuran_pk
      
      if potensiMinus_PST:
        oDetilTransaksi.mutasi_iuran_pst = -oRekDPLK.akum_iuran_pst
        oRekDPLK.akum_iuran_pst = 0.0
      else:
        oRekDPLK.akum_iuran_pst += oDetilTransaksi.mutasi_iuran_pst
      
      if potensiMinus_TMB:
        oDetilTransaksi.mutasi_iuran_tmb = -oRekDPLK.akum_iuran_tmb
        oRekDPLK.akum_iuran_tmb = 0.0
      else:
        oRekDPLK.akum_iuran_tmb += oDetilTransaksi.mutasi_iuran_tmb
      
      Ls_DetilTransaksi.Next()
    #--
  #--end PenarikanDanaPHK

  elif oTransaksi.IsA("PengalihanKeDPLKLain"):
    #buat transaksi biaya pengelolaan
    oBiayaPengelolaan = CreateBiayaTransaksi(config, 'BiayaPengelolaanDana', oTransaksi, \
      oTransaksi.biaya_pengelolaan)
    
    #buat transaksi biaya administrasi
    oBiayaAdmTahunan = CreateBiayaTransaksi(config, 'BiayaAdmTahunan', oTransaksi, \
      oTransaksi.biaya_administrasi)
    
    #buat transaksi biaya transaksi (biaya pengalihan)
    oBiayaAdmTransaksi = CreateBiayaTransaksi(config, 'BiayaAdmTransaksi', oTransaksi, \
      oTransaksi.biaya_pindah)
    oBiayaAdmTransaksi.isPindahPaket = 'F'
    
    #mutasi akan di set ulang dengan saldo rekening investasi DPLK
    oTransaksi.mutasi_iuran_pk = -oRekInv.akum_iuran_pk
    oTransaksi.mutasi_iuran_pst = -oRekInv.akum_iuran_pst
    oTransaksi.mutasi_iuran_tmb = -oRekInv.akum_iuran_tmb
    oTransaksi.mutasi_psl = -oRekInv.akum_psl
    oTransaksi.mutasi_pmb_pk = -oRekInv.akum_pmb_pk
    oTransaksi.mutasi_pmb_pst = -oRekInv.akum_pmb_pst
    oTransaksi.mutasi_pmb_tmb = -oRekInv.akum_pmb_tmb
    oTransaksi.mutasi_pmb_psl = -oRekInv.akum_pmb_psl

    #nihilkan saldo RekeningInvDPLK
    oRekInv.akum_iuran_pk = 0.0
    oRekInv.akum_iuran_pst = 0.0
    oRekInv.akum_iuran_tmb = 0.0
    oRekInv.akum_psl = 0.0
    oRekInv.akum_pmb_pk = 0.0
    oRekInv.akum_pmb_pst = 0.0
    oRekInv.akum_pmb_tmb = 0.0
    oRekInv.akum_pmb_psl = 0.0
    
    #nihilkan saldo tiap RekeningDPLK
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk = 0.0
      oRekDPLK.akum_iuran_pst = 0.0
      oRekDPLK.akum_iuran_tmb = 0.0
      oRekDPLK.akum_psl = 0.0
      oRekDPLK.akum_pmb_pk = 0.0
      oRekDPLK.akum_pmb_pst = 0.0
      oRekDPLK.akum_pmb_tmb = 0.0
      oRekDPLK.akum_pmb_psl = 0.0
      
      #update mutasi transaksi DetilTransaksi
      oDetilTransaksi.mutasi_iuran_pk = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_pk  
      oDetilTransaksi.mutasi_iuran_pst = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_pst  
      oDetilTransaksi.mutasi_iuran_tmb = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_tmb
      oDetilTransaksi.mutasi_psl = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_psl
      oDetilTransaksi.mutasi_pmb_pk = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_pk
      oDetilTransaksi.mutasi_pmb_pst = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_pst 
      oDetilTransaksi.mutasi_pmb_tmb = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_tmb 
      oDetilTransaksi.mutasi_pmb_psl = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_psl 
      
      Ls_DetilTransaksi.Next()
    #--
    
    #penutupan RekeningInvDPLK, samakan tgl tutup dengan tgl transaksi
    oRekInv.status_DPLK = 'N'
    oRekInv.tgl_tutup = oTransaksi.tgl_transaksi
  #--end PengalihanKeDPLKLain
  
  elif oTransaksi.IsA("PengalihanDariDPLKLain") or \
    oTransaksi.kode_jenis_transaksi in ('I','O','P'):
    #cek apakah pengalihan dari DPLK / DPPK / DPK?
    if oTransaksi.kode_jenis_transaksi == 'I':
      #pengalihan dari DPLK lain
      pass
    elif oTransaksi.kode_jenis_transaksi == 'O':
      #pengalihan dari DPPK lain
      pass 
    elif oTransaksi.kode_jenis_transaksi == 'P':
      #pengalihan dari DPK lain
      pass 

    oRekInv.akum_iuran_pk += oTransaksi.mutasi_iuran_pk
    oRekInv.akum_iuran_pst += oTransaksi.mutasi_iuran_pst
    oRekInv.akum_iuran_tmb += oTransaksi.mutasi_iuran_tmb
    oRekInv.akum_psl += oTransaksi.mutasi_psl
    oRekInv.akum_pmb_pk += oTransaksi.mutasi_pmb_pk
    oRekInv.akum_pmb_pst += oTransaksi.mutasi_pmb_pst
    oRekInv.akum_pmb_tmb += oTransaksi.mutasi_pmb_tmb
    oRekInv.akum_pmb_psl += oTransaksi.mutasi_pmb_psl

    #tambahkan mutasi dana dan unit di tiap RekeningDPLK terkait investasi
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk += oDetilTransaksi.mutasi_iuran_pk
      oRekDPLK.akum_iuran_pst += oDetilTransaksi.mutasi_iuran_pst
      oRekDPLK.akum_iuran_tmb += oDetilTransaksi.mutasi_iuran_tmb
      oRekDPLK.akum_psl += oDetilTransaksi.mutasi_psl
      oRekDPLK.akum_pmb_pk += oDetilTransaksi.mutasi_pmb_pk
      oRekDPLK.akum_pmb_pst += oDetilTransaksi.mutasi_pmb_pst
      oRekDPLK.akum_pmb_tmb += oDetilTransaksi.mutasi_pmb_tmb
      oRekDPLK.akum_pmb_psl += oDetilTransaksi.mutasi_pmb_psl
      
      Ls_DetilTransaksi.Next()
    #--
  #--end PengalihanDariDPLKLain

  elif oTransaksi.IsA("PengambilanManfaat"):
    #buat transaksi biaya pencairan (biaya bila dana mengendap < 1 tahun)
    oBiayaAdmTransaksi = CreateBiayaTransaksi(config, 'BiayaAdmTransaksi', oTransaksi, \
      oTransaksi.biaya_pencairan)
    oBiayaAdmTransaksi.isPindahPaket = 'F'

    #buat transaksi biaya pengelolaan
    oBiayaPengelolaan = CreateBiayaTransaksi(config, 'BiayaPengelolaanDana', oTransaksi, \
      oTransaksi.biaya_pengelolaan)
    
    #buat transaksi biaya administrasi
    oBiayaAdmTahunan = CreateBiayaTransaksi(config, 'BiayaAdmTahunan', oTransaksi, \
      oTransaksi.biaya_administrasi)
    
    #mutasi akan di set ulang dengan saldo rekening investasi DPLK
    oTransaksi.mutasi_iuran_pk = -oRekInv.akum_iuran_pk
    oTransaksi.mutasi_iuran_pst = -oRekInv.akum_iuran_pst
    oTransaksi.mutasi_iuran_tmb = -oRekInv.akum_iuran_tmb
    oTransaksi.mutasi_psl = -oRekInv.akum_psl
    oTransaksi.mutasi_pmb_pk = -oRekInv.akum_pmb_pk
    oTransaksi.mutasi_pmb_pst = -oRekInv.akum_pmb_pst
    oTransaksi.mutasi_pmb_tmb = -oRekInv.akum_pmb_tmb
    oTransaksi.mutasi_pmb_psl = -oRekInv.akum_pmb_psl

    #nihilkan saldo RekeningInvDPLK
    oRekInv.akum_iuran_pk = 0.0
    oRekInv.akum_iuran_pst = 0.0
    oRekInv.akum_iuran_tmb = 0.0
    oRekInv.akum_psl = 0.0
    oRekInv.akum_pmb_pk = 0.0
    oRekInv.akum_pmb_pst = 0.0
    oRekInv.akum_pmb_tmb = 0.0
    oRekInv.akum_pmb_psl = 0.0
    
    #nihilkan saldo tiap RekeningDPLK
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk = 0.0
      oRekDPLK.akum_iuran_pst = 0.0
      oRekDPLK.akum_iuran_tmb = 0.0
      oRekDPLK.akum_psl = 0.0
      oRekDPLK.akum_pmb_pk = 0.0
      oRekDPLK.akum_pmb_pst = 0.0
      oRekDPLK.akum_pmb_tmb = 0.0
      oRekDPLK.akum_pmb_psl = 0.0
      
      #update mutasi transaksi DetilTransaksi
      oDetilTransaksi.mutasi_iuran_pk = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_pk  
      oDetilTransaksi.mutasi_iuran_pst = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_pst  
      oDetilTransaksi.mutasi_iuran_tmb = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_tmb
      oDetilTransaksi.mutasi_psl = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_psl
      oDetilTransaksi.mutasi_pmb_pk = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_pk
      oDetilTransaksi.mutasi_pmb_pst = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_pst 
      oDetilTransaksi.mutasi_pmb_tmb = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_tmb 
      oDetilTransaksi.mutasi_pmb_psl = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_psl 

      Ls_DetilTransaksi.Next()
    #--
    
    #penutupan RekeningInvDPLK, samakan tgl tutup dengan tgl transaksi
    oRekInv.status_DPLK = 'N'
    oRekInv.tgl_tutup = oTransaksi.tgl_transaksi
    
    #checking untuk pembuatan register anuitas
    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'PRESISI_ANGKA_FLOAT'
    if oTransaksi.manfaat_anuitas > oP.Numeric_Value:
      #buat register anuitas untuk peserta
      oRA = config.CreatePObject('RegisterAnuitas')
      oRA.nominal_anuitas = oTransaksi.manfaat_anuitas
      oRA.keterangan = 'register bersamaan dengan Pengambilan Manfaat peserta ' +\
        oRekInv.no_peserta
      oRA.terminal_id = oTransaksi.terminal_id
      oRA.kode_jenis_registercif = 'N'
      oRA.no_peserta = oRekInv.no_peserta
      oRA.no_rekening = oRekInv.no_rekening
      oRA.user_id = oTransaksi.user_id
      
      #tanggal register samakan dengan tanggal transaksi
      oRA.tanggal_register = oTransaksi.tgl_transaksi
        
      #set status anuitas rekening investasi DPLK
      oRekInv.status_anuitas = 'F'
    #--end checking pembuatan register anuitas
    
    #checking status asuransi
    if oRekInv.status_asuransi == 'T':
      #peserta ikut asuransi, tutup sekalian keikutsertaan asuransi
      registerCIF_Auth = modman.getModule(config, 'scripts#transaction.registercif_auth')
      oRekAsuransi = registerCIF_Auth.GetRekAsuransiByRekInv(config, oRekInv)
      registerCIF_Auth.CreateHistAsuransi(config, oRekAsuransi, 'TarikManfaat', \
        'Telah memasuki usia pensiun', 'Penutupan bersamaan dengan pengambilan manfaat')
      registerCIF_Auth.UpdateStatusAsuransiOut(config, oRekAsuransi)
    #--end checking status asuransi
  #--end PengambilanManfaat
  
  elif oTransaksi.IsA("PengembalianDana"):
    #buat transaksi biaya pencairan
    oBiayaAdmTransaksi = CreateBiayaTransaksi(config, 'BiayaAdmTransaksi', oTransaksi, \
      oTransaksi.biaya_pencairan)
    oBiayaAdmTransaksi.isPindahPaket = 'F'

    #buat transaksi biaya pengelolaan
    oBiayaPengelolaan = CreateBiayaTransaksi(config, 'BiayaPengelolaanDana', oTransaksi, \
      oTransaksi.biaya_pengelolaan)
    
    #buat transaksi biaya administrasi
    oBiayaAdmTahunan = CreateBiayaTransaksi(config, 'BiayaAdmTahunan', oTransaksi, \
      oTransaksi.biaya_administrasi)
    
    #mutasi akan di set ulang dengan saldo rekening investasi DPLK
    oTransaksi.mutasi_iuran_pk = -oRekInv.akum_iuran_pk
    oTransaksi.mutasi_iuran_pst = -oRekInv.akum_iuran_pst
    oTransaksi.mutasi_iuran_tmb = -oRekInv.akum_iuran_tmb
    oTransaksi.mutasi_psl = -oRekInv.akum_psl
    oTransaksi.mutasi_pmb_pk = -oRekInv.akum_pmb_pk
    oTransaksi.mutasi_pmb_pst = -oRekInv.akum_pmb_pst
    oTransaksi.mutasi_pmb_tmb = -oRekInv.akum_pmb_tmb
    oTransaksi.mutasi_pmb_psl = -oRekInv.akum_pmb_psl

    #nihilkan saldo RekeningInvDPLK
    oRekInv.akum_iuran_pk = 0.0
    oRekInv.akum_iuran_pst = 0.0
    oRekInv.akum_iuran_tmb = 0.0
    oRekInv.akum_psl = 0.0
    oRekInv.akum_pmb_pk = 0.0
    oRekInv.akum_pmb_pst = 0.0
    oRekInv.akum_pmb_tmb = 0.0
    oRekInv.akum_pmb_psl = 0.0
    
    #nihilkan saldo tiap RekeningDPLK
    Ls_DetilTransaksi = oTransaksi.Ls_DetilTransaksiDPLK
    while not Ls_DetilTransaksi.EndOfList:
      oDetilTransaksi = Ls_DetilTransaksi.CurrentElement
      
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = oDetilTransaksi.nomor_rekening
      oRekDPLK.akum_iuran_pk = 0.0
      oRekDPLK.akum_iuran_pst = 0.0
      oRekDPLK.akum_iuran_tmb = 0.0
      oRekDPLK.akum_psl = 0.0
      oRekDPLK.akum_pmb_pk = 0.0
      oRekDPLK.akum_pmb_pst = 0.0
      oRekDPLK.akum_pmb_tmb = 0.0
      oRekDPLK.akum_pmb_psl = 0.0
      
      #update mutasi transaksi DetilTransaksi
      oDetilTransaksi.mutasi_iuran_pk = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_pk  
      oDetilTransaksi.mutasi_iuran_pst = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_pst  
      oDetilTransaksi.mutasi_iuran_tmb = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_iuran_tmb
      oDetilTransaksi.mutasi_psl = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_psl
      oDetilTransaksi.mutasi_pmb_pk = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_pk
      oDetilTransaksi.mutasi_pmb_pst = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_pst 
      oDetilTransaksi.mutasi_pmb_tmb = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_tmb 
      oDetilTransaksi.mutasi_pmb_psl = (oRekDPLK.pct_alokasi / 100.0) * oTransaksi.mutasi_pmb_psl 

      Ls_DetilTransaksi.Next()
    #--
    
    #penutupan RekeningInvDPLK, samakan tgl tutup dengan tgl transaksi
    oRekInv.status_DPLK = 'N'
    oRekInv.tgl_tutup = oTransaksi.tgl_transaksi
  #--end PengembalianDana

  #set status committed true dan data otorisasi
  oTransaksi.isCommitted = 'T'
  oTransaksi.user_id_auth = config.SecurityContext.UserID
  oTransaksi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oTransaksi.tgl_otorisasi = config.ModLibUtils.Now()

def RejectOperation(config, oTransaksi):
  oTransaksi = oTransaksi.CastToLowestDescendant()
  
  #hapus list Advis history dan detil transaksi DPLK
  if oTransaksi.IsA("TransaksiDPLK"):
    oTransaksi.Ls_AdvisHistory.DeleteAllPObjs()
    oTransaksi.Ls_DetilTransaksiDPLK.DeleteAllPObjs()
  
  #hapus objek transaksi
  oTransaksi.Delete()
    
  return 1

def GoOperasiWithMode(config, idTransaksi, mode):
  oTransaksi = config.CreatePObjImplProxy('TransaksiRekInvDPLK')
  oTransaksi.Key = idTransaksi

  if mode == 'A':
    #mode Approval
    ApproveOperation(config, oTransaksi)

  elif mode == 'R':
    #mode Rejection
    RejectOperation(config, oTransaksi)

  elif mode == 'V':
    #mode Verify, not defined yet...used in massal import
    pass

  return 1

def ProsesOtorisasi(config, idTransaksi, mode):
  config.BeginTransaction()
  try:
    GoOperasiWithMode(config, idTransaksi, mode)

    config.Commit()
    errorStatus = 0
    errorMessage = ""
  except:
    config.Rollback()
    errorStatus = 1
    errorMessage = "Gagal otorisasi transaksi: "+ str(sys.exc_info()[1])

  return errorStatus, errorMessage

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  #mode value: 'A' Approve, 'R' Reject, 'V' Verify   
  mode = parameter.FirstRecord.mode 
  idTransaksi = parameter.FirstRecord.id_transaksi
  #proses otorisasi transaksi
  errorStatus, errorMessage = ProsesOtorisasi(config, idTransaksi, mode)
  
  ds = returnpacket.AddNewDatasetEx("status", "error_status: integer; error_message: string;")
  rec = ds.AddRecord()
  rec.error_status = errorStatus
  rec.error_message = errorMessage

  return 1