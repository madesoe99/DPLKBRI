import string, sys
sys.path.append('c:/dafapp/dplk/script_modules')
import transaksiapi
import dafsys4 as dafsys

def HitungBasil(config,rec):
    kolom = ['akum_iuran_pk','akum_iuran_pst','akum_iuran_tmb','akum_psl']
    basil ={}
    S_Awal = rec.akum_iuran_pk+rec.akum_iuran_pst+rec.akum_iuran_tmb+rec.akum_psl+ \
            rec.akum_pmb_pk+rec.akum_pmb_pst+rec.akum_pmb_tmb+rec.akum_pmb_psl

    sSQL = "SELECT * FROM PAKETINVESTASI WHERE kode_paket_investasi='%s' " % rec.kode_paket_investasi
    PI = config.CreateSQL(sSQL).RawResult
    S_Akhir = rec.jml_unit * PI.nav_custody
    
    SELISIH = S_Akhir - S_Awal
    for i in kolom:
        N = float(rec.GetFieldByName(i))
        nilai = 0
        if N not in (None , 0):
            BS = (N/S_Awal) * SELISIH
            nilai = "%.2f" % BS
            
        basil[i] = nilai
    
    return basil

def CreateBagiHasil(config, pst):
    user_id     = 'Tes'
    terminal_id = '193.6.1.105'
    oBaSil = config.CreatePObject('TransaksiBagiHasil')

    #field TransaksiRekInvDPLK
    oBaSil.no_rekening = pst.no_rekening
    oBaSil.branch_code = pst.kode_cab_daftar
    oBaSil.keterangan = 'Bagi Hasil peserta '+pst.no_peserta

    oBaSil.isCommitted     = 'T'
    oBaSil.user_id         = oBaSil.user_id_auth    = user_id
    oBaSil.terminal_id     = oBaSil.terminal_id_auth = terminal_id
    oBaSil.tgl_transaksi   = oBaSil.tgl_sistem = oBaSil.tgl_otorisasi = config.ModLibUtils.Now()
    
    #buat detil transaksi DPLK
    oRekInv = config.CreatePObjImplProxy('RekInvDPLK')
    oRekInv.Key = pst.no_rekening
    Ls_RekeningDPLK = oRekInv.Ls_RekeningDPLK
    
    akumMutasi ={'mutasi_pmb_pk':0.0,'mutasi_pmb_pst':0.0,'mutasi_pmb_tmb':0.0,'mutasi_pmb_psl':0.0}
    while not Ls_RekeningDPLK.EndOfList:
        oRekDPLK = Ls_RekeningDPLK.CurrentElement
        if oRekDPLK.is_deleted == 'F':
            HB = HitungBasil(config,oRekDPLK)            
            #rekening DPLK masih aktif
            
            oDetilTransaksi = config.CreatePObject('DetilTransaksiDPLK')
            oDetilTransaksi.ID_Transaksi = oBaSil.ID_Transaksi
            oDetilTransaksi.nomor_rekening = oRekDPLK.nomor_rekening 
            oDetilTransaksi.kode_paket_investasi = oRekDPLK.kode_paket_investasi
            oDetilTransaksi.mutasi_pmb_pk  = float(HB['akum_iuran_pk'])
            oDetilTransaksi.mutasi_pmb_pst = float(HB['akum_iuran_pst'])
            oDetilTransaksi.mutasi_pmb_tmb = float(HB['akum_iuran_tmb'])
            oDetilTransaksi.mutasi_pmb_psl = float(HB['akum_psl'])
            
            oDetilTransaksi.mutasi_iuran_pk = oDetilTransaksi.mutasi_iuran_pst = \  
            oDetilTransaksi.mutasi_iuran_tmb = oDetilTransaksi.mutasi_psl = 0.0

            # Update saldo rekening
            oRekDPLK.akum_pmb_pk  += float(HB['akum_iuran_pk'])
            oRekDPLK.akum_pmb_pst += float(HB['akum_iuran_pst'])
            oRekDPLK.akum_pmb_tmb += float(HB['akum_iuran_tmb'])
            oRekDPLK.akum_pmb_psl += float(HB['akum_psl'])
            
            # Akumulasi Saldo
            akumMutasi['mutasi_pmb_pk']  += float(HB['akum_iuran_pk'])
            akumMutasi['mutasi_pmb_pst'] += float(HB['akum_iuran_pst'])
            akumMutasi['mutasi_pmb_tmb'] += float(HB['akum_iuran_tmb'])
            akumMutasi['mutasi_pmb_psl'] += float(HB['akum_psl'])
                        
            
        Ls_RekeningDPLK.Next()
        
    oBaSil.mutasi_pmb_pk  = akumMutasi['mutasi_pmb_pk']
    oBaSil.mutasi_pmb_pst = akumMutasi['mutasi_pmb_pst']
    oBaSil.mutasi_pmb_tmb = akumMutasi['mutasi_pmb_tmb']
    oBaSil.mutasi_pmb_psl = akumMutasi['mutasi_pmb_psl']
  
def getRekening(config):
    dSQL = "SELECT * FROM REKINVDPLK WHERE STATUS_DPLK='A'"
    pst = config.CreateSQL(dSQL).RawResult

    config.BeginTransaction()
    try:
        while not pst.Eof :
            # Panggil fungsi Create Bagi Hasil
            CreateBagiHasil(config, pst)
            pst.Next()
        
        config.Commit()         
    except:
        config.Rollback()
        print str(sys.exc_info()[1])
        return 

        #-- MAIN
if __name__ == '__main__': 
    config = dafsys.OpenConfig('c:/dafapp/dplk/default.cfg')
    getRekening(config)
    
