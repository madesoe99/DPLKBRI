--jangan lupa untuk sinkronisasi data master jenis transaksi DPLK

/* Creating table for class PindahPaketInvestasi */

CREATE TABLE PINDAHPAKETINVESTASI(
  ID_TRANSAKSI INTEGER NOT NULL,
  ID_TRANSAKSI_BADMTRANS INTEGER,
  BIAYA_PINDAH DOUBLE PRECISION,
  COUNT_ADVIS INTEGER,
  SALDO_IURAN_PK DOUBLE PRECISION,
  SALDO_IURAN_PST DOUBLE PRECISION,
  SALDO_IURAN_TMB DOUBLE PRECISION,
  SALDO_PSL DOUBLE PRECISION,
  SALDO_PMB_PK DOUBLE PRECISION,
  SALDO_PMB_PST DOUBLE PRECISION,
  SALDO_PMB_TMB DOUBLE PRECISION,
  SALDO_PMB_PSL DOUBLE PRECISION,
  SALDO_JML_DANA DOUBLE PRECISION,
  SALDO_DIPINDAHKAN DOUBLE PRECISION,
PRIMARY KEY (ID_TRANSAKSI)
);