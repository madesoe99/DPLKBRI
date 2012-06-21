import dafsys
from string import *

INPUT = 'Nov.txt'
OUTPUT= 'hasil_import_kekurangan_biaya_penarikan.txt'
SEP = '|'
flo = None

def UpdateTables(config, no_peserta, biaya):
    UpdateRekening(config, no_peserta, biaya)
    UpdateTransaksi(config, no_peserta, biaya)
    
def UpdateRekening(config, no_peserta, biaya):
    oRek = config.CreatePObjImplProxy('RekeningDPLK')
    oRek.Key = no_peserta
    oRek.akum_dana_pengembangan -= biaya
    sSQL = 'SELECT kode_jns_investasi, maks_proporsi \
    FROM RincianPaketInvestasi \
    WHERE kode_paket_investasi = \'%s\'' \
    % (oRek.kode_paket_investasi)
    rSQL = config.CreateSQL(sSQL).RawResult
    while not rSQL.Eof:
        oDet = config.CreatePObjImplProxy('DetailAkumPengembangan')
        oDet.SetKey('no_peserta', no_peserta)
        oDet.SetKey('kode_paket_investasi', oRek.kode_paket_investasi)
        oDet.SetKey('kode_jns_investasi', rSQL.kode_jns_investasi)
        oDet.Nilai_Akumulasi -= (rSQL.maks_proporsi / 100) * biaya
        rSQL.Next()    
    
def UpdateTransaksi(config, no_peserta, biaya):
    global flo
    
    sSQL = 'SELECT ID_Transaksi \
    FROM TransaksiDPLK \
    WHERE no_peserta = \'%s\' \
    AND kode_jenis_transaksi = \'V\' \
    AND tgl_transaksi > \'06-30-2008\'' % (no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult
    if not rSQL.Eof:
        oPD = config.CreatePObjImplProxy('PenarikanDana')
        oPD.Key = rSQL.ID_Transaksi
        flo.write(no_peserta +'; biaya lama = ' + str(oPD.biaya_tarik)+'; tambahan biaya = '+str(biaya)+'\n')
        oPD.biaya_tarik += biaya
        oTransBiaya = config.CreatePObjImplProxy('TransaksiDPLK')
        oTransBiaya.Key = oPD.ID_Transaksi_BAdmTrans
        oTransBiaya.Mutasi_Pengembangan -= biaya
    
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
