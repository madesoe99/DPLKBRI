update rekeningdplk
set bln_tunggakan_wasiat_ummat = t.bln_tunggakan, kewajiban_wasiat_ummat = nom_tunggakan
from rekeningdplk r,
(
	select rw.no_peserta, 
	datediff(month, tgl_akseptasi, '01/24/2011') as bln_tunggakan,
	(datediff(month, tgl_akseptasi, '01/24/2011') * besar_premi) - sum(mutasi_premi) as nom_tunggakan
	from transaksipremi t, rekeningwasiatummat rw
	where 
	t.no_peserta = rw.no_peserta
	and exists
	(select 1 from rekeningdplk
	where t.no_peserta = no_peserta
	and status_dplk = 'A')
	group by rw.no_peserta, tgl_akseptasi, besar_premi
	having (datediff(month, tgl_akseptasi, '01/24/2011') * besar_premi) - sum(mutasi_premi) > 0
) t
where r.no_peserta = t.no_peserta