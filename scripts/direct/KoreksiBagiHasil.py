import string, sys, dafsys
sys.path.append('c:/dafapp/dplk07/script_modules')
import transaksiapi

file_user = 'NewUpdateSaldoAkhirSRR.txt'
SEP = '|'

def DoKoreksi(config):
  fl = open(file_user,'r')
  ls_fl = fl.readlines()
  count = len(ls_fl)
  config.BeginTransaction()
  try:
    I = 0
    while I<=count-1:
      val = ls_fl[I].split(SEP)
      print 'No Peserta              [0]: %s ' %(val[0])
      #print 'Bagi Hasil              [1]: %s ' %(val[1])
      print 'Saldo Akhir SRR         [2]: %s ' %(val[1])
      print 'ID SRRCALCRINCIAN       [3]: %s ' %(val[2])     
      UpdateTransaksiPK(config, val)
      #CreateTransaksi(config, val)
      I += 1
    config.Commit()
  except:
    config.Rollback()
    raise 'Error', str(sys.exc_info()[1])

def UpdateTransaksiPK(config, val):
 
  sUpdTrans = "update historisrr \
               set saldo_akhir_srr = %f\
               where no_peserta = \'%s\'\
                 and id_srrcalcrincian = \'%s\'"\
               % (float(val[1]), val[0],int(val[2]))
  config.ExecSQL(sUpdTrans)

def CreateTransaksi(config, val):
  o = config.CreatePObject('TransaksiDPLKManual')
  o.tgl_transaksi = '03/01/2011'
  o.no_peserta = val[0]
  o.kode_transaksi_manual = 'G'
  o.keterangan = 'Koreksi Bagi Hasil '
  o.mutasi_iuran_pk = 0
  o.mutasi_iuran_pst = 0
  o.mutasi_pengembangan = float(val[1])
  o.mutasi_peralihan = 0
  o.ID_TransactionBatch = 267394
  o.branch_code = '311'
  o.user_id = 'ADE HERMAN'
  o.terminal_id = '10.20.20.15'
  o.tgl_sistem = config.Now()   
  transaksiapi.SetPaketInvestasi(config, o)

  o.isCommitted = 'T'
  o.user_id_auth = 'ADE HERMAN'
  o.terminal_id_auth = '10.20.20.15'
  o.tgl_otorisasi = config.Now()      

  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.Key = o.no_peserta

  oR.akum_dana_iuran_pk     = oR.akum_dana_iuran_pk + 0
  oR.akum_dana_iuran_pst    = oR.akum_dana_iuran_pst + 0
  oR.akum_dana_pengembangan = oR.akum_dana_pengembangan + float(val[1])
  oR.akum_dana_peralihan    = oR.akum_dana_peralihan + 0     

## MAIN PROGRAM    
config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
#config = dafsys.OpenConfig('c:/dafapp/dplk07/testprod.cfg')
DoKoreksi(config)
    
