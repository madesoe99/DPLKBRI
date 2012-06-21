-- Inheritance integrity check for entity Investasi
-- Inheritance integrity error check. Descendant Deposito in class Investasi
SELECT ID_INVESTASI FROM INVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM DEPOSITO INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'D')

-- Inheritance integrity error check. Descendant Obligasi in class Investasi
SELECT ID_INVESTASI FROM INVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM OBLIGASI INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'O')

-- Inheritance integrity error check. Descendant Reksadana in class Investasi
SELECT ID_INVESTASI FROM INVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REKSADANA INNER WHERE
outer.ID_INVESTASI = inner.ID_INVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'R')

-- Inheritance integrity check for entity RegisterCIF
-- Inheritance integrity error check. Descendant RegisterUbahAlamat in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERUBAHALAMAT INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'A')

-- Inheritance integrity error check. Descendant RegisterUbahStatusKerja in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERUBAHSTATUSKERJA INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'K')

-- Inheritance integrity error check. Descendant RegisterWasiatUmmat in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERWASIATUMMAT INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'U')

-- Inheritance integrity error check. Descendant RegisterPindahPaketInvestasi in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERPINDAHPAKETINVESTASI INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'P')

-- Inheritance integrity error check. Descendant RegisterAutoDebet in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERAUTODEBET INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'D')

-- Inheritance integrity error check. Descendant RegisterAnuitas in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERANUITAS INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'N')

-- Inheritance integrity error check. Descendant RegisterAhliWaris in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERAHLIWARIS INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'W')

-- Inheritance integrity error check. Descendant RegisterIuran in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERIURAN INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'I')

-- Inheritance integrity error check. Descendant RegEditNasabahRekening in class RegisterCIF
SELECT REGISTERCIF_ID FROM REGISTERCIF outer WHERE NOT EXISTS(
SELECT 1 FROM REGEDITNASABAHREKENING INNER WHERE
outer.REGISTERCIF_ID = inner.REGISTERCIF_ID
) AND (outer.KODE_JENIS_REGISTERCIF = 'Z')

-- Inheritance integrity check for entity RegisterInvestasi
-- Inheritance integrity error check. Descendant RegisterDeposito in class RegisterInvestasi
SELECT ID_REGISTERINVESTASI FROM REGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERDEPOSITO INNER WHERE
outer.ID_REGISTERINVESTASI = inner.ID_REGISTERINVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'D')

-- Inheritance integrity error check. Descendant RegisterObligasi in class RegisterInvestasi
SELECT ID_REGISTERINVESTASI FROM REGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTEROBLIGASI INNER WHERE
outer.ID_REGISTERINVESTASI = inner.ID_REGISTERINVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'O')

-- Inheritance integrity error check. Descendant RegisterReksadana in class RegisterInvestasi
SELECT ID_REGISTERINVESTASI FROM REGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REGISTERREKSADANA INNER WHERE
outer.ID_REGISTERINVESTASI = inner.ID_REGISTERINVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'R')

-- Inheritance integrity check for entity RincianInvestasi
-- Inheritance integrity error check. Descendant RincianDeposito in class RincianInvestasi
SELECT ID_RINCIANINVESTASI FROM RINCIANINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANINVESTASI INNER WHERE
outer.ID_RINCIANINVESTASI = inner.ID_RINCIANINVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'D')

-- Inheritance integrity error check. Descendant RincianObligasi in class RincianInvestasi
SELECT ID_RINCIANINVESTASI FROM RINCIANINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANINVESTASI INNER WHERE
outer.ID_RINCIANINVESTASI = inner.ID_RINCIANINVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'O')

-- Inheritance integrity error check. Descendant RincianReksadana in class RincianInvestasi
SELECT ID_RINCIANINVESTASI FROM RINCIANINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANINVESTASI INNER WHERE
outer.ID_RINCIANINVESTASI = inner.ID_RINCIANINVESTASI
) AND (outer.KODE_JNS_INVESTASI = 'R')

-- Inheritance integrity check for entity RincianRegisterInvestasi
-- Inheritance integrity error check. Descendant RincianRegisterDeposito in class RincianRegisterInvestasi
SELECT ID_RINCIANREGISTERINV FROM RINCIANREGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANREGISTERINVESTASI INNER WHERE
outer.ID_RINCIANREGISTERINV = inner.ID_RINCIANREGISTERINV
) AND (outer.KODE_JNS_INVESTASI = 'A')

-- Inheritance integrity error check. Descendant RincianRegisterObligasi in class RincianRegisterInvestasi
SELECT ID_RINCIANREGISTERINV FROM RINCIANREGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANREGISTERINVESTASI INNER WHERE
outer.ID_RINCIANREGISTERINV = inner.ID_RINCIANREGISTERINV
) AND (outer.KODE_JNS_INVESTASI = 'B')

-- Inheritance integrity error check. Descendant RincianRegisterReksadana in class RincianRegisterInvestasi
SELECT ID_RINCIANREGISTERINV FROM RINCIANREGISTERINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM RINCIANREGISTERINVESTASI INNER WHERE
outer.ID_RINCIANREGISTERINV = inner.ID_RINCIANREGISTERINV
) AND (outer.KODE_JNS_INVESTASI = 'C')

-- Inheritance integrity check for entity TransaksiDPLK
-- Inheritance integrity error check. Descendant BiayaPengelolaanDana in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'C')

-- Inheritance integrity error check. Descendant Pendaftaran in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PENDAFTARAN INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'A')

-- Inheritance integrity error check. Descendant BiayaAdmTahunan in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'D')

-- Inheritance integrity error check. Descendant IuranPeserta in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'K')

-- Inheritance integrity error check. Descendant PengambilanManfaat in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PENGAMBILANMANFAAT INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'J')

-- Inheritance integrity error check. Descendant BayarPremi in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM BAYARPREMI INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'B')

-- Inheritance integrity error check. Descendant PengalihanDariDPLKLain in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PENGALIHANDARIDPLKLAIN INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'I')

-- Inheritance integrity error check. Descendant PengalihanKeDPLKLain in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PENGALIHANKEDPLKLAIN INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'H')

-- Inheritance integrity error check. Descendant PembagianHasilPortofolio in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'G')

-- Inheritance integrity error check. Descendant PenarikanDana in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PENARIKANDANA INNER WHERE
outer.ID_Transaksi = inner.ID_Transaksi
) AND (outer.KODE_JENIS_TRANSAKSI = 'E')

-- Inheritance integrity error check. Descendant PenarikanDanaPHK in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PENARIKANDANA INNER WHERE
outer.ID_Transaksi = inner.ID_TRANSAKSI
) AND (outer.KODE_JENIS_TRANSAKSI = 'W')

-- Inheritance integrity error check. Descendant PenarikanDanaNormal in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM PENARIKANDANA INNER WHERE
outer.ID_Transaksi = inner.ID_TRANSAKSI
) AND (outer.KODE_JENIS_TRANSAKSI = 'V')

-- Inheritance integrity error check. Descendant BiayaAdmTransaksi in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_Transaksi = inner.ID_TRANSAKSI
) AND (outer.KODE_JENIS_TRANSAKSI = 'X')

-- Inheritance integrity error check. Descendant TransaksiDPLKManual in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIDPLK INNER WHERE
outer.ID_Transaksi = inner.ID_TRANSAKSI
) AND (outer.KODE_JENIS_TRANSAKSI = 'M')

-- Inheritance integrity error check. Descendant TransaksiBagiHasil in class TransaksiDPLK
SELECT ID_Transaksi FROM TRANSAKSIDPLK outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIBAGIHASIL INNER WHERE
outer.ID_Transaksi = inner.ID_TRANSAKSI
) AND (outer.KODE_JENIS_TRANSAKSI = 'G')

-- Inheritance integrity check for entity TransaksiInvestasi
-- Inheritance integrity error check. Descendant TransPiutangInvestasi in class TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSPIUTANGINVESTASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.CLSFTRANSAKSIINVESTASI = 'A')

-- Inheritance integrity error check. Descendant TransPiutangLRInvestasi in class TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSPIUTANGLRINVESTASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.CLSFTRANSAKSIINVESTASI = 'B')

-- Inheritance integrity error check. Descendant TransLRInvestasi in class TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSLRINVESTASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.CLSFTRANSAKSIINVESTASI = 'C')

-- Inheritance integrity error check. Descendant TransaksiSPInvestasi in class TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIINVESTASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.CLSFTRANSAKSIINVESTASI = 'D')

-- Inheritance integrity error check. Descendant TransaksiPNInvestasi in class TransaksiInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSAKSIINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIINVESTASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.CLSFTRANSAKSIINVESTASI = 'E')

-- Inheritance integrity check for entity TransaksiPremi
-- Inheritance integrity error check. Descendant TitipanPremi in class TransaksiPremi
SELECT ID_TRANSAKSI FROM TRANSAKSIPREMI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIPREMI INNER WHERE
outer.ID_TRANSAKSI = inner.ID_TRANSAKSI
) AND (outer.JENIS_TRANSAKSI = 'T')

-- Inheritance integrity error check. Descendant SetoranPremi in class TransaksiPremi
SELECT ID_TRANSAKSI FROM TRANSAKSIPREMI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIPREMI INNER WHERE
outer.ID_TRANSAKSI = inner.ID_TRANSAKSI
) AND (outer.JENIS_TRANSAKSI = 'S')

-- Inheritance integrity error check. Descendant TransaksiPremiManual in class TransaksiPremi
SELECT ID_TRANSAKSI FROM TRANSAKSIPREMI outer WHERE NOT EXISTS(
SELECT 1 FROM TRANSAKSIPREMI INNER WHERE
outer.ID_TRANSAKSI = inner.ID_TRANSAKSI
) AND (outer.JENIS_TRANSAKSI = 'M')

-- Inheritance integrity check for entity TransLRInvestasi
-- Inheritance integrity error check. Descendant KlaimLRReksadana in class TransLRInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM KLAIMLRREKSADANA INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'K')

-- Inheritance integrity error check. Descendant BagiHasilReksadana in class TransLRInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM BAGIHASILREKSADANA INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'B')

-- Inheritance integrity error check. Descendant RealisasiReturn in class TransLRInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REALISASIRETURN INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'U')

-- Inheritance integrity error check. Descendant BagiHasilDeposito in class TransLRInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM BAGIHASILDEPOSITO INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'H')

-- Inheritance integrity error check. Descendant PendapatanObligasi in class TransLRInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM PENDAPATANOBLIGASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'O')

-- Inheritance integrity error check. Descendant PendapatanReksadana in class TransLRInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSLRINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM PENDAPATANREKSADANA INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'R')

-- Inheritance integrity check for entity TransPiutangInvestasi
-- Inheritance integrity error check. Descendant BeliObligasi in class TransPiutangInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSPIUTANGINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM BELIOBLIGASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'B')

-- Inheritance integrity error check. Descendant JualObligasi in class TransPiutangInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSPIUTANGINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM JUALOBLIGASI INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'J')

-- Inheritance integrity error check. Descendant SubscribeReksadana in class TransPiutangInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSPIUTANGINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM SUBSCRIBEREKSADANA INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'S')

-- Inheritance integrity error check. Descendant RedemptReksadana in class TransPiutangInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSPIUTANGINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM REDEMPTREKSADANA INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'R')

-- Inheritance integrity error check. Descendant RolloverDeposito in class TransPiutangInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSPIUTANGINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM ROLLOVERDEPOSITO INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'V')

-- Inheritance integrity error check. Descendant TutupDeposito in class TransPiutangInvestasi
SELECT ID_TRANSAKSIINVESTASI FROM TRANSPIUTANGINVESTASI outer WHERE NOT EXISTS(
SELECT 1 FROM TUTUPDEPOSITO INNER WHERE
outer.ID_TRANSAKSIINVESTASI = inner.ID_TRANSAKSIINVESTASI
) AND (outer.JENIS = 'T')

