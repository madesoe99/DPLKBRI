import sys, os
import com.ihsan.lib.trace as trace
import com.ihsan.utils as utils

SEP = '|'

def InsertIuran(config, filename):
    config.SendDebugMsg('Insert iuran')
    fl = open(filename, 'r')
    try:
      ls_fl = fl.readlines()
      count = len(ls_fl)
      i = 0
      while i <= (count - 1):            
        config.SendDebugMsg(ls_fl[i])
        val = ls_fl[i].split(SEP)
        sSQL = "INSERT INTO iuranmassal VALUES (%s,'%s',%s,%s,'%s') \
        " % (val[0],val[1][:20],val[2],val[3],val[4][:150])
        runSQL(config, sSQL)
        i += 1
    finally:
      fl.close()
      
def runSQL(config, sSQL):
  res = config.ExecSQL(sSQL)
  if res == -9999:
    raise 'SQL Error', config.GetDBConnErrorInfo()

def GetUploadedFile(parameter, recfile):
  
  sw = parameter.GetStreamWrapperByName("upload"+recfile)
  if sw == None:
    raise "Stream not found"

  filename  = 'c:\\' + utils.ExtractFileName(recfile)
  sw.SaveToFile(filename)
  
  return filename

def UpdateTransaksi(config):
  runSQL(config, "INSERT INTO TRANSAKSIDPLK \
                  select ROW_NUMBER() OVER (ORDER BY no_peserta) + \
                  (select last_id from ID_GEN where id_code = 'TRANSAKSIDPLK') AS Row, \
                  'SYSTEM',GETDATE(),GETDATE(),GETDATE(),'SYSTEM','10.35.65.162','10.35.65.162',\
                  'impor massal '+ keterangan, \
                  iuran_pk, iuran_pst, 0, 0, no_peserta, 'A', 'K', id_batch, 'T', null,\
                  null, null, null,null,null,'000',null,null,null,null,null,null,null,null,null,null\
                  FROM iuranmassal")
  runSQL(config, "update REKENINGDPLK \
                  set akum_dana_iuran_pst = akum_dana_iuran_pst + \
                	(select sum(iuran_pst) from iuranmassal \
                	where REKENINGDPLK.no_peserta = no_peserta)")
  
  runSQL(config, "update REKENINGDPLK \
                  set akum_dana_iuran_pk = akum_dana_iuran_pk + \
                	(select sum(iuran_pk) from iuranmassal \
                	where REKENINGDPLK.no_peserta = no_peserta)")
             
  runSQL(config, "update id_gen \
                  set last_id = last_id + (select count(*) from iuranmassal) \
                  where id_code = 'TRANSAKSIDPLK'")
         
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
            PrepareStructure(config)
            filename = GetUploadedFile(parameter, file)
            InsertIuran(config, filename)
#             CleansingDataIuran(config)
            UpdateTransaksi(config)
            config.Commit()
        except:
            config.Rollback()
            errmsg = str(sys.exc_info()[1])
            raise 'Upload Iuran Error', errmsg
    finally:
        returnpacket.CreateValues(['succeed',1])

    return 0
