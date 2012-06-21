## reverse transaksi dari hasil Buat Transaksi dari Histori Giro
## untuk tanggal 24 April 2008

import dafsys

def selectIuranPeserta(config, tgl):
    # ambil iuran peserta yang akan dibalikan
    strSQL = \
        'select t.ID_Transaksi '\
        'from TransactionBatch b, TransaksiDPLK t '\
        'where b.batch_type = \'T\' '\
        'and b.batch_sub_type = \'M\' '\
        'and b.tgl_create = \'%s\' '\
        'and b.tgl_used = \'%s\' '\
        'and b.ID_TransactionBatch = t.ID_TransactionBatch '\
        'and t.kode_jenis_transaksi = \'K\' '\
        'and t.keterangan = \'Transaksi dibuat dari Transaksi-Histori-Giro DPLK\' '\
        % (tgl, tgl)
    return config.CreateSQL(strSQL).RawResult

def reverseHGHStatus(config, tgl):
    # kembalikan status HistoriGiroHarian seperti sebelumnya
    strSQL = \
        'update HistoriGiroHarian '\
        'set isTransactionProceed = \'F\' '\
        'where Tanggal_Histori = \'%s\' '\
        '  and isTransactionProceed = \'T\' '\
        % (tgl)
    resExec = config.ExecSQL(strSQL)
    print 'reverseHGHStatus: '+ str(resExec)

    return resExec

def reverseHGStatus(config, tgl):
    # kembalikan status HistoriGiro seperti sebelumnya
    strSQL = \
        'update HistoriGiro '\
        'set isTransaksiCreated = \'F\' '\
        'from HistoriGiro g, HistoriGiroHarian h '\
        'where isTransaksiCreated = \'T\' '\
        '  and g.ID_HistoriGiroHarian = h.ID_HistoriGiroHarian '\
        '  and Tanggal_Histori = \'%s\' '\
        % (tgl)
    resExec = config.ExecSQL(strSQL)
    print 'reverseHGStatus: '+ str(resExec)

    return resExec

def ReverseIuranPesertaFromBatch(config, resSQL):
    # kembalikan efek penambahan dana iuran peserta dan hapus transaksinya

    i = 0    
    resSQL.First()
    while not resSQL.Eof:
        o = config.CreatePObjImplProxy('IuranPeserta')
        o.Key = resSQL.ID_Transaksi

        oR = config.CreatePObjImplProxy('RekeningDPLK')
        oR.Key = o.no_peserta

        oR.akum_dana_iuran_pk = oR.akum_dana_iuran_pk - o.mutasi_iuran_pk
        oR.akum_dana_iuran_pst = oR.akum_dana_iuran_pst - o.mutasi_iuran_pst
        oR.akum_dana_pengembangan = oR.akum_dana_pengembangan - o.mutasi_pengembangan
        oR.akum_dana_peralihan = oR.akum_dana_peralihan - o.mutasi_peralihan

        o.Delete()

        i += 1
        resSQL.Next()

    print 'ReverseIuranPesertaFromBatch: '+ str(i)        

def Main(config, tgl):
    if raw_input('Reverse pembuatan transaksi dari riwayat (histori) giro tanggal %s?\n(y/n)' % (tgl)) not in ['y', 'Y']:
        print 'Proses dibatalkan.'
        return

    config.BeginTransaction()
    try:
        print 'start process'

        print 'selectIuranPeserta'
        resSQL = selectIuranPeserta(config, tgl)
        print 'ReverseIuranPesertaFromBatch'
        ReverseIuranPesertaFromBatch(config, resSQL)

        print 'reverseHGStatus'
        reverseHGStatus(config, tgl)
        print 'reverseHGHStatus'
        reverseHGHStatus(config, tgl)

        # titipan premi belum ditangani

        print 'commit...'
        config.Commit()
    except:
        config.Rollback()
        raise

    print 'transactions were successfully reversed'

config = dafsys.openConfig('c:/dafapp/dplk07/default.cfg')
Main(config, '2008-04-24')
