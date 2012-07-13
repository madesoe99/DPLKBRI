import sys, os
import com.ihsan.lib.trace as trace
import com.ihsan.utils as utils

SEP = '|'

def InsertPeserta(config, filename):
    config.SendDebugMsg('Insert peserta')
    fl = open(filename, 'r')
    try:
      ls_fl = fl.readlines()
      count = len(ls_fl)
      i = 0
      while i <= (count - 1):            
        config.SendDebugMsg(ls_fl[i])
        val = ls_fl[i].split(SEP)
        sSQL1 = "insert into NASABAHDPLK \
                (no_peserta,kode_jenis_usaha,kode_propinsi,kode_pemilikan,\
                nama_lengkap, tgl_registrasi, tempat_lahir,tanggal_lahir,\
                alamat_jalan, alamat_kota, pekerjaan,NPWP,LAST_UPDATE,\
                USER_ID,AUTH_USER_ID,ISCOMMITTED,TERMINAL_ID,\
                KODE_NASABAH_CORPORATE,JENIS_KELAMIN,status_perkawinan,kewarganegaraan)\
                values\
                ('%s','%s','%s','%s','%s',GETDATE(),'%s','%s','%s','%s','%s','%s',GETDATE(),\
                'SYSTEM','SYSTEM','T','10.35.65.162','%s','%s','%s','%s') \
        " % (val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10],val[11],val[5])
        sSQL2 = "insert into REKENINGDPLK \
                (no_peserta, kode_paket_investasi,kode_cab_daftar, usia_pensiun,\
                AKUM_DANA_IURAN_PST, AKUM_DANA_IURAN_PK, akum_dana_peralihan, AKUM_DANA_PENGEMBANGAN,\
                STATUS_DPLK, sumber_dana, tgl_pensiun, USER_ID, AUTH_USER_ID, LAST_UPDATE, LAST_TERMINAL_ID)\
                values \
                ('%s','%s','%s',%s,%s,%s,%s,%s,'A','%s','%s','SYSTEM','SYSTEM',GETDATE(), '10.35.65.162')\
        "
        runSQL(config, sSQL1)
        runSQL(config, sSQL2)
        i += 1
    finally:
      fl.close()
      
def runSQL(config, sSQL):
  res = config.ExecSQL(sSQL)
  if res == -9999:
    raise Exception, 'SQL Error' +  config.GetDBConnErrorInfo()

def GetUploadedFile(parameter, recfile):
  
  sw = parameter.GetStreamWrapperByName("upload"+recfile)
  if sw == None:
    raise "Stream not found"

  filename  = 'c:\\' + utils.ExtractFileName(recfile)
  sw.SaveToFile(filename)
  
  return filename
         
def PrepareStructure(config):
  runSQL(config, "drop table iuranmassal")
  runSQL(config, "create table iuranmassal \
                  (id_batch integer, \
                  no_peserta varchar(20), \
                  iuran_pst float, \
                  iuran_pk float, \
                  keterangan varchar(150))")
  runSQL(config, "create index idx_massal on iuranmassal(no_peserta)")
#   runSQL(config, "create table logiuranmassal \
#                   (tanggal datetime,\
#                   no_peserta varchar(20), \
#                   keterangan varchar(150))")
    
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
    rec = parameter.FirstRecord
    file = rec.filename 

    try:
        config.BeginTransaction()
        try:
#             PrepareStructure(config)
            filename = GetUploadedFile(parameter, file)
            InsertPeserta(config, filename)
#             CleansingDataIuran(config)
#             UpdateTransaksi(config)
            config.Commit()
        except:
            config.Rollback()
            errmsg = str(sys.exc_info()[1])
            raise Exception, 'Upload Iuran Error' +  errmsg
    finally:
        returnpacket.CreateValues(['succeed',1])

    return 0
