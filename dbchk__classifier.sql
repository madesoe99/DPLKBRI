-- Classifier error check for entity Investasi
SELECT * FROM INVESTASI WHERE 
KODE_JNS_INVESTASI NOT IN ('D', 'O', 'R') AND KODE_JNS_INVESTASI IS NOT NULL
;

-- Classifier error check for entity RegisterCIF
SELECT * FROM REGISTERCIF WHERE 
KODE_JENIS_REGISTERCIF NOT IN ('A', 'K', 'U', 'P', 'D', 'N', 'W', 'I', 'Z') AND KODE_JENIS_REGISTERCIF IS NOT NULL
;

-- Classifier error check for entity RegisterInvestasi
SELECT * FROM REGISTERINVESTASI WHERE 
KODE_JNS_INVESTASI NOT IN ('D', 'O', 'R') AND KODE_JNS_INVESTASI IS NOT NULL
;

-- Classifier error check for entity RincianInvestasi
SELECT * FROM RINCIANINVESTASI WHERE 
KODE_JNS_INVESTASI NOT IN ('D', 'O', 'R') AND KODE_JNS_INVESTASI IS NOT NULL
;

-- Classifier error check for entity RincianRegisterInvestasi
SELECT * FROM RINCIANREGISTERINVESTASI WHERE 
KODE_JNS_INVESTASI NOT IN ('A', 'B', 'C') AND KODE_JNS_INVESTASI IS NOT NULL
;

-- Classifier error check for entity TransaksiDPLK
SELECT * FROM TRANSAKSIDPLK WHERE 
KODE_JENIS_TRANSAKSI NOT IN ('C', 'A', 'D', 'K', 'J', 'B', 'I', 'H', 'G', 'E', 'W', 'V', 'X', 'M', 'G') AND KODE_JENIS_TRANSAKSI IS NOT NULL
;

-- Classifier error check for entity TransaksiInvestasi
SELECT * FROM TRANSAKSIINVESTASI WHERE 
CLSFTRANSAKSIINVESTASI NOT IN ('A', 'B', 'C', 'D', 'E') AND CLSFTRANSAKSIINVESTASI IS NOT NULL
;

-- Classifier error check for entity TransaksiPremi
SELECT * FROM TRANSAKSIPREMI WHERE 
JENIS_TRANSAKSI NOT IN ('T', 'S', 'M') AND JENIS_TRANSAKSI IS NOT NULL
;

-- Classifier error check for entity TransLRInvestasi
SELECT * FROM TRANSLRINVESTASI WHERE 
JENIS NOT IN ('K', 'B', 'U', 'H', 'O', 'R') AND JENIS IS NOT NULL
;

-- Classifier error check for entity TransPiutangInvestasi
SELECT * FROM TRANSPIUTANGINVESTASI WHERE 
JENIS NOT IN ('B', 'J', 'S', 'R', 'V', 'T') AND JENIS IS NOT NULL
;

