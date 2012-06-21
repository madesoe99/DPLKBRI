/* Migrating column for class AhliWaris */

ALTER TABLE dbo.AHLIWARIS ALTER COLUMN NAMA_LENGKAP VARCHAR(100);

/* Migrating column for class HistJenisInvestasi */

ALTER TABLE dbo.HISTJENISINVESTASI ALTER COLUMN NO_REFERENSI VARCHAR(50);

/* Migrating column for class HistoriAhliWaris */

ALTER TABLE dbo.HISTORIAHLIWARIS ALTER COLUMN NO_REFERENSI VARCHAR(50);

/* Migrating column for class HistoriAhliWarisDetail */

ALTER TABLE dbo.HISTORIAHLIWARISDETAIL ALTER COLUMN NAMA_LENGKAP VARCHAR(100);

/* Migrating column for class HistoriAnuitas */

ALTER TABLE dbo.HISTORIANUITAS ALTER COLUMN NO_REFERENSI VARCHAR(50);

/* Migrating column for class HistoriAnuitas */

ALTER TABLE dbo.HISTORIANUITAS ALTER COLUMN NAMA_ASURANSI VARCHAR(50);

/* Migrating column for class HistoriAnuitas */

ALTER TABLE dbo.HISTORIANUITAS ALTER COLUMN NO_POLIS_ANUITAS VARCHAR(30);

/* Migrating column for class HistoriAutoDebet */

ALTER TABLE dbo.HISTORIAUTODEBET ALTER COLUMN NO_REFERENSI VARCHAR(50);

/* Migrating column for class HistoriIuran */







ALTER TABLE dbo.HISTORIIURAN ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Migrating column for class HistoriPindahPaketInvestasi */







ALTER TABLE dbo.HISTORIPINDAHPAKETINVESTASI ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN alamat_jalan VARCHAR(200);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN alamat_kota VARCHAR(50);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN alamat_kode_pos VARCHAR(30);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN alamat_telepon VARCHAR(30);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN alamat_kantor_jalan VARCHAR(200);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN alamat_kantor_kota VARCHAR(50);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN alamat_kantor_propinsi VARCHAR(50);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN ALAMAT_SURAT_JALAN VARCHAR(200);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN ALAMAT_SURAT_KOTA VARCHAR(50);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN ALAMAT_SURAT_PROPINSI VARCHAR(50);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN ALAMAT_SURAT_KODE_POS VARCHAR(50);






/* Migrating column for class HistoriUbahAlamat */







ALTER TABLE dbo.HISTORIUBAHALAMAT ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Altering table for class HistoriUbahAlamat */

ALTER TABLE HISTORIUBAHALAMAT
  ADD ALAMAT_TELEPON2 VARCHAR(30),
  ALAMAT_KANTOR_TELEPON2 VARCHAR(30),
  ALAMAT_JALAN2 VARCHAR(200);

/* Migrating column for class HistoriUbahStatusKerja */







ALTER TABLE dbo.HISTORIUBAHSTATUSKERJA ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Migrating column for class HistoriWasiatUmmat */







ALTER TABLE dbo.HISTORIWASIATUMMAT ALTER COLUMN NO_POLIS VARCHAR(30);






/* Migrating column for class HistoriWasiatUmmat */







ALTER TABLE dbo.HISTORIWASIATUMMAT ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN nama_lengkap VARCHAR(100);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN alamat_jalan VARCHAR(200);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN alamat_kota VARCHAR(50);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN alamat_kode_pos VARCHAR(30);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN alamat_telepon VARCHAR(30);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN pekerjaan VARCHAR(50);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN nama_perusahaan VARCHAR(100);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN alamat_kantor_jalan VARCHAR(200);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN alamat_kantor_kota VARCHAR(50);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN alamat_kantor_propinsi VARCHAR(50);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN ALAMAT_SURAT_JALAN VARCHAR(200);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN ALAMAT_SURAT_KOTA VARCHAR(50);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN ALAMAT_SURAT_PROPINSI VARCHAR(50);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN ALAMAT_SURAT_KODE_POS VARCHAR(30);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN NPWP VARCHAR(50);






/* Migrating column for class NasabahDPLK */







ALTER TABLE dbo.NASABAHDPLK ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Altering table for class NasabahDPLK */

ALTER TABLE NASABAHDPLK
  ADD ALAMAT_KANTOR_TELEPON2 VARCHAR(30),
  ALAMAT_JALAN2 VARCHAR(200),
  ALAMAT_TELEPON2 VARCHAR(30);

/* Migrating column for class NasabahDPLKCorporate */







ALTER TABLE dbo.NASABAHDPLKCORPORATE ALTER COLUMN NAMA_PERUSAHAAN VARCHAR(100);






/* Migrating column for class NasabahDPLKCorporate */







ALTER TABLE dbo.NASABAHDPLKCORPORATE ALTER COLUMN alamat_kantor_jalan VARCHAR(200);






/* Migrating column for class NasabahDPLKCorporate */







ALTER TABLE dbo.NASABAHDPLKCORPORATE ALTER COLUMN alamat_kantor_kota VARCHAR(50);






/* Migrating column for class NasabahDPLKCorporate */







ALTER TABLE dbo.NASABAHDPLKCORPORATE ALTER COLUMN NPWP VARCHAR(50);






/* Migrating column for class NasabahDPLKCorporate */







ALTER TABLE dbo.NASABAHDPLKCORPORATE ALTER COLUMN NO_PERJANJIAN VARCHAR(50);






/* Migrating column for class NasabahDPLKCorporate */







ALTER TABLE dbo.NASABAHDPLKCORPORATE ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Altering table for class NasabahDPLKCorporate */

ALTER TABLE NASABAHDPLKCORPORATE
  ADD ALAMAT_KANTOR_TELEPON2 VARCHAR(30);

/* Migrating column for class RegEditNasabahDPLKCorporate */







ALTER TABLE dbo.REGEDITNASABAHDPLKCORPORATE ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Migrating column for class RegEditNasabahDPLKCorporate */







ALTER TABLE dbo.REGEDITNASABAHDPLKCORPORATE ALTER COLUMN NPWP VARCHAR(50);






/* Migrating column for class RegEditNasabahDPLKCorporate */







ALTER TABLE dbo.REGEDITNASABAHDPLKCORPORATE ALTER COLUMN NO_PERJANJIAN VARCHAR(50);






/* Migrating column for class RegEditNasabahDPLKCorporate */







ALTER TABLE dbo.REGEDITNASABAHDPLKCORPORATE ALTER COLUMN NAMA_PERUSAHAAN VARCHAR(100);






/* Migrating column for class RegEditNasabahDPLKCorporate */







ALTER TABLE dbo.REGEDITNASABAHDPLKCORPORATE ALTER COLUMN alamat_kantor_jalan VARCHAR(200);






/* Migrating column for class RegEditNasabahDPLKCorporate */







ALTER TABLE dbo.REGEDITNASABAHDPLKCORPORATE ALTER COLUMN alamat_kantor_kota VARCHAR(50);






/* Altering table for class RegEditNasabahDPLKCorporate */

ALTER TABLE REGEDITNASABAHDPLKCORPORATE
  ADD ALAMAT_KANTOR_TELEPON2 VARCHAR(30);

/* Migrating column for class RegEditNasabahRekening */







ALTER TABLE dbo.REGEDITNASABAHREKENING ALTER COLUMN nama_lengkap VARCHAR(100);






/* Migrating column for class RegEditNasabahRekening */







ALTER TABLE dbo.REGEDITNASABAHREKENING ALTER COLUMN pekerjaan VARCHAR(100);






/* Migrating column for class RegEditNasabahRekening */







ALTER TABLE dbo.REGEDITNASABAHREKENING ALTER COLUMN nama_perusahaan VARCHAR(100);






/* Migrating column for class RegisterAhliWarisDetail */







ALTER TABLE dbo.REGISTERAHLIWARISDETAIL ALTER COLUMN NAMA_LENGKAP VARCHAR(100);






/* Migrating column for class RegisterAnuitas */







ALTER TABLE dbo.REGISTERANUITAS ALTER COLUMN NAMA_ASURANSI VARCHAR(50);






/* Migrating column for class RegisterAnuitas */







ALTER TABLE dbo.REGISTERANUITAS ALTER COLUMN NO_POLIS_ANUITAS VARCHAR(30);






/* Migrating column for class RegisterCIF */







ALTER TABLE dbo.REGISTERCIF ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN nama_lengkap VARCHAR(100);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN alamat_jalan VARCHAR(200);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN alamat_kota VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN alamat_kode_pos VARCHAR(30);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN alamat_telepon VARCHAR(30);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN pekerjaan VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN nama_perusahaan VARCHAR(100);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN alamat_kantor_jalan VARCHAR(200);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN alamat_kantor_kota VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN alamat_kantor_propinsi VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN ALAMAT_SURAT_JALAN VARCHAR(200);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN ALAMAT_SURAT_KOTA VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN ALAMAT_SURAT_PROPINSI VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN ALAMAT_SURAT_KODE_POS VARCHAR(30);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN NPWP VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN NO_REK_AUTODEBET VARCHAR(20);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN NAMA_REK_AUTODEBET VARCHAR(50);






/* Migrating column for class RegisterNasabahRekening */







ALTER TABLE dbo.REGISTERNASABAHREKENING ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Altering table for class RegisterNasabahRekening */

ALTER TABLE REGISTERNASABAHREKENING
  ADD ALAMAT_JALAN2 VARCHAR(200),
  ALAMAT_KANTOR_TELEPON2 VARCHAR(30),
  ALAMAT_TELEPON2 VARCHAR(30);

/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN alamat_jalan VARCHAR(200);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN alamat_kota VARCHAR(50);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN alamat_kode_pos VARCHAR(30);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN alamat_telepon VARCHAR(30);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN alamat_kantor_jalan VARCHAR(200);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN alamat_kantor_kota VARCHAR(50);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN alamat_kantor_propinsi VARCHAR(50);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN ALAMAT_SURAT_JALAN VARCHAR(200);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN ALAMAT_SURAT_KOTA VARCHAR(50);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN ALAMAT_SURAT_PROPINSI VARCHAR(50);






/* Migrating column for class RegisterUbahAlamat */







ALTER TABLE dbo.REGISTERUBAHALAMAT ALTER COLUMN ALAMAT_SURAT_KODE_POS VARCHAR(30);






/* Altering table for class RegisterUbahAlamat */

ALTER TABLE REGISTERUBAHALAMAT
  ADD ALAMAT_JALAN2 VARCHAR(200),
  ALAMAT_KANTOR_TELEPON2 VARCHAR(30),
  ALAMAT_TELEPON2 VARCHAR(30);

/* Migrating column for class RegNRAhliWaris */







ALTER TABLE dbo.REGNRAHLIWARIS ALTER COLUMN NAMA_LENGKAP VARCHAR(100);






/* Migrating column for class RegNRAhliWaris */







ALTER TABLE dbo.REGNRAHLIWARIS ALTER COLUMN NO_REFERENSI VARCHAR(50);






/* Migrating column for class RekeningAnuitas */







ALTER TABLE dbo.REKENINGANUITAS ALTER COLUMN NAMA_ASURANSI VARCHAR(50);






/* Migrating column for class RekeningAnuitas */







ALTER TABLE dbo.REKENINGANUITAS ALTER COLUMN NO_POLIS_ANUITAS VARCHAR(30);






/* Migrating column for class RekeningWasiatUmmat */







ALTER TABLE dbo.REKENINGWASIATUMMAT ALTER COLUMN NO_POLIS VARCHAR(30);






/* Generating enumeration eJenisTransGiroPI */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisTransGiroPI';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransGiroPI', 'D', 'manual debet');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransGiroPI', 'K', 'manual kredit');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransGiroPI', 'P', 'profit');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransGiroPI', 'B', 'biaya');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransGiroPI', 'T', 'modul transaksi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransGiroPI', 'F', 'modul portofolio');

/* Generating enumeration FTBoolean */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'FTBoolean';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('FTBoolean', 'F', 'false');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('FTBoolean', 'T', 'true');

/* Generating enumeration NYBoolean */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'NYBoolean';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('NYBoolean', 'F', 'no');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('NYBoolean', 'T', 'yes');

/* Generating enumeration eJournalKind */

DELETE FROM Enum_Int WHERE Enum_Name = 'eJournalKind';

INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJournalKind', 10, 'Kas');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJournalKind', 11, 'Umum');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJournalKind', 12, 'Awal');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJournalKind', 13, 'Tutup Buku');

/* Generating enumeration eAccountState */

DELETE FROM Enum_Int WHERE Enum_Name = 'eAccountState';

INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAccountState', 10, 'InActive');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAccountState', 11, 'Active');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAccountState', 12, 'Dead');

/* Generating enumeration eStatus */

DELETE FROM Enum_Int WHERE Enum_Name = 'eStatus';

INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStatus', 1, 'No Journal');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStatus', 2, 'Journalized');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStatus', 3, 'Closed');

/* Generating enumeration eTimeGroup */

DELETE FROM Enum_Int WHERE Enum_Name = 'eTimeGroup';

INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eTimeGroup', 11, 'daily');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eTimeGroup', 12, 'weekly');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eTimeGroup', 13, 'two weekly');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eTimeGroup', 14, 'monthly');

/* Generating enumeration ePeriodState */

DELETE FROM Enum_Int WHERE Enum_Name = 'ePeriodState';

INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('ePeriodState', 10, 'Lower');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('ePeriodState', 15, 'Current');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('ePeriodState', 20, 'Upper');

/* Generating enumeration eGroupingMode */

DELETE FROM Enum_Int WHERE Enum_Name = 'eGroupingMode';

INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eGroupingMode', 1, 'One');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eGroupingMode', 2, 'Two');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eGroupingMode', 3, 'Three');
INSERT INTO Enum_Int (Enum_Name, Enum_Value, Enum_Description) VALUES ('eGroupingMode', 4, 'Four');

/* Generating enumeration eGLTransferMode */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eGLTransferMode';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eGLTransferMode', 'D', 'detail');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eGLTransferMode', 'C', 'compress');

/* Generating enumeration eJenisTransaksiDPLK */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisTransaksiDPLK';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'A', 'Pendaftaran');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'B', 'Pembayaran Premi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'C', 'Biaya Pengelolaan Dana');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'D', 'Biaya Administrasi Tahunan');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'E', 'Penarikan Dana');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'F', 'Pengubahan Jenis Investasi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'G', 'Bagi Hasil');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'H', 'Pengalihan ke DPLK Lain');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'I', 'Pengalihan dari DPLK Lain');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'J', 'Pengambilan Manfaat');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'K', 'Iuran Peserta');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'X', 'Biaya Transaksi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'Z', 'Pajak');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'M', 'Transaksi DPLK Manual');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'V', 'Penarikan Dana 30%');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'W', 'Penarikan Dana PHK');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'O', 'Pengalihan dari DPPK Lain');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiDPLK', 'P', 'Pengalihan dari DPK Lain');

/* Generating enumeration eCaraBayarIuranDPLK */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eCaraBayarIuranDPLK';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eCaraBayarIuranDPLK', 'T', 'Transfer');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eCaraBayarIuranDPLK', 'C', 'Cash');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eCaraBayarIuranDPLK', 'K', 'Kliring');

/* Generating enumeration eJenisTransaksiInvestasi */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisTransaksiInvestasi';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiInvestasi', 'A', 'Alokasi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiInvestasi', 'B', 'Profit');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiInvestasi', 'C', 'Tutup');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiInvestasi', 'D', 'Biaya');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiInvestasi', 'E', 'Potensi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiInvestasi', 'F', 'Kapitalisir');

/* Generating enumeration eHubunganKeluarga */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eHubunganKeluarga';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '0', 'Peserta');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '1', 'Ayah');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '2', 'Ibu');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '3', 'Anak');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '4', 'Kakak');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '5', 'Adik');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '6', 'Istri');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '7', 'Suami');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eHubunganKeluarga', '8', 'Lain-lain');

/* Generating enumeration eReferensiJenisSalesForce */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eReferensiJenisSalesForce';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eReferensiJenisSalesForce', 'A', 'Internal');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eReferensiJenisSalesForce', 'B', 'Eksternal');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eReferensiJenisSalesForce', 'C', 'Kolektor');

/* Generating enumeration eReferensiTransaksiSalesForce */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eReferensiTransaksiSalesForce';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eReferensiTransaksiSalesForce', 'K', 'Beri Komisi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eReferensiTransaksiSalesForce', 'B', 'Bayar Komisi');

/* Generating enumeration eStatusRekeningDPLK */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eStatusRekeningDPLK';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStatusRekeningDPLK', 'A', 'Aktif');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStatusRekeningDPLK', 'N', 'Inaktif');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStatusRekeningDPLK', 'S', 'Suspend');

/* Generating enumeration eJenisSalesForce */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisSalesForce';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisSalesForce', '1', 'Internal');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisSalesForce', '2', 'Channeling');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisSalesForce', '3', 'Collecting');

/* Generating enumeration eJenisMarketingFee */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisMarketingFee';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisMarketingFee', 'A', 'Recruiting');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisMarketingFee', 'B', 'Channeling');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisMarketingFee', 'C', 'Collecting');

/* Generating enumeration eJenisInvestasi */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisInvestasi';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisInvestasi', 'A', 'Tetap');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisInvestasi', 'B', 'Tidak Tetap');

/* Generating enumeration eJenisKelamin */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisKelamin';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisKelamin', 'P', 'Pria');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisKelamin', 'W', 'Wanita');

/* Generating enumeration eSumberVoucher */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eSumberVoucher';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eSumberVoucher', 'T', 'Transaksi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eSumberVoucher', 'I', 'Investasi');

/* Generating enumeration eAuthorizationFlag */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eAuthorizationFlag';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAuthorizationFlag', 'N', 'new');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAuthorizationFlag', 'U', 'updated');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAuthorizationFlag', 'D', 'deleted');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAuthorizationFlag', 'E', 'authorized');

/* Generating enumeration eBranchStatus */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eBranchStatus';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBranchStatus', 'B', 'Branch');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBranchStatus', 'S', 'Sub-branch');

/* Generating enumeration eStdOperationType */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eStdOperationType';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStdOperationType', 'D', 'Delete');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStdOperationType', 'E', 'Edit');

/* Generating enumeration eKirimStatemen */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eKirimStatemen';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eKirimStatemen', 'N', 'Tidak dikirim');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eKirimStatemen', 'R', 'Rumah');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eKirimStatemen', 'K', 'Kantor');

/* Generating enumeration eStatusAhliWaris */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eStatusAhliWaris';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStatusAhliWaris', 'A', 'Aktif');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eStatusAhliWaris', 'N', 'Tidak Aktif');

/* Generating enumeration eBatchType */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eBatchType';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchType', 'R', 'Registration');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchType', 'T', 'Transaction');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchType', 'P', 'Premi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchType', 'I', 'Investment');

/* Generating enumeration eBatchSubType */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eBatchSubType';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchSubType', 'M', 'Manual Input');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchSubType', 'T', 'Teller Transaction');

/* Generating enumeration eAccLinkType */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eAccLinkType';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAccLinkType', 'S', 'Single');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eAccLinkType', 'C', 'Custom');

/* Generating enumeration eOperationCode */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eOperationCode';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eOperationCode', 'F', 'Free');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eOperationCode', 'E', 'Edit');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eOperationCode', 'N', 'New');

/* Generating enumeration eJenisUbahStatus */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisUbahStatus';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisUbahStatus', 'I', 'Masuk');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisUbahStatus', 'O', 'Keluar');

/* Generating enumeration eDaftarKeluarTrans */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eDaftarKeluarTrans';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eDaftarKeluarTrans', 'R', 'Daftar');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eDaftarKeluarTrans', 'O', 'Keluar');

/* Generating enumeration eJenisTransaksiPremi */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisTransaksiPremi';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiPremi', 'T', 'Titipan Premi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiPremi', 'S', 'Setoran Premi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisTransaksiPremi', 'M', 'Transaksi Premi Manual');

/* Generating enumeration eBatchStatus */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eBatchStatus';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchStatus', 'O', 'Buka');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchStatus', 'C', 'Tutup');

/* Generating enumeration eJenisBiaya */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisBiaya';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisBiaya', 'T', 'Tunai');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisBiaya', 'S', 'SKN');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisBiaya', 'R', 'RTGS');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisBiaya', 'P', 'Pindah Buku');

/* Generating enumeration eJenisRegisterCIF */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisRegisterCIF';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'A', 'Alamat');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'W', 'Ahli Waris');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'K', 'Status Kerja');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'U', 'Wasiat Ummat');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'P', 'Paket Investasi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'I', 'Iuran');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'N', 'Anuitas');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'D', 'Auto Debet');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisRegisterCIF', 'Z', 'Lain-lain');

/* Generating enumeration eKategoriSubJnsTransLRInv */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eKategoriSubJnsTransLRInv';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eKategoriSubJnsTransLRInv', 'R', 'Rugi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eKategoriSubJnsTransLRInv', 'L', 'Laba');

/* Generating enumeration eJenisPenerimaanManfaat */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisPenerimaanManfaat';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisPenerimaanManfaat', 'B', 'Pensiun Biasa');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisPenerimaanManfaat', 'D', 'Pensiun Dipercepat');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisPenerimaanManfaat', 'C', 'Pensiun Cacat');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisPenerimaanManfaat', 'J', 'Pensiun Meninggal');

/* Generating enumeration eJnsTransInv */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJnsTransInv';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'A', 'Investasi Baru/Alokasi Investasi Tambahan');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'C', 'Tutup Investasi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'B', 'Pembukuan Pendapatan Investasi secara Tunai');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'D', 'Pembukuan Biaya Investasi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'F', 'Rollover Investasi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'G', 'Transaksi Investasi Manual');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'H', 'Transaksi Piutang LR Investasi Manual');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'I', 'Transaksi LR Investasi Manual');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJnsTransInv', 'P', 'Pembukuan Pendapatan Investasi ke Piutang');

/* Generating enumeration eClsfTransaksiInvestasi */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eClsfTransaksiInvestasi';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eClsfTransaksiInvestasi', 'A', 'Piutang Investasi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eClsfTransaksiInvestasi', 'B', 'Piutang LR Investasi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eClsfTransaksiInvestasi', 'C', 'LR Investasi');

/* Generating enumeration eJenisDP */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisDP';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisDP', 'A', 'DPPK');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisDP', 'B', 'DPLK');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisDP', 'C', 'DPK');

