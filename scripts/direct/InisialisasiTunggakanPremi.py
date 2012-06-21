import dafsys
import string

def KoreksiTunggakanPremi(config):

    dictBulanRomawi = {'01':'I','02':'II','03':'III','04':'IV',\
                     '05':'V','06':'VI','07':'VII','08':'VIII', \
                     '09':'IX','10':'X','11':'XI','12':'XII'}

    config.BeginTransaction()
    
    blnNow = config.FormatDateTime('mm', config.Now())
    thnNow = config.FormatDateTime('yyyy', config.Now())
    
    bulan_romawi = '%s' % (dictBulanRomawi[blnNow])
    
    try:
       sSQL = "SELECT r.no_peserta,r.bln_tunggakan_wasiat_ummat, r.kewajiban_wasiat_ummat \
                 FROM REKENINGDPLK r\
                WHERE  STATUS_DPLK = 'A' \
                  AND STATUS_WASIAT_UMMAT = 'T' \
                  AND bln_tunggakan_wasiat_ummat > 0 \
                ORDER BY R.NO_PESERTA "
  
       rSQL = config.CreateSQL(sSQL).RawResult
       no = 100
  
       while not rSQL.Eof:
           no_surat = str(no)+'/BMI/DPLK-PREMI/'+bulan_romawi+'/'+str(thnNow)
           print 'peserta  : ' + rSQL.no_peserta
           print 'no surat : ' + no_surat
    
           oReg = config.CreatePObject('TunggakanPremi')
           oReg.no_peserta    = rSQL.no_peserta
           oReg.No_Surat      = no_surat
           oReg.bln_tunggakan = rSQL.bln_tunggakan_wasiat_ummat or 0
           oReg.nom_tunggakan = rSQL.kewajiban_wasiat_ummat or 0.0
           
           oR = config.CreatePObjImplProxy('RekeningDPLK')
           oR.Key = oReg.no_peserta
           oR.collectivity_wasiat_ummat = 'F'
                      
           no = no + 1               
                      
           rSQL.Next()
           
           #UpdateRekeningDPLK(config)
           
       config.Commit()
    except:
       config.Rollback()
       raise
  
def UpdateRekeningDPLK(config):
    
           sUpdRek = "UPDATE REKENINGDPLK \
                         SET COLLECTIVITY_WASIAT_UMMAT = 'F' \
                         WHERE  STATUS_DPLK = 'A' \
                         AND STATUS_WASIAT_UMMAT = 'T' \
                         AND bln_tunggakan_wasiat_ummat > 0 "\
                         
           config.ExecSQL(sUpdRek)

## MAIN PROGRAM    
#config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
config = dafsys.OpenConfig('c:/dafapp/dplk07/testprod.cfg')
KoreksiTunggakanPremi(config)    

