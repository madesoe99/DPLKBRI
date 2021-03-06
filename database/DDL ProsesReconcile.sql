

CREATE TABLE DETILRIWAYATGIRO
(
ID_DETIL_GIRO INT PRIMARY KEY,
IS_VALID VARCHAR(1),
IS_CREATED_TRANSACTION VARCHAR(1),
NO_REKENING VARCHAR(20),
NOMINAL FLOAT,
REKENING_SUMBER VARCHAR(20),
ACCOUNT_GIRO VARCHAR(20),
ID_RECONCILE INT,
KETERANGAN VARCHAR (100),
IS_CORPORATE VARCHAR(1)
)

CREATE TABLE RIWAYATGIRO
(
ID_RECONCILE INT PRIMARY KEY,
ACCOUNT_GIRO VARCHAR(20) PRIMARY KEY,
IS_RECONCILED VARCHAR(1),
SUM_NOMINAL FLOAT,
SUM_PROCCED_NOMINAL FLOAT
)

CREATE TABLE PROSESRECONCILE
(
ID_RECONCILE INT PRIMARY KEY,
TANGGAL_TRANSAKSI DATETIME,
WAKTU_MULAI DATETIME,
WAKTU_SELESAI DATETIME
)
