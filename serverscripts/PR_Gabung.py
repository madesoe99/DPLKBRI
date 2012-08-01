import time, sys, os
import pyFlexcel
import dafsys4 as dafsys

def CekSumber(config,RekSumber):
    strSQL  = "SELECT a.no_rekening FROM REKENINGDPLK c,REKINVDPLK a, NASABAHDPLK b "
    strSQL += " WHERE a.NO_PESERTA=b.no_peserta AND c.NO_REKENING=a.no_rekening "
    strSQL += " AND REKSUMBER_NO='%s' and pct_alokasi!='100' GROUP BY a.no_rekening" % RekSumber
                
    resSQL = config.CreateSQL(strSQL).RawResult
    
    return resSQL.RecordCount

def GetRekening(config,kode,RekSumber):
    par = "and pct_alokasi!='100'"
    if kode != 'K':
        par = "AND kode_paket_investasi='"+kode+"' and pct_alokasi ='100'"
    strSQL  = "SELECT c.no_rekening,STATUS_DPLK,KODE_NASABAH_CORPORATE,IURAN_PST FROM REKENINGDPLK c,REKINVDPLK a, NASABAHDPLK b "
    strSQL += " WHERE a.NO_PESERTA=b.no_peserta AND c.NO_REKENING=a.no_rekening "
    strSQL += "  AND REKSUMBER_NO='%s'  %s " % (RekSumber,par)
                
    resSQL = config.CreateSQL(strSQL).RawResult
    Norek = resSQL.no_rekening or ''
    if kode == 'K':
        CS = CekSumber(config,RekSumber)
        if CS > 1: Norek =''
        
    return Norek, resSQL.STATUS_DPLK or '', resSQL.KODE_NASABAH_CORPORATE or '', resSQL.IURAN_PST or 0

def cekPR(config,nama_file):
    strSQL  = "SELECT COUNT(*) JML FROM PROSESRECONCILE WHERE IS_FILE_VALID='T' AND NAMA_FILE='"+nama_file+"'"
    resSQL = config.CreateSQL(strSQL).RawResult
    
    return resSQL.JML or 0

def GetIdGen(config,kode):
    strSQL  = "SELECT LAST_ID FROM ID_GEN WHERE ID_CODE='"+kode+"'"
    resSQL = config.CreateSQL(strSQL).RawResult
    
    return resSQL.LAST_ID or 0

def UpdateIdGen(config,kode,id):
    strSQL  = "UPDATE ID_GEN SET LAST_ID="+id+" WHERE ID_CODE='"+kode+"'"
    resSQL = config.ExecSQL(strSQL)

def InputTabelDetail(config,Data):
    iSQL = "INSERT INTO DETILRIWAYATGIRO (IS_VALID,IS_CREATED_TRANSACTION,NOMINAL,REKENING_SUMBER,NO_REKENING,ACCOUNT_GIRO,ID_RECONCILE,KETERANGAN,ID_DETIL_GIRO,IS_CORPORATE) "
    iSQL += "VALUES ('%(is_valid)s','F',%(nominal)s,'%(sumber)s','%(NoRek)s','%(acc_giro)s',%(id_reconcile)s,'%(ket)s',%(id_d)s,'%(is_corporate)s')" % Data

    input = config.ExecSQL(iSQL)
    if (input == 0):
       raise Exception, 'Gagal!!'

def UploadData(config,rec):
    acc_giro = rec[1]
    y,m,d = config.ModLibUtils.DecodeDate(config.Now())[:3]
    tgl =str(d).zfill(2)+str(m).zfill(2)+str(y)
    nama_file = rec[0]+'_'+acc_giro+'_'+tgl+'.xls'    
    CPR = cekPR(config,nama_file)
    if CPR > 0: return 0
    hfilename = config.GetGlobalSetting('RECONCILE_FILE_DIR')+'\\'+nama_file
    remarks ='barhasil baca file'
    
    if not os.path.exists(hfilename):
        remarks ='file '+nama_file+' tidak ditemukan'

    PR = config.CreatePObject('ProsesReconcile')
    PR.tanggal_transaksi  = int(config.Now())
    PR.waktu_mulai        = config.Now()
    PR.nama_file          = nama_file
    PR.jenis_reconcile    = 'M'
    PR.is_file_valid      = 'F'
    PR.keterangan         = remarks
    id_r = PR.id_reconcile

    RG = config.CreatePObject('RiwayatGiro')
    RG.account_giro   = acc_giro
    RG.id_reconcile   = id_r
    RG.is_reconciled  = 'F'
    RG.is_pindahbuku  = 'F'
    RG.sum_pindahbuku  = 0
    
    #print id_r
    config.Commit()
    
    if os.path.exists(hfilename):
        config.BeginTransaction()    
        try:        
            oParameter = config.CreatePObjImplProxy('Parameter')
            oParameter.Key = 'MIN_JML_IURAN_PST'
            MIN_JML_IURAN_PST = oParameter.Numeric_Value

            id_detil = GetIdGen(config,'DETILRIWAYATGIRO')
            owb = pyFlexcel.Open(hfilename)
            owb.ActivateWorksheet('Sheet1')

            ulangi = True
            sum_nominal =0
            j=1
            while ulangi :
                i = j+1
                no = owb.GetCellValue(i,1)
                if no not in (None, ''):
                    nominal = float(owb.GetCellValue(i,2) or 0)
                    sumber = str(owb.GetCellValue(i,1) or '')
                    sum_nominal += nominal

                    NoRek, status, is_korporat, iuran_pst = GetRekening(config,rec[0], sumber)
                    
                    ket =''
                    is_corporate ='T'
                    is_valid = 'T'
                    if NoRek == '':
                      ket = 'Rekening DPLK tidak ditemukan'
                      is_valid = 'F'
                    elif status == 'N':
                      ket = 'Status DPLK sudah Non Aktif'
                      is_valid = 'F'
                    elif nominal <= 0:
                      ket = 'Nominal Tidak valid'
                      is_valid = 'F'
                    elif is_korporat == '':
                      is_corporate ='F'
                      if nominal < iuran_pst or nominal < MIN_JML_IURAN_PST:
                        ket = 'Untuk Peserta Perorangan, nominal angsuran tidak boleh kurang dari nominal iuran peserta !!'
                        is_valid = 'F'

                    Data={'id_d':id_detil,'NoRek':NoRek,'is_valid':is_valid,'ket':ket,'nominal':nominal,'sumber':sumber,'acc_giro':acc_giro,'id_reconcile':id_r,'is_corporate':is_corporate}

                    input = InputTabelDetail(config,Data)
                    id_detil += 1
                    j +=1
                else:
                    ulangi = False

            UpdateIdGen(config,'DETILRIWAYATGIRO',str(id_detil))

            PR.waktu_selesai   = config.Now()
            PR.is_file_valid   = 'T'
            RG.sum_nominal     = sum_nominal
            
            config.Commit()         
        except:
            config.Rollback()
            print str(sys.exc_info()[1])
            return 
        
def GetGiro(config):
    acc_giro = config.SysVarIntf.GetStringSysVar('GIROTAMPUNGAN','GiroDPLK')
    acc_giro =  eval(acc_giro)
    for i in acc_giro:
        UploadData(config,i)

        
        #-- MAIN
if __name__ == '__main__': 
    config = dafsys.OpenConfig('c:/dafapp/dplk/default.cfg')
    GetGiro(config)
    #UploadData(config)
  
  
  
