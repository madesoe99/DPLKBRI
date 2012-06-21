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
      rec = dataset.AddRecord()
      oGLI = config.CreatePObjImplProxy('GLInterface')
      oGLI.Key = 'KW_PREMI'
      
      rec.accountCode = oGLI.account_code
      if rSQL.ISDEBET == 'T':
        #posisi debet
        rec.debit = rSQL.sum_mutasi_premi
        rec.credit = 0.0
      else:
        #posisi kredit 
        rec.debit = 0.0
        rec.credit = rSQL.sum_mutasi_premi
      
      AssignBranchCurrencyPremi(config, rec)
      AssignOriginBatchPremi(rec, rSQL, oTB)
      rec.keterangan = '%s: akumulasi Kewajiban Premi ke Asuransi Takaful' \
        % (namaTransaksi)

    elif rSQL.JENIS_TRANSAKSI == 'S':
      #setoran premi, buat 2 jurnal item (omitted)
      pass
      
    elif rSQL.JENIS_TRANSAKSI == 'T':
      #titipan premi, buat 2 jurnal item
      
      #Cr Kewajiban Premi ke Asuransi Takaful
      rec = dataset.AddRecord()
      oGLI = config.CreatePObjImplProxy('GLInterface')
      oGLI.Key = 'KW_PREMI'
      
      rec.accountCode = oGLI.account_code
      #posisi selalu kredit
      rec.debit = 0.0
      rec.credit = rSQL.sum_mutasi_premi
      
      AssignBranchCurrencyPremi(config, rec)
      AssignOriginBatchPremi(rec, rSQL, oTB)
      rec.keterangan = '%s: akumulasi Kewajiban Premi ke Asuransi Takaful' \
        % (namaTransaksi)

      if oTB.account_link_type == 'S':
        #Dr Giro Premi
        rec = dataset.AddRecord()
        oGLI.Key = 'GR_PREMI'
        
        rec.accountCode = oGLI.account_code
        #posisi selalu kredit
        rec.debit = rSQL.sum_mutasi_premi
        rec.credit = 0.0
        
        AssignBranchCurrencyPremi(config, rec)
        AssignOriginBatchPremi(rec, rSQL, oTB)
        rec.keterangan = '%s: akumulasi Giro Premi' % (namaTransaksi)
        
    rSQL.Next()
    
  return 1

def CreatingTransactionRecord(config, dataset, rSQL, namaTransaksi, oTB):
  #buat record untuk agregate transaksi DPLK
  rSQL.First()
  while not rSQL.Eof:
    
    if rSQL.KODE_JENIS_TRANSAKSI == 'K':
      #iuran peserta buat 2 jurnal item
      
      #Dr untuk Giro sesuai paket investasi
      rec = dataset.AddRecord()
      oPI = config.CreatePObjImplProxy('PaketInvestasi')
      oPI.Key = rSQL.KODE_PAKET_INVESTASI 
      
      rec.accountCode = oPI.acc_giro 
      rec.debit = (rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0)
      rec.credit = 0.0
      
      AssignBranchCurrency(config, rec)
      AssignOriginBatch(rec, rSQL, oTB)
      rec.keterangan = '%s: akumulasi Iuran Peserta paket %s' \
        % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
      
      if oTB.account_link_type == 'S':
        #Single: Cr untuk Kewajiban Iuran, supaya jurnal langsung lengkap
        recC = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'KW_IURAN'
        
        recC.accountCode = oGLI.account_code
        recC.debit = rec.credit
        recC.credit = rec.debit
        
        AssignBranchCurrency(config, recC)
        recC.originBatch = rec.originBatch
        recC.keterangan = '%s: kewajiban Iuran Peserta paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        
      
    elif rSQL.KODE_JENIS_TRANSAKSI == 'C':
      #biaya pengelolaan dana buat 2 jurnal item
      
      #Cr untuk Kewajiban Biaya Pengelolaan
      rec = dataset.AddRecord()
      oGLI = config.CreatePObjImplProxy('GLInterface')
      oGLI.Key = 'BBN_KELOLA'
      
      rec.accountCode = oGLI.account_code
      rec.debit = 0.0
      rec.credit = abs((rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) + \
        (rSQL.sum_mutasi_pengembangan or 0.0) + (rSQL.sum_mutasi_peralihan or 0.0))
      
      AssignBranchCurrency(config, rec)
      AssignOriginBatch(rec, rSQL, oTB)
      rec.keterangan = '%s: fee Biaya Pengelolaan paket %s' \
        % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)

      if oTB.account_link_type == 'S':
        #Single: Dr untuk Pengurang Biaya Pengelolaan, supaya jurnal langsung lengkap
        recD = dataset.AddRecord()        
        oGLI.Key = 'PA_KELOLA' 
        
        recD.accountCode = oGLI.account_code 
        recD.debit = rec.credit
        recD.credit = rec.debit
        
        AssignBranchCurrency(config, recD)
        recD.originBatch = rec.originBatch
        recD.keterangan = '%s: Pengurang Biaya Pengelolaan paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)            
      
    elif rSQL.KODE_JENIS_TRANSAKSI == 'D':
      #biaya administrasi tahunan buat 2 jurnal item

      #Cr untuk Kewajiban Biaya Administrasi Tahunan
      rec = dataset.AddRecord()
      oGLI = config.CreatePObjImplProxy('GLInterface')
      oGLI.Key = 'BBN_ADM'
      
      rec.accountCode = oGLI.account_code
      rec.debit = 0.0
      rec.credit = abs((rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) + \
        (rSQL.sum_mutasi_pengembangan or 0.0) + (rSQL.sum_mutasi_peralihan or 0.0))
      
      AssignBranchCurrency(config, rec)
      AssignOriginBatch(rec, rSQL, oTB)
      rec.keterangan = '%s: fee Biaya Administrasi Tahunan paket %s' \
        % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)

      if oTB.account_link_type == 'S':
        #Single: Dr untuk Pengurang Biaya Pengelolaan, supaya jurnal langsung lengkap
        recD = dataset.AddRecord()        
        oGLI.Key = 'PA_ADM' 
        
        recD.accountCode = oGLI.account_code 
        recD.debit = rec.credit
        recD.credit = rec.debit
        
        AssignBranchCurrency(config, recD)
        recD.originBatch = rec.originBatch
        recD.keterangan = '%s: Pengurang Biaya Administrasi Tahunan paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)            
        
    elif rSQL.KODE_JENIS_TRANSAKSI == 'X':
      #pengubahan jenis investasi (biaya pindah paket investasi) buat 2 jurnal item

      #Dr untuk Pengurang manfaat pindah paket
      rec = dataset.AddRecord()
      oGLI = config.CreatePObjImplProxy('GLInterface')
      oGLI.Key = 'PA_PAKET' 
      
      rec.accountCode = oGLI.account_code 
      rec.debit = abs((rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) + \
        (rSQL.sum_mutasi_pengembangan or 0.0) + (rSQL.sum_mutasi_peralihan or 0.0))
      rec.credit = 0.0
      
      AssignBranchCurrency(config, rec)
      AssignOriginBatch(rec, rSQL, oTB)
      rec.keterangan = '%s: pengurang manfaat pindah paket %s' \
        % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
      
      if oTB.account_link_type == 'S':
        #Single: Cr untuk Pendapatan, supaya jurnal langsung lengkap
        recC = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'BBN_PAKET'
        
        recC.accountCode = oGLI.account_code
        recC.debit = rec.credit
        recC.credit = rec.debit
        
        AssignBranchCurrency(config, recC)
        recC.originBatch = rec.originBatch
        recC.keterangan = '%s: kewajiban Biaya Pindah Paket Investasi paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
       
    elif rSQL.KODE_JENIS_TRANSAKSI == 'G':
      #bagi hasil buat 2 jurnal item

      #Cr untuk Kewajiban Dana Hasil Pengembangan Dibagikan
      rec = dataset.AddRecord()
      oGLI = config.CreatePObjImplProxy('GLInterface')
      oGLI.Key = 'KW_BGINVES'
      
      rec.accountCode = oGLI.account_code
      rec.debit = 0.0
      rec.credit = rSQL.sum_mutasi_pengembangan
      
      AssignBranchCurrency(config, rec)
      AssignOriginBatch(rec, rSQL, oTB)
      rec.keterangan = '%s: kewajiban dana Hasil Pengembangan dibagikan paket %s' \
        % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)

      if oTB.account_link_type == 'S':
        #Single: Dr untuk Kewajiban Dana Hasil Pengembangan, supaya jurnal langsung lengkap
        recD = dataset.AddRecord()        
        oGLI.Key = 'KW_INVEST' 
        
        recD.accountCode = oGLI.account_code 
        recD.debit = rec.credit
        recD.credit = rec.debit
        
        AssignBranchCurrency(config, recD)
        recD.originBatch = rec.originBatch
        recD.keterangan = '%s: kewajiban dana Hasil Pengembangan paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)            
      
    elif rSQL.KODE_JENIS_TRANSAKSI == 'H':
      #pengalihan ke DPLK lain buat 4 (ABCD) jurnal item
      
      #perlu SQL lagi untuk mendapatkan: 
      # - Biaya Pindah (X = Biaya Transaksi)
      # - Saldo dana dipindahkan
      # - Biaya lain-lain (Biaya buku cek/kliring)
      # * batasi dengan id_batch, kode_paket_investasi
      
      sSQLSpesial = 'select SUM(p.SALDO_DANA_DIPINDAHKAN) as sum_saldo_dipindah, \
                            SUM(p.BIAYA_PINDAH) as sum_biaya_pindah, \
                            SUM(p.BIAYA_LAIN) as sum_biaya_lain \
                     from PENGALIHANKEDPLKLAIN p, TRANSAKSIDPLK t \
                     where p.ID_Transaksi = t.ID_Transaksi and \
                           t.ID_TRANSACTIONBATCH = %d and \
                           t.KODE_PAKET_INVESTASI = \'%s\'' \
                     % (oTB.ID_TransactionBatch,rSQL.KODE_PAKET_INVESTASI)
      rSQLSpesial = config.CreateSQL(sSQLSpesial).RawResult
      
      rSQLSpesial.First()
      while not rSQLSpesial.Eof:
      
        #Dr untuk Pengalihan Dana ke DPLK lain
        recA = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'PA_ALIHKE'
        
        recA.accountCode = oGLI.account_code
        recA.debit = (rSQLSpesial.sum_saldo_dipindah or 0.0) + (rSQLSpesial.sum_biaya_pindah or 0.0)
        recA.credit = 0.0
        
        AssignBranchCurrency(config, recA)
        AssignOriginBatch(recA, rSQL, oTB)
        recA.keterangan = '%s: pengurang Pengalihan ke DPLK lain paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
        
        #Cr untuk Fee Pindah ke DPLK lain
        recB = dataset.AddRecord()
        oGLI.Key = 'BBN_PINDAH'
        
        recB.accountCode = oGLI.account_code
        recB.debit = 0.0
        recB.credit = rSQLSpesial.sum_biaya_pindah
        
        AssignBranchCurrency(config, recB)
        recB.originBatch = recA.originBatch
        recB.keterangan = '%s: fee Biaya Pindah ke DPLK lain paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        
      
        #Cr untuk Fee Biaya buku cek / kliring
        recC = dataset.AddRecord()
        oGLI.Key = 'BBN_CEK'
        
        recC.accountCode = oGLI.account_code
        recC.debit = 0.0
        recC.credit = rSQLSpesial.sum_biaya_lain
        
        AssignBranchCurrency(config, recC)
        recC.originBatch = recA.originBatch
        recC.keterangan = '%s: fee Biaya buku cek / kliring paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        if oTB.account_link_type == 'S':
          #Single: Cr untuk Kewajiban Pengalihan Dana ke DP Lain, 
          #supaya jurnal langsung lengkap
          recD = dataset.AddRecord()
          oGLI.Key = 'KW_ALIHKE'
          
          recD.accountCode = oGLI.account_code
          recD.debit = 0.0
          recD.credit = (rSQLSpesial.sum_saldo_dipindah or 0.0) - (rSQLSpesial.sum_biaya_lain or 0.0)
          
          AssignBranchCurrency(config, recD)
          recD.originBatch = recA.originBatch
          recD.keterangan = '%s: kewajiban Pengalihan Dana ke DP Lain paket %s' \
            % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        rSQLSpesial.Next() 
        
    elif rSQL.KODE_JENIS_TRANSAKSI == 'J':
      #pengambilan manfaat buat 6 (ABCDEF) jurnal item

      #perlu SQL lagi untuk mendapatkan: 
      # - Saldo Manfaat
      # - Biaya Pencairan (< 1 th)
      # - Pajak
      # - Manfaat Non Tunai (dibelikan Anuitas)
      # - Biaya lain-lain (Biaya buku cek/kliring)
      # * batasi dengan id_batch, kode_paket_investasi
      
      sSQLSpesial = 'select SUM(p.SALDO_MANFAAT) as sum_saldo_manfaat, \
                            SUM(p.BIAYA_PENCAIRAN) as sum_biaya_pencairan, \
                            SUM(p.BIAYA_LAIN) as sum_biaya_lain, \
                            SUM(p.MANFAAT_ANUITAS) as sum_manfaat_anuitas, \
                            SUM(p.PAJAK) as sum_pajak \
                     from PENGAMBILANMANFAAT p, TRANSAKSIDPLK t \
                     where p.ID_Transaksi = t.ID_Transaksi and \
                           t.ID_TRANSACTIONBATCH = %d and \
                           t.KODE_PAKET_INVESTASI = \'%s\'' \
                     % (oTB.ID_TransactionBatch,rSQL.KODE_PAKET_INVESTASI)
      rSQLSpesial = config.CreateSQL(sSQLSpesial).RawResult
      
      rSQLSpesial.First()
      while not rSQLSpesial.Eof:
      
        #Dr untuk Penarikan Manfaat Pensiun
        recA = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'PA_MANFAAT'
        
        recA.accountCode = oGLI.account_code
        recA.debit = (rSQLSpesial.sum_saldo_manfaat or 0.0) + (rSQLSpesial.sum_biaya_pencairan or 0.0)
        recA.credit = 0.0
        
        AssignBranchCurrency(config, recA)
        AssignOriginBatch(recA, rSQL, oTB)
        recA.keterangan = '%s: pengurang Tarik Manfaat peserta paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
        
        #Cr untuk Fee Kepesertaan < 1 tahun
        recB = dataset.AddRecord()
        oGLI.Key = 'BBN_<1TH'
        
        recB.accountCode = oGLI.account_code
        recB.debit = 0.0
        recB.credit = rSQLSpesial.sum_biaya_pencairan
        
        AssignBranchCurrency(config, recB)
        recB.originBatch = recA.originBatch
        recB.keterangan = '%s: fee Biaya Kepesertaan < 1 tahun paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        
      
        #Cr untuk Kewajiban PPh peserta
        recC = dataset.AddRecord()
        oGLI.Key = 'KW_PPH'
        
        recC.accountCode = oGLI.account_code
        recC.debit = 0.0
        recC.credit = rSQLSpesial.sum_pajak
        
        AssignBranchCurrency(config, recC)
        recC.originBatch = recA.originBatch
        recC.keterangan = '%s: fee Kewajiban PPh peserta paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        #Cr untuk Biaya buku cek / kliring
        recE = dataset.AddRecord()
        oGLI.Key = 'BBN_CEK'
        
        recE.accountCode = oGLI.account_code
        recE.debit = 0.0
        recE.credit = rSQLSpesial.sum_biaya_lain
        
        AssignBranchCurrency(config, recE)
        recE.originBatch = recA.originBatch
        recE.keterangan = '%s: fee Biaya buku cek / kliring paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        #Cr untuk Kewajiban Hutang Manfaat Anuitas
        recF = dataset.AddRecord()
        oGLI.Key = 'KW_MPANUIT'
        
        recF.accountCode = oGLI.account_code
        recF.debit = 0.0
        recF.credit = rSQLSpesial.sum_manfaat_anuitas
        
        AssignBranchCurrency(config, recF)
        recF.originBatch = recA.originBatch
        recF.keterangan = '%s: kewajiban Hutang Manfaat Anuitas paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        if oTB.account_link_type == 'S':
          #Single: Cr untuk Kewajiban Penarikan Manfaat Tunai, 
          #supaya jurnal langsung lengkap
          recD = dataset.AddRecord()
          oGLI.Key = 'KW_MPTUNAI'
          
          recD.accountCode = oGLI.account_code
          recD.debit = 0.0
          recD.credit = (rSQLSpesial.sum_saldo_manfaat or 0.0) - (rSQLSpesial.sum_pajak or 0.0) - \
            (rSQLSpesial.sum_biaya_lain or 0.0) - (rSQLSpesial.sum_manfaat_anuitas or 0.0)
          
          AssignBranchCurrency(config, recD)
          recD.originBatch = recA.originBatch
          recD.keterangan = '%s: kewajiban Penarikan Manfaat Tunai paket %s' \
            % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        rSQLSpesial.Next() 
      
    elif rSQL.KODE_JENIS_TRANSAKSI in ['I','O','P']:
      #pengalihan dari DPLK,DPPK,DPK lain buat 2 jurnal item

      #Dr untuk Giro sesuai paket investasi      
      oPI = config.CreatePObjImplProxy('PaketInvestasi')
      oPI.Key = rSQL.KODE_PAKET_INVESTASI 

      if rSQL.KODE_JENIS_TRANSAKSI == 'I':
        #pengalihan dari DPLK lain, pecah akumulasi dana menjadi 3 item jurnal
        jenisDP = 'DPLK'

        #akumulasi iuran  
        recI = dataset.AddRecord()
        recI.accountCode = oPI.acc_giro 
        recI.debit = (rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0)        
        recI.credit = 0.0
      
        AssignBranchCurrency(config, recI)
        AssignOriginBatch(recI, rSQL, oTB)
        
        recI.keterangan = '%s: akumulasi iuran Pengalihan dari DPLK lain paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
      
        #akumulasi pengembangan
        recP = dataset.AddRecord()
        recP.accountCode = oPI.acc_giro 
        recP.debit = rSQL.sum_mutasi_pengembangan        
        recP.credit = 0.0
      
        AssignBranchCurrency(config, recP)
        AssignOriginBatch(recP, rSQL, oTB)
        
        recP.keterangan = '%s: akumulasi pengembangan Pengalihan dari DPLK lain paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)

        #akumulasi peralihan
        recPer = dataset.AddRecord()
        recPer.accountCode = oPI.acc_giro 
        recPer.debit = rSQL.sum_mutasi_peralihan        
        recPer.credit = 0.0
      
        AssignBranchCurrency(config, recPer)
        AssignOriginBatch(recPer, rSQL, oTB)
        
        recPer.keterangan = '%s: akumulasi peralihan Pengalihan dari DPLK lain paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)

      else:
        #pengalihan dari DPK / DPPK lain, satukan akumulasi dalam 1 item jurnal
        rec = dataset.AddRecord()
        rec.accountCode = oPI.acc_giro 
        rec.debit = (rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) + \
          (rSQL.sum_mutasi_pengembangan or 0.0) + (rSQL.sum_mutasi_peralihan or 0.0)        
        rec.credit = 0.0
      
        AssignBranchCurrency(config, rec)
        AssignOriginBatch(rec, rSQL, oTB)
        
        if rSQL.KODE_JENIS_TRANSAKSI == 'O':
          jenisDP = 'DPPK'
        elif rSQL.KODE_JENIS_TRANSAKSI == 'P':
          jenisDP = 'DPK'
        
        rec.keterangan = '%s: akumulasi Pengalihan dari %s lain paket %s' \
          % (namaTransaksi, jenisDP, rSQL.KODE_PAKET_INVESTASI)
      
      if oTB.account_link_type == 'S':
        #Single: Cr untuk Kewajiban dana Peralihan dari DPLK,DPPK,DPK lain, 
        #supaya jurnal langsung lengkap
        recC = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'KW_ALIHDAR'
        
        recC.accountCode = oGLI.account_code
        recC.debit = 0.0
        recC.credit = (rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) + \
          (rSQL.sum_mutasi_pengembangan or 0.0) + (rSQL.sum_mutasi_peralihan or 0.0)
        
        AssignBranchCurrency(config, recC)
        AssignOriginBatch(recC, rSQL, oTB)
        recC.keterangan = '%s: kewajiban dana Peralihan dari %s lain paket %s' \
          % (namaTransaksi, jenisDP, rSQL.KODE_PAKET_INVESTASI)        

    elif rSQL.KODE_JENIS_TRANSAKSI == 'V':
      config.SendDebugMsg('ccji_ctr')
      #penarikan dana 30% buat 5 (ABCDE) jurnal item

      #perlu SQL lagi untuk mendapatkan: 
      # - Potongan dana pengembangan
      # - Iuran (Jumlah) yang ditarik
      # - Pajak
      # - Biaya lain-lain (Biaya buku cek/kliring)
      # * batasi dengan id_batch, kode_paket_investasi
      
      sSQLSpesial = 'select SUM(p.jml_tarik) as sum_jml_tarik, \
                            SUM(p.BIAYA_TARIK) as sum_biaya_tarik, \
                            SUM(p.BIAYA_LAIN) as sum_biaya_lain, \
                            SUM(p.PAJAK) as sum_pajak \
                     from PENARIKANDANA p, TRANSAKSIDPLK t \
                     where p.penarikan_phk = \'F\' and \
                           p.ID_Transaksi = t.ID_Transaksi and \
                           t.ID_TRANSACTIONBATCH = %d and \
                           t.KODE_PAKET_INVESTASI = \'%s\'' \
                     % (oTB.ID_TransactionBatch,rSQL.KODE_PAKET_INVESTASI)
      rSQLSpesial = config.CreateSQL(sSQLSpesial).RawResult
      
      config.SendDebugMsg('ccji_ctr2')
      rSQLSpesial.First()
      while not rSQLSpesial.Eof:
      
        config.SendDebugMsg('ccji_ctr21')
        #Dr untuk Penarikan Dana Sebagian (30%)
        recA = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'PA_TARIK'
        
        recA.accountCode = oGLI.account_code
        recA.debit = (rSQLSpesial.sum_jml_tarik or 0.0) + (rSQLSpesial.sum_biaya_tarik or 0.0)
        recA.credit = 0.0
        
        AssignBranchCurrency(config, recA)
        AssignOriginBatch(recA, rSQL, oTB)
        recA.keterangan = '%s: pengurang Penarikan Dana 30%% paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
        
        #Cr untuk Fee Penarikan 30%
        recB = dataset.AddRecord()
        oGLI.Key = 'BBN_30%'
        
        recB.accountCode = oGLI.account_code
        recB.debit = 0.0
        recB.credit = rSQLSpesial.sum_biaya_tarik
        
        AssignBranchCurrency(config, recB)
        recB.originBatch = recA.originBatch
        recB.keterangan = '%s: fee Biaya Penarikan 30%% paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        
      
        #Cr untuk Kewajiban PPh peserta
        recC = dataset.AddRecord()
        oGLI.Key = 'KW_PPH'
        
        recC.accountCode = oGLI.account_code
        recC.debit = 0.0
        recC.credit = rSQLSpesial.sum_pajak
        
        AssignBranchCurrency(config, recC)
        recC.originBatch = recA.originBatch
        recC.keterangan = '%s: fee Kewajiban PPh peserta paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        #Cr untuk Biaya buku cek / kliring
        recE = dataset.AddRecord()
        oGLI.Key = 'BBN_CEK'
        
        recE.accountCode = oGLI.account_code
        recE.debit = 0.0
        recE.credit = rSQLSpesial.sum_biaya_lain
        
        AssignBranchCurrency(config, recE)
        recE.originBatch = recA.originBatch
        recE.keterangan = '%s: fee Biaya buku cek / kliring paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        config.SendDebugMsg('ccji_ctr3')
        if oTB.account_link_type == 'S':
          #Single: Cr untuk Kewajiban Pengalihan Dana ke DP Lain, 
          #supaya jurnal langsung lengkap
          recD = dataset.AddRecord()
          oGLI.Key = 'KW_TRKDANA'
          
          recD.accountCode = oGLI.account_code
          recD.debit = 0.0
          recD.credit = (rSQLSpesial.sum_jml_tarik or 0.0) - (rSQLSpesial.sum_pajak or 0.0) - \
            (rSQLSpesial.sum_biaya_lain or 0.0)
          
          AssignBranchCurrency(config, recD)
          recD.originBatch = recA.originBatch
          recD.keterangan = '%s: kewajiban Penarikan Dana 30%% paket %s' \
            % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        rSQLSpesial.Next() 
        config.SendDebugMsg('ccji_ctr4')

    elif rSQL.KODE_JENIS_TRANSAKSI == 'W':
      #penarikan dana PHK buat 5 (ABCDE) jurnal item

      #perlu SQL lagi untuk mendapatkan: 
      # - Biaya Penarikan
      # - Total Iuran (Jumlah) yang ditarik
      # - Pajak
      # - Biaya lain-lain (Biaya buku cek/kliring)
      # * batasi dengan id_batch, kode_paket_investasi
      
      sSQLSpesial = 'select SUM(p.jml_tarik) as sum_jml_tarik, \
                            SUM(p.BIAYA_TARIK) as sum_biaya_tarik, \
                            SUM(p.BIAYA_LAIN) as sum_biaya_lain, \
                            SUM(p.PAJAK) as sum_pajak \
                     from PENARIKANDANA p, TRANSAKSIDPLK t \
                     where p.penarikan_phk = \'T\' and \
                           p.ID_Transaksi = t.ID_Transaksi and \
                           t.ID_TRANSACTIONBATCH = %d and \
                           t.KODE_PAKET_INVESTASI = \'%s\'' \
                     % (oTB.ID_TransactionBatch,rSQL.KODE_PAKET_INVESTASI)
      rSQLSpesial = config.CreateSQL(sSQLSpesial).RawResult
      
      rSQLSpesial.First()
      while not rSQLSpesial.Eof:
      
        #Dr untuk Penarikan Dana PHK
        recA = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'PA_TARIK'
        
        recA.accountCode = oGLI.account_code
        recA.debit = rSQLSpesial.sum_jml_tarik
        recA.credit = 0.0
        
        AssignBranchCurrency(config, recA)
        AssignOriginBatch(recA, rSQL, oTB)
        recA.keterangan = '%s: pengurang Penarikan Dana PHK paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
        
        #Cr untuk Fee Penarikan PHK
        recB = dataset.AddRecord()
        oGLI.Key = 'BBN_PHK'
        
        recB.accountCode = oGLI.account_code
        recB.debit = 0.0
        recB.credit = rSQLSpesial.sum_biaya_tarik
        
        AssignBranchCurrency(config, recB)
        recB.originBatch = recA.originBatch
        recB.keterangan = '%s: fee Biaya Penarikan PHK paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        
      
        #Cr untuk Kewajiban PPh peserta
        recC = dataset.AddRecord()
        oGLI.Key = 'KW_PPH'
        
        recC.accountCode = oGLI.account_code
        recC.debit = 0.0
        recC.credit = rSQLSpesial.sum_pajak
        
        AssignBranchCurrency(config, recC)
        recC.originBatch = recA.originBatch
        recC.keterangan = '%s: fee Kewajiban PPh peserta paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        #Cr untuk Biaya buku cek / kliring
        recE = dataset.AddRecord()
        oGLI.Key = 'BBN_CEK'
        
        recE.accountCode = oGLI.account_code
        recE.debit = 0.0
        recE.credit = rSQLSpesial.sum_biaya_lain
        
        AssignBranchCurrency(config, recE)
        recE.originBatch = recA.originBatch
        recE.keterangan = '%s: fee Biaya buku cek / kliring paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        if oTB.account_link_type == 'S':
          #Single: Cr untuk Kewajiban Pengalihan Dana ke DP Lain, 
          #supaya jurnal langsung lengkap
          recD = dataset.AddRecord()
          oGLI.Key = 'KW_TRKDANA'
          
          recD.accountCode = oGLI.account_code
          recD.debit = 0.0
          recD.credit = (rSQLSpesial.sum_jml_tarik or 0.0) - (rSQLSpesial.sum_pajak or 0.0) - \
            (rSQLSpesial.sum_biaya_lain or 0.0) - (rSQLSpesial.sum_biaya_tarik or 0.0)
          
          AssignBranchCurrency(config, recD)
          recD.originBatch = recA.originBatch
          recD.keterangan = '%s: kewajiban Penarikan Dana PHK paket %s' \
            % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)        

        rSQLSpesial.Next() 

    elif rSQL.KODE_JENIS_TRANSAKSI == 'M':
      #transaksi manual buat 1 jurnal item (incomplete)
      oGLI = config.CreatePObjImplProxy('GLInterface')
      
      #cek masing-masing field sum_mutasi
      if rSQL.sum_mutasi_pk != 0.0 or rSQL.sum_mutasi_pst != 0.0:
        #sebagai transaksi iuran peserta
        rec = dataset.AddRecord()
        oPI = config.CreatePObjImplProxy('PaketInvestasi')
        oPI.Key = rSQL.KODE_PAKET_INVESTASI 
      
        #giro sesuai paket
        rec.accountCode = oPI.acc_giro
        sum_iuran = (rSQL.sum_mutasi_pk or 0.0) + (rSQL.sum_mutasi_pst or 0.0) 
        if sum_iuran > 0:       
          rec.debit = 0.0
          rec.credit = abs(sum_iuran)
        else:
          rec.debit = abs(sum_iuran)
          rec.credit = 0.0          
        
        AssignBranchCurrency(config, rec)
        AssignOriginBatch(rec, rSQL, oTB)
        rec.keterangan = '%s: akumulasi Iuran Peserta paket %s' \
        % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
        
      elif rSQL.sum_mutasi_pengembangan > 0.0:
        #sebagai transaksi bagi hasil 
        rec = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'KW_BGINVES'
        
        rec.accountCode = oGLI.account_code
        if rSQL.sum_mutasi_pengembangan > 0: 
          rec.debit = 0.0
          rec.credit = abs(rSQL.sum_mutasi_pengembangan)
        else:
          rec.debit = abs(rSQL.sum_mutasi_pengembangan)
          rec.credit = 0.0
        
        AssignBranchCurrency(config, rec)
        AssignOriginBatch(rec, rSQL, oTB)
        rec.keterangan = '%s: kewajiban dana Hasil Pengembangan dibagikan paket %s' \
          % (namaTransaksi, rSQL.KODE_PAKET_INVESTASI)
      
      elif rSQL.sum_mutasi_peralihan > 0.0:
        #sebagai 
        recC = dataset.AddRecord()
        oGLI = config.CreatePObjImplProxy('GLInterface')
        oGLI.Key = 'KW_ALIHDAR'
        
        recC.accountCode = oGLI.account_code
        if rSQL.sum_mutasi_peralihan > 0:
          recC.debit = 0.0
          recC.credit = abs(rSQL.sum_mutasi_peralihan)
        else:
          recC.debit = abs(rSQL.sum_mutasi_peralihan)
          recC.credit = 0.0
        
        AssignBranchCurrency(config, recC)
        recC.originBatch = rec.originBatch
        recC.keterangan = '%s: kewajiban dana Peralihan dari %s lain paket %s' \
          % (namaTransaksi, jenisDP, rSQL.KODE_PAKET_INVESTASI)        
            
    rSQL.Next()

  return 1

def CreatingRegistrationRecord(config, dataset, rSQL, namaTransaksi, oTB):

  #Cr Fee Pendaftaran
  rec = dataset.AddRecord()
  oGLI = config.CreatePObjImplProxy('GLInterface')
  oGLI.Key = 'BBN_DAFTAR'
  
  rec.accountCode = oGLI.account_code
  rec.debit = 0.0
  rec.credit = rSQL.sum_biaya_daftar
  
  AssignBranchCurrency(config, rec)
  AssignOriginBatch(rec, rSQL, oTB)
  rec.keterangan = '%s: akumulasi fee Pendaftaran' % (namaTransaksi)

  if oTB.account_link_type == 'S':
    #Dr Giro Pendaftaran
    rec = dataset.AddRecord()
    oGLI.Key = 'GR_DAFTAR'
    
    rec.accountCode = oGLI.account_code
    #posisi selalu kredit
    rec.debit = rSQL.sum_biaya_daftar
    rec.credit = 0.0
    
    AssignBranchCurrency(config, rec)
    AssignOriginBatchDaftar(rec, oTB)
    rec.keterangan = '%s: akumulasi Giro Pendaftaran' % (namaTransaksi)

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
