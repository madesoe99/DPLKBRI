/* Create rekening / nasabah table indexes */

/* Index untuk browsing data rekening by branch */
CREATE INDEX rek_branch ON rekeningdplk (kode_cab_daftar);

/* Index untuk browsing data nasabah by nama */
CREATE INDEX nas_name ON nasabahdplk (nama_lengkap);