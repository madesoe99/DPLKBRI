def strOQLHistori(kode_jenis_registercif):
  if kode_jenis_registercif == 'A':
    return 'select from HistoriUbahAlamat \
      ( \
        no_referensi, \
        no_peserta, \
        LNasabahDPLK.nama_lengkap as nama_lengkap, \
        user_id, \
        terminal_id, \
        tanggal_histori, \
        self \
      ) then order by no_referensi;'
  elif kode_jenis_registercif == 'D':
    return 'select from HistoriAutoDebet \
      ( \
        no_referensi, \
        no_peserta, \
        LRekeningDPLK.LNasabahDPLK.nama_lengkap as nama_lengkap, \
        user_id, \
        terminal_id, \
        tanggal_histori, \
        self \
      ) then order by no_referensi;'
  elif kode_jenis_registercif == 'I':
    return 'select from HistoriIuran \
      ( \
        no_referensi, \
        no_peserta, \
        LRekeningDPLK.LNasabahDPLK.nama_lengkap as nama_lengkap, \
        user_id, \
        terminal_id, \
        tanggal_histori, \
        self \
      ) then order by no_referensi;'
  elif kode_jenis_registercif == 'K':
    return 'select from HistoriUbahStatusKerja \
      ( \
        no_referensi, \
        no_peserta, \
        LNasabahDPLK.nama_lengkap as nama_lengkap, \
        user_id, \
        terminal_id, \
        tanggal_histori, \
        self \
      ) then order by no_referensi;'
  elif kode_jenis_registercif == 'N':
    return 'select from HistoriAnuitas \
      ( \
        no_referensi, \
        no_peserta, \
        LRekeningDPLK.LNasabahDPLK.nama_lengkap as nama_lengkap, \
        user_id, \
        terminal_id, \
        tanggal_histori, \
        self \
      ) then order by no_referensi;'
  elif kode_jenis_registercif == 'P':
    return 'select from HistoriPindahPaketInvestasi \
      ( \
        no_referensi, \
        no_peserta, \
        LRekeningDPLK.LNasabahDPLK.nama_lengkap as nama_lengkap, \
        user_id, \
        terminal_id, \
        tanggal_histori, \
        self \
      ) then order by no_referensi;'
  elif kode_jenis_registercif == 'U':
    return 'select from HistoriWasiatUmmat \
      ( \
        no_referensi, \
        no_peserta, \
        LRekeningDPLK.LNasabahDPLK.nama_lengkap as nama_lengkap, \
        user_id, \
        terminal_id, \
        tanggal_histori, \
        self \
      ) then order by no_referensi;'
  elif kode_jenis_registercif == 'W':
    return 'select from HistoriAhliWaris \
      ( \
        no_referensi, \
        no_peserta, \
        LNasabahDPLK.nama_lengkap as nama_lengkap, \
        user_id, \
        terminal_id, \
        tanggal_histori, \
        self \
      ) then order by no_referensi;'
  else:
    raise Exception, 'Kesalahan Jenis Histori' + 'Kode jenis register CIF tidak ditemukan.'

def FormShow(form, parameter):
  uipNoData = form.GetUIPartByName('uipNoData')
  qHistori = form.GetPanelByName('qHistori')

  uipNoData.Edit()
  uipNoData.kode_jenis_registercif = parameter.FirstRecord.kode_jenis_registercif

  qHistori.OQLText = strOQLHistori(uipNoData.kode_jenis_registercif)
  qHistori.DisplayData()

