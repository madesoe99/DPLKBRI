import dafsys
from string import *

INPUT = 'koreksi_biaya_penarikan_10000.txt'
OUTPUT= 'hasil_import_koreksi_biaya_penarikan_10000.txt'
SEP = '|'
flo = None

def UpdateTables(config, no_peserta, biaya):
    UpdateRekening(config, no_peserta, biaya)
    UpdateTransaksi(config, no_peserta, biaya)
    
def UpdateRekening(config, no_peserta, biaya):
    oRek = config.CreatePObjImplProxy('RekeningDPLK')
    oRek.Key = no_peserta
    oRek.akum_dana_iuran_pst -= biaya
    
def UpdateTransaksi(config, no_peserta, biaya):
    global flo
    # penarikan 30% dan PHK
    sSQL = "SELECT ID_Transaksi \
    FROM TransaksiDPLK \
    WHERE no_peserta = '%s' \
    AND kode_jenis_transaksi in ('V', 'W') \
    AND tgl_transaksi >= '01-01-2009'" % (no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult
    if not rSQL.Eof:
        # koreksi dana diterima dan biaya penarikan
        oPD = config.CreatePObjImplProxy('PenarikanDana')
        oPD.Key = rSQL.ID_Transaksi
        flo.write(no_peserta +'; biaya lama = ' + str(oPD.biaya_tarik)+'; tambahan biaya = '+str(biaya)+'\n')
        oPD.biaya_tarik += biaya
        oPD.dana_diterima -= biaya

        # koreksi mutasi biaya
        oTransBiaya = config.CreatePObjImplProxy('TransaksiDPLK')
        oTransBiaya.Key = oPD.ID_Transaksi_BAdmTrans
        oTransBiaya.Mutasi_Iuran_Pst -= biaya
    
def ExecImport(config):
    global flo
    fl = open(INPUT,'r')
    flo = open(OUTPUT,'w')
    ls = fl.readlines()
    rowCount = len(ls)
    try:    
        config.BeginTransaction()
        try:
            i = 0
            while i<=rowCount-1:    
                val = split(ls[i],SEP)
                no_peserta = val[0]; biaya = float(strip(val[1]))
                print no_peserta
                UpdateTables(config, no_peserta, biaya)
                i += 1
            config.Commit()
        except:
            config.Rollback()
            raise
    finally:
        fl.close()
        flo.close()
    
#~ main program
config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
ExecImport(config)
