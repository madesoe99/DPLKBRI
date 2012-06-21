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

    try:
      lastday_baghas = moduleapi.GetLastDayOfMonth(monthBaghas, yearBaghas)
      lastday_inv = moduleapi.GetLastDayOfMonth(monthInvestasi, yearInvestasi)
      tgl_baghas = '%s/%s/%s' % (str(monthBaghas),str(lastday_baghas),str(yearBaghas))
      tgl_investasi = '%s/%s/%s' % (str(monthInvestasi),str(lastday_inv),str(yearInvestasi))
      status.tgl_baghas = tgl_baghas; status.tgl_investasi = tgl_investasi
      strtgl_baghas = '%s-%s-%s 23:59:59.000' % (yearBaghas, monthBaghas, lastday_baghas)
      strtgl_investasi = '%s-%s-%s 23:59:59.000' % (yearInvestasi, monthInvestasi, lastday_inv)
        
      FillDanaPerPaket(config, strtgl_baghas, strtgl_investasi, ds_danapaket)
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
  
def BuildSQLDanaPaket(config, tgl_investasi):
  sSQL = "SELECT r.kode_paket_investasi as paket,\
  sum(mutasi_iuran_pst) + sum(mutasi_iuran_pk) +\
  sum(mutasi_pengembangan) + sum(mutasi_peralihan) as nominal\
  FROM transaksidplk t, rekeningdplk r \
  WHERE \
  t.no_peserta = r.no_peserta\
  and status_dplk = 'A'\
  and isCommitted = 'T'\
  and tgl_transaksi <= '%s'\
  GROUP BY r.kode_paket_investasi\
  ORDER BY r.kode_paket_investasi"  % (tgl_investasi)
  config.SendDebugMsg(sSQL)
  
  rSQL = config.CreateSQL(sSQL).RawResult
  	
  return rSQL

def BuildSQLDanaTutup(config, strtgl_baghas, strtgl_investasi):
  dictDanaTutup = {}
  sSQL = "select r.kode_paket_investasi, sum(mutasi_iuran_pk) + sum(mutasi_iuran_pst) +\
          sum(mutasi_pengembangan) + sum(mutasi_peralihan) as dana\
          from transaksidplk t, rekeningdplk r\
          where \
          t.no_peserta = r.no_peserta\
          and r.no_peserta in\
          (\
          	select t.no_peserta\
          	from transaksidplk t, nasabahdplk n\
          	where \
          	t.no_peserta = n.no_peserta\
          	and tgl_registrasi <= '%s'\
          	and kode_jenis_transaksi = 'J'\
          	and tgl_transaksi > '%s'\
          	and tgl_transaksi <= '%s'\
          )\
          group by r.kode_paket_investasi\
          order by r.kode_paket_investasi"  % (strtgl_investasi, strtgl_investasi, strtgl_baghas)
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

