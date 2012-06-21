update HISTORISRR
set saldo_akhir_srr = a.saldo_akhir_srr + (b.mutasi_iuran_pk + b.mutasi_iuran_pst + b.mutasi_pengembangan + b.mutasi_peralihan)
from HISTORISRR a, transaksidplk b
where 
a.no_peserta = b.no_peserta
and a.id_srrcalcrincian = 73 
and b.kode_jenis_transaksi = 'D'
and b.tgl_transaksi = '06/30/2009'
