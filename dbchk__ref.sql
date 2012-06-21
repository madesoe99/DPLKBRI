-- Number of rows for entity AdvisHistory
SELECT count(*) FROM ADVISHISTORY;

-- Number of rows for link LTransaksiDPLK in entity AdvisHistory
SELECT count(*) FROM ADVISHISTORY a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI = b.ID_Transaksi
;

-- Number of rows for entity AhliWaris
SELECT count(*) FROM AHLIWARIS;

-- Number of rows for link LNasabahDPLK in entity AhliWaris
SELECT count(*) FROM AHLIWARIS a, NASABAHDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity BagiHasil
SELECT count(*) FROM BAGIHASIL;

-- Number of rows for link LRincianPaketInvestasi in entity BagiHasil
SELECT count(*) FROM BAGIHASIL a, RINCIANPAKETINVESTASI b WHERE 
a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
AND a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
;

-- Number of rows for entity BagiHasilDeposito
SELECT count(*) FROM BAGIHASILDEPOSITO;

-- Number of rows for link LDeposito in entity BagiHasilDeposito
SELECT count(*) FROM BAGIHASILDEPOSITO a, DEPOSITO b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity BagiHasilReksadana
SELECT count(*) FROM BAGIHASILREKSADANA;

-- Number of rows for link LReksadana in entity BagiHasilReksadana
SELECT count(*) FROM BAGIHASILREKSADANA a, REKSADANA b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity BeliObligasi
SELECT count(*) FROM BELIOBLIGASI;

-- Number of rows for link LObligasi in entity BeliObligasi
SELECT count(*) FROM BELIOBLIGASI a, OBLIGASI b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity BranchLocation
SELECT count(*) FROM BRANCHLOCATION;

-- Number of rows for link LMasterBranch in entity BranchLocation
SELECT count(*) FROM BRANCHLOCATION a, BRANCHLOCATION b WHERE 
a.masterbranch_code = b.branch_code
;

-- Number of additional rows for optional link LMasterBranch in entity BranchLocation
SELECT count(*) FROM BranchLocation WHERE 
(
a.masterbranch_code IS NULL
);

-- Number of rows for entity DetailAkumPengembangan
SELECT count(*) FROM DETAILAKUMPENGEMBANGAN;

-- Number of rows for link LRekeningDPLK in entity DetailAkumPengembangan
SELECT count(*) FROM DETAILAKUMPENGEMBANGAN a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for link LRincianPaketInvestasi in entity DetailAkumPengembangan
SELECT count(*) FROM DETAILAKUMPENGEMBANGAN a, RINCIANPAKETINVESTASI b WHERE 
a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
AND a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
;

-- Number of rows for entity HistJenisInvestasi
SELECT count(*) FROM HISTJENISINVESTASI;

-- Number of rows for link LPaketInvestasi in entity HistJenisInvestasi
SELECT count(*) FROM HISTJENISINVESTASI a, PAKETINVESTASI b WHERE 
a.kode_paket_investasi = b.kode_paket_investasi
;

-- Number of rows for link LRekeningDPLK in entity HistJenisInvestasi
SELECT count(*) FROM HISTJENISINVESTASI a, REKENINGDPLK b WHERE 
a.no_peserta = b.no_peserta
;

-- Number of rows for entity HistNABReksadana
SELECT count(*) FROM HISTNABREKSADANA;

-- Number of rows for link LReksadana in entity HistNABReksadana
SELECT count(*) FROM HISTNABREKSADANA a, REKSADANA b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for link LTransactionBatch in entity HistNABReksadana
SELECT count(*) FROM HISTNABREKSADANA a, TRANSACTIONBATCH b WHERE 
a.ID_TRANSACTIONBATCH = b.ID_TRANSACTIONBATCH
;

-- Number of additional rows for optional link LTransactionBatch in entity HistNABReksadana
SELECT count(*) FROM HistNABReksadana WHERE 
(
a.ID_TRANSACTIONBATCH IS NULL
);

-- Number of rows for entity HistoriAhliWaris
SELECT count(*) FROM HISTORIAHLIWARIS;

-- Number of rows for link LNasabahDPLK in entity HistoriAhliWaris
SELECT count(*) FROM HISTORIAHLIWARIS a, NASABAHDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity HistoriAhliWarisDetail
SELECT count(*) FROM HISTORIAHLIWARISDETAIL;

-- Number of rows for link LHistoriAhliWaris in entity HistoriAhliWarisDetail
SELECT count(*) FROM HISTORIAHLIWARISDETAIL a, HISTORIAHLIWARIS b WHERE 
a.HISTORIAHLIWARIS_ID = b.HISTORIAHLIWARIS_ID
;

-- Number of rows for entity HistoriAnuitas
SELECT count(*) FROM HISTORIANUITAS;

-- Number of rows for link LRekeningDPLK in entity HistoriAnuitas
SELECT count(*) FROM HISTORIANUITAS a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity HistoriAutoDebet
SELECT count(*) FROM HISTORIAUTODEBET;

-- Number of rows for link LRekeningDPLK in entity HistoriAutoDebet
SELECT count(*) FROM HISTORIAUTODEBET a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity HistoriGiro
SELECT count(*) FROM HISTORIGIRO;

-- Number of rows for link LHistoriGiroHarian in entity HistoriGiro
SELECT count(*) FROM HISTORIGIRO a, HISTORIGIROHARIAN b WHERE 
a.ID_HISTORIGIROHARIAN = b.ID_HISTORIGIROHARIAN
;

-- Number of rows for link LMasterGiro in entity HistoriGiro
SELECT count(*) FROM HISTORIGIRO a, MASTERGIRO b WHERE 
a.ACC_GIRO = b.ACC_GIRO
;

-- Number of rows for entity HistoriGiroHarian
SELECT count(*) FROM HISTORIGIROHARIAN;

-- Number of rows for link LMasterGiro in entity HistoriGiroHarian
SELECT count(*) FROM HISTORIGIROHARIAN a, MASTERGIRO b WHERE 
a.ACC_GIRO = b.ACC_GIRO
;

-- Number of rows for entity HistoriIuran
SELECT count(*) FROM HISTORIIURAN;

-- Number of rows for link LRekeningDPLK in entity HistoriIuran
SELECT count(*) FROM HISTORIIURAN a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity HistoriPindahPaketInvestasi
SELECT count(*) FROM HISTORIPINDAHPAKETINVESTASI;

-- Number of rows for link LPaketInvestasi in entity HistoriPindahPaketInvestasi
SELECT count(*) FROM HISTORIPINDAHPAKETINVESTASI a, PAKETINVESTASI b WHERE 
a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
;

-- Number of rows for link LRekeningDPLK in entity HistoriPindahPaketInvestasi
SELECT count(*) FROM HISTORIPINDAHPAKETINVESTASI a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity HistoriSRR
SELECT count(*) FROM HISTORISRR;

-- Number of rows for link LSRRCalcRincian in entity HistoriSRR
SELECT count(*) FROM HISTORISRR a, SRRCALCRINCIAN b WHERE 
a.ID_SRRCALCRINCIAN = b.ID_SRRCALCRINCIAN
;

-- Number of rows for link LRekeningDPLK in entity HistoriSRR
SELECT count(*) FROM HISTORISRR a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity HistoriUbahAlamat
SELECT count(*) FROM HISTORIUBAHALAMAT;

-- Number of rows for link LNasabahDPLK in entity HistoriUbahAlamat
SELECT count(*) FROM HISTORIUBAHALAMAT a, NASABAHDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity HistoriUbahStatusKerja
SELECT count(*) FROM HISTORIUBAHSTATUSKERJA;

-- Number of rows for link LNasabahDPLK in entity HistoriUbahStatusKerja
SELECT count(*) FROM HISTORIUBAHSTATUSKERJA a, NASABAHDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for link LNasabahDPLKCorporate in entity HistoriUbahStatusKerja
SELECT count(*) FROM HISTORIUBAHSTATUSKERJA a, NASABAHDPLKCORPORATE b WHERE 
a.KODE_NASABAH_CORPORATE = b.KODE_NASABAH_CORPORATE
;

-- Number of rows for entity HistoriWasiatUmmat
SELECT count(*) FROM HISTORIWASIATUMMAT;

-- Number of rows for link LRekeningDPLK in entity HistoriWasiatUmmat
SELECT count(*) FROM HISTORIWASIATUMMAT a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity HistPerubahanDeposito
SELECT count(*) FROM HISTPERUBAHANDEPOSITO;

-- Number of rows for link LDeposito in entity HistPerubahanDeposito
SELECT count(*) FROM HISTPERUBAHANDEPOSITO a, DEPOSITO b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity Investasi
SELECT count(*) FROM INVESTASI;

-- Number of rows for link LPihakKetiga in entity Investasi
SELECT count(*) FROM INVESTASI a, PIHAKKETIGA b WHERE 
a.KODE_PIHAK_KETIGA = b.kode_pihak_ketiga
;

-- Number of rows for link LRincianPaketInvestasi in entity Investasi
SELECT count(*) FROM INVESTASI a, RINCIANPAKETINVESTASI b WHERE 
a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
AND a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
;

-- Number of additional rows for optional link LRincianPaketInvestasi in entity Investasi
SELECT count(*) FROM Investasi WHERE 
(
a.KODE_PAKET_INVESTASI IS NULL
OR a.KODE_JNS_INVESTASI IS NULL
);

-- Number of rows for entity IuranPendaftaran
SELECT count(*) FROM IURANPENDAFTARAN;

-- Number of rows for link LRekeningDPLK in entity IuranPendaftaran
SELECT count(*) FROM IURANPENDAFTARAN a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for link LTransactionBatch in entity IuranPendaftaran
SELECT count(*) FROM IURANPENDAFTARAN a, TRANSACTIONBATCH b WHERE 
a.ID_TRANSACTIONBATCH = b.ID_TRANSACTIONBATCH
;

-- Number of rows for entity IuranPeserta
SELECT count(*) FROM TRANSAKSIDPLK WHERE KODE_JENIS_TRANSAKSI = 'K';

-- Number of rows for link LTransactionBatchPremi in entity IuranPeserta
SELECT count(*) FROM TRANSAKSIDPLK a, TRANSACTIONBATCH b WHERE 
KODE_JENIS_TRANSAKSI = 'K' AND 
a.ID_BATCHPREMI = b.ID_TRANSACTIONBATCH
;

-- Number of additional rows for optional link LTransactionBatchPremi in entity IuranPeserta
SELECT count(*) FROM IuranPeserta WHERE KODE_JENIS_TRANSAKSI = 'K' AND 
(
a.ID_BATCHPREMI IS NULL
);

-- Number of rows for entity JualObligasi
SELECT count(*) FROM JUALOBLIGASI;

-- Number of rows for link LObligasi in entity JualObligasi
SELECT count(*) FROM JUALOBLIGASI a, OBLIGASI b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity NamaJnsTransInv
SELECT count(*) FROM NAMAJNSTRANSINV;

-- Number of rows for link LJenisInvestasi in entity NamaJnsTransInv
SELECT count(*) FROM NAMAJNSTRANSINV a, JENISINVESTASI b WHERE 
a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
;

-- Number of rows for link LJnsTransInvestasi in entity NamaJnsTransInv
SELECT count(*) FROM NAMAJNSTRANSINV a, JNSTRANSINVESTASI b WHERE 
a.KODE_JENIS_TRINVESTASI = b.KODE_JENIS_TRINVESTASI
;

-- Number of rows for entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK;

-- Number of rows for link LDaerahAsal in entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK a, DAERAHASAL b WHERE 
a.kode_propinsi = b.kode_propinsi
;

-- Number of rows for link LJenisUsaha in entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK a, JENISUSAHA b WHERE 
a.kode_jenis_usaha = b.kode_jenis_usaha
;

-- Number of rows for link LKepemilikan in entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK a, KEPEMILIKAN b WHERE 
a.kode_pemilikan = b.kode_pemilikan
;

-- Number of rows for link LRekeningDPLK in entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK a, REKENINGDPLK b WHERE 
a.no_peserta = b.no_peserta
;

-- Number of rows for link LNasabahDPLKCorporate in entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK a, NASABAHDPLKCORPORATE b WHERE 
a.KODE_NASABAH_CORPORATE = b.KODE_NASABAH_CORPORATE
;

-- Number of additional rows for optional link LNasabahDPLKCorporate in entity NasabahDPLK
SELECT count(*) FROM NasabahDPLK WHERE 
(
a.KODE_NASABAH_CORPORATE IS NULL
);

-- Number of rows for link LOperationCode in entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK a, OPERATIONCODE b WHERE 
a.OPERATION_CODE = b.OPERATION_CODE
;

-- Number of rows for link LKelompok in entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK a, KELOMPOK b WHERE 
a.KODE_KELOMPOK = b.KODE_KELOMPOK
;

-- Number of additional rows for optional link LKelompok in entity NasabahDPLK
SELECT count(*) FROM NasabahDPLK WHERE 
(
a.KODE_KELOMPOK IS NULL
);

-- Number of rows for link LLDPLain in entity NasabahDPLK
SELECT count(*) FROM NASABAHDPLK a, LDP b WHERE 
a.KODE_DP = b.KODE_DP
;

-- Number of additional rows for optional link LLDPLain in entity NasabahDPLK
SELECT count(*) FROM NasabahDPLK WHERE 
(
a.KODE_DP IS NULL
);

-- Number of rows for entity NasabahDPLKCorporate
SELECT count(*) FROM NASABAHDPLKCORPORATE;

-- Number of rows for link LJenisUsaha in entity NasabahDPLKCorporate
SELECT count(*) FROM NASABAHDPLKCORPORATE a, JENISUSAHA b WHERE 
a.KODE_JENIS_USAHA = b.kode_jenis_usaha
;

-- Number of rows for link LKepemilikan in entity NasabahDPLKCorporate
SELECT count(*) FROM NASABAHDPLKCORPORATE a, KEPEMILIKAN b WHERE 
a.KODE_PEMILIKAN = b.kode_pemilikan
;

-- Number of rows for link LOperationCode in entity NasabahDPLKCorporate
SELECT count(*) FROM NASABAHDPLKCORPORATE a, OPERATIONCODE b WHERE 
a.OPERATION_CODE = b.OPERATION_CODE
;

-- Number of rows for entity Obligasi
SELECT count(*) FROM OBLIGASI;

-- Number of rows for link LCustodianBank in entity Obligasi
SELECT count(*) FROM OBLIGASI a, CUSTODIANBANK b WHERE 
a.BANKCODE = b.BANKCODE
;

-- Number of rows for entity PembagianHasilPortofolio
SELECT count(*) FROM TRANSAKSIDPLK WHERE KODE_JENIS_TRANSAKSI = 'G';

-- Number of rows for link Lbagi_hasil in entity PembagianHasilPortofolio
SELECT count(*) FROM TRANSAKSIDPLK a, BAGIHASIL b WHERE 
KODE_JENIS_TRANSAKSI = 'G' AND 
a.idbghasil = b.idbghasil
;

-- Number of rows for entity PenarikanDana
SELECT count(*) FROM PENARIKANDANA;

-- Number of rows for link LBiayaAdmTransaksi in entity PenarikanDana
SELECT count(*) FROM PENARIKANDANA a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BADMTRANS = b.ID_TRANSAKSI
;

-- Number of rows for entity PenarikanDanaNormal
SELECT count(*) FROM PENARIKANDANA;

-- Number of rows for link LBiayaAdmTransaksi in entity PenarikanDanaNormal
SELECT count(*) FROM PENARIKANDANA a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BADMTRANS = b.ID_TRANSAKSI
;

-- Number of rows for entity PenarikanDanaPHK
SELECT count(*) FROM PENARIKANDANA;

-- Number of rows for link LBiayaAdmTransaksi in entity PenarikanDanaPHK
SELECT count(*) FROM PENARIKANDANA a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BADMTRANS = b.ID_TRANSAKSI
;

-- Number of rows for entity PendapatanObligasi
SELECT count(*) FROM PENDAPATANOBLIGASI;

-- Number of rows for link LObligasi in entity PendapatanObligasi
SELECT count(*) FROM PENDAPATANOBLIGASI a, OBLIGASI b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity PendapatanReksadana
SELECT count(*) FROM PENDAPATANREKSADANA;

-- Number of rows for link LReksadana in entity PendapatanReksadana
SELECT count(*) FROM PENDAPATANREKSADANA a, REKSADANA b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity PengalihanDariDPLKLain
SELECT count(*) FROM PENGALIHANDARIDPLKLAIN;

-- Number of rows for link LLDP in entity PengalihanDariDPLKLain
SELECT count(*) FROM PENGALIHANDARIDPLKLAIN a, LDP b WHERE 
a.KODE_DP = b.KODE_DP
;

-- Number of rows for entity PengalihanKeDPLKLain
SELECT count(*) FROM PENGALIHANKEDPLKLAIN;

-- Number of rows for link LBiayaAdmTahunan in entity PengalihanKeDPLKLain
SELECT count(*) FROM PENGALIHANKEDPLKLAIN a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BADMTHN = b.ID_Transaksi
;

-- Number of rows for link LBiayaPengelolaanDana in entity PengalihanKeDPLKLain
SELECT count(*) FROM PENGALIHANKEDPLKLAIN a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BPENG = b.ID_Transaksi
;

-- Number of rows for link LBiayaAdmTransaksi in entity PengalihanKeDPLKLain
SELECT count(*) FROM PENGALIHANKEDPLKLAIN a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BADMTRANS = b.ID_TRANSAKSI
;

-- Number of rows for link LLDP in entity PengalihanKeDPLKLain
SELECT count(*) FROM PENGALIHANKEDPLKLAIN a, LDP b WHERE 
a.KODE_DP = b.KODE_DP
;

-- Number of rows for entity PengambilanManfaat
SELECT count(*) FROM PENGAMBILANMANFAAT;

-- Number of rows for link Ljenis_penerimaan_manfaat in entity PengambilanManfaat
SELECT count(*) FROM PENGAMBILANMANFAAT a, JENISPENERIMAANMANFAAT b WHERE 
a.kode_jns_manfaat = b.kode_jns_manfaat
;

-- Number of rows for link LAhliWaris in entity PengambilanManfaat
SELECT count(*) FROM PENGAMBILANMANFAAT a, AHLIWARIS b WHERE 
a.AHLIWARIS_ID = b.AHLIWARIS_ID
;

-- Number of additional rows for optional link LAhliWaris in entity PengambilanManfaat
SELECT count(*) FROM PengambilanManfaat WHERE 
(
a.AHLIWARIS_ID IS NULL
);

-- Number of rows for link LBiayaAdmTahunan in entity PengambilanManfaat
SELECT count(*) FROM PENGAMBILANMANFAAT a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BADMTHN = b.ID_Transaksi
;

-- Number of rows for link LBiayaPengelolaanDana in entity PengambilanManfaat
SELECT count(*) FROM PENGAMBILANMANFAAT a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BPENG = b.ID_Transaksi
;

-- Number of rows for link LBiayaAdmTransaksi in entity PengambilanManfaat
SELECT count(*) FROM PENGAMBILANMANFAAT a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_BADMTRANS = b.ID_TRANSAKSI
;

-- Number of rows for entity RealisasiReturn
SELECT count(*) FROM REALISASIRETURN;

-- Number of rows for link LReksadana in entity RealisasiReturn
SELECT count(*) FROM REALISASIRETURN a, REKSADANA b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity RedemptReksadana
SELECT count(*) FROM REDEMPTREKSADANA;

-- Number of rows for link LKlaimLRReksadana in entity RedemptReksadana
SELECT count(*) FROM REDEMPTREKSADANA a, KLAIMLRREKSADANA b WHERE 
a.ID_TRANSAKSIINVESTASI_KLAIM = b.ID_TRANSAKSIINVESTASI
;

-- Number of additional rows for optional link LKlaimLRReksadana in entity RedemptReksadana
SELECT count(*) FROM RedemptReksadana WHERE 
(
a.ID_TRANSAKSIINVESTASI_KLAIM IS NULL
);

-- Number of rows for link LReksadana in entity RedemptReksadana
SELECT count(*) FROM REDEMPTREKSADANA a, REKSADANA b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity RegEditNasabahDPLKCorporate
SELECT count(*) FROM REGEDITNASABAHDPLKCORPORATE;

-- Number of rows for link LKepemilikan in entity RegEditNasabahDPLKCorporate
SELECT count(*) FROM REGEDITNASABAHDPLKCORPORATE a, KEPEMILIKAN b WHERE 
a.KODE_PEMILIKAN = b.kode_pemilikan
;

-- Number of rows for link LJenisUsaha in entity RegEditNasabahDPLKCorporate
SELECT count(*) FROM REGEDITNASABAHDPLKCORPORATE a, JENISUSAHA b WHERE 
a.KODE_JENIS_USAHA = b.kode_jenis_usaha
;

-- Number of rows for link LNasabahDPLKCorporate in entity RegEditNasabahDPLKCorporate
SELECT count(*) FROM REGEDITNASABAHDPLKCORPORATE a, NASABAHDPLKCORPORATE b WHERE 
a.KODE_NASABAH_CORPORATE = b.KODE_NASABAH_CORPORATE
;

-- Number of additional rows for optional link LNasabahDPLKCorporate in entity RegEditNasabahDPLKCorporate
SELECT count(*) FROM RegEditNasabahDPLKCorporate WHERE 
(
a.KODE_NASABAH_CORPORATE IS NULL
);

-- Number of rows for link LOperationCode in entity RegEditNasabahDPLKCorporate
SELECT count(*) FROM REGEDITNASABAHDPLKCORPORATE a, OPERATIONCODE b WHERE 
a.OPERATION_CODE = b.OPERATION_CODE
;

-- Number of rows for link LNasabahDPLKHolding in entity RegEditNasabahDPLKCorporate
SELECT count(*) FROM REGEDITNASABAHDPLKCORPORATE a, NASABAHDPLKCORPORATE b WHERE 
a.KODE_HOLDING = b.KODE_NASABAH_CORPORATE
;

-- Number of additional rows for optional link LNasabahDPLKHolding in entity RegEditNasabahDPLKCorporate
SELECT count(*) FROM RegEditNasabahDPLKCorporate WHERE 
(
a.KODE_HOLDING IS NULL
);

-- Number of rows for entity RegEditNasabahRekening
SELECT count(*) FROM REGEDITNASABAHREKENING;

-- Number of rows for link LJenisUsaha in entity RegEditNasabahRekening
SELECT count(*) FROM REGEDITNASABAHREKENING a, JENISUSAHA b WHERE 
a.KODE_JENIS_USAHA = b.kode_jenis_usaha
;

-- Number of rows for link LKepemilikan in entity RegEditNasabahRekening
SELECT count(*) FROM REGEDITNASABAHREKENING a, KEPEMILIKAN b WHERE 
a.KODE_PEMILIKAN = b.kode_pemilikan
;

-- Number of rows for link LDaerahAsal in entity RegEditNasabahRekening
SELECT count(*) FROM REGEDITNASABAHREKENING a, DAERAHASAL b WHERE 
a.KODE_PROPINSI = b.kode_propinsi
;

-- Number of rows for link LSumberDana in entity RegEditNasabahRekening
SELECT count(*) FROM REGEDITNASABAHREKENING a, SUMBERDANA b WHERE 
a.SUMBER_DANA = b.SUMBER_DANA
;

-- Number of rows for link LKelompok in entity RegEditNasabahRekening
SELECT count(*) FROM REGEDITNASABAHREKENING a, KELOMPOK b WHERE 
a.KODE_KELOMPOK = b.KODE_KELOMPOK
;

-- Number of additional rows for optional link LKelompok in entity RegEditNasabahRekening
SELECT count(*) FROM RegEditNasabahRekening WHERE 
(
a.KODE_KELOMPOK IS NULL
);

-- Number of rows for entity RegisterAhliWarisDetail
SELECT count(*) FROM REGISTERAHLIWARISDETAIL;

-- Number of rows for link LRegisterAhliWaris in entity RegisterAhliWarisDetail
SELECT count(*) FROM REGISTERAHLIWARISDETAIL a, REGISTERAHLIWARIS b WHERE 
a.REGISTERCIF_ID = b.REGISTERCIF_ID
;

-- Number of rows for entity RegisterCIF
SELECT count(*) FROM REGISTERCIF;

-- Number of rows for link LNasabahDPLK in entity RegisterCIF
SELECT count(*) FROM REGISTERCIF a, NASABAHDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for link LJenisRegisterCIF in entity RegisterCIF
SELECT count(*) FROM REGISTERCIF a, JENISREGISTERCIF b WHERE 
a.KODE_JENIS_REGISTERCIF = b.KODE_JENIS_REGISTERCIF
;

-- Number of rows for link LUserApp in entity RegisterCIF
SELECT count(*) FROM REGISTERCIF a, USERAPP b WHERE 
a.USER_ID = b.user_id
;

-- Number of rows for entity RegisterDeposito
SELECT count(*) FROM REGISTERDEPOSITO;

-- Number of rows for link LMasterGiro in entity RegisterDeposito
SELECT count(*) FROM REGISTERDEPOSITO a, MASTERGIRO b WHERE 
a.ACC_GIRO = b.ACC_GIRO
;

-- Number of additional rows for optional link LMasterGiro in entity RegisterDeposito
SELECT count(*) FROM RegisterDeposito WHERE 
(
a.ACC_GIRO IS NULL
);

-- Number of rows for entity RegisterInvestasi
SELECT count(*) FROM REGISTERINVESTASI;

-- Number of rows for link LPihakKetiga in entity RegisterInvestasi
SELECT count(*) FROM REGISTERINVESTASI a, PIHAKKETIGA b WHERE 
a.KODE_PIHAK_KETIGA = b.kode_pihak_ketiga
;

-- Number of rows for link LRincianPaketInvestasi in entity RegisterInvestasi
SELECT count(*) FROM REGISTERINVESTASI a, RINCIANPAKETINVESTASI b WHERE 
a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
AND a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
;

-- Number of additional rows for optional link LRincianPaketInvestasi in entity RegisterInvestasi
SELECT count(*) FROM RegisterInvestasi WHERE 
(
a.KODE_JNS_INVESTASI IS NULL
OR a.KODE_PAKET_INVESTASI IS NULL
);

-- Number of rows for link LTransactionBatch in entity RegisterInvestasi
SELECT count(*) FROM REGISTERINVESTASI a, TRANSACTIONBATCH b WHERE 
a.ID_TRANSACTIONBATCH = b.ID_TRANSACTIONBATCH
;

-- Number of rows for entity RegisterIuran
SELECT count(*) FROM REGISTERIURAN;

-- Number of rows for link LRekeningDPLK in entity RegisterIuran
SELECT count(*) FROM REGISTERIURAN a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING;

-- Number of rows for link LDaerahAsal in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, DAERAHASAL b WHERE 
a.KODE_PROPINSI = b.kode_propinsi
;

-- Number of rows for link LKepemilikan in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, KEPEMILIKAN b WHERE 
a.KODE_PEMILIKAN = b.kode_pemilikan
;

-- Number of additional rows for optional link LKepemilikan in entity RegisterNasabahRekening
SELECT count(*) FROM RegisterNasabahRekening WHERE 
(
a.KODE_PEMILIKAN IS NULL
);

-- Number of rows for link LJenisUsaha in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, JENISUSAHA b WHERE 
a.KODE_JENIS_USAHA = b.kode_jenis_usaha
;

-- Number of additional rows for optional link LJenisUsaha in entity RegisterNasabahRekening
SELECT count(*) FROM RegisterNasabahRekening WHERE 
(
a.KODE_JENIS_USAHA IS NULL
);

-- Number of rows for link LNasabahDPLKCorporate in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, NASABAHDPLKCORPORATE b WHERE 
a.KODE_NASABAH_CORPORATE = b.KODE_NASABAH_CORPORATE
;

-- Number of additional rows for optional link LNasabahDPLKCorporate in entity RegisterNasabahRekening
SELECT count(*) FROM RegisterNasabahRekening WHERE 
(
a.KODE_NASABAH_CORPORATE IS NULL
);

-- Number of rows for link LPaketInvestasi in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, PAKETINVESTASI b WHERE 
a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
;

-- Number of rows for link LSumberDana in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, SUMBERDANA b WHERE 
a.sumber_dana = b.SUMBER_DANA
;

-- Number of rows for link LKelompok in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, KELOMPOK b WHERE 
a.KODE_KELOMPOK = b.KODE_KELOMPOK
;

-- Number of additional rows for optional link LKelompok in entity RegisterNasabahRekening
SELECT count(*) FROM RegisterNasabahRekening WHERE 
(
a.KODE_KELOMPOK IS NULL
);

-- Number of rows for link LRegisterIuranPeserta in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, TRANSAKSIDPLK b WHERE 
a.ID_TRANSAKSI_IURANPESERTA = b.ID_Transaksi
;

-- Number of rows for link LRegisterIuranPendaftaran in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, IURANPENDAFTARAN b WHERE 
a.ID_TRANSAKSI_IURANPENDAFTARAN = b.ID_TRANSAKSI
;

-- Number of rows for link LLDPLain in entity RegisterNasabahRekening
SELECT count(*) FROM REGISTERNASABAHREKENING a, LDP b WHERE 
a.KODE_DP = b.KODE_DP
;

-- Number of additional rows for optional link LLDPLain in entity RegisterNasabahRekening
SELECT count(*) FROM RegisterNasabahRekening WHERE 
(
a.KODE_DP IS NULL
);

-- Number of rows for entity RegisterObligasi
SELECT count(*) FROM REGISTEROBLIGASI;

-- Number of rows for link LCustodianBank in entity RegisterObligasi
SELECT count(*) FROM REGISTEROBLIGASI a, CUSTODIANBANK b WHERE 
a.BANKCODE = b.BANKCODE
;

-- Number of rows for entity RegisterPindahPaketInvestasi
SELECT count(*) FROM REGISTERPINDAHPAKETINVESTASI;

-- Number of rows for link LPaketInvestasi in entity RegisterPindahPaketInvestasi
SELECT count(*) FROM REGISTERPINDAHPAKETINVESTASI a, PAKETINVESTASI b WHERE 
a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
;

-- Number of rows for link LTransactionBatch in entity RegisterPindahPaketInvestasi
SELECT count(*) FROM REGISTERPINDAHPAKETINVESTASI a, TRANSACTIONBATCH b WHERE 
a.ID_TRANSACTIONBATCH = b.ID_TRANSACTIONBATCH
;

-- Number of rows for entity RegisterReksadana
SELECT count(*) FROM REGISTERREKSADANA;

-- Number of rows for link LCustodianBank in entity RegisterReksadana
SELECT count(*) FROM REGISTERREKSADANA a, CUSTODIANBANK b WHERE 
a.BANKCODE = b.BANKCODE
;

-- Number of additional rows for optional link LCustodianBank in entity RegisterReksadana
SELECT count(*) FROM RegisterReksadana WHERE 
(
a.BANKCODE IS NULL
);

-- Number of rows for link LJenisReksadana in entity RegisterReksadana
SELECT count(*) FROM REGISTERREKSADANA a, JENISREKSADANA b WHERE 
a.KODE_JNS_REKSADANA = b.KODE_JNS_REKSADANA
;

-- Number of rows for entity RegisterUbahStatusKerja
SELECT count(*) FROM REGISTERUBAHSTATUSKERJA;

-- Number of rows for link LNasabahDPLKCorporate in entity RegisterUbahStatusKerja
SELECT count(*) FROM REGISTERUBAHSTATUSKERJA a, NASABAHDPLKCORPORATE b WHERE 
a.KODE_NASABAH_CORPORATE = b.KODE_NASABAH_CORPORATE
;

-- Number of additional rows for optional link LNasabahDPLKCorporate in entity RegisterUbahStatusKerja
SELECT count(*) FROM RegisterUbahStatusKerja WHERE 
(
a.KODE_NASABAH_CORPORATE IS NULL
);

-- Number of rows for entity RegNRAhliWaris
SELECT count(*) FROM REGNRAHLIWARIS;

-- Number of rows for link LRegisterNasabahRekening in entity RegNRAhliWaris
SELECT count(*) FROM REGNRAHLIWARIS a, REGISTERNASABAHREKENING b WHERE 
a.REGISTERNR_ID = b.REGISTERNR_ID
;

-- Number of rows for entity RekeningAnuitas
SELECT count(*) FROM REKENINGANUITAS;

-- Number of rows for link LRekeningDPLK in entity RekeningAnuitas
SELECT count(*) FROM REKENINGANUITAS a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity RekeningAutoDebet
SELECT count(*) FROM REKENINGAUTODEBET;

-- Number of rows for link LRekeningDPLK in entity RekeningAutoDebet
SELECT count(*) FROM REKENINGAUTODEBET a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity RekeningDPLK
SELECT count(*) FROM REKENINGDPLK;

-- Number of rows for link LNasabahDPLK in entity RekeningDPLK
SELECT count(*) FROM REKENINGDPLK a, NASABAHDPLK b WHERE 
a.no_peserta = b.no_peserta
;

-- Number of rows for link LPaketInvestasi in entity RekeningDPLK
SELECT count(*) FROM REKENINGDPLK a, PAKETINVESTASI b WHERE 
a.kode_paket_investasi = b.kode_paket_investasi
;

-- Number of rows for link LBranchLocation in entity RekeningDPLK
SELECT count(*) FROM REKENINGDPLK a, BRANCHLOCATION b WHERE 
a.kode_cab_daftar = b.branch_code
;

-- Number of rows for link LOperationCode in entity RekeningDPLK
SELECT count(*) FROM REKENINGDPLK a, OPERATIONCODE b WHERE 
a.OPERATION_CODE = b.OPERATION_CODE
;

-- Number of rows for link LSumberDana in entity RekeningDPLK
SELECT count(*) FROM REKENINGDPLK a, SUMBERDANA b WHERE 
a.sumber_dana = b.SUMBER_DANA
;

-- Number of rows for entity RekeningWasiatUmmat
SELECT count(*) FROM REKENINGWASIATUMMAT;

-- Number of rows for link LRekeningDPLK in entity RekeningWasiatUmmat
SELECT count(*) FROM REKENINGWASIATUMMAT a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity Reksadana
SELECT count(*) FROM REKSADANA;

-- Number of rows for link LCustodianBank in entity Reksadana
SELECT count(*) FROM REKSADANA a, CUSTODIANBANK b WHERE 
a.BANKCODE = b.BANKCODE
;

-- Number of additional rows for optional link LCustodianBank in entity Reksadana
SELECT count(*) FROM Reksadana WHERE 
(
a.BANKCODE IS NULL
);

-- Number of rows for link LJenisReksadana in entity Reksadana
SELECT count(*) FROM REKSADANA a, JENISREKSADANA b WHERE 
a.KODE_JNS_REKSADANA = b.KODE_JNS_REKSADANA
;

-- Number of rows for entity RincianDeposito
SELECT count(*) FROM RINCIANINVESTASI WHERE KODE_JNS_INVESTASI = 'D';

-- Number of rows for link LDeposito in entity RincianDeposito
SELECT count(*) FROM RINCIANINVESTASI a, DEPOSITO b WHERE 
KODE_JNS_INVESTASI = 'D' AND 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity RincianInvestasi
SELECT count(*) FROM RINCIANINVESTASI;

-- Number of rows for link LInvestasi in entity RincianInvestasi
SELECT count(*) FROM RINCIANINVESTASI a, INVESTASI b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for link LRincianPaketInvestasi in entity RincianInvestasi
SELECT count(*) FROM RINCIANINVESTASI a, RINCIANPAKETINVESTASI b WHERE 
a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
AND a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
;

-- Number of rows for entity RincianObligasi
SELECT count(*) FROM RINCIANINVESTASI WHERE KODE_JNS_INVESTASI = 'O';

-- Number of rows for link LObligasi in entity RincianObligasi
SELECT count(*) FROM RINCIANINVESTASI a, OBLIGASI b WHERE 
KODE_JNS_INVESTASI = 'O' AND 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity RincianPaketInvestasi
SELECT count(*) FROM RINCIANPAKETINVESTASI;

-- Number of rows for link LPaketInvestasi in entity RincianPaketInvestasi
SELECT count(*) FROM RINCIANPAKETINVESTASI a, PAKETINVESTASI b WHERE 
a.kode_paket_investasi = b.kode_paket_investasi
;

-- Number of rows for link LJenisInvestasi in entity RincianPaketInvestasi
SELECT count(*) FROM RINCIANPAKETINVESTASI a, JENISINVESTASI b WHERE 
a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
;

-- Number of rows for entity RincianPihakKetiga
SELECT count(*) FROM RINCIANPIHAKKETIGA;

-- Number of rows for link LPihakKetiga in entity RincianPihakKetiga
SELECT count(*) FROM RINCIANPIHAKKETIGA a, PIHAKKETIGA b WHERE 
a.KODE_PIHAK_KETIGA = b.kode_pihak_ketiga
;

-- Number of rows for link LJenisInvestasi in entity RincianPihakKetiga
SELECT count(*) FROM RINCIANPIHAKKETIGA a, JENISINVESTASI b WHERE 
a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
;

-- Number of rows for entity RincianRegisterDeposito
SELECT count(*) FROM RINCIANREGISTERINVESTASI WHERE KODE_JNS_INVESTASI = 'A';

-- Number of rows for link LRegisterDeposito in entity RincianRegisterDeposito
SELECT count(*) FROM RINCIANREGISTERINVESTASI a, REGISTERDEPOSITO b WHERE 
KODE_JNS_INVESTASI = 'A' AND 
a.ID_REGISTERINVESTASI = b.ID_REGISTERINVESTASI
;

-- Number of rows for entity RincianRegisterInvestasi
SELECT count(*) FROM RINCIANREGISTERINVESTASI;

-- Number of rows for link LRegisterInvestasi in entity RincianRegisterInvestasi
SELECT count(*) FROM RINCIANREGISTERINVESTASI a, REGISTERINVESTASI b WHERE 
a.ID_REGISTERINVESTASI = b.ID_REGISTERINVESTASI
;

-- Number of rows for link LRincianPaketInvestasi in entity RincianRegisterInvestasi
SELECT count(*) FROM RINCIANREGISTERINVESTASI a, RINCIANPAKETINVESTASI b WHERE 
a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
AND a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
;

-- Number of rows for entity RincianRegisterObligasi
SELECT count(*) FROM RINCIANREGISTERINVESTASI WHERE KODE_JNS_INVESTASI = 'B';

-- Number of rows for link LRegisterObligasi in entity RincianRegisterObligasi
SELECT count(*) FROM RINCIANREGISTERINVESTASI a, REGISTEROBLIGASI b WHERE 
KODE_JNS_INVESTASI = 'B' AND 
a.ID_REGISTERINVESTASI = b.ID_REGISTERINVESTASI
;

-- Number of rows for entity RincianRegisterReksadana
SELECT count(*) FROM RINCIANREGISTERINVESTASI WHERE KODE_JNS_INVESTASI = 'C';

-- Number of rows for link LRegisterReksadana in entity RincianRegisterReksadana
SELECT count(*) FROM RINCIANREGISTERINVESTASI a, REGISTERREKSADANA b WHERE 
KODE_JNS_INVESTASI = 'C' AND 
a.ID_REGISTERINVESTASI = b.ID_REGISTERINVESTASI
;

-- Number of rows for entity RincianReksadana
SELECT count(*) FROM RINCIANINVESTASI WHERE KODE_JNS_INVESTASI = 'R';

-- Number of rows for link LReksadana in entity RincianReksadana
SELECT count(*) FROM RINCIANINVESTASI a, REKSADANA b WHERE 
KODE_JNS_INVESTASI = 'R' AND 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity RolloverDeposito
SELECT count(*) FROM ROLLOVERDEPOSITO;

-- Number of rows for link LDeposito in entity RolloverDeposito
SELECT count(*) FROM ROLLOVERDEPOSITO a, DEPOSITO b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity SessionBLOB
SELECT count(*) FROM SESSIONBLOB;

-- Number of rows for link LBLOBData in entity SessionBLOB
SELECT count(*) FROM SESSIONBLOB a, BLOBREGISTRATION b WHERE 
a.ID1 = b.ID
;

-- Number of additional rows for optional link LBLOBData in entity SessionBLOB
SELECT count(*) FROM SessionBLOB WHERE 
(
a.ID1 IS NULL
);

-- Number of rows for entity SRRCalc
SELECT count(*) FROM SRRCALC;

-- Number of rows for link LUserCreate in entity SRRCalc
SELECT count(*) FROM SRRCALC a, USERAPP b WHERE 
a.USER_ID_CREATE = b.user_id
;

-- Number of rows for entity SRRCalcBagiHasil
SELECT count(*) FROM SRRCALCBAGIHASIL;

-- Number of rows for link LBagiHasil in entity SRRCalcBagiHasil
SELECT count(*) FROM SRRCALCBAGIHASIL a, BAGIHASIL b WHERE 
a.IDBGHASIL = b.idbghasil
;

-- Number of rows for link LSRRCalcRincian in entity SRRCalcBagiHasil
SELECT count(*) FROM SRRCALCBAGIHASIL a, SRRCALCRINCIAN b WHERE 
a.ID_SRRCALCRINCIAN = b.ID_SRRCALCRINCIAN
;

-- Number of rows for entity SRRCalcRincian
SELECT count(*) FROM SRRCALCRINCIAN;

-- Number of rows for link LPaketInvestasi in entity SRRCalcRincian
SELECT count(*) FROM SRRCALCRINCIAN a, PAKETINVESTASI b WHERE 
a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
;

-- Number of rows for link LSRRCalc in entity SRRCalcRincian
SELECT count(*) FROM SRRCALCRINCIAN a, SRRCALC b WHERE 
a.ID_SRRCALC = b.ID_SRRCALC
;

-- Number of rows for entity SubJnsTransLRInvestasi
SELECT count(*) FROM SUBJNSTRANSLRINVESTASI;

-- Number of rows for link LJenisInvestasi in entity SubJnsTransLRInvestasi
SELECT count(*) FROM SUBJNSTRANSLRINVESTASI a, JENISINVESTASI b WHERE 
a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
;

-- Number of rows for entity SubscribeReksadana
SELECT count(*) FROM SUBSCRIBEREKSADANA;

-- Number of rows for link LReksadana in entity SubscribeReksadana
SELECT count(*) FROM SUBSCRIBEREKSADANA a, REKSADANA b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity TitipanPremi
SELECT count(*) FROM TRANSAKSIPREMI WHERE JENIS_TRANSAKSI = 'T';

-- Number of rows for link LRekeningDPLK in entity TitipanPremi
SELECT count(*) FROM TRANSAKSIPREMI a, REKENINGDPLK b WHERE 
JENIS_TRANSAKSI = 'T' AND 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for entity TransactionBatch
SELECT count(*) FROM TRANSACTIONBATCH;

-- Number of rows for link LUserOwner in entity TransactionBatch
SELECT count(*) FROM TRANSACTIONBATCH a, USERAPP b WHERE 
a.USER_ID_OWNER = b.user_id
;

-- Number of rows for entity TransaksiBagiHasil
SELECT count(*) FROM TRANSAKSIBAGIHASIL;

-- Number of rows for link LBagiHasil in entity TransaksiBagiHasil
SELECT count(*) FROM TRANSAKSIBAGIHASIL a, BAGIHASIL b WHERE 
a.IDBGHASIL = b.idbghasil
;

-- Number of rows for entity TransaksiDPLK
SELECT count(*) FROM TRANSAKSIDPLK;

-- Number of rows for link LTransactionBatch in entity TransaksiDPLK
SELECT count(*) FROM TRANSAKSIDPLK a, TRANSACTIONBATCH b WHERE 
a.ID_TRANSACTIONBATCH = b.ID_TRANSACTIONBATCH
;

-- Number of rows for link LRekeningDPLK in entity TransaksiDPLK
SELECT count(*) FROM TRANSAKSIDPLK a, REKENINGDPLK b WHERE 
a.NO_PESERTA = b.no_peserta
;

-- Number of rows for link LJenisTransaksiDPLK in entity TransaksiDPLK
SELECT count(*) FROM TRANSAKSIDPLK a, JENISTRANSAKSIDPLK b WHERE 
a.KODE_JENIS_TRANSAKSI = b.kode_jenis_transaksi
;

-- Number of rows for link LPaketInvestasi in entity TransaksiDPLK
SELECT count(*) FROM TRANSAKSIDPLK a, PAKETINVESTASI b WHERE 
a.KODE_PAKET_INVESTASI = b.kode_paket_investasi
;

-- Number of rows for entity TransaksiDPLKManual
SELECT count(*) FROM TRANSAKSIDPLK WHERE KODE_JENIS_TRANSAKSI = 'M';

-- Number of rows for link LJenisTransaksiManual in entity TransaksiDPLKManual
SELECT count(*) FROM TRANSAKSIDPLK a, JENISTRANSAKSIDPLK b WHERE 
KODE_JENIS_TRANSAKSI = 'M' AND 
a.KODE_TRANSAKSI_MANUAL = b.kode_jenis_transaksi
;

-- Number of rows for entity TransaksiInvestasi
SELECT count(*) FROM TRANSAKSIINVESTASI;

-- Number of rows for link LTransactionBatch in entity TransaksiInvestasi
SELECT count(*) FROM TRANSAKSIINVESTASI a, TRANSACTIONBATCH b WHERE 
a.ID_TRANSACTIONBATCH = b.ID_TRANSACTIONBATCH
;

-- Number of rows for link LNamaJnsTransInv in entity TransaksiInvestasi
SELECT count(*) FROM TRANSAKSIINVESTASI a, NAMAJNSTRANSINV b WHERE 
a.KODE_JNS_INVESTASI = b.KODE_JNS_INVESTASI
AND a.KODE_JENIS_TRINVESTASI = b.KODE_JENIS_TRINVESTASI
;

-- Number of rows for link LInvestasi in entity TransaksiInvestasi
SELECT count(*) FROM TRANSAKSIINVESTASI a, INVESTASI b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for link LIndukTransaksiInvestasi in entity TransaksiInvestasi
SELECT count(*) FROM TRANSAKSIINVESTASI a, TRANSAKSIINVESTASI b WHERE 
a.ID_TRANSAKSIINDUK = b.ID_TRANSAKSIINVESTASI
;

-- Number of additional rows for optional link LIndukTransaksiInvestasi in entity TransaksiInvestasi
SELECT count(*) FROM TransaksiInvestasi WHERE 
(
a.ID_TRANSAKSIINDUK IS NULL
);

-- Number of rows for entity TransaksiPremi
SELECT count(*) FROM TRANSAKSIPREMI;

-- Number of rows for link LTransactionBatch in entity TransaksiPremi
SELECT count(*) FROM TRANSAKSIPREMI a, TRANSACTIONBATCH b WHERE 
a.ID_TRANSACTIONBATCH = b.ID_TRANSACTIONBATCH
;

-- Number of rows for entity TransLRInvestasi
SELECT count(*) FROM TRANSLRINVESTASI;

-- Number of rows for link LSubJnsTransLRInvestasi in entity TransLRInvestasi
SELECT count(*) FROM TRANSLRINVESTASI a, SUBJNSTRANSLRINVESTASI b WHERE 
a.KODE_SUBJNS_LRINVESTASI = b.KODE_SUBJNS_LRINVESTASI
;

-- Number of additional rows for optional link LSubJnsTransLRInvestasi in entity TransLRInvestasi
SELECT count(*) FROM TransLRInvestasi WHERE 
(
a.KODE_SUBJNS_LRINVESTASI IS NULL
);

-- Number of rows for link LAsalTransLRInvestasi in entity TransLRInvestasi
SELECT count(*) FROM TRANSLRINVESTASI a, TRANSLRINVESTASI b WHERE 
a.ID_ASALTRANSLR = b.ID_TRANSAKSIINVESTASI
;

-- Number of additional rows for optional link LAsalTransLRInvestasi in entity TransLRInvestasi
SELECT count(*) FROM TransLRInvestasi WHERE 
(
a.ID_ASALTRANSLR IS NULL
);

-- Number of rows for entity TransPiutangLRInvestasi
SELECT count(*) FROM TRANSPIUTANGLRINVESTASI;

-- Number of rows for link LTransPiutangInvestasi in entity TransPiutangLRInvestasi
SELECT count(*) FROM TRANSPIUTANGLRINVESTASI a, TRANSPIUTANGINVESTASI b WHERE 
a.ID_TRANSAKSIINVESTASI_PIUTINV = b.ID_TRANSAKSIINVESTASI
;

-- Number of additional rows for optional link LTransPiutangInvestasi in entity TransPiutangLRInvestasi
SELECT count(*) FROM TransPiutangLRInvestasi WHERE 
(
a.ID_TRANSAKSIINVESTASI_PIUTINV IS NULL
);

-- Number of rows for link LTransLRInvestasi in entity TransPiutangLRInvestasi
SELECT count(*) FROM TRANSPIUTANGLRINVESTASI a, TRANSLRINVESTASI b WHERE 
a.ID_TRANSAKSIINVESTASI_LRINV = b.ID_TRANSAKSIINVESTASI
;

-- Number of additional rows for optional link LTransLRInvestasi in entity TransPiutangLRInvestasi
SELECT count(*) FROM TransPiutangLRInvestasi WHERE 
(
a.ID_TRANSAKSIINVESTASI_LRINV IS NULL
);

-- Number of rows for entity TutupDeposito
SELECT count(*) FROM TUTUPDEPOSITO;

-- Number of rows for link LDeposito in entity TutupDeposito
SELECT count(*) FROM TUTUPDEPOSITO a, DEPOSITO b WHERE 
a.ID_INVESTASI = b.ID_INVESTASI
;

-- Number of rows for entity UserApp
SELECT count(*) FROM USERAPP;

-- Number of rows for link LBranchLocation in entity UserApp
SELECT count(*) FROM USERAPP a, BRANCHLOCATION b WHERE 
a.branch_code = b.branch_code
;

-- Number of rows for link LSupervisor in entity UserApp
SELECT count(*) FROM USERAPP a, USERAPP b WHERE 
a.USER_ID1 = b.user_id
;

-- Number of additional rows for optional link LSupervisor in entity UserApp
SELECT count(*) FROM UserApp WHERE 
(
a.USER_ID1 IS NULL
);

-- Number of rows for entity UserGroupApp
SELECT count(*) FROM USERGROUPAPP;

-- Number of rows for link LUser in entity UserGroupApp
SELECT count(*) FROM USERGROUPAPP a, USERAPP b WHERE 
a.user_id = b.user_id
;

-- Number of rows for link LUserGroup in entity UserGroupApp
SELECT count(*) FROM USERGROUPAPP a, USERGROUP b WHERE 
a.group_id = b.group_id
;

