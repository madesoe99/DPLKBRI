import time, sys, os
import pyFlexcel
import dafsys4 as dafsys

def GetRekening(config,NoRek):
    strSQL  = "SELECT STATUS_DPLK,KODE_NASABAH_CORPORATE, IURAN_PST FROM REKINVDPLK a, NASABAHDPLK b WHERE a.NO_PESERTA=b.no_peserta AND no_rekening='"+NoRek+"'"
    resSQL = config.CreateSQL(strSQL).RawResult
    
    return resSQL.STATUS_DPLK or '', resSQL.KODE_NASABAH_CORPORATE or '', resSQL.IURAN_PST or 0

def cekPR(config,nama_file):
    strSQL  = "SELECT COUNT(*) JML FROM PROSESRECONCILE WHERE IS_FILE_VALID='T' AND TANGGAL_TRANSAKSI='2012-07-11' AND NAMA_FILE='"+nama_file+"'"
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

def UploadData(config):
    y,m,d = config.ModLibUtils.DecodeDate(config.Now())[:3]
    tgl =str(d).zfill(2)+str(m).zfill(2)+str(y)
    nama_file = 'E_CHANNEL_'+tgl+'.xls'
    CPR = cekPR(config, nama_file)
    if CPR > 0: return 0

    PR = config.CreatePObject('ProsesReconcile')
    PR.tanggal_transaksi  = int(config.Now())
    PR.waktu_mulai        = config.Now()
    PR.nama_file          = nama_file
    PR.jenis_reconcile    = 'E'
    PR.is_file_valid      = 'F'
    id_r = PR.id_reconcile
    config.Commit()
    
    config.BeginTransaction()    
    try:
        acc_giro = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING','GiroPenampungan')
        
        RG = config.CreatePObject('RiwayatGiro')
        RG.account_giro   = acc_giro
        RG.id_reconcile   = id_r
        RG.is_reconciled  = 'F'
        
        id_detil = GetIdGen(config,'DETILRIWAYATGIRO')
        hfilename = config.GetGlobalSetting('RECONCILE_FILE_DIR')+'\\'+nama_file
        owb = pyFlexcel.Open(hfilename)
        owb.ActivateWorksheet('Sheet1')

        ulangi = True
        sum_nominal =0
        j=1
        while ulangi :
            i = j+1
            no = owb.GetCellValue(i,1)
            if no not in (None, ''):
                NoRek = str(owb.GetCellValue(i,1) or '')
                nominal = float(owb.GetCellValue(i,2) or 0)
                sumber = str(owb.GetCellValue(i,3) or '')
                status, is_korporat, iuran_pst = GetRekening(config, NoRek)
                sum_nominal += nominal
                
                ket =''
                is_corporate ='T'
                is_valid = 'T'
                if status == '':
                  ket = 'Rekening tidak ditemukan'
                  is_valid = 'F'
                elif status == 'N':
                  ket = 'Status DPLK sudah Non Aktif'
                  is_valid = 'F'
                elif nominal <= 0:
                  ket = 'Nominal Tidak valid'
                  is_valid = 'F'
                elif is_korporat == '':
                  is_corporate ='F'
                  if nominal < iuran_pst :
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
        
#-- MAIN
if __name__ == '__main__':
  config = dafsys.OpenConfig('c:/dafapp/dplk/default.cfg')
  UploadData(config)
  
  
