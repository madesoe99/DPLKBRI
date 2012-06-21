-- Referential integrity error check for entity AdvisHistory
-- Referential integrity error check for for link LTransaksiDPLK in entity AdvisHistory
SELECT ADVISHISTORY_ID, ID_TRANSAKSI FROM ADVISHISTORY outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI = inner.ID_Transaksi
);

-- Referential integrity error check for entity AhliWaris
-- Referential integrity error check for for link LNasabahDPLK in entity AhliWaris
SELECT AHLIWARIS_ID, NO_PESERTA FROM AHLIWARIS outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity BagiHasil
-- Referential integrity error check for for link LRincianPaketInvestasi in entity BagiHasil
SELECT idbghasil, KODE_PAKET_INVESTASI, KODE_JNS_INVESTASI FROM BAGIHASIL outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANPAKETINVESTASI INNER WHERE
outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
AND outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
);

-- Referential integrity error check for entity BagiHasilDeposito
-- Referential integrity error check for for link LDeposito in entity BagiHasilDeposito
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM BAGIHASILDEPOSITO outer WHERE NOT EXISTS(
SELECT 1 FROM DEPOSITO INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity BagiHasilReksadana
-- Referential integrity error check for for link LReksadana in entity BagiHasilReksadana
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM BAGIHASILREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM REKSADANA INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity BeliObligasi
-- Referential integrity error check for for link LObligasi in entity BeliObligasi
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM BELIOBLIGASI outer WHERE NOT EXISTS(
SELECT 1 FROM OBLIGASI INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity BranchLocation
-- Referential integrity error check for for link LMasterBranch in entity BranchLocation
SELECT branch_code, masterbranch_code FROM BRANCHLOCATION outer WHERE NOT EXISTS(
SELECT 1 FROM BRANCHLOCATION INNER WHERE
outer.masterbranch_code = inner.branch_code
);

-- Referential integrity error check for entity DetailAkumPengembangan
-- Referential integrity error check for for link LRekeningDPLK in entity DetailAkumPengembangan
SELECT KODE_JNS_INVESTASI, KODE_PAKET_INVESTASI, NO_PESERTA, NO_PESERTA FROM DETAILAKUMPENGEMBANGAN outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for for link LRincianPaketInvestasi in entity DetailAkumPengembangan
SELECT KODE_JNS_INVESTASI, KODE_PAKET_INVESTASI, NO_PESERTA, KODE_JNS_INVESTASI, KODE_PAKET_INVESTASI FROM DETAILAKUMPENGEMBANGAN outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANPAKETINVESTASI INNER WHERE
outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
AND outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
);

-- Referential integrity error check for entity HistJenisInvestasi
-- Referential integrity error check for for link LPaketInvestasi in entity HistJenisInvestasi
SELECT no_urut_hist_inv, kode_paket_investasi FROM HISTJENISINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM PAKETINVESTASI INNER WHERE
outer.kode_paket_investasi = inner.kode_paket_investasi
);

-- Referential integrity error check for for link LRekeningDPLK in entity HistJenisInvestasi
SELECT no_urut_hist_inv, no_peserta FROM HISTJENISINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.no_peserta = inner.no_peserta
);

-- Referential integrity error check for entity HistNABReksadana
-- Referential integrity error check for for link LReksadana in entity HistNABReksadana
SELECT HISTNABREKSADANAID, ID_INVESTASI FROM HISTNABREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM REKSADANA INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for for link LTransactionBatch in entity HistNABReksadana
SELECT HISTNABREKSADANAID, ID_TRANSACTIONBATCH FROM HISTNABREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSACTIONBATCH INNER WHERE
outer.ID_TRANSACTIONBATCH = inner.ID_TRANSACTIONBATCH
);

-- Referential integrity error check for entity HistoriAhliWaris
-- Referential integrity error check for for link LNasabahDPLK in entity HistoriAhliWaris
SELECT HISTORIAHLIWARIS_ID, NO_PESERTA FROM HISTORIAHLIWARIS outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity HistoriAhliWarisDetail
-- Referential integrity error check for for link LHistoriAhliWaris in entity HistoriAhliWarisDetail
SELECT HISTORIAWD_ID, HISTORIAHLIWARIS_ID FROM HISTORIAHLIWARISDETAIL outer WHERE NOT EXISTS(
SELECT 1 FROM HISTORIAHLIWARIS INNER WHERE
outer.HISTORIAHLIWARIS_ID = inner.HISTORIAHLIWARIS_ID
);

-- Referential integrity error check for entity HistoriAnuitas
-- Referential integrity error check for for link LRekeningDPLK in entity HistoriAnuitas
SELECT HISTORIANUITAS_ID, NO_PESERTA FROM HISTORIANUITAS outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity HistoriAutoDebet
-- Referential integrity error check for for link LRekeningDPLK in entity HistoriAutoDebet
SELECT HISTORIAUTODEBET_ID, NO_PESERTA FROM HISTORIAUTODEBET outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity HistoriGiro
-- Referential integrity error check for for link LHistoriGiroHarian in entity HistoriGiro
SELECT NOMOR_URUT, ACC_GIRO, ID_HISTORIGIROHARIAN, NOMOR_BATCH_COREBANKING, ID_HISTORIGIROHARIAN FROM HISTORIGIRO outer WHERE NOT EXISTS(
SELECT 1 FROM HISTORIGIROHARIAN INNER WHERE
outer.ID_HISTORIGIROHARIAN = inner.ID_HISTORIGIROHARIAN
);

-- Referential integrity error check for for link LMasterGiro in entity HistoriGiro
SELECT NOMOR_URUT, ACC_GIRO, ID_HISTORIGIROHARIAN, NOMOR_BATCH_COREBANKING, ACC_GIRO FROM HISTORIGIRO outer WHERE NOT EXISTS(
SELECT 1 FROM MASTERGIRO INNER WHERE
outer.ACC_GIRO = inner.ACC_GIRO
);

-- Referential integrity error check for entity HistoriGiroHarian
-- Referential integrity error check for for link LMasterGiro in entity HistoriGiroHarian
SELECT ID_HISTORIGIROHARIAN, ACC_GIRO FROM HISTORIGIROHARIAN outer WHERE NOT EXISTS(
SELECT 1 FROM MASTERGIRO INNER WHERE
outer.ACC_GIRO = inner.ACC_GIRO
);

-- Referential integrity error check for entity HistoriIuran
-- Referential integrity error check for for link LRekeningDPLK in entity HistoriIuran
SELECT HISTORIIURAN_ID, NO_PESERTA FROM HISTORIIURAN outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity HistoriPindahPaketInvestasi
-- Referential integrity error check for for link LPaketInvestasi in entity HistoriPindahPaketInvestasi
SELECT HISTORIPPI_ID, KODE_PAKET_INVESTASI FROM HISTORIPINDAHPAKETINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM PAKETINVESTASI INNER WHERE
outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
);

-- Referential integrity error check for for link LRekeningDPLK in entity HistoriPindahPaketInvestasi
SELECT HISTORIPPI_ID, NO_PESERTA FROM HISTORIPINDAHPAKETINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity HistoriSRR
-- Referential integrity error check for for link LSRRCalcRincian in entity HistoriSRR
SELECT ID_HISTORISRR, ID_SRRCALCRINCIAN FROM HISTORISRR outer WHERE NOT EXISTS(
SELECT 1 FROM SRRCALCRINCIAN INNER WHERE
outer.ID_SRRCALCRINCIAN = inner.ID_SRRCALCRINCIAN
);

-- Referential integrity error check for for link LRekeningDPLK in entity HistoriSRR
SELECT ID_HISTORISRR, NO_PESERTA FROM HISTORISRR outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity HistoriUbahAlamat
-- Referential integrity error check for for link LNasabahDPLK in entity HistoriUbahAlamat
SELECT HISTORIUA_ID, NO_PESERTA FROM HISTORIUBAHALAMAT outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity HistoriUbahStatusKerja
-- Referential integrity error check for for link LNasabahDPLK in entity HistoriUbahStatusKerja
SELECT HISTORIUBAHSTATUSKERJA_ID, NO_PESERTA FROM HISTORIUBAHSTATUSKERJA outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for for link LNasabahDPLKCorporate in entity HistoriUbahStatusKerja
SELECT HISTORIUBAHSTATUSKERJA_ID, KODE_NASABAH_CORPORATE FROM HISTORIUBAHSTATUSKERJA outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLKCORPORATE INNER WHERE
outer.KODE_NASABAH_CORPORATE = inner.KODE_NASABAH_CORPORATE
);

-- Referential integrity error check for entity HistoriWasiatUmmat
-- Referential integrity error check for for link LRekeningDPLK in entity HistoriWasiatUmmat
SELECT HISTORIWU_ID, NO_PESERTA FROM HISTORIWASIATUMMAT outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity HistPerubahanDeposito
-- Referential integrity error check for for link LDeposito in entity HistPerubahanDeposito
SELECT ID_HISTPERUBAHAN, ID_INVESTASI FROM HISTPERUBAHANDEPOSITO outer WHERE NOT EXISTS(
SELECT 1 FROM DEPOSITO INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity Investasi
-- Referential integrity error check for for link LPihakKetiga in entity Investasi
SELECT ID_INVESTASI, KODE_PIHAK_KETIGA FROM INVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM PIHAKKETIGA INNER WHERE
outer.KODE_PIHAK_KETIGA = inner.kode_pihak_ketiga
);

-- Referential integrity error check for for link LRincianPaketInvestasi in entity Investasi
SELECT ID_INVESTASI, KODE_PAKET_INVESTASI, KODE_JNS_INVESTASI FROM INVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANPAKETINVESTASI INNER WHERE
outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
AND outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
);

-- Referential integrity error check for entity IuranPendaftaran
-- Referential integrity error check for for link LRekeningDPLK in entity IuranPendaftaran
SELECT ID_TRANSAKSI, NO_PESERTA FROM IURANPENDAFTARAN outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for for link LTransactionBatch in entity IuranPendaftaran
SELECT ID_TRANSAKSI, ID_TRANSACTIONBATCH FROM IURANPENDAFTARAN outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSACTIONBATCH INNER WHERE
outer.ID_TRANSACTIONBATCH = inner.ID_TRANSACTIONBATCH
);

-- Referential integrity error check for entity IuranPeserta
-- Referential integrity error check for for link LTransactionBatchPremi in entity IuranPeserta
SELECT ID_Transaksi, ID_BATCHPREMI FROM TRANSAKSIDPLK outer WHERE KODE_JENIS_TRANSAKSI = 'K' AND NOT EXISTS(
SELECT 1 FROM TRANSACTIONBATCH INNER WHERE
outer.ID_BATCHPREMI = inner.ID_TRANSACTIONBATCH
);

-- Referential integrity error check for entity JualObligasi
-- Referential integrity error check for for link LObligasi in entity JualObligasi
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM JUALOBLIGASI outer WHERE NOT EXISTS(
SELECT 1 FROM OBLIGASI INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity NamaJnsTransInv
-- Referential integrity error check for for link LJenisInvestasi in entity NamaJnsTransInv
SELECT KODE_JNS_INVESTASI, KODE_JENIS_TRINVESTASI, KODE_JNS_INVESTASI FROM NAMAJNSTRANSINV outer WHERE NOT EXISTS(
SELECT 1 FROM JENISINVESTASI INNER WHERE
outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
);

-- Referential integrity error check for for link LJnsTransInvestasi in entity NamaJnsTransInv
SELECT KODE_JNS_INVESTASI, KODE_JENIS_TRINVESTASI, KODE_JENIS_TRINVESTASI FROM NAMAJNSTRANSINV outer WHERE NOT EXISTS(
SELECT 1 FROM JNSTRANSINVESTASI INNER WHERE
outer.KODE_JENIS_TRINVESTASI = inner.KODE_JENIS_TRINVESTASI
);

-- Referential integrity error check for entity NasabahDPLK
-- Referential integrity error check for for link LDaerahAsal in entity NasabahDPLK
SELECT no_peserta, kode_propinsi FROM NASABAHDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM DAERAHASAL INNER WHERE
outer.kode_propinsi = inner.kode_propinsi
);

-- Referential integrity error check for for link LJenisUsaha in entity NasabahDPLK
SELECT no_peserta, kode_jenis_usaha FROM NASABAHDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM JENISUSAHA INNER WHERE
outer.kode_jenis_usaha = inner.kode_jenis_usaha
);

-- Referential integrity error check for for link LKepemilikan in entity NasabahDPLK
SELECT no_peserta, kode_pemilikan FROM NASABAHDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM KEPEMILIKAN INNER WHERE
outer.kode_pemilikan = inner.kode_pemilikan
);

-- Referential integrity error check for for link LRekeningDPLK in entity NasabahDPLK
SELECT no_peserta, no_peserta FROM NASABAHDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.no_peserta = inner.no_peserta
);

-- Referential integrity error check for for link LNasabahDPLKCorporate in entity NasabahDPLK
SELECT no_peserta, KODE_NASABAH_CORPORATE FROM NASABAHDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLKCORPORATE INNER WHERE
outer.KODE_NASABAH_CORPORATE = inner.KODE_NASABAH_CORPORATE
);

-- Referential integrity error check for for link LOperationCode in entity NasabahDPLK
SELECT no_peserta, OPERATION_CODE FROM NASABAHDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM OPERATIONCODE INNER WHERE
outer.OPERATION_CODE = inner.OPERATION_CODE
);

-- Referential integrity error check for for link LKelompok in entity NasabahDPLK
SELECT no_peserta, KODE_KELOMPOK FROM NASABAHDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM KELOMPOK INNER WHERE
outer.KODE_KELOMPOK = inner.KODE_KELOMPOK
);

-- Referential integrity error check for for link LLDPLain in entity NasabahDPLK
SELECT no_peserta, KODE_DP FROM NASABAHDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM LDP INNER WHERE
outer.KODE_DP = inner.KODE_DP
);

-- Referential integrity error check for entity NasabahDPLKCorporate
-- Referential integrity error check for for link LJenisUsaha in entity NasabahDPLKCorporate
SELECT KODE_NASABAH_CORPORATE, KODE_JENIS_USAHA FROM NASABAHDPLKCORPORATE outer WHERE NOT EXISTS(
SELECT 1 FROM JENISUSAHA INNER WHERE
outer.KODE_JENIS_USAHA = inner.kode_jenis_usaha
);

-- Referential integrity error check for for link LKepemilikan in entity NasabahDPLKCorporate
SELECT KODE_NASABAH_CORPORATE, KODE_PEMILIKAN FROM NASABAHDPLKCORPORATE outer WHERE NOT EXISTS(
SELECT 1 FROM KEPEMILIKAN INNER WHERE
outer.KODE_PEMILIKAN = inner.kode_pemilikan
);

-- Referential integrity error check for for link LOperationCode in entity NasabahDPLKCorporate
SELECT KODE_NASABAH_CORPORATE, OPERATION_CODE FROM NASABAHDPLKCORPORATE outer WHERE NOT EXISTS(
SELECT 1 FROM OPERATIONCODE INNER WHERE
outer.OPERATION_CODE = inner.OPERATION_CODE
);

-- Referential integrity error check for entity Obligasi
-- Referential integrity error check for for link LCustodianBank in entity Obligasi
SELECT ID_INVESTASI, BANKCODE FROM OBLIGASI outer WHERE NOT EXISTS(
SELECT 1 FROM CUSTODIANBANK INNER WHERE
outer.BANKCODE = inner.BANKCODE
);

-- Referential integrity error check for entity PembagianHasilPortofolio
-- Referential integrity error check for for link Lbagi_hasil in entity PembagianHasilPortofolio
SELECT ID_Transaksi, idbghasil FROM TRANSAKSIDPLK outer WHERE KODE_JENIS_TRANSAKSI = 'G' AND NOT EXISTS(
SELECT 1 FROM BAGIHASIL INNER WHERE
outer.idbghasil = inner.idbghasil
);

-- Referential integrity error check for entity PenarikanDana
-- Referential integrity error check for for link LBiayaAdmTransaksi in entity PenarikanDana
SELECT ID_Transaksi, ID_TRANSAKSI_BADMTRANS FROM PENARIKANDANA outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BADMTRANS = inner.ID_TRANSAKSI
);

-- Referential integrity error check for entity PenarikanDanaNormal
-- Referential integrity error check for for link LBiayaAdmTransaksi in entity PenarikanDanaNormal
SELECT ID_TRANSAKSI, ID_TRANSAKSI_BADMTRANS FROM PENARIKANDANA outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BADMTRANS = inner.ID_TRANSAKSI
);

-- Referential integrity error check for entity PenarikanDanaPHK
-- Referential integrity error check for for link LBiayaAdmTransaksi in entity PenarikanDanaPHK
SELECT ID_TRANSAKSI, ID_TRANSAKSI_BADMTRANS FROM PENARIKANDANA outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BADMTRANS = inner.ID_TRANSAKSI
);

-- Referential integrity error check for entity PendapatanObligasi
-- Referential integrity error check for for link LObligasi in entity PendapatanObligasi
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM PENDAPATANOBLIGASI outer WHERE NOT EXISTS(
SELECT 1 FROM OBLIGASI INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity PendapatanReksadana
-- Referential integrity error check for for link LReksadana in entity PendapatanReksadana
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM PENDAPATANREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM REKSADANA INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity PengalihanDariDPLKLain
-- Referential integrity error check for for link LLDP in entity PengalihanDariDPLKLain
SELECT ID_Transaksi, KODE_DP FROM PENGALIHANDARIDPLKLAIN outer WHERE NOT EXISTS(
SELECT 1 FROM LDP INNER WHERE
outer.KODE_DP = inner.KODE_DP
);

-- Referential integrity error check for entity PengalihanKeDPLKLain
-- Referential integrity error check for for link LBiayaAdmTahunan in entity PengalihanKeDPLKLain
SELECT ID_Transaksi, ID_TRANSAKSI_BADMTHN FROM PENGALIHANKEDPLKLAIN outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BADMTHN = inner.ID_Transaksi
);

-- Referential integrity error check for for link LBiayaPengelolaanDana in entity PengalihanKeDPLKLain
SELECT ID_Transaksi, ID_TRANSAKSI_BPENG FROM PENGALIHANKEDPLKLAIN outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BPENG = inner.ID_Transaksi
);

-- Referential integrity error check for for link LBiayaAdmTransaksi in entity PengalihanKeDPLKLain
SELECT ID_Transaksi, ID_TRANSAKSI_BADMTRANS FROM PENGALIHANKEDPLKLAIN outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BADMTRANS = inner.ID_TRANSAKSI
);

-- Referential integrity error check for for link LLDP in entity PengalihanKeDPLKLain
SELECT ID_Transaksi, KODE_DP FROM PENGALIHANKEDPLKLAIN outer WHERE NOT EXISTS(
SELECT 1 FROM LDP INNER WHERE
outer.KODE_DP = inner.KODE_DP
);

-- Referential integrity error check for entity PengambilanManfaat
-- Referential integrity error check for for link Ljenis_penerimaan_manfaat in entity PengambilanManfaat
SELECT ID_Transaksi, kode_jns_manfaat FROM PENGAMBILANMANFAAT outer WHERE NOT EXISTS(
SELECT 1 FROM JENISPENERIMAANMANFAAT INNER WHERE
outer.kode_jns_manfaat = inner.kode_jns_manfaat
);

-- Referential integrity error check for for link LAhliWaris in entity PengambilanManfaat
SELECT ID_Transaksi, AHLIWARIS_ID FROM PENGAMBILANMANFAAT outer WHERE NOT EXISTS(
SELECT 1 FROM AHLIWARIS INNER WHERE
outer.AHLIWARIS_ID = inner.AHLIWARIS_ID
);

-- Referential integrity error check for for link LBiayaAdmTahunan in entity PengambilanManfaat
SELECT ID_Transaksi, ID_TRANSAKSI_BADMTHN FROM PENGAMBILANMANFAAT outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BADMTHN = inner.ID_Transaksi
);

-- Referential integrity error check for for link LBiayaPengelolaanDana in entity PengambilanManfaat
SELECT ID_Transaksi, ID_TRANSAKSI_BPENG FROM PENGAMBILANMANFAAT outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BPENG = inner.ID_Transaksi
);

-- Referential integrity error check for for link LBiayaAdmTransaksi in entity PengambilanManfaat
SELECT ID_Transaksi, ID_TRANSAKSI_BADMTRANS FROM PENGAMBILANMANFAAT outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_BADMTRANS = inner.ID_TRANSAKSI
);

-- Referential integrity error check for entity RealisasiReturn
-- Referential integrity error check for for link LReksadana in entity RealisasiReturn
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM REALISASIRETURN outer WHERE NOT EXISTS(
SELECT 1 FROM REKSADANA INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity RedemptReksadana
-- Referential integrity error check for for link LKlaimLRReksadana in entity RedemptReksadana
SELECT ID_TRANSAKSIINVESTASI, ID_TRANSAKSIINVESTASI_KLAIM FROM REDEMPTREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM KLAIMLRREKSADANA INNER WHERE
outer.ID_TRANSAKSIINVESTASI_KLAIM = inner.ID_TRANSAKSIINVESTASI
);

-- Referential integrity error check for for link LReksadana in entity RedemptReksadana
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM REDEMPTREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM REKSADANA INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity RegEditNasabahDPLKCorporate
-- Referential integrity error check for for link LKepemilikan in entity RegEditNasabahDPLKCorporate
SELECT REGEDITNDPLKCORP_ID, KODE_PEMILIKAN FROM REGEDITNASABAHDPLKCORPORATE outer WHERE NOT EXISTS(
SELECT 1 FROM KEPEMILIKAN INNER WHERE
outer.KODE_PEMILIKAN = inner.kode_pemilikan
);

-- Referential integrity error check for for link LJenisUsaha in entity RegEditNasabahDPLKCorporate
SELECT REGEDITNDPLKCORP_ID, KODE_JENIS_USAHA FROM REGEDITNASABAHDPLKCORPORATE outer WHERE NOT EXISTS(
SELECT 1 FROM JENISUSAHA INNER WHERE
outer.KODE_JENIS_USAHA = inner.kode_jenis_usaha
);

-- Referential integrity error check for for link LNasabahDPLKCorporate in entity RegEditNasabahDPLKCorporate
SELECT REGEDITNDPLKCORP_ID, KODE_NASABAH_CORPORATE FROM REGEDITNASABAHDPLKCORPORATE outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLKCORPORATE INNER WHERE
outer.KODE_NASABAH_CORPORATE = inner.KODE_NASABAH_CORPORATE
);

-- Referential integrity error check for for link LOperationCode in entity RegEditNasabahDPLKCorporate
SELECT REGEDITNDPLKCORP_ID, OPERATION_CODE FROM REGEDITNASABAHDPLKCORPORATE outer WHERE NOT EXISTS(
SELECT 1 FROM OPERATIONCODE INNER WHERE
outer.OPERATION_CODE = inner.OPERATION_CODE
);

-- Referential integrity error check for for link LNasabahDPLKHolding in entity RegEditNasabahDPLKCorporate
SELECT REGEDITNDPLKCORP_ID, KODE_HOLDING FROM REGEDITNASABAHDPLKCORPORATE outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLKCORPORATE INNER WHERE
outer.KODE_HOLDING = inner.KODE_NASABAH_CORPORATE
);

-- Referential integrity error check for entity RegEditNasabahRekening
-- Referential integrity error check for for link LJenisUsaha in entity RegEditNasabahRekening
SELECT REGISTERCIF_ID, KODE_JENIS_USAHA FROM REGEDITNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM JENISUSAHA INNER WHERE
outer.KODE_JENIS_USAHA = inner.kode_jenis_usaha
);

-- Referential integrity error check for for link LKepemilikan in entity RegEditNasabahRekening
SELECT REGISTERCIF_ID, KODE_PEMILIKAN FROM REGEDITNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM KEPEMILIKAN INNER WHERE
outer.KODE_PEMILIKAN = inner.kode_pemilikan
);

-- Referential integrity error check for for link LDaerahAsal in entity RegEditNasabahRekening
SELECT REGISTERCIF_ID, KODE_PROPINSI FROM REGEDITNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM DAERAHASAL INNER WHERE
outer.KODE_PROPINSI = inner.kode_propinsi
);

-- Referential integrity error check for for link LSumberDana in entity RegEditNasabahRekening
SELECT REGISTERCIF_ID, SUMBER_DANA FROM REGEDITNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM SUMBERDANA INNER WHERE
outer.SUMBER_DANA = inner.SUMBER_DANA
);

-- Referential integrity error check for for link LKelompok in entity RegEditNasabahRekening
SELECT REGISTERCIF_ID, KODE_KELOMPOK FROM REGEDITNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM KELOMPOK INNER WHERE
outer.KODE_KELOMPOK = inner.KODE_KELOMPOK
);

-- Referential integrity error check for entity RegisterAhliWarisDetail
-- Referential integrity error check for for link LRegisterAhliWaris in entity RegisterAhliWarisDetail
SELECT REGISTERAWD_ID, REGISTERCIF_ID FROM REGISTERAHLIWARISDETAIL outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERAHLIWARIS INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
);

-- Referential integrity error check for entity RegisterCIF
-- Referential integrity error check for for link LNasabahDPLK in entity RegisterCIF
SELECT REGISTERCIF_ID, NO_PESERTA FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for for link LJenisRegisterCIF in entity RegisterCIF
SELECT REGISTERCIF_ID, KODE_JENIS_REGISTERCIF FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM JENISREGISTERCIF INNER WHERE
outer.KODE_JENIS_REGISTERCIF = inner.KODE_JENIS_REGISTERCIF
);

-- Referential integrity error check for for link LUserApp in entity RegisterCIF
SELECT REGISTERCIF_ID, USER_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM USERAPP INNER WHERE
outer.USER_ID = inner.user_id
);

-- Referential integrity error check for entity RegisterDeposito
-- Referential integrity error check for for link LMasterGiro in entity RegisterDeposito
SELECT ID_REGISTERINVESTASI, ACC_GIRO FROM REGISTERDEPOSITO outer WHERE NOT EXISTS(
SELECT 1 FROM MASTERGIRO INNER WHERE
outer.ACC_GIRO = inner.ACC_GIRO
);

-- Referential integrity error check for entity RegisterInvestasi
-- Referential integrity error check for for link LPihakKetiga in entity RegisterInvestasi
SELECT ID_REGISTERINVESTASI, KODE_PIHAK_KETIGA FROM REGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM PIHAKKETIGA INNER WHERE
outer.KODE_PIHAK_KETIGA = inner.kode_pihak_ketiga
);

-- Referential integrity error check for for link LRincianPaketInvestasi in entity RegisterInvestasi
SELECT ID_REGISTERINVESTASI, KODE_JNS_INVESTASI, KODE_PAKET_INVESTASI FROM REGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANPAKETINVESTASI INNER WHERE
outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
AND outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
);

-- Referential integrity error check for for link LTransactionBatch in entity RegisterInvestasi
SELECT ID_REGISTERINVESTASI, ID_TRANSACTIONBATCH FROM REGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSACTIONBATCH INNER WHERE
outer.ID_TRANSACTIONBATCH = inner.ID_TRANSACTIONBATCH
);

-- Referential integrity error check for entity RegisterIuran
-- Referential integrity error check for for link LRekeningDPLK in entity RegisterIuran
SELECT REGISTERCIF_ID, NO_PESERTA FROM REGISTERIURAN outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity RegisterNasabahRekening
-- Referential integrity error check for for link LDaerahAsal in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, KODE_PROPINSI FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM DAERAHASAL INNER WHERE
outer.KODE_PROPINSI = inner.kode_propinsi
);

-- Referential integrity error check for for link LKepemilikan in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, KODE_PEMILIKAN FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM KEPEMILIKAN INNER WHERE
outer.KODE_PEMILIKAN = inner.kode_pemilikan
);

-- Referential integrity error check for for link LJenisUsaha in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, KODE_JENIS_USAHA FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM JENISUSAHA INNER WHERE
outer.KODE_JENIS_USAHA = inner.kode_jenis_usaha
);

-- Referential integrity error check for for link LNasabahDPLKCorporate in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, KODE_NASABAH_CORPORATE FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLKCORPORATE INNER WHERE
outer.KODE_NASABAH_CORPORATE = inner.KODE_NASABAH_CORPORATE
);

-- Referential integrity error check for for link LPaketInvestasi in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, KODE_PAKET_INVESTASI FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM PAKETINVESTASI INNER WHERE
outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
);

-- Referential integrity error check for for link LSumberDana in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, sumber_dana FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM SUMBERDANA INNER WHERE
outer.sumber_dana = inner.SUMBER_DANA
);

-- Referential integrity error check for for link LKelompok in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, KODE_KELOMPOK FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM KELOMPOK INNER WHERE
outer.KODE_KELOMPOK = inner.KODE_KELOMPOK
);

-- Referential integrity error check for for link LRegisterIuranPeserta in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, ID_TRANSAKSI_IURANPESERTA FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_TRANSAKSI_IURANPESERTA = inner.ID_Transaksi
);

-- Referential integrity error check for for link LRegisterIuranPendaftaran in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, ID_TRANSAKSI_IURANPENDAFTARAN FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM IURANPENDAFTARAN INNER WHERE
outer.ID_TRANSAKSI_IURANPENDAFTARAN = inner.ID_TRANSAKSI
);

-- Referential integrity error check for for link LLDPLain in entity RegisterNasabahRekening
SELECT REGISTERNR_ID, KODE_DP FROM REGISTERNASABAHREKENING outer WHERE NOT EXISTS(
SELECT 1 FROM LDP INNER WHERE
outer.KODE_DP = inner.KODE_DP
);

-- Referential integrity error check for entity RegisterObligasi
-- Referential integrity error check for for link LCustodianBank in entity RegisterObligasi
SELECT ID_REGISTERINVESTASI, BANKCODE FROM REGISTEROBLIGASI outer WHERE NOT EXISTS(
SELECT 1 FROM CUSTODIANBANK INNER WHERE
outer.BANKCODE = inner.BANKCODE
);

-- Referential integrity error check for entity RegisterPindahPaketInvestasi
-- Referential integrity error check for for link LPaketInvestasi in entity RegisterPindahPaketInvestasi
SELECT REGISTERCIF_ID, KODE_PAKET_INVESTASI FROM REGISTERPINDAHPAKETINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM PAKETINVESTASI INNER WHERE
outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
);

-- Referential integrity error check for for link LTransactionBatch in entity RegisterPindahPaketInvestasi
SELECT REGISTERCIF_ID, ID_TRANSACTIONBATCH FROM REGISTERPINDAHPAKETINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSACTIONBATCH INNER WHERE
outer.ID_TRANSACTIONBATCH = inner.ID_TRANSACTIONBATCH
);

-- Referential integrity error check for entity RegisterReksadana
-- Referential integrity error check for for link LCustodianBank in entity RegisterReksadana
SELECT ID_REGISTERINVESTASI, BANKCODE FROM REGISTERREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM CUSTODIANBANK INNER WHERE
outer.BANKCODE = inner.BANKCODE
);

-- Referential integrity error check for for link LJenisReksadana in entity RegisterReksadana
SELECT ID_REGISTERINVESTASI, KODE_JNS_REKSADANA FROM REGISTERREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM JENISREKSADANA INNER WHERE
outer.KODE_JNS_REKSADANA = inner.KODE_JNS_REKSADANA
);

-- Referential integrity error check for entity RegisterUbahStatusKerja
-- Referential integrity error check for for link LNasabahDPLKCorporate in entity RegisterUbahStatusKerja
SELECT REGISTERCIF_ID, KODE_NASABAH_CORPORATE FROM REGISTERUBAHSTATUSKERJA outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLKCORPORATE INNER WHERE
outer.KODE_NASABAH_CORPORATE = inner.KODE_NASABAH_CORPORATE
);

-- Referential integrity error check for entity RegNRAhliWaris
-- Referential integrity error check for for link LRegisterNasabahRekening in entity RegNRAhliWaris
SELECT REGNRAHLIWARIS_ID, REGISTERNR_ID FROM REGNRAHLIWARIS outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERNASABAHREKENING INNER WHERE
outer.REGISTERNR_ID = inner.REGISTERNR_ID
);

-- Referential integrity error check for entity RekeningAnuitas
-- Referential integrity error check for for link LRekeningDPLK in entity RekeningAnuitas
SELECT NO_REKENING, NO_PESERTA FROM REKENINGANUITAS outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity RekeningAutoDebet
-- Referential integrity error check for for link LRekeningDPLK in entity RekeningAutoDebet
SELECT NO_REKENING, NO_PESERTA, NO_PESERTA FROM REKENINGAUTODEBET outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity RekeningDPLK
-- Referential integrity error check for for link LNasabahDPLK in entity RekeningDPLK
SELECT no_peserta, no_peserta FROM REKENINGDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM NASABAHDPLK INNER WHERE
outer.no_peserta = inner.no_peserta
);

-- Referential integrity error check for for link LPaketInvestasi in entity RekeningDPLK
SELECT no_peserta, kode_paket_investasi FROM REKENINGDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PAKETINVESTASI INNER WHERE
outer.kode_paket_investasi = inner.kode_paket_investasi
);

-- Referential integrity error check for for link LBranchLocation in entity RekeningDPLK
SELECT no_peserta, kode_cab_daftar FROM REKENINGDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM BRANCHLOCATION INNER WHERE
outer.kode_cab_daftar = inner.branch_code
);

-- Referential integrity error check for for link LOperationCode in entity RekeningDPLK
SELECT no_peserta, OPERATION_CODE FROM REKENINGDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM OPERATIONCODE INNER WHERE
outer.OPERATION_CODE = inner.OPERATION_CODE
);

-- Referential integrity error check for for link LSumberDana in entity RekeningDPLK
SELECT no_peserta, sumber_dana FROM REKENINGDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM SUMBERDANA INNER WHERE
outer.sumber_dana = inner.SUMBER_DANA
);

-- Referential integrity error check for entity RekeningWasiatUmmat
-- Referential integrity error check for for link LRekeningDPLK in entity RekeningWasiatUmmat
SELECT REKENINGWASIATUMMAT_ID, NO_PESERTA FROM REKENINGWASIATUMMAT outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity Reksadana
-- Referential integrity error check for for link LCustodianBank in entity Reksadana
SELECT ID_INVESTASI, BANKCODE FROM REKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM CUSTODIANBANK INNER WHERE
outer.BANKCODE = inner.BANKCODE
);

-- Referential integrity error check for for link LJenisReksadana in entity Reksadana
SELECT ID_INVESTASI, KODE_JNS_REKSADANA FROM REKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM JENISREKSADANA INNER WHERE
outer.KODE_JNS_REKSADANA = inner.KODE_JNS_REKSADANA
);

-- Referential integrity error check for entity RincianDeposito
-- Referential integrity error check for for link LDeposito in entity RincianDeposito
SELECT ID_RINCIANINVESTASI, ID_INVESTASI FROM RINCIANINVESTASI outer WHERE KODE_JNS_INVESTASI = 'D' AND NOT EXISTS(
SELECT 1 FROM DEPOSITO INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity RincianInvestasi
-- Referential integrity error check for for link LInvestasi in entity RincianInvestasi
SELECT ID_RINCIANINVESTASI, ID_INVESTASI FROM RINCIANINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM INVESTASI INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for for link LRincianPaketInvestasi in entity RincianInvestasi
SELECT ID_RINCIANINVESTASI, KODE_JNS_INVESTASI, KODE_PAKET_INVESTASI FROM RINCIANINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANPAKETINVESTASI INNER WHERE
outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
AND outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
);

-- Referential integrity error check for entity RincianObligasi
-- Referential integrity error check for for link LObligasi in entity RincianObligasi
SELECT ID_RINCIANINVESTASI, ID_INVESTASI FROM RINCIANINVESTASI outer WHERE KODE_JNS_INVESTASI = 'O' AND NOT EXISTS(
SELECT 1 FROM OBLIGASI INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity RincianPaketInvestasi
-- Referential integrity error check for for link LPaketInvestasi in entity RincianPaketInvestasi
SELECT kode_paket_investasi, KODE_JNS_INVESTASI, kode_paket_investasi FROM RINCIANPAKETINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM PAKETINVESTASI INNER WHERE
outer.kode_paket_investasi = inner.kode_paket_investasi
);

-- Referential integrity error check for for link LJenisInvestasi in entity RincianPaketInvestasi
SELECT kode_paket_investasi, KODE_JNS_INVESTASI, KODE_JNS_INVESTASI FROM RINCIANPAKETINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM JENISINVESTASI INNER WHERE
outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
);

-- Referential integrity error check for entity RincianPihakKetiga
-- Referential integrity error check for for link LPihakKetiga in entity RincianPihakKetiga
SELECT KODE_PIHAK_KETIGA, KODE_JNS_INVESTASI, KODE_PIHAK_KETIGA FROM RINCIANPIHAKKETIGA outer WHERE NOT EXISTS(
SELECT 1 FROM PIHAKKETIGA INNER WHERE
outer.KODE_PIHAK_KETIGA = inner.kode_pihak_ketiga
);

-- Referential integrity error check for for link LJenisInvestasi in entity RincianPihakKetiga
SELECT KODE_PIHAK_KETIGA, KODE_JNS_INVESTASI, KODE_JNS_INVESTASI FROM RINCIANPIHAKKETIGA outer WHERE NOT EXISTS(
SELECT 1 FROM JENISINVESTASI INNER WHERE
outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
);

-- Referential integrity error check for entity RincianRegisterDeposito
-- Referential integrity error check for for link LRegisterDeposito in entity RincianRegisterDeposito
SELECT ID_RINCIANREGISTERINV, ID_REGISTERINVESTASI FROM RINCIANREGISTERINVESTASI outer WHERE KODE_JNS_INVESTASI = 'A' AND NOT EXISTS(
SELECT 1 FROM REGISTERDEPOSITO INNER WHERE
outer.ID_REGISTERINVESTASI = inner.ID_REGISTERINVESTASI
);

-- Referential integrity error check for entity RincianRegisterInvestasi
-- Referential integrity error check for for link LRegisterInvestasi in entity RincianRegisterInvestasi
SELECT ID_RINCIANREGISTERINV, ID_REGISTERINVESTASI FROM RINCIANREGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERINVESTASI INNER WHERE
outer.ID_REGISTERINVESTASI = inner.ID_REGISTERINVESTASI
);

-- Referential integrity error check for for link LRincianPaketInvestasi in entity RincianRegisterInvestasi
SELECT ID_RINCIANREGISTERINV, KODE_PAKET_INVESTASI, KODE_JNS_INVESTASI FROM RINCIANREGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANPAKETINVESTASI INNER WHERE
outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
AND outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
);

-- Referential integrity error check for entity RincianRegisterObligasi
-- Referential integrity error check for for link LRegisterObligasi in entity RincianRegisterObligasi
SELECT ID_RINCIANREGISTERINV, ID_REGISTERINVESTASI FROM RINCIANREGISTERINVESTASI outer WHERE KODE_JNS_INVESTASI = 'B' AND NOT EXISTS(
SELECT 1 FROM REGISTEROBLIGASI INNER WHERE
outer.ID_REGISTERINVESTASI = inner.ID_REGISTERINVESTASI
);

-- Referential integrity error check for entity RincianRegisterReksadana
-- Referential integrity error check for for link LRegisterReksadana in entity RincianRegisterReksadana
SELECT ID_RINCIANREGISTERINV, ID_REGISTERINVESTASI FROM RINCIANREGISTERINVESTASI outer WHERE KODE_JNS_INVESTASI = 'C' AND NOT EXISTS(
SELECT 1 FROM REGISTERREKSADANA INNER WHERE
outer.ID_REGISTERINVESTASI = inner.ID_REGISTERINVESTASI
);

-- Referential integrity error check for entity RincianReksadana
-- Referential integrity error check for for link LReksadana in entity RincianReksadana
SELECT ID_RINCIANINVESTASI, ID_INVESTASI FROM RINCIANINVESTASI outer WHERE KODE_JNS_INVESTASI = 'R' AND NOT EXISTS(
SELECT 1 FROM REKSADANA INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity RolloverDeposito
-- Referential integrity error check for for link LDeposito in entity RolloverDeposito
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM ROLLOVERDEPOSITO outer WHERE NOT EXISTS(
SELECT 1 FROM DEPOSITO INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity SessionBLOB
-- Referential integrity error check for for link LBLOBData in entity SessionBLOB
SELECT ID, ID1 FROM SESSIONBLOB outer WHERE NOT EXISTS(
SELECT 1 FROM BLOBREGISTRATION INNER WHERE
outer.ID1 = inner.ID
);

-- Referential integrity error check for entity SRRCalc
-- Referential integrity error check for for link LUserCreate in entity SRRCalc
SELECT ID_SRRCALC, USER_ID_CREATE FROM SRRCALC outer WHERE NOT EXISTS(
SELECT 1 FROM USERAPP INNER WHERE
outer.USER_ID_CREATE = inner.user_id
);

-- Referential integrity error check for entity SRRCalcBagiHasil
-- Referential integrity error check for for link LBagiHasil in entity SRRCalcBagiHasil
SELECT ID_SRRCALCBAGIHASIL, IDBGHASIL FROM SRRCALCBAGIHASIL outer WHERE NOT EXISTS(
SELECT 1 FROM BAGIHASIL INNER WHERE
outer.IDBGHASIL = inner.idbghasil
);

-- Referential integrity error check for for link LSRRCalcRincian in entity SRRCalcBagiHasil
SELECT ID_SRRCALCBAGIHASIL, ID_SRRCALCRINCIAN FROM SRRCALCBAGIHASIL outer WHERE NOT EXISTS(
SELECT 1 FROM SRRCALCRINCIAN INNER WHERE
outer.ID_SRRCALCRINCIAN = inner.ID_SRRCALCRINCIAN
);

-- Referential integrity error check for entity SRRCalcRincian
-- Referential integrity error check for for link LPaketInvestasi in entity SRRCalcRincian
SELECT ID_SRRCALCRINCIAN, KODE_PAKET_INVESTASI FROM SRRCALCRINCIAN outer WHERE NOT EXISTS(
SELECT 1 FROM PAKETINVESTASI INNER WHERE
outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
);

-- Referential integrity error check for for link LSRRCalc in entity SRRCalcRincian
SELECT ID_SRRCALCRINCIAN, ID_SRRCALC FROM SRRCALCRINCIAN outer WHERE NOT EXISTS(
SELECT 1 FROM SRRCALC INNER WHERE
outer.ID_SRRCALC = inner.ID_SRRCALC
);

-- Referential integrity error check for entity SubJnsTransLRInvestasi
-- Referential integrity error check for for link LJenisInvestasi in entity SubJnsTransLRInvestasi
SELECT KODE_SUBJNS_LRINVESTASI, KODE_JNS_INVESTASI FROM SUBJNSTRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM JENISINVESTASI INNER WHERE
outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
);

-- Referential integrity error check for entity SubscribeReksadana
-- Referential integrity error check for for link LReksadana in entity SubscribeReksadana
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM SUBSCRIBEREKSADANA outer WHERE NOT EXISTS(
SELECT 1 FROM REKSADANA INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity TitipanPremi
-- Referential integrity error check for for link LRekeningDPLK in entity TitipanPremi
SELECT ID_TRANSAKSI, NO_PESERTA FROM TRANSAKSIPREMI outer WHERE JENIS_TRANSAKSI = 'T' AND NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for entity TransactionBatch
-- Referential integrity error check for for link LUserOwner in entity TransactionBatch
SELECT ID_TRANSACTIONBATCH, USER_ID_OWNER FROM TRANSACTIONBATCH outer WHERE NOT EXISTS(
SELECT 1 FROM USERAPP INNER WHERE
outer.USER_ID_OWNER = inner.user_id
);

-- Referential integrity error check for entity TransaksiBagiHasil
-- Referential integrity error check for for link LBagiHasil in entity TransaksiBagiHasil
SELECT ID_TRANSAKSI, IDBGHASIL FROM TRANSAKSIBAGIHASIL outer WHERE NOT EXISTS(
SELECT 1 FROM BAGIHASIL INNER WHERE
outer.IDBGHASIL = inner.idbghasil
);

-- Referential integrity error check for entity TransaksiDPLK
-- Referential integrity error check for for link LTransactionBatch in entity TransaksiDPLK
SELECT ID_Transaksi, ID_TRANSACTIONBATCH FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSACTIONBATCH INNER WHERE
outer.ID_TRANSACTIONBATCH = inner.ID_TRANSACTIONBATCH
);

-- Referential integrity error check for for link LRekeningDPLK in entity TransaksiDPLK
SELECT ID_Transaksi, NO_PESERTA FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM REKENINGDPLK INNER WHERE
outer.NO_PESERTA = inner.no_peserta
);

-- Referential integrity error check for for link LJenisTransaksiDPLK in entity TransaksiDPLK
SELECT ID_Transaksi, KODE_JENIS_TRANSAKSI FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM JENISTRANSAKSIDPLK INNER WHERE
outer.KODE_JENIS_TRANSAKSI = inner.kode_jenis_transaksi
);

-- Referential integrity error check for for link LPaketInvestasi in entity TransaksiDPLK
SELECT ID_Transaksi, KODE_PAKET_INVESTASI FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PAKETINVESTASI INNER WHERE
outer.KODE_PAKET_INVESTASI = inner.kode_paket_investasi
);

-- Referential integrity error check for entity TransaksiDPLKManual
-- Referential integrity error check for for link LJenisTransaksiManual in entity TransaksiDPLKManual
SELECT ID_TRANSAKSI, KODE_TRANSAKSI_MANUAL FROM TRANSAKSIDPLK outer WHERE KODE_JENIS_TRANSAKSI = 'M' AND NOT EXISTS(
SELECT 1 FROM JENISTRANSAKSIDPLK INNER WHERE
outer.KODE_TRANSAKSI_MANUAL = inner.kode_jenis_transaksi
);

-- Referential integrity error check for entity TransaksiInvestasi
-- Referential integrity error check for for link LTransactionBatch in entity TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI, ID_TRANSACTIONBATCH FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSACTIONBATCH INNER WHERE
outer.ID_TRANSACTIONBATCH = inner.ID_TRANSACTIONBATCH
);

-- Referential integrity error check for for link LNamaJnsTransInv in entity TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI, KODE_JNS_INVESTASI, KODE_JENIS_TRINVESTASI FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM NAMAJNSTRANSINV INNER WHERE
outer.KODE_JNS_INVESTASI = inner.KODE_JNS_INVESTASI
AND outer.KODE_JENIS_TRINVESTASI = inner.KODE_JENIS_TRINVESTASI
);

-- Referential integrity error check for for link LInvestasi in entity TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM INVESTASI INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for for link LIndukTransaksiInvestasi in entity TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI, ID_TRANSAKSIINDUK FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIINVESTASI INNER WHERE
outer.ID_TRANSAKSIINDUK = inner.ID_TRANSAKSIINVESTASI
);

-- Referential integrity error check for entity TransaksiPremi
-- Referential integrity error check for for link LTransactionBatch in entity TransaksiPremi
SELECT ID_TRANSAKSI, ID_TRANSACTIONBATCH FROM TRANSAKSIPREMI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSACTIONBATCH INNER WHERE
outer.ID_TRANSACTIONBATCH = inner.ID_TRANSACTIONBATCH
);

-- Referential integrity error check for entity TransLRInvestasi
-- Referential integrity error check for for link LSubJnsTransLRInvestasi in entity TransLRInvestasi
SELECT ID_TRANSAKSIINVESTASI, KODE_SUBJNS_LRINVESTASI FROM TRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM SUBJNSTRANSLRINVESTASI INNER WHERE
outer.KODE_SUBJNS_LRINVESTASI = inner.KODE_SUBJNS_LRINVESTASI
);

-- Referential integrity error check for for link LAsalTransLRInvestasi in entity TransLRInvestasi
SELECT ID_TRANSAKSIINVESTASI, ID_ASALTRANSLR FROM TRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSLRINVESTASI INNER WHERE
outer.ID_ASALTRANSLR = inner.ID_TRANSAKSIINVESTASI
);

-- Referential integrity error check for entity TransPiutangLRInvestasi
-- Referential integrity error check for for link LTransPiutangInvestasi in entity TransPiutangLRInvestasi
SELECT ID_TRANSAKSIINVESTASI, ID_TRANSAKSIINVESTASI_PIUTINV FROM TRANSPIUTANGLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSPIUTANGINVESTASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI_PIUTINV = inner.ID_TRANSAKSIINVESTASI
);

-- Referential integrity error check for for link LTransLRInvestasi in entity TransPiutangLRInvestasi
SELECT ID_TRANSAKSIINVESTASI, ID_TRANSAKSIINVESTASI_LRINV FROM TRANSPIUTANGLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSLRINVESTASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI_LRINV = inner.ID_TRANSAKSIINVESTASI
);

-- Referential integrity error check for entity TutupDeposito
-- Referential integrity error check for for link LDeposito in entity TutupDeposito
SELECT ID_TRANSAKSIINVESTASI, ID_INVESTASI FROM TUTUPDEPOSITO outer WHERE NOT EXISTS(
SELECT 1 FROM DEPOSITO INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
);

-- Referential integrity error check for entity UserApp
-- Referential integrity error check for for link LBranchLocation in entity UserApp
SELECT user_id, branch_code FROM USERAPP outer WHERE NOT EXISTS(
SELECT 1 FROM BRANCHLOCATION INNER WHERE
outer.branch_code = inner.branch_code
);

-- Referential integrity error check for for link LSupervisor in entity UserApp
SELECT user_id, USER_ID1 FROM USERAPP outer WHERE NOT EXISTS(
SELECT 1 FROM USERAPP INNER WHERE
outer.USER_ID1 = inner.user_id
);

-- Referential integrity error check for entity UserGroupApp
-- Referential integrity error check for for link LUser in entity UserGroupApp
SELECT user_id, group_id, user_id FROM USERGROUPAPP outer WHERE NOT EXISTS(
SELECT 1 FROM USERAPP INNER WHERE
outer.user_id = inner.user_id
);

-- Referential integrity error check for for link LUserGroup in entity UserGroupApp
SELECT user_id, group_id, group_id FROM USERGROUPAPP outer WHERE NOT EXISTS(
SELECT 1 FROM USERGROUP INNER WHERE
outer.group_id = inner.group_id
);

