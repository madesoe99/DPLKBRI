# CATATAN :
# 17 September 2010 : SEMUA PENARIKAN DARI GIRO PAKET A, BUKAN GIRO PAKET MASING - MASING  

import sys

class record : pass

def AssignBranchCurrency(config, record):
  #ambil setting yang ada di variabel default
  record.branchCode = config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', \
    'BranchCodeTransaksi')
  record.currencyCode = config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', \
    'DefaultCurrency')
  
def AssignBranchCurrencyPremi(config, record):
  #ambil setting yang ada di variabel default
  record.branchCode = config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', \
    'BranchCodePremi')
  record.currencyCode = config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', \
    'DefaultCurrency')

def AssignOriginBatch(record, rSQL, oTB):
  #isikan keterangan asal batch pada record
  record.originBatch = '%s:%d:%s:%s' % (oTB.account_link_type,oTB.ID_TransactionBatch, \
    rSQL.KODE_JENIS_TRANSAKSI,rSQL.KODE_PAKET_INVESTASI)

def AssignOriginBatchPremi(record, rSQL, oTB):
  #isikan keterangan asal batch pada record
  record.originBatch = '%s:%d:%s' % (oTB.account_link_type,oTB.ID_TransactionBatch, \
    rSQL.JENIS_TRANSAKSI)

def AssignOriginBatchDaftar(record, oTB):
  #isikan keterangan asal batch pada record
  record.originBatch = '%s:%d' % (oTB.account_link_type,oTB.ID_TransactionBatch)

def AssignOriginBatchInvestasi(record, oTB, oTI):
  #isikan keterangan asal batch pada record
  record.originBatch = '%s:%d:%s' % (oTB.account_link_type,oTB.ID_TransactionBatch, \
    oTI.kode_jenis_trinvestasi)

def CreatingInvestmentRecord(config, dataset, oTB):

  sys.path.append(config.HomeDir + '/scripts/appinterface')
  oModule = __import__('BatchInvestasiProcess')
  oReq = record()
  oReq.dataset = dataset
  oReq.oTB = oTB

  oModule.FunctionMain(config, oReq)
    
  return 1

def CreatingPremiRecord(config, dataset, rSQL, namaTransaksi, oTB):
  rSQL.First()
  while not rSQL.Eof:
  
    if rSQL.JENIS_TRANSAKSI == 'M':
      #transaksi premi manual, hanya buat 1 item jurnal (tidak lengkap)
      #cek flag isDebet, untuk menentukan debet atau kredit
      if rSQL.ISDEBET == 'T':
        debit = rSQL.sum_mutasi_premi; credit = 0.0
      else:
        debit = 0.0; credit = rSQL.sum_mutasi_premi
      ket = '%s: akumulasi Kewajiban Premi ke Asuransi Takaful' % (namaTransaksi)
      CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_PREMI', debit, credit, ket)

    elif rSQL.JENIS_TRANSAKSI == 'S':
      #setoran premi, buat 2 jurnal item (omitted)
      pass
      
    elif rSQL.JENIS_TRANSAKSI == 'T':
      #titipan premi, buat 2 jurnal item
      
      #Cr Kewajiban Premi ke Asuransi Takaful
      ket = '%s: akumulasi Kewajiban Premi ke Asuransi Takaful' % (namaTransaksi)
      CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_PREMI', 0.0, rSQL.sum_mutasi_premi, ket)
      if oTB.account_link_type == 'S':
        ket = '%s: akumulasi Giro Premi' % (namaTransaksi)
        CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'GR_PREMI', rSQL.sum_mutasi_premi, 0.0, ket)

    rSQL.Next()
    
  return 1

def CreateSingleRecord(config, dataset, oTB, rSQL, tab_param, key, debit, credit, ket):
  if debit <> 0.0 or credit <> 0.0:
    rec = dataset.AddRecord()
    if tab_param <> 'HistoriGiro':
      oPI = config.CreatePObjImplProxy(tab_param)
      oPI.Key = key
    
    if tab_param == 'PaketInvestasi':    
      rec.accountCode = oPI.acc_giro
    elif tab_param == 'GLInterface':
      rec.accountCode = oPI.account_code 
    elif tab_param == 'HistoriGiro':
      oPI = config.CreatePObjImplProxy('PaketInvestasi')
      oPI.Key = key
      oMG = config.CreatePObjImplProxy('MasterGiro')
      oMG.key = oPI.acc_giro
      rec.accountCode = oMG.acc_histori_giro 
    
    rec.debit = debit 
    rec.credit = credit 
    
    AssignBranchCurrency(config, rec)
    AssignOriginBatch(rec, rSQL, oTB)
    rec.keterangan = ket
      
def CreateTransaksiIuran(config, dataset, oTB, rSQL, namaTransaksi):
  #Debet : Giro Paket, Credit : Kewajiban Iuran
  kode_paket = rSQL.KODE_PAKET_INVESTASI 
  ket = '%s: akumulasi Iuran Peserta paket %s' % (namaTransaksi, kode_paket)
  nom_iuran_pk = (rSQL.sum_mutasi_pk or 0.0) 
  nom_iuran_pst = (rSQL.sum_mutasi_pst or 0.0)
  nom_iuran = nom_iuran_pk + nom_iuran_pst  
  CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, nom_iuran, 0.0, ket)      
  if oTB.account_link_type == 'S':
    ket = '%s: kewajiban Iuran Peserta paket %s' % (namaTransaksi, kode_paket) 
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_IURAN', 0.0, nom_iuran_pst, ket)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_IURAN_PK', 0.0, nom_iuran_pk, ket)
    
def CreateTransaksiBiayaPengelolaan(config, dataset, oTB, rSQL, namaTransaksi):
  #Cr untuk Kewajiban Biaya Pengelolaan
  kode_paket = rSQL.KODE_PAKET_INVESTASI 
  ket = '%s: fee Biaya Pengelolaan paket %s' % (namaTransaksi, kode_paket)
  nom_biaya = abs((rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) + \
    (rSQL.sum_mutasi_pengembangan or 0.0) + (rSQL.sum_mutasi_peralihan or 0.0))      
  CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_KELOLA', 0.0, nom_biaya, ket)
  
  if oTB.account_link_type == 'S':
    #Single: Dr untuk Pengurang Biaya Pengelolaan, supaya jurnal langsung lengkap
    ket = '%s: Pengurang Biaya Pengelolaan paket %s' % (namaTransaksi, kode_paket)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'PA_KELOLA', nom_biaya, 0.0, ket)
      
def CreateTransaksiBiayaAdm(config, dataset, oTB, rSQL, namaTransaksi):
  kode_paket = rSQL.KODE_PAKET_INVESTASI 
  nom_biaya = abs((rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) + \
    (rSQL.sum_mutasi_pengembangan or 0.0) + (rSQL.sum_mutasi_peralihan or 0.0))
  ket = '%s: fee Biaya Administrasi Tahunan paket %s' % (namaTransaksi, kode_paket)
  #Cr untuk Kewajiban Biaya Administrasi Tahunan
  CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_ADM', nom_biaya, 0.0, ket)
  
  if oTB.account_link_type == 'S':
    #Single: Dr untuk Pengurang Biaya Pengelolaan, supaya jurnal langsung lengkap
    ket = '%s: Pengurang Biaya Administrasi Tahunan paket %s' % (namaTransaksi, kode_paket)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'PA_ADM', 0.0, nom_biaya, ket)

def CreateTransaksiPindahPaket(config, dataset, oTB, rSQL, namaTransaksi):
  kode_paket = rSQL.KODE_PAKET_INVESTASI 
  ket = '%s: pengurang manfaat pindah paket %s' % (namaTransaksi, kode_paket)
  nom_pindah = abs((rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) + \
    (rSQL.sum_mutasi_pengembangan or 0.0) + (rSQL.sum_mutasi_peralihan or 0.0))
  CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'PA_PAKET', nom_pindah, 0.0, ket)
  if oTB.account_link_type == 'S':
    ket = '%s: kewajiban Biaya Pindah Paket Investasi paket %s' % (namaTransaksi, kode_paket)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_PAKET', 0.0, nom_pindah, ket)

def CreateTransaksiBagiHasil(config, dataset, oTB, rSQL, namaTransaksi):
  kode_paket = rSQL.KODE_PAKET_INVESTASI 
  ket = '%s: kewajiban dana Hasil Pengembangan dibagikan paket %s' % (namaTransaksi, kode_paket)
  CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_BGINVES', 0.0, rSQL.sum_mutasi_pengembangan, ket)
  if oTB.account_link_type == 'S':
    #Single: Dr untuk Kewajiban Dana Hasil Pengembangan, supaya jurnal langsung lengkap
    ket = '%s: kewajiban dana Hasil Pengembangan paket %s' % (namaTransaksi, kode_paket)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_INVEST', rSQL.sum_mutasi_pengembangan, 0.0, ket)

def CreateTransaksiPengalihanKeDPLK(config, dataset, oTB, rSQL, namaTransaksi):
  # - Biaya Pindah (X = Biaya Transaksi)
  # - Saldo dana dipindahkan
  # - Biaya lain-lain (Biaya buku cek/kliring)
  # * batasi dengan id_batch, kode_paket_investasi
  kode_paket = rSQL.KODE_PAKET_INVESTASI   
  sSQLSpesial = 'select SUM(p.SALDO_DANA_DIPINDAHKAN) as sum_saldo_dipindah, \
                        SUM(p.BIAYA_PINDAH) as sum_biaya_pindah, \
                        SUM(p.BIAYA_LAIN) as sum_biaya_lain \
                 from PENGALIHANKEDPLKLAIN p, TRANSAKSIDPLK t \
                 where p.ID_Transaksi = t.ID_Transaksi and \
                       t.ID_TRANSACTIONBATCH = %d and \
                       t.KODE_PAKET_INVESTASI = \'%s\'' \
                 % (oTB.ID_TransactionBatch, kode_paket)
  rSQLSpesial = config.CreateSQL(sSQLSpesial).RawResult  
  rSQLSpesial.First()
  ket1 = '%s: pengurang Pengalihan ke DPLK lain paket %s' % (namaTransaksi, kode_paket)
  ket2 = '%s: fee Biaya Pindah ke DPLK lain paket %s' % (namaTransaksi, kode_paket)
  ket3 = '%s: fee Biaya buku cek / kliring paket %s' % (namaTransaksi, kode_paket)
  ket4 = '%s: kewajiban Pengalihan Dana ke DP Lain paket %s' % (namaTransaksi, kode_paket)
  
  while not rSQLSpesial.Eof:
    nom_biaya_pindah = (rSQLSpesial.sum_biaya_pindah or 0.0)
    nom_saldo_pindah = (rSQLSpesial.sum_saldo_dipindah or 0.0) 
    nom_biaya_lain = (rSQLSpesial.sum_biaya_lain or 0.0) 
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'PA_ALIHKE', nom_saldo_pindah + nom_biaya_pindah, 0.0, ket1)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_ADM', 0.0, nom_biaya_pindah, ket2)
#     CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_CEK', 0.0, nom_biaya_lain, ket3)
    
    if oTB.account_link_type == 'S':
      CreateSingleRecord(config, dataset, oTB, rSQL, 'HistoriGiro', 'A', 0.0, nom_saldo_pindah, ket4)
#       CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, 0.0, nom_saldo_pindah, ket4)

#       CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, 0.0, nom_saldo_pindah - nom_biaya_lain, ket4)      
#       CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_ALIHKE', 0.0, nom_saldo_pindah - nom_biaya_lain, ket4)
      
    rSQLSpesial.Next() 

def CreateTransaksiPengambilanManfaat(config, dataset, oTB, rSQL, namaTransaksi):
      # - Saldo Manfaat
      # - Biaya Pencairan (< 1 th)
      # - Pajak
      # - Manfaat Non Tunai (dibelikan Anuitas)
      # - Biaya lain-lain (Biaya buku cek/kliring)
      # * batasi dengan id_batch, kode_paket_investasi
      kode_paket = rSQL.KODE_PAKET_INVESTASI
      sSQLSpesial = 'select SUM(p.SALDO_MANFAAT) as sum_saldo_manfaat, \
                            SUM(p.BIAYA_PENCAIRAN) as sum_biaya_pencairan, \
                            SUM(p.BIAYA_LAIN) as sum_biaya_lain, \
                            SUM(p.MANFAAT_ANUITAS) as sum_manfaat_anuitas, \
                            SUM(p.PAJAK) as sum_pajak \
                     from PENGAMBILANMANFAAT p, TRANSAKSIDPLK t \
                     where p.ID_Transaksi = t.ID_Transaksi and \
                           t.ID_TRANSACTIONBATCH = %d and \
                           t.KODE_PAKET_INVESTASI = \'%s\'' \
                     % (oTB.ID_TransactionBatch, kode_paket)
      rSQLSpesial = config.CreateSQL(sSQLSpesial).RawResult
      ket1 = '%s: pengurang Tarik Manfaat peserta paket %s' % (namaTransaksi, kode_paket)
      ket2 = '%s: fee Biaya Kepesertaan < 1 tahun paket %s' % (namaTransaksi, kode_paket)
      ket3 = '%s: fee Kewajiban PPh peserta paket %s' % (namaTransaksi, kode_paket)
      ket4 = '%s: fee Biaya buku cek / kliring paket %s' % (namaTransaksi, kode_paket)
      ket5 = '%s: kewajiban Hutang Manfaat Anuitas paket %s' % (namaTransaksi, kode_paket)
      ket6 = '%s: kewajiban Penarikan Manfaat Tunai paket %s' % (namaTransaksi, kode_paket)
      
      rSQLSpesial.First()
      while not rSQLSpesial.Eof:
        nom_manfaat = (rSQLSpesial.sum_saldo_manfaat or 0.0)
        nom_biaya_cair = (rSQLSpesial.sum_biaya_pencairan or 0.0)
        nom_pajak = (rSQLSpesial.sum_pajak or 0.0)
        nom_biaya_lain = (rSQLSpesial.sum_biaya_lain or 0.0)
        nom_anuitas = rSQLSpesial.sum_manfaat_anuitas or 0.0
        #Dr untuk Penarikan Manfaat Pensiun
        CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'PA_MANFAAT', nom_manfaat + nom_biaya_cair, 0.0, ket1)              
        #Cr untuk Fee Kepesertaan < 1 tahun
        CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_ADM', 0.0, nom_biaya_cair, ket2)              
        #Cr untuk Kewajiban PPh peserta
        CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_PPH', 0.0, nom_pajak, ket3)              
        #Cr untuk Biaya buku cek / kliring
#         CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_CEK', 0.0, nom_biaya_lain, ket4)              
        #Cr untuk Kewajiban Hutang Manfaat Anuitas
        CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'HUT_MP', 0.0, nom_anuitas, ket5)
        if oTB.account_link_type == 'S':
          #Single: Cr untuk Kewajiban Penarikan Manfaat Tunai, 
          nom = nom_manfaat - nom_pajak - nom_anuitas
#           nom = nom_manfaat - nom_pajak - nom_biaya_lain - nom_anuitas
#           CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_MPTUNAI', 0.0, nom, ket6)
          CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', 'A', 0.0, nom, ket6)      

        rSQLSpesial.Next() 
      
def CreateTransaksiPengalihanDariDPLain(config, dataset, oTB, rSQL, namaTransaksi):
  dictJenisDP = {'I' : 'DPLK',
                 'O' : 'DPPK',
                 'P' : 'DPK'}
  kode_paket = rSQL.KODE_PAKET_INVESTASI
  nom_iuran = (rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0)
  nom_pengembangan = rSQL.sum_mutasi_pengembangan or 0.0
  nom_peralihan = rSQL.sum_mutasi_peralihan or 0.0
  nom_total = nom_iuran + nom_pengembangan + nom_peralihan   
  ket1 = '%s: akumulasi iuran Pengalihan dari DPLK lain paket %s' % (namaTransaksi, kode_paket)
  ket2 = '%s: akumulasi pengembangan Pengalihan dari DPLK lain paket %s' % (namaTransaksi, kode_paket)
  ket3 = '%s: akumulasi peralihan Pengalihan dari DPLK lain paket %s' % (namaTransaksi, kode_paket)
  ket4 = '%s: akumulasi Pengalihan dari %s lain paket %s' % (namaTransaksi, dictJenisDP[rSQL.KODE_JENIS_TRANSAKSI], kode_paket)
  ket5 = '%s: kewajiban dana Peralihan dari %s lain paket %s' % (namaTransaksi, dictJenisDP[rSQL.KODE_JENIS_TRANSAKSI], kode_paket)

  if rSQL.KODE_JENIS_TRANSAKSI == 'I': # dari DPLK
#     CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, nom_iuran, 0.0, ket1)
#     CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, nom_pengembangan, 0.0, ket2)
#     CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, nom_peralihan, 0.0, ket3)  
    CreateSingleRecord(config, dataset, oTB, rSQL, 'HistoriGiro', 'A', nom_iuran, 0.0, ket1)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'HistoriGiro', 'A', nom_pengembangan, 0.0, ket2)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'HistoriGiro', 'A', nom_peralihan, 0.0, ket3)  

  else: # dari DPPK dan DPK
#     CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, nom_total, 0.0, ket4)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'HistoriGiro', 'A', nom_total, 0.0, ket4)
      
  if oTB.account_link_type == 'S':
    #Single: Cr untuk Kewajiban dana Peralihan dari DPLK,DPPK,DPK lain,
    if dictJenisDP[rSQL.KODE_JENIS_TRANSAKSI] == 'DPLK': 
      CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_ALIHDPLK', 0.0, nom_total, ket5)
    else:
      CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_ALIHDPPK', 0.0, nom_total, ket5)


def CreateTransaksiPenarikan30(config, dataset, oTB, rSQL, namaTransaksi):
  kode_paket = rSQL.KODE_PAKET_INVESTASI
  sSQLSpesial = "select SUM(p.jml_tarik) as sum_jml_tarik, \
                        SUM(p.BIAYA_TARIK) as sum_biaya_tarik, \
                        SUM(p.BIAYA_LAIN) as sum_biaya_lain, \
                        SUM(p.PAJAK) as sum_pajak \
                 from PENARIKANDANA p, TRANSAKSIDPLK t \
                 where t.kode_jenis_transaksi = 'V' and \
                       p.ID_Transaksi = t.ID_Transaksi and \
                       t.ID_TRANSACTIONBATCH = %d and \
                       t.KODE_PAKET_INVESTASI = '%s'" \
                 % (oTB.ID_TransactionBatch,rSQL.KODE_PAKET_INVESTASI)
  rSQLSpesial = config.CreateSQL(sSQLSpesial).RawResult
  ket1 = '%s: pengurang Penarikan Dana 30%% paket %s' % (namaTransaksi, kode_paket)
  ket2 = '%s: fee Biaya Penarikan 30%% paket %s'  % (namaTransaksi, kode_paket)
  ket3 = '%s: fee Kewajiban PPh peserta paket %s' % (namaTransaksi, kode_paket)
  ket4 = '%s: fee Biaya buku cek / kliring paket %s' % (namaTransaksi, kode_paket)
  ket5 = '%s: kewajiban Penarikan Dana 30%% paket %s' % (namaTransaksi, kode_paket)
    
  rSQLSpesial.First()
  while not rSQLSpesial.Eof:
    nom_tarik = (rSQLSpesial.sum_jml_tarik or 0.0)
    nom_biaya_tarik = (rSQLSpesial.sum_biaya_tarik or 0.0)
    nom_pajak = rSQLSpesial.sum_pajak or 0.0
    nom_biaya_lain = rSQLSpesial.sum_biaya_lain or 0.0
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'PA_TARIK', nom_tarik, 0.0, ket1)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'PA_ADM', nom_biaya_tarik, 0.0, ket1)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_ADM', 0.0, nom_biaya_tarik, ket2)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_PPH', 0.0, nom_pajak, ket3)
#     CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_CEK', 0.0, nom_biaya_lain, ket4)
    
    if oTB.account_link_type == 'S':
      #Single: Cr untuk Kewajiban Pengalihan Dana ke DP Lain, 
#       CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_TRKDANA', 0.0, nom_tarik - nom_pajak - nom_biaya_lain, ket5)
#       CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, 0.0, nom_tarik - nom_pajak - nom_biaya_lain, ket5)
      CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', 'A', 0.0, nom_tarik - nom_pajak, ket5)

    rSQLSpesial.Next() 

def CreateTransaksiPenarikanPHK(config, dataset, oTB, rSQL, namaTransaksi):
  kode_paket = rSQL.KODE_PAKET_INVESTASI
  sSQLSpesial = "select SUM(p.jml_tarik) as sum_jml_tarik, \
                        SUM(p.BIAYA_TARIK) as sum_biaya_tarik, \
                        SUM(p.BIAYA_LAIN) as sum_biaya_lain, \
                        SUM(p.PAJAK) as sum_pajak \
                 from PENARIKANDANA p, TRANSAKSIDPLK t \
                 where t.kode_jenis_transaksi = 'W' and \
                       p.ID_Transaksi = t.ID_Transaksi and \
                       t.ID_TRANSACTIONBATCH = %d and \
                       t.KODE_PAKET_INVESTASI = '%s'" \
                 % (oTB.ID_TransactionBatch,rSQL.KODE_PAKET_INVESTASI)
  rSQLSpesial = config.CreateSQL(sSQLSpesial).RawResult
  ket1 =  '%s: pengurang Penarikan Dana PHK paket %s' % (namaTransaksi, kode_paket)
  ket2 =  '%s: fee Biaya Penarikan PHK paket %s' % (namaTransaksi, kode_paket)
  ket3 =  '%s: fee Kewajiban PPh peserta paket %s' % (namaTransaksi, kode_paket)
  ket4 =  '%s: fee Biaya buku cek / kliring paket %s' % (namaTransaksi, kode_paket)
  ket5 =  '%s: kewajiban Penarikan Dana PHK paket %s' % (namaTransaksi, kode_paket)
  
  rSQLSpesial.First()  
  while not rSQLSpesial.Eof:
    nom_tarik = rSQLSpesial.sum_jml_tarik or 0.0
    nom_biaya_tarik = rSQLSpesial.sum_biaya_tarik or 0.0
    nom_pajak = rSQLSpesial.sum_pajak or 0.0
    nom_biaya_lain = rSQLSpesial.sum_biaya_lain or 0.0
    #Dr untuk Penarikan Dana PHK
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'PA_TARIK', nom_tarik, 0.0, ket1)
    #Cr untuk Kewajiban Beban PHK
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_PHK', 0.0, nom_biaya_tarik, ket2)
    #Cr untuk Kewajiban PPh peserta
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_PPH', 0.0, nom_pajak, ket3)
    #Cr untuk Biaya buku cek / kliring
#     CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_CEK', 0.0, nom_biaya_lain, ket4)
    
    if oTB.account_link_type == 'S':
      #Single: Cr untuk Kewajiban Pengalihan Dana ke DP Lain,
#       nom_kwjb = nom_tarik - nom_biaya_tarik - nom_pajak - nom_biaya_lain
      nom_kwjb = nom_tarik - nom_pajak - nom_biaya_tarik
#       CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_TRKDANA', 0.0, nom_kwjb, ket5)
      CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', 'A', 0.0, nom_kwjb, ket5)  
    rSQLSpesial.Next() 

def CreateTransaksiManual(config, dataset, oTB, rSQL, namaTransaksi):
  kode_paket = rSQL.KODE_PAKET_INVESTASI 
  #cek masing-masing field sum_mutasi
  if rSQL.sum_mutasi_pk != 0.0 or rSQL.sum_mutasi_pst != 0.0:
    sum_iuran = (rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) 
    if sum_iuran > 0: 
      debit = 0.0; credit = abs(sum_iuran)
    else: 
      debit = abs(sum_iuran); credit = 0.0
      
    ket1 = '%s: akumulasi Iuran Peserta paket %s' % (namaTransaksi, kode_paket)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'PaketInvestasi', kode_paket, debit, credit, ket1)
    
  elif rSQL.sum_mutasi_pengembangan > 0.0:
    if rSQL.sum_mutasi_pengembangan > 0: 
      debit = 0.0; credit = abs(rSQL.sum_mutasi_pengembangan)
    else:
      debit = abs(rSQL.sum_mutasi_pengembangan);  credit = 0.0
      
    ket2 = '%s: kewajiban dana Hasil Pengembangan dibagikan paket %s' % (namaTransaksi, kode_paket)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_BGINVES', debit, credit, ket2)
  
  elif rSQL.sum_mutasi_peralihan > 0.0:
    if rSQL.sum_mutasi_peralihan > 0:
      debit = 0.0; credit = abs(rSQL.sum_mutasi_peralihan)
    else:
      debit = abs(rSQL.sum_mutasi_peralihan); credit = 0.0

    ket3 = '%s: kewajiban dana Peralihan dari DP lain paket %s' % (namaTransaksi, kode_paket)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'KW_ALIHDPLK', debit, credit, ket3)
    
def CreatingTransactionRecord(config, dataset, rSQL, namaTransaksi, oTB):
  #buat record untuk agregate transaksi DPLK
  rSQL.First()
  while not rSQL.Eof:   
    if rSQL.KODE_JENIS_TRANSAKSI == 'K': 
      CreateTransaksiIuran(config, dataset, oTB, rSQL, namaTransaksi)
            
    elif rSQL.KODE_JENIS_TRANSAKSI == 'C':
      CreateTransaksiBiayaPengelolaan(config, dataset, oTB, rSQL, namaTransaksi)
              
    elif rSQL.KODE_JENIS_TRANSAKSI == 'D':
      CreateTransaksiBiayaAdm(config, dataset, oTB, rSQL, namaTransaksi)
      
    elif rSQL.KODE_JENIS_TRANSAKSI == 'X':
      CreateTransaksiPindahPaket(config, dataset, oTB, rSQL, namaTransaksi)
      
#     elif rSQL.KODE_JENIS_TRANSAKSI == 'G':
#       CreateTransaksiBagiHasil(config, dataset, oTB, rSQL, namaTransaksi)
      
    elif rSQL.KODE_JENIS_TRANSAKSI == 'H':
      CreateTransaksiPengalihanKeDPLK(config, dataset, oTB, rSQL, namaTransaksi)
        
    elif rSQL.KODE_JENIS_TRANSAKSI == 'J':
      CreateTransaksiPengambilanManfaat(config, dataset, oTB, rSQL, namaTransaksi)
            
    elif rSQL.KODE_JENIS_TRANSAKSI in ['I','O','P']:
      CreateTransaksiPengalihanDariDPLain(config, dataset, oTB, rSQL, namaTransaksi)

    elif rSQL.KODE_JENIS_TRANSAKSI == 'V':
      CreateTransaksiPenarikan30(config, dataset, oTB, rSQL, namaTransaksi)
      
    elif rSQL.KODE_JENIS_TRANSAKSI == 'W':
      CreateTransaksiPenarikanPHK(config, dataset, oTB, rSQL, namaTransaksi)
      
    elif rSQL.KODE_JENIS_TRANSAKSI == 'M':
      CreateTransaksiManual(config, dataset, oTB, rSQL, namaTransaksi)

    rSQL.Next()

  return 1

def CreatingRegistrationRecord(config, dataset, rSQL, namaTransaksi, oTB):

  #Cr Fee Pendaftaran
  ket = '%s: akumulasi fee Pendaftaran' % (namaTransaksi)
  CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'BBN_DAFTAR', 0.0, rSQL.sum_biaya_daftar, ket)

  if oTB.account_link_type == 'S':
    #Dr Giro Pendaftaran
    rec.keterangan = '%s: akumulasi Giro Pendaftaran' % (namaTransaksi)
    CreateSingleRecord(config, dataset, oTB, rSQL, 'GLInterface', 'GR_DAFTAR', rSQL.sum_biaya_daftar, 0.0, ket)
    
  return 1
  
def AddingTransaksiBatchToDataSet(config, dataset, oTB):
  status = 1

  #cek batch type and nama transaksi
  if oTB.batch_type == 'R':
    sColumn = 'SUM(t.BESAR_BIAYA_DAFTAR) as sum_biaya_daftar, \
               t.ID_TRANSACTIONBATCH '
    sNamaTransaksi = 'IURANPENDAFTARAN'
    sWhere = ''                 
    sGroupBy = 't.ID_TRANSACTIONBATCH'
  elif oTB.batch_type == 'T':
    sColumn = 'SUM(t.MUTASI_IURAN_PK) as sum_mutasi_pk, \
               SUM(t.MUTASI_IURAN_PST) as sum_mutasi_pst, \
               SUM(t.MUTASI_PENGEMBANGAN) as sum_mutasi_pengembangan, \
               SUM(t.MUTASI_PERALIHAN) as sum_mutasi_peralihan, \
               t.KODE_JENIS_TRANSAKSI, \
               t.KODE_PAKET_INVESTASI '
    sNamaTransaksi = 'TRANSAKSIDPLK'
    sWhere = ' and (t.KODE_JENIS_TRANSAKSI <> \'X\' or t.ISPINDAHPAKET = \'T\') '                 
    sGroupBy = 't.KODE_PAKET_INVESTASI,t.KODE_JENIS_TRANSAKSI'
  elif oTB.batch_type == 'P':
    sColumn = 'SUM(MUTASI_PREMI) as sum_mutasi_premi, \
               t.JENIS_TRANSAKSI,\
               t.ISDEBET '
    sNamaTransaksi = 'TRANSAKSIPREMI'
    sWhere = ''                 
    sGroupBy = 't.JENIS_TRANSAKSI,t.ISDEBET'
  #elif oTB.batch_type == 'I':
    #untuk tipe batch investasi ada pengecualian, memakai Ls_TransaksiInvestasi 
  
  #langsung pake SQL saja, sekalian GROUPING & SUMMING (kecuali untuk Investasi)
  if oTB.batch_type != 'I': 
    sSQL = 'select %s \
            from %s t \
            where t.ID_TRANSACTIONBATCH = %d %s \
            group by %s \
            order by %s' \
            % (sColumn,sNamaTransaksi,oTB.ID_TransactionBatch,sWhere,sGroupBy,sGroupBy)
    rSQL = config.CreateSQL(sSQL).RawResult
  
  #bedakan penanganan untuk tiap jenis Transaksi, rSQL-nya beda-beda
  if oTB.batch_type == 'R':
    CreatingRegistrationRecord(config, dataset, rSQL, sNamaTransaksi, oTB)
  elif oTB.batch_type == 'T':
    CreatingTransactionRecord(config, dataset, rSQL, sNamaTransaksi, oTB)  
  elif oTB.batch_type == 'P':  
    CreatingPremiRecord(config, dataset, rSQL, sNamaTransaksi, oTB)      
  elif oTB.batch_type == 'I':
    CreatingInvestmentRecord(config, dataset, oTB)  
        
  return status

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  config.BeginTransaction()
  try:
    dsObjectInfo = parameter.GetDatasetByName('__ObjectInfo')
    recOI = dsObjectInfo.GetRecord(0)

    # buat object yang terdefinisi dalam objek info
    objClassName = recOI.className
    objKey = recOI.objectID
    blockID = recOI.blockID
    
    parameter.DeleteDataset('__ObjectInfo')
    sSerial = parameter.GetSerializationString()
    returnpacket.SetSerializationString(sSerial[0], sSerial[1])
    dsCJI = returnpacket.GetDatasetByName('__CandJournalItem')

    obj = config.CreatePObjImplProxy(objClassName)
    obj.Key = objKey
    
    # masukin candidate journal item-nya
    # ASUMSI transaksi bersifat 'ready to pick' (udah lewat fase otorisasi bila ada)
    if objClassName == 'TransactionBatch':
      #add all transaksi dalam batch ke dalam dataset dsCJI
      status = AddingTransaksiBatchToDataSet(config, dsCJI, obj)
      
      if obj.IsFieldNull('journal_block_id'):
        #set id journal block untuk transaction batch
        obj.journal_block_id = blockID
        
    config.Commit()
  except:
    config.Rollback()
    raise  

  return 1
