create table transaksibaghas_120810
(no_peserta varchar(11),
mutasi_iuran_pst float,
mutasi_iuran_pk float,
mutasi_pengembangan float,
mutasi_peralihan float);

insert into transaksibaghas_120810
select no_peserta, sum(mutasi_iuran_pst), sum(mutasi_iuran_pk),
sum(mutasi_pengembangan), sum(mutasi_peralihan)
from transaksidplk
where kode_jenis_transaksi = 'G'
and tgl_transaksi >= '07/31/2010'
group by no_peserta;

create index idx_bgh120810 on transaksibaghas_120810(no_peserta);

update rekeningdplk
set akum_dana_iuran_pst = akum_dana_iuran_pst - mutasi_iuran_pst,
akum_dana_iuran_pk = akum_dana_iuran_pk - mutasi_iuran_pk,
akum_dana_pengembangan = akum_dana_pengembangan - mutasi_pengembangan,
akum_dana_peralihan = akum_dana_peralihan - mutasi_peralihan
from rekeningdplk r, transaksibaghas_120810 t
where 
r.no_peserta = t.no_peserta;


delete from HistoriSRR
where id_srrcalcrincian in
(select id_srrcalcrincian from SRRCalcRincian where id_srrcalc = 35);

delete from SRRCalcRincian where id_srrcalc = 35;

delete from SRRCalc where id_srrcalc = 35;

delete from bagihasil
where idbghasil in
(424,423,422,421,420);

delete from SRRCalcBagiHasil
where idbghasil in
(424,423,422,421,420);

create table detilakum_120810
(no_peserta varchar(11),
kode_jns_investasi varchar(1),
nominal float);

create index idx_dt120810 on detilakum_120810(no_peserta);

insert into detilakum_120810
select no_peserta, substring(keterangan, 21, 1), sum(mutasi_pengembangan) 
from transaksidplk
where kode_jenis_transaksi = 'G'
and tgl_transaksi >= '07/31/2010'
group by no_peserta, substring(keterangan, 21, 1);

update detailakumpengembangan
set nilai_akumulasi = nilai_akumulasi - nominal
from detailakumpengembangan d, detilakum_120810 dt
where 
d.no_peserta = dt.no_peserta
and d.kode_jns_investasi = dt.kode_jns_investasi;

delete
from transaksidplk
where kode_jenis_transaksi = 'G'
and tgl_transaksi >= '07/31/2010';

update parameter
set numeric_value = 40360, varchar_value = '1-7-2010'
where key_parameter = 'BATAS_TGL_TUTUP_BATCH';
