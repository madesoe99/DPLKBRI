import dafsys, sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def Koreksi(config):
  config.BeginTransaction()
  try:
    sHist = "select id_historisrr, no_peserta \
            from historisrr a, srrcalcrincian b, srrcalc c \
            where \
            a.id_srrcalcrincian = b.id_srrcalcrincian \
            and b.id_srrcalc = c.id_srrcalc \
            and c.id_srrcalc = 14" #koreksi srr des'08
    rHist = config.CreateSQL(sHist).RawResult
    rHist.First()
    while not rHist.Eof:
      no_peserta = rHist.no_peserta
      tanggal = '01/01/2009'
      saldo_awal = moduleapi.GetSaldoAwal(config, no_peserta, tanggal)
      print no_peserta+':'+str(saldo_awal)
      oHist = config.CreatePObjImplProxy('HistoriSRR')
      oHist.key = rHist.id_historisrr
      oHist.saldo_akhir_srr = saldo_awal
      rHist.Next()
      
    config.Commit()	
  except:
    config.Rollback()
    raise 'Error koreksi : ', str(sys.exc_info()[1]) 

# Main

cfg = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
Koreksi(cfg)
