Hari = {0:'Senin',
        1:'Selasa',
        2:'Rabu',
        3:'Kamis',
        4:"Jum'at",
        5:'Sabtu',
        6:'Minggu'}

bln = { '01'  : 'Januari',
        '02'  : 'Febuari',
        '03'  : 'Maret',
        '04'  : 'April',
        '05'  : 'Mei',
        '06'  : 'Juni',
        '07'  : 'Juli',
        '08'  : 'Agustus',
        '09'  : 'September',
        '10' : 'Oktober',
        '11' : 'November',
        '12' : 'Desember'}

def tgl_indo(config,tgl,jenis,tipe=0):
    if tipe == 0:
        tdate =config.ModLibUtils.DecodeDate(tgl)
    else:
        tdate = tgl
    tanggal = Tanggal(tdate,jenis)
    return tanggal
  
def Tanggal(tdate,jenis):
  from datetime import date
  hari=date(int(tdate[0]),int(tdate[1]),int(tdate[2])).weekday()

  if tdate[2]<=9:
    tgl='0%s' % (tdate[2])
  else:
    tgl='%s' % (tdate[2])
  if tdate[1]<=9:
    bulan='0%s' % (tdate[1])
  else:
    bulan='%s' % (tdate[1])

  tanggal = '%s %s %s' % (tgl, bln[bulan], str(tdate[0]))
  if jenis == 1:
    tanggal = '%s %s %s' % (tgl, bln[bulan].upper(), str(tdate[0]))
  elif jenis == 2:
    tanggal = '%s %s %s' % (tgl, bln[bulan][0:3].upper(), str(tdate[0]))
  elif jenis == 3:
    tanggal = '%s-%s-%s' % (tgl, bulan, str(tdate[0]))
  elif jenis == 4:
    tanggal = '%s ,%s-%s-%s' % (Hari[hari],tgl, bulan, str(tdate[0]))
  elif jenis == 5:
    tanggal = '%s ,%s-%s-%s' % (Hari[hari],tgl, bln[bulan].upper(), str(tdate[0]))
  elif jenis == 6:
    tanggal = '%s ,%s-%s-%s' % (Hari[hari],tgl, bln[bulan], str(tdate[0]))
  elif jenis == 7:
    tanggal = '%s ,%s-%s-%s' % (Hari[hari],tgl, bln[bulan][0:3].upper(), str(tdate[0]))
  elif jenis == 8:
    tanggal = '%s' % (Hari[hari])
  #raise '',tanggal
  return tanggal
