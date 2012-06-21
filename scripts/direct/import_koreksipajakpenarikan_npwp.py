import dafsys
from string import *

INPUT = 'koreksi_pajak_penarikan.txt'
OUTPUT= 'hasil_import_koreksi_pajak_penarikan.txt'
SEP = '|'
flo = None

def UpdateTables(config, no_peserta, pajak):
    UpdateRekening(config, no_peserta, pajak)
    UpdateTransaksi(config, no_peserta, pajak)
    
def UpdateRekening(config, no_peserta, pajak):
    oRek = config.CreatePObjImplProxy('RekeningDPLK')
    oRek.Key = no_peserta
    oRek.akum_dana_iuran_pst -= pajak
    
def UpdateTransaksi(config, no_peserta, pajak):
    global flo
    # penarikan 30% dan PHK
    sSQL = "SELECT ID_Transaksi \
    FROM TransaksiDPLK \
    WHERE no_peserta = '%s' \
    AND kode_jenis_transaksi in ('V', 'W') \
    AND tgl_transaksi >= '01-01-2009'" % (no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult
    if not rSQL.Eof:
        # koreksi mutasi penarikan
        oTransPenarikan = config.CreatePObjImplProxy('TransaksiDPLK')
        oTransPenarikan.Key = rSQL.ID_Transaksi
        oTransPenarikan.Mutasi_Iuran_Pst -= pajak

        # koreksi dana diterima dan biaya penarikan
        oPD = config.CreatePObjImplProxy('PenarikanDana')
        oPD.Key = rSQL.ID_Transaksi
        flo.write(no_peserta +'; pajak lama = ' + str(oPD.pajak)+'; tambahan pajak = '+str(pajak)+'\n')
        oPD.pajak += pajak
        oPD.dana_diterima -= pajak

    
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
                no_peserta = val[0]; pajak = float(strip(val[1]))
                print no_peserta
                UpdateTables(config, no_peserta, pajak)
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
