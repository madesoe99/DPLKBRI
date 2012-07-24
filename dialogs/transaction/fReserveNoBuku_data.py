import sys
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

modman.loadStdModules(globals(),
  [
    "moduleapi"
  ]
)

#sys.path.append("c:/dafapp/dplk07/script_modules")
#import moduleapi

def reserveNumber(config, params, returns):
  kode_cab = params.FirstRecord.GetFieldByName("cabang.branch_code")
  no_awal  = params.FirstRecord.GetFieldByName("no_awal")
  no_akhir = params.FirstRecord.GetFieldByName("no_akhir")
  
  userid = config.SecurityContext.userid
  
  config.BeginTransaction()
  try:

    countAwal = int(no_awal)
    countAkhir = int(no_akhir)
    while countAwal <= countAkhir:
    
       #config.SendDebugMsg('no : '+ str(countAwal))
       noBuku = '%s' % (moduleapi.MyZFill(str(countAwal), 6))

       oReg = config.CreatePObject('MasterBukuDPLK')
       oReg.no_seri_buku = noBuku
       config.SendDebugMsg('No Seri Buku : '+ str(noBuku))
       oReg.kode_cabang = kode_cab
       config.SendDebugMsg('kode_cab : '+ str(kode_cab))
       oReg.tgl_input  = config.Now()
       oReg.user_id = userid
       config.SendDebugMsg('user id :'+userid)
       oReg.status_buku = 'F'
       
       countAwal = countAwal + 1

    config.Commit()
  except:
    config.Rollback()
    raise Exception, '\n\n%s' % str(sys.exc_info()[1])


