delete
from transaksidplk
where no_peserta in
(select no_peserta from transaksidplk
where (kode_jenis_transaksi = 'C')
and tgl_transaksi > '2008-12-30'
and keterangan not like '%Manfaat%')
and
no_peserta not in
(select no_peserta from transaksidplk
where kode_jenis_transaksi = 'G'
and tgl_transaksi > '2008-12-30')

and (kode_jenis_transaksi = 'C' or kode_jenis_transaksi = 'D' )
and tgl_transaksi > '2008-12-30'
and keterangan not like '%Manfaat%'