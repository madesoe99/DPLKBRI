#
# SCRIPT PROSES BATCH INVESTASI
#
# Koneksi Investasi ke Accounting
# 
import CreateCandidateJournalItem as CJI

class record : pass

def FindAccountCode(config, noRek) :
  strSQL = 'select * from MasterGiro where no_giro = \'%s\' ' % noRek
  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  if rSQL.Eof :
    return ''
  else :
    return rSQL.acc_giro

def FindAccountFromParameter(config, param) :
  strSQL = 'select * from GLInterface where intf_code = \'%s\' ' % param
  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  if rSQL.Eof :
    return ''
  else :
    return rSQL.ACCOUNT_CODE


def RegistrasiDeposito(config, inp, dataset, oTI) :
  config.SendDebugMsg('Proses Registrasi no bilyet : '+oTI.no_bilyet)
  #alokasi investasi buat 2 jurnal item (REGISTRASI INVESTASI BARU)
  oLsInvestasi = inp.oLsInvestasi
  oLsInvestasi.First()
  while not oLsInvestasi.EndOfList :
    oRincian = oLsInvestasi.CurrentElement
    oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
       
    #Cr deposito paket berjangka
    rec = dataset.AddRecord()
    
    #rec.accountCode = oPaketInvestasi.acc_giro
    rec.accountCode = FindAccountFromParameter(config, 'PI_GPA')
    
    rec.debit = oTI.mutasi_kredit*(oRincian.proporsi or 1)
    rec.credit = oTI.mutasi_debet*(oRincian.proporsi or 1)
    
    CJI.AssignBranchCurrency(config, rec)
    CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
    rec.keterangan = 'Investasi pada %s - %s' \
      % (inp.oPihakKetiga.nama_pihak_ketiga, oTI.no_bilyet)
    config.SendDebugMsg(rec.keterangan)
    
    oLsInvestasi.Next()
    
  if inp.req.oTB.account_link_type == 'S':
    #Single: Db Giro sesuai paket investasi
    recS = dataset.AddRecord()
    #ambil kode account untuk pihak ketiga
    oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
    oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
    oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
    ls_acc = oRincianPK.acc_investasi.split(';')
    config.SendDebugMsg('ls_acc='+str(ls_acc))
    oInv = oTI.LInvestasi.CastToLowestDescendant()
    if oInv.jmlHariOnCall > 0: #deposito on call
      recS.accountCode = ls_acc[1]
    else: #deposito berjangka
      recS.accountCode = ls_acc[0]
     
    recS.debit = oTI.mutasi_debet
    recS.credit = oTI.mutasi_kredit
  
    CJI.AssignBranchCurrency(config, recS)
    CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
    #recS.originBatch = rec.originBatch
    recS.keterangan = rec.keterangan

def BagiHasilDeposito(config, inp, dataset, oTI) : 
  if oTI.clsfTransaksiInvestasi == 'B' : #untuk transaksi piutang LR investasi tdk dimasukkan record
    return
  config.SendDebugMsg('Proses Bagi Hasil no bilyet : '+oTI.no_bilyet)
  #kemungkinan harus dibagi sesuai proporsi setiap paket investasi
  oLsInvestasi = inp.oLsInvestasi
  #oLsInvestasi.First()
  #while not oLsInvestasi.EndOfList :
  #oRincian = oLsInvestasi.CurrentElement
  #oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
     
  #Db deposito paket berjangka
  rec = dataset.AddRecord()
  #pendapatan pihak ketiga
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)  
  rec.accountCode = oRincianPK.acc_pendapatan
  config.SendDebugMsg('Bagi Hasil : %s' %(rec.accountCode))
  rec.debit = oTI.mutasi_debet
  rec.credit = oTI.mutasi_kredit
  
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Bagi Hasil pada %s - %s' \
    % (inp.oPihakKetiga.nama_pihak_ketiga, oTI.no_bilyet)
  config.SendDebugMsg(rec.keterangan)
  
  #oLsInvestasi.Next()
    
  if inp.req.oTB.account_link_type == 'S':
    #Single: Db Giro data giro bagi hasil
    recS = dataset.AddRecord()
    oInv = oTI.LInvestasi.CastToLowestDescendant()
    if oInv.kapitalisir_rollover == 'T' :
      recS.accountCode = oRincianPK.acc_piut_pendapatan
    else :
      recS.accountCode = FindAccountCode(config,oInv.no_rekening)
    config.SendDebugMsg('Bagi Hasil Destination : %s' %(recS.accountCode))
    recS.debit = oTI.mutasi_kredit
    recS.credit = oTI.mutasi_debet
  
    CJI.AssignBranchCurrency(config, recS)
    CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
    #recS.originBatch = rec.originBatch
    recS.keterangan = rec.keterangan

def KapitalisirDeposito (config, inp, dataset, oTI) :
  if oTI.clsfTransaksiInvestasi == 'A' : #untuk transaksi piutang investasi tdk dimasukkan record
    return
  config.SendDebugMsg('Proses Kapitalisir no bilyet : '+oTI.no_bilyet)
  #kemungkinan harus dibagi sesuai proporsi setiap paket investasi
  oLsInvestasi = inp.oLsInvestasi
  oLsInvestasi.First()
  #while not oLsInvestasi.EndOfList :
    #oRincian = oLsInvestasi.CurrentElement
    #oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
       
    #Db deposito paket berjangka
  rec = dataset.AddRecord()
  #pendapatan pihak ketiga
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)  
  rec.accountCode = oRincianPK.acc_piut_pendapatan
  config.SendDebugMsg('Kapitalisir piutang : %s' %(rec.accountCode))
  rec.debit = oTI.mutasi_debet
  rec.credit = oTI.mutasi_kredit
  
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Bagi Hasil pada %s - %s' \
    % (inp.oPihakKetiga.nama_pihak_ketiga, oTI.no_bilyet)
  config.SendDebugMsg(rec.keterangan)
    
  #  oLsInvestasi.Next()
    
  if inp.req.oTB.account_link_type == 'S':
    #Single: Db Giro data giro bagi hasil
    recS = dataset.AddRecord()
    oInv = oTI.LInvestasi.CastToLowestDescendant()
    #oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
    #oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
    #oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
    ls_acc = oRincianPK.acc_investasi.split(';')
    if oInv.jmlHariOnCall > 0: #deposito on call 
      recS.accountCode = ls_acc[1]
    else: #deposito berjangka
      recS.accountCode = ls_acc[0]
    
    config.SendDebugMsg('Kapitalisir Tujuan : %s' %(recS.accountCode))
    recS.debit = oTI.mutasi_kredit
    recS.credit = oTI.mutasi_debet
  
    CJI.AssignBranchCurrency(config, recS)
    CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
    #recS.originBatch = rec.originBatch
    recS.keterangan = rec.keterangan
    
def TutupDeposito (config, inp, dataset, oTI) :
  config.SendDebugMsg('Proses Tutup Deposito no bilyet : '+oTI.no_bilyet)
  #alokasi investasi buat 2 jurnal item (Tutup INVESTASI)
  oLsInvestasi = inp.oLsInvestasi
  oLsInvestasi.First()
  #while not oLsInvestasi.EndOfList :
    #oRincian = oLsInvestasi.CurrentElement
    #oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
       
    #Cr deposito paket berjangka
  rec = dataset.AddRecord()
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)  
  if oTI.clsfTransaksiInvestasi == 'B' : #untuk transaksi piutang investasi tdk dimasukkan record
    rec.accountCode = oRincianPK.acc_piut_pendapatan
  else :
    oInv = oTI.LInvestasi.CastToLowestDescendant()
    config.SendDebugMsg('oncall : %s ' % oInv.jmlHariOnCall)
    ls_acc = oRincianPK.acc_investasi.split(';')
    config.SendDebugMsg('ls_acc : %s ' % ls_acc)
    if oInv.jmlHariOnCall > 0: #deposito on call
      rec.accountCode = ls_acc[1]
    else: #deposito berjangka
      rec.accountCode = ls_acc[0]
  
  config.SendDebugMsg('Tutup Deposito : %s' %(rec.accountCode))
  rec.debit = oTI.mutasi_debet
  rec.credit = oTI.mutasi_kredit
  
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Tutup Deposito pada %s - %s' \
    % (inp.oPihakKetiga.nama_pihak_ketiga, oTI.no_bilyet)
  config.SendDebugMsg(rec.keterangan)
    
  #  oLsInvestasi.Next()
    
  if inp.req.oTB.account_link_type == 'S':
    #Single: Db Giro sesuai paket investasi
    recS = dataset.AddRecord()
    #ambil dari no_rekening di tutupdeposito
    if oTI.clsftransaksiinvestasi == 'B' :
      oTutup = oTI.LIndukTransaksiInvestasi.CastToLowestDescendant()
    else :
      oTutup = oTI.CastToLowestDescendant()
    recS.accountCode = FindAccountCode(config, oTutup.no_rekening)
    
    config.SendDebugMsg('Tujuan Rekening Tutup Deposito : %s' %(recS.accountCode))
    recS.debit = oTI.mutasi_kredit
    recS.credit = oTI.mutasi_debet
  
    CJI.AssignBranchCurrency(config, recS)
    CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
    #recS.originBatch = rec.originBatch
    recS.keterangan = rec.keterangan
  
def TransaksiManual(config, inp, dataset, oTI) :
  config.SendDebugMsg('Proses Manual Investasi : '+oTI.nama_investasi+' '+oTI.no_bilyet)
  #kemungkinan harus dibagi sesuai proporsi setiap paket investasi
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  oLsInvestasi = inp.oLsInvestasi
  oLsInvestasi.First()
  while not oLsInvestasi.EndOfList :
    oRincian = oLsInvestasi.CurrentElement
    oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
       
    #Cr deposito paket berjangka
    rec = dataset.AddRecord()
    
    #rec.accountCode = oPaketInvestasi.acc_giro
    if oTI.kode_jns_investasi == 'D' :
      rec.accountCode = FindAccountFromParameter(config, 'PI_GPA')
    elif oTI.kode_jns_investasi == 'O' :
      rec.accountCode = FindAccountFromParameter(config, 'PI_GPB')
    elif oTI.kode_jns_investasi == 'R' :
      rec.accountCode = FindAccountFromParameter(config, 'PI_GPC')
    else :
      'PERINGATAN','Transaksi Manual tidak mengenali kode jenis investasi'
      
      
    rec.debit = oTI.mutasi_debet*(oRincian.proporsi or 1)
    rec.credit = oTI.mutasi_kredit*(oRincian.proporsi or 1)
    
    CJI.AssignBranchCurrency(config, rec)
    CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
    rec.keterangan = 'Transaksi Manual %s pada %s - %s %s' \
      % (inp.ket,inp.oPihakKetiga.nama_pihak_ketiga, oTI.no_bilyet, oTI.nama_investasi)
    config.SendDebugMsg(rec.keterangan)
    
    oLsInvestasi.Next()
  
  
def TransaksiPiutangLR(config, inp, dataset, oTI) :
  config.SendDebugMsg('Proses Piutang LR Investasi : '+oTI.nama_investasi+' '+oTI.no_bilyet)
  #kemungkinan harus dibagi sesuai proporsi setiap paket investasi
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  oLsInvestasi = inp.oLsInvestasi
  #oLsInvestasi.First()
  #while not oLsInvestasi.EndOfList :
  #oRincian = oLsInvestasi.CurrentElement
  #oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
     
  #Cr deposito paket berjangka
  rec = dataset.AddRecord()
  oTutup = oTI.CastToLowestDescendant()
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
  rec.accountCode = oRincianPK.acc_piut_pendapatan
  rec.debit = oTI.mutasi_debet
  rec.credit = oTI.mutasi_kredit
  
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Transaksi Piutang LR Manual %s pada %s - %s %s' \
    % (inp.ket,inp.oPihakKetiga.nama_pihak_ketiga, oTI.no_bilyet, oTI.nama_investasi)
  config.SendDebugMsg(rec.keterangan)
    
  #oLsInvestasi.Next()
    
def TransaksiLRManual (config, inp, dataset, oTI) :
  config.SendDebugMsg('Proses LR Manual Investasi : '+oTI.nama_investasi)
  #kemungkinan harus dibagi sesuai proporsi setiap paket investasi
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  oLsInvestasi = inp.oLsInvestasi
  #oLsInvestasi.First()
  #while not oLsInvestasi.EndOfList :
  #oRincian = oLsInvestasi.CurrentElement
  #oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
     
  #Cr deposito paket berjangka
  rec = dataset.AddRecord()
  
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
  rec.accountCode = oRincianPK.acc_pendapatan
  rec.debit = oTI.mutasi_debet
  rec.credit = oTI.mutasi_kredit
  
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Transaksi LR Manual %s pada %s - %s %s' \
    % (inp.ket,inp.oPihakKetiga.nama_pihak_ketiga, oTI.no_bilyet, oTI.nama_investasi)
  config.SendDebugMsg(rec.keterangan)
    
  #oLsInvestasi.Next()
    
def RegistrasiObligasi (config, inp, dataset, oTI) :
  config.SendDebugMsg('Registrasi Sukuk : '+oTI.nama_investasi)
  
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  oLsInvestasi = inp.oLsInvestasi
  oRincian = oLsInvestasi.CurrentElement
  oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
  
  rec = dataset.AddRecord()
  
  #rec.accountCode = oPaketInvestasi.acc_giro
  rec.accountCode = FindAccountFromParameter(config, 'PI_GPB')
  
  config.SendDebugMsg('Registrasi Sukuk : %s' %(rec.accountCode))
  rec.debit = oTI.mutasi_kredit*(oRincian.proporsi or 1)
  rec.credit = oTI.mutasi_debet*(oRincian.proporsi or 1)
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Registrasi Sukuk dengan nama %s '% (oTI.nama_investasi)
  config.SendDebugMsg(rec.keterangan)
       
  #Single: Db Giro sesuai Pihak ke 3
  recS = dataset.AddRecord()
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
  recS.accountCode = oRincianPK.acc_investasi
  config.SendDebugMsg('Registrasi Sukuk : %s' %(recS.accountCode))
  recS.debit = oTI.mutasi_debet
  recS.credit = oTI.mutasi_kredit

  CJI.AssignBranchCurrency(config, recS)
  CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
  #recS.originBatch = rec.originBatch
  recS.keterangan = rec.keterangan
  
def PendapatanObligasi(config, inp, dataset, oTI) :
  config.SendDebugMsg('Pendapatan Sukuk : '+oTI.nama_investasi)
  
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  oLsInvestasi = inp.oLsInvestasi
  oRincian = oLsInvestasi.CurrentElement
  oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
  
  rec = dataset.AddRecord()
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
  rec.accountCode = oRincianPK.acc_pendapatan
  config.SendDebugMsg('Pendapatan Sukuk : %s' %(rec.accountCode))
  #rec.accountCode = oPaketInvestasi.acc_manfaat
  rec.debit = oTI.mutasi_debet*(oRincian.proporsi or 1)
  rec.credit = oTI.mutasi_kredit*(oRincian.proporsi or 1)
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Transaksi Pendapatan Sukuk dengan nama %s '% (oTI.nama_investasi)
  config.SendDebugMsg(rec.keterangan)
      
  #Single: Db Giro data giro transaksi pendapatan obligasi
  recS = dataset.AddRecord()
  oInv = oTI.CastToLowestDescendant()
  recS.accountCode = FindAccountCode(config,oInv.no_rekening)
  config.SendDebugMsg('Tujuan Rekening Pendapatan Sukuk : %s' %(recS.accountCode))
  recS.debit = oTI.mutasi_kredit
  recS.credit = oTI.mutasi_debet

  CJI.AssignBranchCurrency(config, recS)
  CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
  #recS.originBatch = rec.originBatch
  recS.keterangan = rec.keterangan

def KoreksiNilaiWajar(config, inp, dataset, oTI) :
  config.SendDebugMsg('Koreksi Nilai Wajar Sukuk : '+oTI.nama_investasi)
  if oTI.mutasi_debet == oTI.mutasi_kredit == 0.0 :
    return
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  oLsInvestasi = inp.oLsInvestasi
  oRincian = oLsInvestasi.CurrentElement
  oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
  
  rec = dataset.AddRecord()
  if oTI.clsfTransaksiInvestasi == 'D' :
    rec.accountCode = FindAccountFromParameter(config,'PI_SPIO')
  else :
    rec.accountCode = FindAccountFromParameter(config,'PI_PNIO')
  config.SendDebugMsg('Koreksi Nilai Wajar : %s' %(rec.accountCode))
  rec.debit = oTI.mutasi_debet
  rec.credit = oTI.mutasi_kredit
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Transaksi Selisih Nilai Sukuk dengan nama %s '% (oTI.nama_investasi)
  config.SendDebugMsg(rec.keterangan)
      
def PenjualanObligasi(config, inp, dataset, oTI) :
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  oLsInvestasi = inp.oLsInvestasi
  oRincian = oLsInvestasi.CurrentElement
  oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
  
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
  
  oTInv = oTI.CastToLowestDescendant()
  
  if oTI.clsfTransaksiInvestasi == 'A' : #Piutang investasi
    rec = dataset.AddRecord()
    rec.accountCode = oRincianPK.acc_investasi
    config.SendDebugMsg('Reksadana : %s' %(rec.accountCode))
    rec.debit = oTI.mutasi_debet*(oRincian.proporsi or 1)
    rec.credit = oTI.mutasi_kredit*(oRincian.proporsi or 1)
    CJI.AssignBranchCurrency(config, rec)
    CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
    rec.keterangan = 'Jual Sukuk dengan nama %s '% (oTI.nama_investasi)
    config.SendDebugMsg(rec.keterangan)
         
    #Single: Db Giro sesuai Pihak ke 3
    recS = dataset.AddRecord()
    recS.accountCode = FindAccountCode(config, oTInv.no_rekening)
    config.SendDebugMsg('Jual Sukuk : %s' %(recS.accountCode))
    recS.debit = oTI.mutasi_kredit
    recS.credit = oTI.mutasi_debet
  
    CJI.AssignBranchCurrency(config, recS)
    CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
    #recS.originBatch = rec.originBatch
    recS.keterangan = rec.keterangan
  elif oTI.clsfTransaksiInvestasi == 'C' : #pendapatan penjualan
    rec = dataset.AddRecord()
    rec.accountCode = FindAccountCode(config, oTInv.no_rekening)
    config.SendDebugMsg('Jual Sukuk : %s' %(rec.accountCode))
    rec.debit = oTI.mutasi_kredit*(oRincian.proporsi or 1)
    rec.credit = oTI.mutasi_debet*(oRincian.proporsi or 1)
    CJI.AssignBranchCurrency(config, rec)
    CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
    rec.keterangan = 'Pendapatan/Biaya Jual Sukuk dengan nama %s '% (oTI.nama_investasi)
    config.SendDebugMsg(rec.keterangan)
         
    #Single: Db Giro sesuai Pihak ke 3
    recS = dataset.AddRecord()
    recS.accountCode = oRincianPK.acc_penjualan
    config.SendDebugMsg('Jual Sukuk : %s' %(recS.accountCode))
    recS.debit = oTI.mutasi_debet
    recS.credit = oTI.mutasi_kredit
  
    CJI.AssignBranchCurrency(config, recS)
    CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
    #recS.originBatch = rec.originBatch
    recS.keterangan = rec.keterangan
  else :
    rec = dataset.AddRecord()
    if oTI.clsfTransaksiInvestasi == 'D' :
      rec.accountCode = FindAccountFromParameter(config,'PI_SPIO')
    else :
      rec.accountCode = FindAccountFromParameter(config,'PI_KPNI')
    config.SendDebugMsg('Selisih Nilai investasi ketika Jual Sukuk : %s' %(rec.accountCode))
    rec.debit = oTI.mutasi_debet
    rec.credit = oTI.mutasi_kredit
    CJI.AssignBranchCurrency(config, rec)
    CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
    rec.keterangan = 'Selisih Nilai Investasi ketika Jual Sukuk bernama %s '% (oTI.nama_investasi)
    config.SendDebugMsg(rec.keterangan)
      
def TransReksadana(config, inp, dataset, oTI) :
  config.SendDebugMsg('%s Reksadana : %s' %(inp.ket,oTI.nama_investasi))
  
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  
  oLsInvestasi = inp.oLsInvestasi
  oRincian = oLsInvestasi.CurrentElement
  oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
  
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
  
  #cek jika nilai mutasi = 0 maka di lewat
  if oTI.mutasi_kredit == 0.0 and oTI.mutasi_debet == 0.0 :
    return
  rec = dataset.AddRecord()
  
  #rec.accountCode = oPaketInvestasi.acc_giro
  rec.accountCode = FindAccountFromParameter(config, 'PI_GPC')
  
  if oTI.kode_jenis_trinvestasi == 'R' : #Redemption
    oRedempt = oTI.CastToLowestDescendant()
    if oRedempt.biaya_redempt == 0.0 :
      rec.accountCode = FindAccountFromParameter(config, 'PI_PIUTL')#FindAccountCode(config, oRedempt.no_rekening)
    
  config.SendDebugMsg('Reksadana : %s' %(rec.accountCode))
  rec.debit = oTI.mutasi_kredit*(oRincian.proporsi or 1)
  rec.credit = oTI.mutasi_debet*(oRincian.proporsi or 1)
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = '%s Reksadana dengan nama %s '% (inp.ket,oTI.nama_investasi)
  config.SendDebugMsg(rec.keterangan)
  
  #Single: Db Giro sesuai Pihak ke 3
  recS = dataset.AddRecord()
  recS.accountCode = oRincianPK.acc_investasi
  config.SendDebugMsg('Reksadana : %s' %(recS.accountCode))
  recS.debit = oTI.mutasi_debet
  recS.credit = oTI.mutasi_kredit

  CJI.AssignBranchCurrency(config, recS)
  CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
  #recS.originBatch = rec.originBatch
  recS.keterangan = rec.keterangan
  
  config.SendDebugMsg(rec.keterangan)
def PerubahanNAB(config, inp, dataset, oTI) :
  config.SendDebugMsg('Koreksi NAB Reksadana : '+oTI.nama_investasi)
  if oTI.mutasi_debet == oTI.mutasi_kredit == 0.0 :
    return
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  oLsInvestasi = inp.oLsInvestasi
  oRincian = oLsInvestasi.CurrentElement
  oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
  
  rec = dataset.AddRecord()
  if oTI.clsfTransaksiInvestasi == 'D' :
    rec.accountCode = FindAccountFromParameter(config,'PI_SPIR')
  else :
    rec.accountCode = FindAccountFromParameter(config,'PI_KPNI')
  config.SendDebugMsg('Perubahan NAB Reksadana : %s' %(rec.accountCode))
  rec.debit = oTI.mutasi_debet
  rec.credit = oTI.mutasi_kredit
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = 'Transaksi Perubahan NAB dengan nama %s '% (oTI.nama_investasi)
  config.SendDebugMsg(rec.keterangan)
  
def ReturnReksadana(config, inp, dataset, oTI) :
  if oTI.clsftransaksiinvestasi == 'E' : #PNInvestasi
    return
  config.SendDebugMsg('%s Reksadana : %s' %(inp.ket,oTI.nama_investasi))
  
  config.SendDebugMsg(oTI.clsfTransaksiInvestasi)
  
  oLsInvestasi = inp.oLsInvestasi
  oRincian = oLsInvestasi.CurrentElement
  oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
  
  oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
  oRincianPK.SetKey('kode_jns_investasi',oTI.kode_jns_investasi)
  oRincianPK.SetKey('kode_pihak_ketiga',inp.oPihakKetiga.kode_pihak_ketiga)
  
  rec = dataset.AddRecord()
  
  if oTI.kode_jenis_trinvestasi == 'U' : #Real Return
    oRedempt = oTI.LIndukTransaksiInvestasi.CastToLowestDescendant()
    if oRedempt.biaya_redempt == 0.0 :
      rec.accountCode = FindAccountFromParameter(config, 'PI_PIUTL')#FindAccountCode(config, oRedempt.no_rekening)
    else :
      #rec.accountCode = oPaketInvestasi.acc_giro
      rec.accountCode = FindAccountFromParameter(config, 'PI_GPC')
      
  else :
    rec.accountCode = FindAccountFromParameter(config,'PI_KPNI')
    
  rec.debit = oTI.mutasi_kredit
  rec.credit = oTI.mutasi_debet
  CJI.AssignBranchCurrency(config, rec)
  CJI.AssignOriginBatchInvestasi(rec, inp.req.oTB, oTI)
  rec.keterangan = '%s Reksadana dengan nama %s '% (inp.ket,oTI.nama_investasi)
  config.SendDebugMsg(rec.keterangan)
  
  #Single: Db Giro sesuai Pihak ke 3
  recS = dataset.AddRecord()
  if oTI.kode_jenis_trinvestasi == 'U' : #Real Return"
    recS.accountCode = FindAccountFromParameter(config, 'PI_LRPR')#oRincianPK.acc_pendapatan
  else:
    recS.accountCode = oRincianPK.acc_pendapatan
  recS.debit = oTI.mutasi_debet
  recS.credit = oTI.mutasi_kredit

  CJI.AssignBranchCurrency(config, recS)
  CJI.AssignOriginBatchInvestasi(recS, inp.req.oTB, oTI)
  #recS.originBatch = rec.originBatch
  recS.keterangan = rec.keterangan
  
  config.SendDebugMsg(rec.keterangan)
  
def PassProcess(config, inp, dataset, oTI) :
  pass

def FunctionMain(config, req) :
  FirstInput = record()
  JD = 'D' #Jenis Investasi Deposito
  JO = 'O' #Jenis Investasi Obligasi
  JR = 'R' #Jenis Investasi Reksadana
  Params = '(config,FirstInput,req.dataset, oTI)' #Parameter Fungsi
                                                  #config, Input, Dataset, Object TransaksiInvestasi  
  FunctionEval = {JD+'A':('RegistrasiDeposito',''),
                  JD+'C':('TutupDeposito',''),
                  JD+'E':('BagiHasilDeposito',''),
                  JD+'F':('KapitalisirDeposito',''),
                  JD+'G':('TransaksiManual','Deposito'),
                  JD+'H':('TransaksiPiutangLR','Deposito'),
                  JD+'I':('TransaksiLRManual','Deposito'),
                  JO+'O':('RegistrasiObligasi',''),
                  JO+'K':('PendapatanObligasi',''),
                  JO+'N':('KoreksiNilaiWajar',''),
                  JO+'I':('TransaksiManual','Sukuk'),
                  JO+'H':('TransaksiLRManual','Sukuk'),
                  JO+'J':('PenjualanObligasi',''),
                  JR+'S':('TransReksadana','Subsribe'),
                  JR+'R':('TransReksadana','Redemption'),
                  JR+'H':('TransaksiManual','Reksadana'),
                  JR+'G':('TransaksiLRManual','Reksadana'),
                  JR+'N':('PerubahanNAB','Reksadana'),
                  JR+'U':('ReturnReksadana','Real Return'),
                  JR+'L':('ReturnReksadana','Unreal Return'),
                  JR+'Q':('ReturnReksadana','Koreksi Biaya'),
                  '':('PassProcess','')} #Fungsi Proses Transaksi
  
  TransClassName = {'A':'TransPiutangInvestasi',
                    'B':'TransPiutangLRInvestasi',
                    'C':'TransLRInvestasi',
                    'D':'TransaksiSPInvestasi',
                    'E':'TransaksiPNInvestasi'}
  
  FirstInput.req = req
  lsTransaksiInvestasi = req.oTB.Ls_TransaksiInvestasi
  lsTransaksiInvestasi.First()  
  while not lsTransaksiInvestasi.EndOfList:
    oTI = lsTransaksiInvestasi.CurrentElement
    #konversi objek transkasi investasi terlebih dahulu    
    oTISupport = oTI.CastAs(TransClassName[oTI.clsfTransaksiInvestasi])
    
    #ambil info pendukungnya terlebih dahulu
    FirstInput.RPI = oTI.LInvestasi.LRincianPaketInvestasi
    FirstInput.oPihakKetiga = oTISupport.LInvestasi.LPihakKetiga
    FirstInput.oLsInvestasi = oTISupport.LInvestasi.Ls_RincianInvestasi
    
    #oLsInvestasi.First()
    #while not oLsInvestasi.EndOfList :
    #  oRincian = oLsInvestasi.CurrentElement
    #  FirstInput.oJenisInvestasi = oRincian.LRincianPaketInvestasi.LJenisInvestasi
    #  FirstInput.oPaketInvestasi = oRincian.LRincianPaketInvestasi.LPaketInvestasi
    #  FirstInput.oRincian = oRincian
      
    config.SendDebugMsg(oTI.kode_jenis_trinvestasi+oTI.no_bilyet)
      
    if FunctionEval.has_key(oTI.kode_jns_investasi+oTI.kode_jenis_trinvestasi) :
       FirstInput.ket = FunctionEval[oTI.kode_jns_investasi+oTI.kode_jenis_trinvestasi][1]
       eval(FunctionEval[oTI.kode_jns_investasi+oTI.kode_jenis_trinvestasi][0]+Params)
    else :
       strError = 'Jenis Transaksi Investasi \'%s\' Belum Terdefinisi' \
                %(oTI.kode_jns_investasi+oTI.kode_jenis_trinvestasi)
       config.SendDebugMsg(strError)
       raise 'PERINGATAN',strError
                                 
    #oLsInvestasi.Next()
  
    config.SendDebugMsg('yes3')
    
    lsTransaksiInvestasi.Next()
  
  #debugging untuk kebutuhan cek Fungsi
  config.SendDebugMsg('End BatchInvestasiProcess')
