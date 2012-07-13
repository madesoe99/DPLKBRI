import string, sys, dafsys
sys.path.append('c:/dafapp/dplk07/script_modules')
import transaksiapi

file_user = 'Pertamina-EP-Pengelolaan.txt'
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
      CreateTransaksi(config, val)
      I += 1
    config.Commit()
  except:
    config.Rollback()
    raise Exception, 'Error' +  str(sys.exc_info()[1])

def CreateTransaksi(config, val):
  o = config.CreatePObject('TransaksiDPLKManual')
  o.tgl_transaksi = '04/01/2010'
  o.no_peserta = val[0]
  o.kode_transaksi_manual = 'M'
  o.keterangan = 'BIAYA PENGELOLAAN 2009'
  o.mutasi_iuran_pk = 0
  o.mutasi_iuran_pst = 0
  o.mutasi_pengembangan = float(val[1])
  o.mutasi_peralihan = 0
  o.ID_TransactionBatch = 186153 
  o.branch_code = '311'
  o.user_id = 'ADE HERMAN'
  o.terminal_id = '172.16.11.174'
  o.tgl_sistem = config.Now()   
  transaksiapi.SetPaketInvestasi(config, o)

  o.isCommitted = 'T'
  o.user_id_auth = 'ADE HERMAN'
  o.terminal_id_auth = '172.16.11.174'
  o.tgl_otorisasi = config.Now()      

  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.Key = o.no_peserta

  oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk + 0
  oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst + 0
  oR.akum_dana_pengembangan = oR.akum_dana_pengembangan + float(val[1])
  oR.akum_dana_peralihan = oR.akum_dana_peralihan + 0     

## MAIN PROGRAM    
config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
DoKoreksi(config)
    
