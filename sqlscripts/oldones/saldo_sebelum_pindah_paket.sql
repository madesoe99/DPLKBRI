
select a.no_peserta,
sum(mutasi_iuran_pst)+sum(mutasi_iuran_pk)+sum(mutasi_pengembangan)+sum(mutasi_peralihan) as saldo_sebelum_pindah_paket
from transaksidplk a, 
(
	select no_peserta, tgl_transaksi as tgl_pindah_paket
	from transaksidplk
	where kode_jenis_transaksi = 'X'
	and keterangan like 'BiayaAdmTransaksi Pemindahan Paket Investasi peserta%'
) b
where 
a.no_peserta = b.no_peserta
and a.no_peserta in ('30500030012', '88100030477')
and tgl_transaksi < tgl_pindah_paket
group by a.no_peserta
order by a.no_peserta