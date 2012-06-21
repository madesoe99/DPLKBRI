def FormShow(form, parameter):

  #cek code number tag parameter
  if parameter.FirstRecord.code == 10000:
    form.Caption = 'Lihat Detil Biaya Administrasi Transaksi'
  elif parameter.FirstRecord.code == 10001:
    form.Caption = 'Lihat Detil Biaya Administrasi Tahunan'
  elif parameter.FirstRecord.code == 10002:
    form.Caption = 'Lihat Detil Biaya Pengelolaan Dana'
  elif parameter.FirstRecord.code == 10003:
    form.Caption = 'Lihat Detil Transaksi Bagi Hasil'
  elif parameter.FirstRecord.code == 10004:
    form.Caption = 'Lihat Detil Biaya Pindah Paket Investasi'
