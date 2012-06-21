import sys
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def get_distribusi_hi(config, parameter, returns):
    moduleapi = modman.getModule(config, 'moduleapi')
    
    rec = parameter.FirstRecord
    monthBaghas = rec.monthBaghas
    yearBaghas = rec.yearBaghas
    monthInvestasi = rec.monthPiutang
    yearInvestasi = rec.yearPiutang
    
    status = returns.CreateValues(
        ['Is_Err', 0],
        ['Err_Message', ''],        
        ['inv_deposito',0.0],
        ['inv_sukuk',0.0],
        ['inv_reksadana',0.0],
        ['hi_deposito',0.0],
        ['hi_sukuk',0.0],
        ['hi_reksadana',0.0],
        ['tgl_baghas',''],
        ['tgl_investasi','']
    )
    ds_danapaket = returns.AddNewDatasetEx('danapaket', \
    'paket:string;nominal:float;')

    ## Tambahan By ade Herman - 2011-02-02-----
    ds_proporsipaket = returns.AddNewDatasetEx('proporsipaket', \
    'paket:string;prosentase:float;')
    ### -------- End -------------------

    try:
      lastday_baghas = moduleapi.GetLastDayOfMonth(monthBaghas, yearBaghas)
      lastday_inv = moduleapi.GetLastDayOfMonth(monthInvestasi, yearInvestasi)
      tgl_baghas = '%s/%s/%s' % (str(monthBaghas),str(lastday_baghas),str(yearBaghas))
      tgl_investasi = '%s/%s/%s' % (str(monthInvestasi),str(lastday_inv),str(yearInvestasi))
      status.tgl_baghas = tgl_baghas; status.tgl_investasi = tgl_investasi
      strtgl_baghas = '%s-%s-%s 23:59:59.000' % (yearBaghas, monthBaghas, lastday_baghas)
      strtgl_investasi = '%s-%s-%s 23:59:59.000' % (yearInvestasi, monthInvestasi, lastday_inv)
      
      awl_baghas = '%s/01/%s' % (str(monthBaghas),str(yearBaghas))
      akh_baghas = '%s/01/%s' % (str(monthBaghas+1),str(yearBaghas))
        
      FillDanaPerPaket(config, strtgl_baghas, strtgl_investasi, ds_danapaket)
      ## Tambahan By ade Herman - 2011-02-02-----
      FillProporsiPerPaket(config, awl_baghas, akh_baghas, ds_proporsipaket)
      ### -------- End -------------------
      status.inv_deposito = GetNominalInv(config, "'A'", 'Deposito', strtgl_investasi)
      status.inv_sukuk = GetNominalInv(config, "'A','D'", 'Obligasi', strtgl_investasi)
      status.inv_reksadana = GetNominalInv(config, "'A','D'", 'Reksadana', strtgl_investasi)
      status.hi_deposito = GetHasilInv(config, 'D', strtgl_investasi, strtgl_baghas)
      status.hi_sukuk = GetHasilInv(config, 'O', strtgl_investasi, strtgl_baghas)
      status.hi_reksadana = GetHasilInv(config, 'R', strtgl_investasi, strtgl_baghas)
    except:
        status.Is_Err = 1
        status.Err_Message = str(sys.exc_info()[1])

    return 1

def FillDanaPerPaket(config, strtgl_baghas, strtgl_investasi, ds_danapaket):
  dictDanaTutup = BuildSQLDanaTutup(config, strtgl_baghas, strtgl_investasi)
  rSQL = BuildSQLDanaPaket(config, strtgl_investasi)
  while not rSQL.Eof:
    rec = ds_danapaket.AddRecord()
    rec.paket = rSQL.paket
    if dictDanaTutup.has_key(rSQL.paket):
      dana_tutup = dictDanaTutup[rSQL.paket]
    else:
      dana_tutup = 0.0
    rec.nominal = rSQL.nominal + dana_tutup
    rSQL.Next()
    

## Tanbahan By Ade Herman --- 2011-02-02-----
def FillProporsiPerPaket(config, awl_baghas, akh_baghas, ds_proporsipaket):
  rSQL = BuildSQLProporsiPerPaket(config, awl_baghas,akh_baghas)
  while not rSQL.Eof:
    rec = ds_proporsipaket.AddRecord()
    rec.paket = rSQL.paket
    rec.prosentase = rSQL.prosentase
    rSQL.Next()

def BuildSQLProporsiPerPaket(config,tgl_awal,tgl_akhir):

   y,m,d = config.ModDateTime.DecodeDate(config.Now())
   tglHitung = [y,m,d]
   
   strSQL = \
         "select r.kode_paket_investasi as paket, (sum(t.prosenKredit)-sum(t.prosenDebet)) as prosentase \
            from rincianinvestasi r, ( \
              select r.kode_paket_investasi as kode_paket_investasi, \
                     r.id_investasi as id_investasi, \
                     (r.proporsi * t.mutasi_kredit) as prosenKredit, \
                     (r.proporsi * t.mutasi_debet) as prosenDebet \
                from rincianinvestasi r, transaksiinvestasi t \
               where r.id_investasi = t.id_investasi \
                 and t.tgl_transaksi >= '%s' \
                 and t.tgl_transaksi < '%s'  \
                 and t.kode_jenis_trinvestasi IN ('E','I') \
               ) t \
          where r.kode_paket_investasi = t.kode_paket_investasi \
            and r.id_investasi = t.id_investasi \
          group by r.kode_paket_investasi ; "\
          % (tgl_awal, tgl_akhir)

   rSQL = config.CreateSQL(strSQL).RawResult
   return rSQL
## ------------------ End -----------------------
  
  
def BuildSQLDanaPaket(config, tgl_investasi):
  sSQL = "SELECT r.kode_paket_investasi as paket,\
  sum(mutasi_iuran_pst) + sum(mutasi_iuran_pk) +\
  sum(mutasi_pengembangan) + sum(mutasi_peralihan) as nominal\
  FROM transaksidplk t, rekeningdplk r \
  WHERE \
  t.no_peserta = r.no_peserta\
  and status_dplk ='A'\
  and isCommitted = 'T'\
  and tgl_transaksi <= '%s'\
  GROUP BY r.kode_paket_investasi\
  ORDER BY r.kode_paket_investasi"  % (tgl_investasi)
  config.SendDebugMsg(sSQL)
  
  rSQL = config.CreateSQL(sSQL).RawResult
  	
  return rSQL

def BuildSQLDanaTutup(config, strtgl_baghas, strtgl_investasi):
  dictDanaTutup = {}
  #sSQL = "select r.kode_paket_investasi, sum(mutasi_iuran_pk) + sum(mutasi_iuran_pst) +\
  #        sum(mutasi_pengembangan) + sum(mutasi_peralihan) as dana\
  #        from transaksidplk t, rekeningdplk r\
  #        where \
  #        t.no_peserta = r.no_peserta\
  #        and r.no_peserta in\
  #        (\
  #        	select t.no_peserta\
  #        	from transaksidplk t, nasabahdplk n\
  #        	where \
  #        	t.no_peserta = n.no_peserta\
  #        	and tgl_registrasi <= '%s'\
  #        	and kode_jenis_transaksi = 'J'\
  #        	and tgl_transaksi > '%s'\
  #        	and tgl_transaksi <= '%s'\
  #        )\
  #        group by r.kode_paket_investasi\
  #        order by r.kode_paket_investasi"  % (strtgl_investasi, strtgl_investasi, strtgl_baghas)
  #config.SendDebugMsg(sSQL)


  sSQL = "select r.kode_paket_investasi, sum(mutasi_iuran_pk) + sum(mutasi_iuran_pst) +\
          sum(mutasi_pengembangan) + sum(mutasi_peralihan) as dana\
          from transaksidplk t, rekeningdplk r\
          where \
          t.no_peserta = r.no_peserta\
          and t.iscommitted = 'T'\
          and t.tgl_transaksi < '%s'\
          and r.no_peserta in\
          (\
          	select t.no_peserta\
          	from transaksidplk t, nasabahdplk n\
          	where \
          	t.no_peserta = n.no_peserta\
          	and tgl_registrasi <= '%s'\
          	and kode_jenis_transaksi = 'J'\
          	and t.iscommitted = 'T'\
          	and tgl_transaksi > '%s'\
          )\
          group by r.kode_paket_investasi\
          order by r.kode_paket_investasi"  % (strtgl_investasi, strtgl_investasi, strtgl_investasi)
  config.SendDebugMsg(sSQL)


  
  rSQL = config.CreateSQL(sSQL).RawResult
  rSQL.First()
  while not rSQL.Eof:
    dictDanaTutup[rSQL.kode_paket_investasi] = rSQL.dana or 0.0
    rSQL.Next()
  	
  return dictDanaTutup
  
def GetHasilInv(config, jenisinv, strtgl_investasi, strtgl_baghas):
  strSQL = "\
    select sum(mutasi_kredit) - sum(mutasi_debet) as hasil_investasi \
    from TransaksiInvestasi ti, Investasi i \
    where clsfTransaksiInvestasi = 'C' \
    and tgl_transaksi > '%s' \
    and tgl_transaksi <= '%s' \
    and i.id_investasi = ti.id_investasi \
    and i.kode_jns_investasi = '%s'"\
    % (strtgl_investasi, strtgl_baghas, jenisinv)
    
  config.SendDebugMsg(strSQL)
  res = config.CreateSQL(strSQL).RawResult
  
  return res.hasil_investasi or 0.0 

def GetNominalInv(config, cls, jenisinv, strSQLEndDate):
  strSQL = "\
    select \
    	sum(mutasi_debet) - sum(mutasi_kredit) as nominal_investasi \
    from TransaksiInvestasi t, %s d \
    where isCommitted = 'T' \
    	and clsfTransaksiInvestasi in (%s) \
    	and t.id_investasi = d.id_investasi \
    	and tgl_transaksi <= '%s'"\
    % (jenisinv, cls, strSQLEndDate)
  config.SendDebugMsg(strSQL)
  res = config.CreateSQL(strSQL).RawResult
  
  return res.nominal_investasi or 0.0 

def cetak_skb(config, parameter, returns):
    rec = parameter.FirstRecord
    lampiran = rec.lampiran
    semester = rec.semester
    tahun = rec.tahun
    kode_pihak_ketiga = rec.kode_pihak_ketiga
    
    status = returns.CreateValues(
        ['Is_Err', 0],
        ['Err_Message', ''])
    ds_lampiranA = returns.AddNewDatasetEx('lampiranA', \
    'nomor_bilyet:string;tgl_penempatan:datetime;tgl_pencairan:datetime;\
    nominal_investasi:float;nominal_baghas:float;')
    ds_lampiranB = returns.AddNewDatasetEx('lampiranB', \
    'nomor_rekening:string;bulan:string;saldo_akhir_bulan:float;nominal_baghas:float;')

    try:
      if lampiran in ('B','C'):    
        FillLampiranA(config, semester, tahun, kode_pihak_ketiga, ds_lampiranA)
      elif lampiran == 'D':    
        FillLampiranB(config, semester, tahun, kode_pihak_ketiga, ds_lampiranB)
    except:
        status.Is_Err = 1
        status.Err_Message = str(sys.exc_info()[1])

    return 1

def FillLampiranA(config, semester, tahun, kode_pihak_ketiga, ds_lampiranA):
  rSQL = BuildSQLLampiranA(config, semester, tahun, kode_pihak_ketiga)
  while not rSQL.Eof:
    rec = ds_lampiranA.AddRecord()
    rec.nomor_bilyet = rSQL.no_bilyet
    rec.tgl_penempatan = rSQL.tgl_buka
    rec.tgl_pencairan = rSQL.tgl_tutup or ''
    rec.nominal_investasi = rSQL.nominal_pembukaan
#     rec.nominal_baghas = rSQL.nominal_baghas
    rSQL.Next()
    
def BuildSQLLampiranA(config, semester, tahun, kode_pihak_ketiga):
   sSQL = "select NO_BILYET, TGL_BUKA, TGL_TUTUP, NOMINAL_PEMBUKAAN \
            from INVESTASI \
            where KODE_PIHAK_KETIGA = '%s'" % (kode_pihak_ketiga)
   rSQL = config.CreateSQL(strSQL).RawResult
   
   return rSQL
   
def FillLampiranB(config, semester, tahun, kode_pihak_ketiga, ds_lampiranB):
  rSQL = BuildSQLLampiranB(config, semester, tahun, kode_pihak_ketiga)
  while not rSQL.Eof:
    rec = ds_lampiranB.AddRecord()
    rec.nomor_rekening = rSQL.nomor_rekening
    rec.bulan = rSQL.bulan
    rec.saldo_akhir_bulan = rSQL.saldo_akhir_bulan
    rec.nominal_investasi = rSQL.nominal_investasi
    rec.nominal_baghas = rSQL.nominal_baghas
    rSQL.Next()

def BuildSQLLampiranB(config, semester, tahun, kode_pihak_ketiga):
   sSQL = ""
   rSQL = config.CreateSQL(strSQL).RawResult
   return rSQL
