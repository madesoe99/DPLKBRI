-- Referential index for link LTransaksiDPLK in entity AdvisHistory
CREATE INDEX idx_0_0 ON ADVISHISTORY(ID_TRANSAKSI);

-- Referential index for link LNasabahDPLK in entity AhliWaris
CREATE INDEX idx_1_0 ON AHLIWARIS(NO_PESERTA);

-- Referential index for link LRincianPaketInvestasi in entity BagiHasil
CREATE INDEX idx_2_0 ON BAGIHASIL(KODE_PAKET_INVESTASI, KODE_JNS_INVESTASI);

-- Referential index for link LDeposito in entity BagiHasilDeposito
CREATE INDEX idx_3_0 ON BAGIHASILDEPOSITO(ID_INVESTASI);

-- Referential index for link LReksadana in entity BagiHasilReksadana
CREATE INDEX idx_4_0 ON BAGIHASILREKSADANA(ID_INVESTASI);

-- Referential index for link LObligasi in entity BeliObligasi
CREATE INDEX idx_6_0 ON BELIOBLIGASI(ID_INVESTASI);

-- Referential index for link LMasterBranch in entity BranchLocation
CREATE INDEX idx_11_0 ON BRANCHLOCATION(masterbranch_code);

-- Referential index for link LRekeningDPLK in entity DetailAkumPengembangan
CREATE INDEX idx_17_0 ON DETAILAKUMPENGEMBANGAN(NO_PESERTA);

-- Referential index for link LRincianPaketInvestasi in entity DetailAkumPengembangan
CREATE INDEX idx_17_1 ON DETAILAKUMPENGEMBANGAN(KODE_JNS_INVESTASI, KODE_PAKET_INVESTASI);

-- Referential index for link LPaketInvestasi in entity HistJenisInvestasi
CREATE INDEX idx_22_0 ON HISTJENISINVESTASI(kode_paket_investasi);

-- Referential index for link LRekeningDPLK in entity HistJenisInvestasi
CREATE INDEX idx_22_1 ON HISTJENISINVESTASI(no_peserta);

-- Referential index for link LReksadana in entity HistNABReksadana
CREATE INDEX idx_23_0 ON HISTNABREKSADANA(ID_INVESTASI);

-- Referential index for link LTransactionBatch in entity HistNABReksadana
CREATE INDEX idx_23_1 ON HISTNABREKSADANA(ID_TRANSACTIONBATCH);

-- Referential index for link LNasabahDPLK in entity HistoriAhliWaris
CREATE INDEX idx_24_0 ON HISTORIAHLIWARIS(NO_PESERTA);

-- Referential index for link LHistoriAhliWaris in entity HistoriAhliWarisDetail
CREATE INDEX idx_25_0 ON HISTORIAHLIWARISDETAIL(HISTORIAHLIWARIS_ID);

-- Referential index for link LRekeningDPLK in entity HistoriAnuitas
CREATE INDEX idx_26_0 ON HISTORIANUITAS(NO_PESERTA);

-- Referential index for link LRekeningDPLK in entity HistoriAutoDebet
CREATE INDEX idx_27_0 ON HISTORIAUTODEBET(NO_PESERTA);

-- Referential index for link LHistoriGiroHarian in entity HistoriGiro
CREATE INDEX idx_28_0 ON HISTORIGIRO(ID_HISTORIGIROHARIAN);

-- Referential index for link LMasterGiro in entity HistoriGiro
CREATE INDEX idx_28_1 ON HISTORIGIRO(ACC_GIRO);

-- Referential index for link LMasterGiro in entity HistoriGiroHarian
CREATE INDEX idx_29_0 ON HISTORIGIROHARIAN(ACC_GIRO);

-- Referential index for link LRekeningDPLK in entity HistoriIuran
CREATE INDEX idx_30_0 ON HISTORIIURAN(NO_PESERTA);

-- Referential index for link LPaketInvestasi in entity HistoriPindahPaketInvestasi
CREATE INDEX idx_32_0 ON HISTORIPINDAHPAKETINVESTASI(KODE_PAKET_INVESTASI);

-- Referential index for link LRekeningDPLK in entity HistoriPindahPaketInvestasi
CREATE INDEX idx_32_1 ON HISTORIPINDAHPAKETINVESTASI(NO_PESERTA);

-- Referential index for link LSRRCalcRincian in entity HistoriSRR
CREATE INDEX idx_33_0 ON HISTORISRR(ID_SRRCALCRINCIAN);

-- Referential index for link LRekeningDPLK in entity HistoriSRR
CREATE INDEX idx_33_1 ON HISTORISRR(NO_PESERTA);

-- Referential index for link LNasabahDPLK in entity HistoriUbahAlamat
CREATE INDEX idx_34_0 ON HISTORIUBAHALAMAT(NO_PESERTA);

-- Referential index for link LNasabahDPLK in entity HistoriUbahStatusKerja
CREATE INDEX idx_35_0 ON HISTORIUBAHSTATUSKERJA(NO_PESERTA);

-- Referential index for link LNasabahDPLKCorporate in entity HistoriUbahStatusKerja
CREATE INDEX idx_35_1 ON HISTORIUBAHSTATUSKERJA(KODE_NASABAH_CORPORATE);

-- Referential index for link LRekeningDPLK in entity HistoriWasiatUmmat
CREATE INDEX idx_36_0 ON HISTORIWASIATUMMAT(NO_PESERTA);

-- Referential index for link LDeposito in entity HistPerubahanDeposito
CREATE INDEX idx_37_0 ON HISTPERUBAHANDEPOSITO(ID_INVESTASI);

-- Referential index for link LPihakKetiga in entity Investasi
CREATE INDEX idx_39_0 ON INVESTASI(KODE_PIHAK_KETIGA);

-- Referential index for link LRincianPaketInvestasi in entity Investasi
CREATE INDEX idx_39_1 ON INVESTASI(KODE_PAKET_INVESTASI, KODE_JNS_INVESTASI);

-- Referential index for link LRekeningDPLK in entity IuranPendaftaran
CREATE INDEX idx_40_0 ON IURANPENDAFTARAN(NO_PESERTA);

-- Referential index for link LTransactionBatch in entity IuranPendaftaran
CREATE INDEX idx_40_1 ON IURANPENDAFTARAN(ID_TRANSACTIONBATCH);

-- Referential index for link LTransactionBatchPremi in entity IuranPeserta
CREATE INDEX idx_41_0 ON TRANSAKSIDPLK(ID_BATCHPREMI);

-- Referential index for link LObligasi in entity JualObligasi
CREATE INDEX idx_49_0 ON JUALOBLIGASI(ID_INVESTASI);

-- Referential index for link LJenisInvestasi in entity NamaJnsTransInv
CREATE INDEX idx_55_0 ON NAMAJNSTRANSINV(KODE_JNS_INVESTASI);

-- Referential index for link LJnsTransInvestasi in entity NamaJnsTransInv
CREATE INDEX idx_55_1 ON NAMAJNSTRANSINV(KODE_JENIS_TRINVESTASI);

-- Referential index for link LDaerahAsal in entity NasabahDPLK
CREATE INDEX idx_56_0 ON NASABAHDPLK(kode_propinsi);

-- Referential index for link LJenisUsaha in entity NasabahDPLK
CREATE INDEX idx_56_1 ON NASABAHDPLK(kode_jenis_usaha);

-- Referential index for link LKepemilikan in entity NasabahDPLK
CREATE INDEX idx_56_2 ON NASABAHDPLK(kode_pemilikan);

-- Referential index for link LRekeningDPLK in entity NasabahDPLK
CREATE INDEX idx_56_3 ON NASABAHDPLK(no_peserta);

-- Referential index for link LNasabahDPLKCorporate in entity NasabahDPLK
CREATE INDEX idx_56_4 ON NASABAHDPLK(KODE_NASABAH_CORPORATE);

-- Referential index for link LOperationCode in entity NasabahDPLK
CREATE INDEX idx_56_5 ON NASABAHDPLK(OPERATION_CODE);

-- Referential index for link LKelompok in entity NasabahDPLK
CREATE INDEX idx_56_6 ON NASABAHDPLK(KODE_KELOMPOK);

-- Referential index for link LLDPLain in entity NasabahDPLK
CREATE INDEX idx_56_7 ON NASABAHDPLK(KODE_DP);

-- Referential index for link LJenisUsaha in entity NasabahDPLKCorporate
CREATE INDEX idx_57_0 ON NASABAHDPLKCORPORATE(KODE_JENIS_USAHA);

-- Referential index for link LKepemilikan in entity NasabahDPLKCorporate
CREATE INDEX idx_57_1 ON NASABAHDPLKCORPORATE(KODE_PEMILIKAN);

-- Referential index for link LOperationCode in entity NasabahDPLKCorporate
CREATE INDEX idx_57_2 ON NASABAHDPLKCORPORATE(OPERATION_CODE);

-- Referential index for link LCustodianBank in entity Obligasi
CREATE INDEX idx_58_0 ON OBLIGASI(BANKCODE);

-- Referential index for link Lbagi_hasil in entity PembagianHasilPortofolio
CREATE INDEX idx_62_0 ON TRANSAKSIDPLK(idbghasil);

-- Referential index for link LBiayaAdmTransaksi in entity PenarikanDana
CREATE INDEX idx_63_0 ON PENARIKANDANA(ID_TRANSAKSI_BADMTRANS);

-- Referential index for link LBiayaAdmTransaksi in entity PenarikanDanaNormal
CREATE INDEX idx_64_0 ON PENARIKANDANA(ID_TRANSAKSI_BADMTRANS);

-- Referential index for link LBiayaAdmTransaksi in entity PenarikanDanaPHK
CREATE INDEX idx_65_0 ON PENARIKANDANA(ID_TRANSAKSI_BADMTRANS);

-- Referential index for link LObligasi in entity PendapatanObligasi
CREATE INDEX idx_67_0 ON PENDAPATANOBLIGASI(ID_INVESTASI);

-- Referential index for link LReksadana in entity PendapatanReksadana
CREATE INDEX idx_68_0 ON PENDAPATANREKSADANA(ID_INVESTASI);

-- Referential index for link LLDP in entity PengalihanDariDPLKLain
CREATE INDEX idx_69_0 ON PENGALIHANDARIDPLKLAIN(KODE_DP);

-- Referential index for link LBiayaAdmTahunan in entity PengalihanKeDPLKLain
CREATE INDEX idx_70_0 ON PENGALIHANKEDPLKLAIN(ID_TRANSAKSI_BADMTHN);

-- Referential index for link LBiayaPengelolaanDana in entity PengalihanKeDPLKLain
CREATE INDEX idx_70_1 ON PENGALIHANKEDPLKLAIN(ID_TRANSAKSI_BPENG);

-- Referential index for link LBiayaAdmTransaksi in entity PengalihanKeDPLKLain
CREATE INDEX idx_70_2 ON PENGALIHANKEDPLKLAIN(ID_TRANSAKSI_BADMTRANS);

-- Referential index for link LLDP in entity PengalihanKeDPLKLain
CREATE INDEX idx_70_3 ON PENGALIHANKEDPLKLAIN(KODE_DP);

-- Referential index for link Ljenis_penerimaan_manfaat in entity PengambilanManfaat
CREATE INDEX idx_71_0 ON PENGAMBILANMANFAAT(kode_jns_manfaat);

-- Referential index for link LAhliWaris in entity PengambilanManfaat
CREATE INDEX idx_71_1 ON PENGAMBILANMANFAAT(AHLIWARIS_ID);

-- Referential index for link LBiayaAdmTahunan in entity PengambilanManfaat
CREATE INDEX idx_71_2 ON PENGAMBILANMANFAAT(ID_TRANSAKSI_BADMTHN);

-- Referential index for link LBiayaPengelolaanDana in entity PengambilanManfaat
CREATE INDEX idx_71_3 ON PENGAMBILANMANFAAT(ID_TRANSAKSI_BPENG);

-- Referential index for link LBiayaAdmTransaksi in entity PengambilanManfaat
CREATE INDEX idx_71_4 ON PENGAMBILANMANFAAT(ID_TRANSAKSI_BADMTRANS);

-- Referential index for link LReksadana in entity RealisasiReturn
CREATE INDEX idx_73_0 ON REALISASIRETURN(ID_INVESTASI);

-- Referential index for link LKlaimLRReksadana in entity RedemptReksadana
CREATE INDEX idx_74_0 ON REDEMPTREKSADANA(ID_TRANSAKSIINVESTASI_KLAIM);

-- Referential index for link LReksadana in entity RedemptReksadana
CREATE INDEX idx_74_1 ON REDEMPTREKSADANA(ID_INVESTASI);

-- Referential index for link LKepemilikan in entity RegEditNasabahDPLKCorporate
CREATE INDEX idx_76_0 ON REGEDITNASABAHDPLKCORPORATE(KODE_PEMILIKAN);

-- Referential index for link LJenisUsaha in entity RegEditNasabahDPLKCorporate
CREATE INDEX idx_76_1 ON REGEDITNASABAHDPLKCORPORATE(KODE_JENIS_USAHA);

-- Referential index for link LNasabahDPLKCorporate in entity RegEditNasabahDPLKCorporate
CREATE INDEX idx_76_2 ON REGEDITNASABAHDPLKCORPORATE(KODE_NASABAH_CORPORATE);

-- Referential index for link LOperationCode in entity RegEditNasabahDPLKCorporate
CREATE INDEX idx_76_3 ON REGEDITNASABAHDPLKCORPORATE(OPERATION_CODE);

-- Referential index for link LNasabahDPLKHolding in entity RegEditNasabahDPLKCorporate
CREATE INDEX idx_76_4 ON REGEDITNASABAHDPLKCORPORATE(KODE_HOLDING);

-- Referential index for link LJenisUsaha in entity RegEditNasabahRekening
CREATE INDEX idx_77_0 ON REGEDITNASABAHREKENING(KODE_JENIS_USAHA);

-- Referential index for link LKepemilikan in entity RegEditNasabahRekening
CREATE INDEX idx_77_1 ON REGEDITNASABAHREKENING(KODE_PEMILIKAN);

-- Referential index for link LDaerahAsal in entity RegEditNasabahRekening
CREATE INDEX idx_77_2 ON REGEDITNASABAHREKENING(KODE_PROPINSI);

-- Referential index for link LSumberDana in entity RegEditNasabahRekening
CREATE INDEX idx_77_3 ON REGEDITNASABAHREKENING(SUMBER_DANA);

-- Referential index for link LKelompok in entity RegEditNasabahRekening
CREATE INDEX idx_77_4 ON REGEDITNASABAHREKENING(KODE_KELOMPOK);

-- Referential index for link LRegisterAhliWaris in entity RegisterAhliWarisDetail
CREATE INDEX idx_79_0 ON REGISTERAHLIWARISDETAIL(REGISTERCIF_ID);

-- Referential index for link LNasabahDPLK in entity RegisterCIF
CREATE INDEX idx_82_0 ON REGISTERCIF(NO_PESERTA);

-- Referential index for link LJenisRegisterCIF in entity RegisterCIF
CREATE INDEX idx_82_1 ON REGISTERCIF(KODE_JENIS_REGISTERCIF);

-- Referential index for link LUserApp in entity RegisterCIF
CREATE INDEX idx_82_2 ON REGISTERCIF(USER_ID);

-- Referential index for link LMasterGiro in entity RegisterDeposito
CREATE INDEX idx_83_0 ON REGISTERDEPOSITO(ACC_GIRO);

-- Referential index for link LPihakKetiga in entity RegisterInvestasi
CREATE INDEX idx_84_0 ON REGISTERINVESTASI(KODE_PIHAK_KETIGA);

-- Referential index for link LRincianPaketInvestasi in entity RegisterInvestasi
CREATE INDEX idx_84_1 ON REGISTERINVESTASI(KODE_JNS_INVESTASI, KODE_PAKET_INVESTASI);

-- Referential index for link LTransactionBatch in entity RegisterInvestasi
CREATE INDEX idx_84_2 ON REGISTERINVESTASI(ID_TRANSACTIONBATCH);

-- Referential index for link LRekeningDPLK in entity RegisterIuran
CREATE INDEX idx_85_0 ON REGISTERIURAN(NO_PESERTA);

-- Referential index for link LDaerahAsal in entity RegisterNasabahRekening
CREATE INDEX idx_86_0 ON REGISTERNASABAHREKENING(KODE_PROPINSI);

-- Referential index for link LKepemilikan in entity RegisterNasabahRekening
CREATE INDEX idx_86_1 ON REGISTERNASABAHREKENING(KODE_PEMILIKAN);

-- Referential index for link LJenisUsaha in entity RegisterNasabahRekening
CREATE INDEX idx_86_2 ON REGISTERNASABAHREKENING(KODE_JENIS_USAHA);

-- Referential index for link LNasabahDPLKCorporate in entity RegisterNasabahRekening
CREATE INDEX idx_86_3 ON REGISTERNASABAHREKENING(KODE_NASABAH_CORPORATE);

-- Referential index for link LPaketInvestasi in entity RegisterNasabahRekening
CREATE INDEX idx_86_4 ON REGISTERNASABAHREKENING(KODE_PAKET_INVESTASI);

-- Referential index for link LSumberDana in entity RegisterNasabahRekening
CREATE INDEX idx_86_5 ON REGISTERNASABAHREKENING(sumber_dana);

-- Referential index for link LKelompok in entity RegisterNasabahRekening
CREATE INDEX idx_86_6 ON REGISTERNASABAHREKENING(KODE_KELOMPOK);

-- Referential index for link LRegisterIuranPeserta in entity RegisterNasabahRekening
CREATE INDEX idx_86_7 ON REGISTERNASABAHREKENING(ID_TRANSAKSI_IURANPESERTA);

-- Referential index for link LRegisterIuranPendaftaran in entity RegisterNasabahRekening
CREATE INDEX idx_86_8 ON REGISTERNASABAHREKENING(ID_TRANSAKSI_IURANPENDAFTARAN);

-- Referential index for link LLDPLain in entity RegisterNasabahRekening
CREATE INDEX idx_86_9 ON REGISTERNASABAHREKENING(KODE_DP);

-- Referential index for link LCustodianBank in entity RegisterObligasi
CREATE INDEX idx_87_0 ON REGISTEROBLIGASI(BANKCODE);

-- Referential index for link LPaketInvestasi in entity RegisterPindahPaketInvestasi
CREATE INDEX idx_88_0 ON REGISTERPINDAHPAKETINVESTASI(KODE_PAKET_INVESTASI);

-- Referential index for link LTransactionBatch in entity RegisterPindahPaketInvestasi
CREATE INDEX idx_88_1 ON REGISTERPINDAHPAKETINVESTASI(ID_TRANSACTIONBATCH);

-- Referential index for link LCustodianBank in entity RegisterReksadana
CREATE INDEX idx_89_0 ON REGISTERREKSADANA(BANKCODE);

-- Referential index for link LJenisReksadana in entity RegisterReksadana
CREATE INDEX idx_89_1 ON REGISTERREKSADANA(KODE_JNS_REKSADANA);

-- Referential index for link LNasabahDPLKCorporate in entity RegisterUbahStatusKerja
CREATE INDEX idx_91_0 ON REGISTERUBAHSTATUSKERJA(KODE_NASABAH_CORPORATE);

-- Referential index for link LRegisterNasabahRekening in entity RegNRAhliWaris
CREATE INDEX idx_93_0 ON REGNRAHLIWARIS(REGISTERNR_ID);

-- Referential index for link LRekeningDPLK in entity RekeningAnuitas
CREATE INDEX idx_94_0 ON REKENINGANUITAS(NO_PESERTA);

-- Referential index for link LRekeningDPLK in entity RekeningAutoDebet
CREATE INDEX idx_95_0 ON REKENINGAUTODEBET(NO_PESERTA);

-- Referential index for link LNasabahDPLK in entity RekeningDPLK
CREATE INDEX idx_96_0 ON REKENINGDPLK(no_peserta);

-- Referential index for link LPaketInvestasi in entity RekeningDPLK
CREATE INDEX idx_96_1 ON REKENINGDPLK(kode_paket_investasi);

-- Referential index for link LBranchLocation in entity RekeningDPLK
CREATE INDEX idx_96_2 ON REKENINGDPLK(kode_cab_daftar);

-- Referential index for link LOperationCode in entity RekeningDPLK
CREATE INDEX idx_96_3 ON REKENINGDPLK(OPERATION_CODE);

-- Referential index for link LSumberDana in entity RekeningDPLK
CREATE INDEX idx_96_4 ON REKENINGDPLK(sumber_dana);

-- Referential index for link LRekeningDPLK in entity RekeningWasiatUmmat
CREATE INDEX idx_97_0 ON REKENINGWASIATUMMAT(NO_PESERTA);

-- Referential index for link LCustodianBank in entity Reksadana
CREATE INDEX idx_98_0 ON REKSADANA(BANKCODE);

-- Referential index for link LJenisReksadana in entity Reksadana
CREATE INDEX idx_98_1 ON REKSADANA(KODE_JNS_REKSADANA);

-- Referential index for link LDeposito in entity RincianDeposito
CREATE INDEX idx_99_0 ON RINCIANINVESTASI(ID_INVESTASI);

-- Referential index for link LInvestasi in entity RincianInvestasi
CREATE INDEX idx_100_0 ON RINCIANINVESTASI(ID_INVESTASI);

-- Referential index for link LRincianPaketInvestasi in entity RincianInvestasi
CREATE INDEX idx_100_1 ON RINCIANINVESTASI(KODE_JNS_INVESTASI, KODE_PAKET_INVESTASI);

-- Referential index for link LObligasi in entity RincianObligasi
CREATE INDEX idx_101_0 ON RINCIANINVESTASI(ID_INVESTASI);

-- Referential index for link LPaketInvestasi in entity RincianPaketInvestasi
CREATE INDEX idx_102_0 ON RINCIANPAKETINVESTASI(kode_paket_investasi);

-- Referential index for link LJenisInvestasi in entity RincianPaketInvestasi
CREATE INDEX idx_102_1 ON RINCIANPAKETINVESTASI(KODE_JNS_INVESTASI);

-- Referential index for link LPihakKetiga in entity RincianPihakKetiga
CREATE INDEX idx_103_0 ON RINCIANPIHAKKETIGA(KODE_PIHAK_KETIGA);

-- Referential index for link LJenisInvestasi in entity RincianPihakKetiga
CREATE INDEX idx_103_1 ON RINCIANPIHAKKETIGA(KODE_JNS_INVESTASI);

-- Referential index for link LRegisterDeposito in entity RincianRegisterDeposito
CREATE INDEX idx_104_0 ON RINCIANREGISTERINVESTASI(ID_REGISTERINVESTASI);

-- Referential index for link LRegisterInvestasi in entity RincianRegisterInvestasi
CREATE INDEX idx_105_0 ON RINCIANREGISTERINVESTASI(ID_REGISTERINVESTASI);

-- Referential index for link LRincianPaketInvestasi in entity RincianRegisterInvestasi
CREATE INDEX idx_105_1 ON RINCIANREGISTERINVESTASI(KODE_PAKET_INVESTASI, KODE_JNS_INVESTASI);

-- Referential index for link LRegisterObligasi in entity RincianRegisterObligasi
CREATE INDEX idx_106_0 ON RINCIANREGISTERINVESTASI(ID_REGISTERINVESTASI);

-- Referential index for link LRegisterReksadana in entity RincianRegisterReksadana
CREATE INDEX idx_107_0 ON RINCIANREGISTERINVESTASI(ID_REGISTERINVESTASI);

-- Referential index for link LReksadana in entity RincianReksadana
CREATE INDEX idx_108_0 ON RINCIANINVESTASI(ID_INVESTASI);

-- Referential index for link LDeposito in entity RolloverDeposito
CREATE INDEX idx_109_0 ON ROLLOVERDEPOSITO(ID_INVESTASI);

-- Referential index for link LBLOBData in entity SessionBLOB
CREATE INDEX idx_110_0 ON SESSIONBLOB(ID1);

-- Referential index for link LUserCreate in entity SRRCalc
CREATE INDEX idx_112_0 ON SRRCALC(USER_ID_CREATE);

-- Referential index for link LBagiHasil in entity SRRCalcBagiHasil
CREATE INDEX idx_113_0 ON SRRCALCBAGIHASIL(IDBGHASIL);

-- Referential index for link LSRRCalcRincian in entity SRRCalcBagiHasil
CREATE INDEX idx_113_1 ON SRRCALCBAGIHASIL(ID_SRRCALCRINCIAN);

-- Referential index for link LPaketInvestasi in entity SRRCalcRincian
CREATE INDEX idx_114_0 ON SRRCALCRINCIAN(KODE_PAKET_INVESTASI);

-- Referential index for link LSRRCalc in entity SRRCalcRincian
CREATE INDEX idx_114_1 ON SRRCALCRINCIAN(ID_SRRCALC);

-- Referential index for link LJenisInvestasi in entity SubJnsTransLRInvestasi
CREATE INDEX idx_115_0 ON SUBJNSTRANSLRINVESTASI(KODE_JNS_INVESTASI);

-- Referential index for link LReksadana in entity SubscribeReksadana
CREATE INDEX idx_116_0 ON SUBSCRIBEREKSADANA(ID_INVESTASI);

-- Referential index for link LRekeningDPLK in entity TitipanPremi
CREATE INDEX idx_118_0 ON TRANSAKSIPREMI(NO_PESERTA);

-- Referential index for link LUserOwner in entity TransactionBatch
CREATE INDEX idx_119_0 ON TRANSACTIONBATCH(USER_ID_OWNER);

-- Referential index for link LBagiHasil in entity TransaksiBagiHasil
CREATE INDEX idx_120_0 ON TRANSAKSIBAGIHASIL(IDBGHASIL);

-- Referential index for link LTransactionBatch in entity TransaksiDPLK
CREATE INDEX idx_121_0 ON TRANSAKSIDPLK(ID_TRANSACTIONBATCH);

-- Referential index for link LRekeningDPLK in entity TransaksiDPLK
CREATE INDEX idx_121_1 ON TRANSAKSIDPLK(NO_PESERTA);

-- Referential index for link LJenisTransaksiDPLK in entity TransaksiDPLK
CREATE INDEX idx_121_2 ON TRANSAKSIDPLK(KODE_JENIS_TRANSAKSI);

-- Referential index for link LPaketInvestasi in entity TransaksiDPLK
CREATE INDEX idx_121_3 ON TRANSAKSIDPLK(KODE_PAKET_INVESTASI);

-- Referential index for link LJenisTransaksiManual in entity TransaksiDPLKManual
CREATE INDEX idx_122_0 ON TRANSAKSIDPLK(KODE_TRANSAKSI_MANUAL);

-- Referential index for link LTransactionBatch in entity TransaksiInvestasi
CREATE INDEX idx_123_0 ON TRANSAKSIINVESTASI(ID_TRANSACTIONBATCH);

-- Referential index for link LNamaJnsTransInv in entity TransaksiInvestasi
CREATE INDEX idx_123_1 ON TRANSAKSIINVESTASI(KODE_JNS_INVESTASI, KODE_JENIS_TRINVESTASI);

-- Referential index for link LInvestasi in entity TransaksiInvestasi
CREATE INDEX idx_123_2 ON TRANSAKSIINVESTASI(ID_INVESTASI);

-- Referential index for link LIndukTransaksiInvestasi in entity TransaksiInvestasi
CREATE INDEX idx_123_3 ON TRANSAKSIINVESTASI(ID_TRANSAKSIINDUK);

-- Referential index for link LTransactionBatch in entity TransaksiPremi
CREATE INDEX idx_125_0 ON TRANSAKSIPREMI(ID_TRANSACTIONBATCH);

-- Referential index for link LSubJnsTransLRInvestasi in entity TransLRInvestasi
CREATE INDEX idx_128_0 ON TRANSLRINVESTASI(KODE_SUBJNS_LRINVESTASI);

-- Referential index for link LAsalTransLRInvestasi in entity TransLRInvestasi
CREATE INDEX idx_128_1 ON TRANSLRINVESTASI(ID_ASALTRANSLR);

-- Referential index for link LTransPiutangInvestasi in entity TransPiutangLRInvestasi
CREATE INDEX idx_130_0 ON TRANSPIUTANGLRINVESTASI(ID_TRANSAKSIINVESTASI_PIUTINV);

-- Referential index for link LTransLRInvestasi in entity TransPiutangLRInvestasi
CREATE INDEX idx_130_1 ON TRANSPIUTANGLRINVESTASI(ID_TRANSAKSIINVESTASI_LRINV);

-- Referential index for link LDeposito in entity TutupDeposito
CREATE INDEX idx_131_0 ON TUTUPDEPOSITO(ID_INVESTASI);

-- Referential index for link LBranchLocation in entity UserApp
CREATE INDEX idx_132_0 ON USERAPP(branch_code);

-- Referential index for link LSupervisor in entity UserApp
CREATE INDEX idx_132_1 ON USERAPP(USER_ID1);

-- Referential index for link LUser in entity UserGroupApp
CREATE INDEX idx_134_0 ON USERGROUPAPP(user_id);

-- Referential index for link LUserGroup in entity UserGroupApp
CREATE INDEX idx_134_1 ON USERGROUPAPP(group_id);

