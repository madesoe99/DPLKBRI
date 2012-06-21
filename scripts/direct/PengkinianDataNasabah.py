import string, sys, dafsys
sys.path.append('c:/dafapp/dplk07/script_modules')
import transaksiapi

file_user = 'rekap-12.csv'
SEP = '|'

def DoKoreksi(config):

  fl = open(file_user,'r')
  ls_fl = fl.readlines()
  count = len(ls_fl)
  config.BeginTransaction()
  try:
    I = 0
    while I<=count-1:
      val = ls_fl[I].split(SEP)
      print 'No Peserta              [0]: %s ' %(val[0])
      print 'Nama Lengkap            [1]: %s ' %(val[1])
      print 'Alamat telepon2         [2]: %s ' %(val[2])
      print 'Tanggal Registrasi      [3]: %s ' %(val[3])
      print 'Tempat Lahir            [4]: %s ' %(val[4])
      print 'Tanggal Lahir           [5]: %s ' %(val[5])
      print 'Alamat Jalan            [6]: %s ' %(val[6])
      print 'Alamat rt/rw            [7]: %s ' %(val[7])
      print 'Alamat kelurahan        [8]: %s ' %(val[8])
      print 'Alamat kecamatan        [9]: %s ' %(val[9])
      print 'Alamat kota            [10]: %s ' %(val[10])
      print 'Alamat kode pos        [11]: %s ' %(val[11])
      print 'Alamat telepon         [12]: %s ' %(val[12])
      print 'Pekerjaan              [13]: %s ' %(val[13])
      print 'Nama perusahaan        [14]: %s ' %(val[14])
      print 'Alamat kantor jalan    [15]: %s ' %(val[15])
      print 'Alamat kantor kode pos [16]: %s ' %(val[16])
      print 'Alamat kantor kelurahan[17]: %s ' %(val[17])
      print 'Alamat kantor kecamatan[18]: %s ' %(val[18])
      print 'Alamat kantor kota     [19]: %s ' %(val[19])
      print 'Alamat kantor propinsi [20]: %s ' %(val[20])
      print 'Alamat kantor telepon  [21]: %s ' %(val[21])
      print 'Alamat surat jalan     [22]: %s ' %(val[22])
      print 'Alamat surat rt/rw     [23]: %s ' %(val[23])
      print 'Alamat surat kelurahan [24]: %s ' %(val[24])
      print 'Alamat surat kecamatan [25]: %s ' %(val[25])
      print 'Alamat surat kota      [26]: %s ' %(val[26])
      print 'Alamat surat propinsi  [27]: %s ' %(val[27])
      print 'Alamat surat kode pos  [28]: %s ' %(val[28])
      print 'NPWP                   [29]: %s ' %(val[29])
      print 'Email                  [30]: %s ' %(val[30])
      print '###----------End --------------#'
      UpdateNasabahDPLK(config, val)
      I += 1
    config.Commit()
  except:
    config.Rollback()
    raise 'Error'

def UpdateNasabahDPLK(config, val):
 
  sUpdTrans = "UPDATE NASABAHDPLK \
               SET NAMA_LENGKAP = \'%s',\
               ALAMAT_TELEPON2 = \'%s\',\
               TGL_REGISTRASI = \'%s\',\
               TEMPAT_LAHIR = \'%s\',\
               TANGGAL_LAHIR = \'%s\',\
               ALAMAT_JALAN = \'%s\',\
               ALAMAT_RTRW = \'%s\',\
               ALAMAT_KELURAHAN = \'%s\',\
               ALAMAT_KECAMATAN = \'%s\',\
               ALAMAT_KOTA = \'%s\',\
               ALAMAT_KODE_POS = \'%s\',\
               ALAMAT_TELEPON = \'%s\',\
               PEKERJAAN = \'%s\',\
               NAMA_PERUSAHAAN = \'%s\',\
               ALAMAT_KANTOR_JALAN = \'%s\',\
               ALAMAT_KANTOR_KODE_POS = \'%s\',\
               ALAMAT_KANTOR_KELURAHAN = \'%s\',\
               ALAMAT_KANTOR_KECAMATAN = \'%s\',\
               ALAMAT_KANTOR_KOTA= \'%s\',\
               ALAMAT_KANTOR_PROPINSI = \'%s\',\
               ALAMAT_KANTOR_TELEPON = \'%s\',\
               ALAMAT_SURAT_JALAN = \'%s\',\
               ALAMAT_SURAT_RTRW = \'%s\',\
               ALAMAT_SURAT_KELURAHAN = \'%s\',\
               ALAMAT_SURAT_KECAMATAN = \'%s\',\
               ALAMAT_SURAT_KOTA = \'%s\',\
               ALAMAT_SURAT_PROPINSI = \'%s\',\
               ALAMAT_SURAT_KODE_POS = \'%s\',\
               NPWP = \'%s\',\
               ALAMAT_EMAIL = \'%s\',\
               OPERATION_CODE = \'%s\'\
               WHERE NO_PESERTA = \'%s\'"\
               % (val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10],
                  val[11],val[12],val[13],val[14],val[15],val[16],val[17],val[18],val[19],
                  val[20],val[21],val[22],val[23],val[24],val[25],val[26],val[27],
                  val[28],val[29],val[30],'T',val[0])
  
  config.ExecSQL(sUpdTrans)


## MAIN PROGRAM    
config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
DoKoreksi(config)
    
