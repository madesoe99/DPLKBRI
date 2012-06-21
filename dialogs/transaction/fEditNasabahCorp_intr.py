def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')
  uipNasabahDPLKCorporate = form.GetUIPartByName('uipNasabahDPLKCorporate')
  
  uipRegEditNasabahDPLKCorporate.Edit()
  uipRegEditNasabahDPLKCorporate.kode_nasabah_corporate = uipNasabahDPLKCorporate.kode_nasabah_corporate
  uipRegEditNasabahDPLKCorporate.SetFieldValue('LKepemilikan.kode_pemilikan',uipNasabahDPLKCorporate.GetFieldValue('LKepemilikan.kode_pemilikan'))
  uipRegEditNasabahDPLKCorporate.SetFieldValue('LKepemilikan.keterangan',uipNasabahDPLKCorporate.GetFieldValue('LKepemilikan.keterangan'))
  uipRegEditNasabahDPLKCorporate.SetFieldValue('LJenisUsaha.kode_jenis_usaha',uipNasabahDPLKCorporate.GetFieldValue('LJenisUsaha.kode_jenis_usaha'))
  uipRegEditNasabahDPLKCorporate.SetFieldValue('LJenisUsaha.nama_jenis_usaha',uipNasabahDPLKCorporate.GetFieldValue('LJenisUsaha.nama_jenis_usaha'))
  uipRegEditNasabahDPLKCorporate.NPWP = uipNasabahDPLKCorporate.NPWP
  uipRegEditNasabahDPLKCorporate.no_perjanjian = uipNasabahDPLKCorporate.no_perjanjian
  uipRegEditNasabahDPLKCorporate.no_referensi = uipNasabahDPLKCorporate.no_referensi
  uipRegEditNasabahDPLKCorporate.nama_perusahaan = uipNasabahDPLKCorporate.nama_perusahaan
  uipRegEditNasabahDPLKCorporate.alamat_kantor_jalan = uipNasabahDPLKCorporate.alamat_kantor_jalan
  uipRegEditNasabahDPLKCorporate.alamat_kantor_kelurahan = uipNasabahDPLKCorporate.alamat_kantor_kelurahan
  uipRegEditNasabahDPLKCorporate.alamat_kantor_kecamatan = uipNasabahDPLKCorporate.alamat_kantor_kecamatan
  uipRegEditNasabahDPLKCorporate.alamat_kantor_kota = uipNasabahDPLKCorporate.alamat_kantor_kota
  uipRegEditNasabahDPLKCorporate.alamat_kantor_kode_pos = uipNasabahDPLKCorporate.alamat_kantor_kode_pos
  uipRegEditNasabahDPLKCorporate.alamat_kantor_telepon = uipNasabahDPLKCorporate.alamat_kantor_telepon

  uipRegEditNasabahDPLKCorporate.user_id = app.UserID

  dh = app.ExecuteScript('getsessioninfo',app.CreateValues(['id',1]))
  uipRegEditNasabahDPLKCorporate.terminal_id = dh.FirstRecord.sessioninfo

