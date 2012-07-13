import sys,string,time
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

MUAMALAT_PASSBOOK_MAXLINE = 32
MUAMALAT_TOP_PAGE_MAXLINE = 14
FORMAT_MUAMALAT = 3

class record:
    pass

def DAFScriptMain(config, parameter, returns):
    returns.CreateValues(['Is_Error', 1], ['Error_Message', 'Tidak ada aksi'])
    return 1


def GetInfoPassbook(config, parameter, returns):

    status = returns.CreateValues(
        ['Is_Err', 0], 
        ['Err_Message', ''],
        ['Nama', ''],
        ['BarisCetakTerakhir', 0]
    )
    try:    
        No_Peserta = parameter.FirstRecord.No_Peserta
        Rekening = config.CreatePObjImplProxy('RekeningDPLK')
        Rekening.key = No_Peserta
        
        if Rekening.isnull:
            raise Exception, "" + "Nomor Peserta Tidak Ditemukan"
        
        sReg = "SELECT * \
        FROM registerpassbook \
        WHERE no_peserta = '%s'" % No_Peserta
        RegisterPassbook = config.CreateSQL(sReg).RawResult
        
        if Rekening.has_passbook <> 'T' or RegisterPassbook.Eof:
            raise Exception, "" + "Rekening Tidak Memiliki Layanan Passbook"
          
        # Cari objek nasabah
        Nasabah = Rekening.LNasabahDPLK
        Nama = Nasabah.Nama_Lengkap
            
        BarisCetakTerakhir = (RegisterPassbook.Baris_Cetak_Terakhir or 0)
        PASSBOOK_MAXLINE = MUAMALAT_PASSBOOK_MAXLINE
            
        if BarisCetakTerakhir == None : BarisCetakTerakhir = 0
        if BarisCetakTerakhir >= PASSBOOK_MAXLINE : BarisCetakTerakhir -= PASSBOOK_MAXLINE

        status.Nama = Nama
        status.BarisCetakTerakhir = BarisCetakTerakhir
    except:
        status.Is_Err = 1
        status.Err_Message = str(sys.exc_info()[1])
        
    return 1

    
    
def PrintPassbookTransaction(config, parameter, returnpacket):

  def GetJenisMutasi(TransactionData):    
    if TransactionData.mutasi_total < 0.0 or TransactionData.kode_jenis_transaksi in ['J','V','W']:
      jenis_mutasi = 'D'
    else:
      jenis_mutasi = 'C'
      
    return jenis_mutasi
    
  def CountTransactionData(No_Peserta,add_condition):
      strSQL = "select count(*) \
            from TransaksiDPLK t \
            where t.No_Peserta= '%s' \
            and kode_jenis_transaksi not in ('A','B') \
            and isCommitted = 'T' and %s "\
            %(No_Peserta,add_condition)
            
      config.SendDebugMsg(strSQL)      
      resSQL = config.CreateSQL(strSQL).RawResult
      return resSQL.GetFieldValueAt(0)

  def GetTransactionData(No_Peserta,add_condition):
      strSQL = "\
        select tgl_transaksi \
          , id_transaksi \
          , kode_jenis_transaksi \
          , isnull(kode_transaksi_manual,'M') as kode_transaksi_manual \
          , isnull(mutasi_peralihan,0.0) + isnull(mutasi_pengembangan,0.0) + isnull(mutasi_iuran_pst,0.0) + isnull(mutasi_iuran_pk,0.0) as mutasi_total \
          , substring(keterangan,21,10) as keterangan \
          , substring(keterangan,1,26) as keteranganM \
          , ispindahpaket, user_id \
        from TransaksiDPLK t\
        where no_peserta = '%s' \
          and kode_jenis_transaksi not in ('A','B') \
          and isCommitted = 'T' and %s\
        order by tgl_transaksi, id_transaksi  " \
        % (No_Peserta, add_condition)
      config.SendDebugMsg(strSQL)
    
      return config.CreateSQL(strSQL).RawResult
      
  def ConstructReportTransPassbook(config,RegisterPassbook,MulaiBaris,TglMulai,isCetakUlang):
      
      date_globalformat = 'mm-dd-yyyy'
  
      # Jika request adalah cetak ulang maka query tanggal
      if isCetakUlang:
        dateQueryCondition = " t.tgl_transaksi >= '%s' " \
                             % config.FormatDateTime(date_globalformat,TglMulai)
      else:          
        # -- ambil info data tanggal dan id detil yang sudah tercetak terakhir
        Id_Detil_Terakhir = RegisterPassbook.ID_Transaksi or 0
        t = RegisterPassbook.Tanggal_Cetak_Terakhir or (1899,1,1,0,0,0,0,0,0)
        TglMulai = config.ModLibUtils.EncodeDate(t[0],t[1],t[2])
                              
        dateQueryCondition = " t.tgl_transaksi >= '%s' and  \
                               t.id_transaksi >  %d  " \
                             % (config.FormatDateTime(date_globalformat,TglMulai), RegisterPassbook.ID_Transaksi or 0)
                                    
      config.SendDebugMsg('SReport %s' % dateQueryCondition)
      # Hitung Transaksi
      TotalTransaksi = 0
      TotalTransaksi += CountTransactionData(No_Peserta,dateQueryCondition)
  
      if TotalTransaksi <= 0 :
         raise Exception, '\nPERINGATAN' + 'Tidak Ada Transaksi Yang Dicetak'
  
      # Data Transaksi yang dicetak
      ReportData = chr(15)
      
      TransactionData = GetTransactionData(No_Peserta,dateQueryCondition)
      TransactionData.First()
      
      sTglMulai = config.FormatDateTime(date_globalformat,TglMulai)
      if isCetakUlang : saldo_awal = moduleapi.GetSaldoAwal(config,No_Peserta,sTglMulai)
      else : saldo_awal = moduleapi.GetSaldoById(config,No_Peserta,Id_Detil_Terakhir)
      config.SendDebugMsg('S_Report : nompst = %s; saldo awal %s' % (No_Peserta, str(saldo_awal)))
  
      dictDataTransaksi = {
          'NO'           : '',
          'TANGGAL'      : '',
          'SANDI'        : '',
          'JENIS_MUTASI' : ' ',
          'NILAI_MUTASI' : '',
          'SALDO'        : '',
          'USER'         : ''         
      }
      
  
      config.SendDebugMsg('SReport1')
      ROWFORMAT = '%(NO)2s      %(TANGGAL)s        %(SANDI)s     %(NILAI_MUTASI)23s  %(JENIS_MUTASI)s  %(SALDO)28s   %(USER)-8s'
  
      PASSBOOK_MAXLINE = MUAMALAT_PASSBOOK_MAXLINE
      TOP_PAGE_MAXLINE = MUAMALAT_TOP_PAGE_MAXLINE
                  
      TopMargin = 5 * '\n'
      LeftMargin = 1 * ' '            
      
      ReportData += TopMargin
  
      #Atur Posisi Baris Mulai di print
  
      Baris = MulaiBaris
      for i in range(1,Baris):
          if i == TOP_PAGE_MAXLINE + 1 :
             ReportData +=  2 * '\n'
          ReportData += '\n'
      
      id_detil_terakhir = 0
      config.SendDebugMsg('SReport2')
      while not TransactionData.Eof:
          #Ganti Halaman
          if Baris > PASSBOOK_MAXLINE:
             ReportData += '\f' + TopMargin
             Baris=1
  
          #Pindah Ke Halaman Bawah
          if Baris == TOP_PAGE_MAXLINE + 1 :
             ReportData +=  2 * '\n'
  
          y, m, d,hh,mm,ss = TransactionData.tgl_transaksi[:6]
          
          dictDataTransaksi['NO'] = str(Baris)               
          dictDataTransaksi['TANGGAL'] = '%s/%s/%s'% (str(d).zfill(2), str(m).zfill(2), str(y))
          
          # -- MAPPING CODE           
          dictDataTransaksi['SANDI'] = TransactionData.kode_jenis_transaksi                  
                         
          Keterangan = (TransactionData.keterangan or '')                
          dictDataTransaksi['KETERANGAN'] = Keterangan[:39].replace('\n',"").replace(chr(13)," ")
  
          # Untuk Jenis Transaksi Debet tidak perlu dicetak kodenya
          jenis_mutasi = GetJenisMutasi(TransactionData)
          dictDataTransaksi['JENIS_MUTASI'] = jenis_mutasi
          
          dictDataTransaksi['NILAI_MUTASI'] = config.FormatFloat('#,##0.00',abs(TransactionData.mutasi_total))
          config.SendDebugMsg('Saldo Awal : ' + str(saldo_awal))
          saldo_awal += TransactionData.mutasi_total
          dictDataTransaksi['SALDO'] = config.FormatFloat('#,##0.00',saldo_awal)
          #
          dictDataTransaksi['USER']  = TransactionData.User_ID[:8]
           
          ReportData += LeftMargin + ROWFORMAT % dictDataTransaksi + '\n'                
  
          BarisCetakTerakhir = Baris
          TglCetakTerakhir = '%s-%s-%s %s:%s:%s'%(y,m,d,hh,mm,ss)
          id_detil_terakhir = TransactionData.ID_Transaksi
          Baris += 1
  
          TransactionData.Next()
          
      
      return ReportData,BarisCetakTerakhir,TglCetakTerakhir,id_detil_terakhir
    

    #-----Main Function ----------------------------------------
    
        
  status = returnpacket.CreateValues(
      ['Is_Err', 0], 
      ['Err_Message', '']
  )
  rec = parameter.FirstRecord
  config.BeginTransaction()
  try :
      No_Peserta = rec.No_Peserta
      
      sReg = "SELECT id_register \
      FROM registerpassbook \
      WHERE no_peserta = '%s'" % No_Peserta
      rReg = config.CreateSQL(sReg).RawResult
      
      RegisterPassbook = config.CreatePObjImplProxy('RegisterPassbook')
      RegisterPassbook.key = rReg.id_register
      
      if RegisterPassbook.isnull:
          raise Exception, "" + "Rekening Tidak Memiliki Layanan Passbook"
      
      sBaseFileName = 'TransaksiPassbook.txt'
      sFileName = config.UserHomeDirectory + sBaseFileName

      BarisMulai = int(rec.BarisMulai)
      isCetakUlang = rec.isCetakUlang
      stButton = rec.stButton
      
      if isCetakUlang :
         TglMulai = rec.TglMulai
      else:
         TglMulai = None

      oFile = open(sFileName,'w')
      ReportData, BarisCetakTerakhir, TglCetakTerakhir ,id_detil_terakhir= \
          ConstructReportTransPassbook(config,RegisterPassbook,BarisMulai,TglMulai,isCetakUlang)
      oFile.write(ReportData)
      oFile.close()
      
      
      # Jika menekan tombol cetak
      if stButton == 2 :
        #Update RegisterPassbook
        
         if (not isCetakUlang) or (RegisterPassbook.ID_Transaksi < id_detil_terakhir):
            # Update Tanggal_Cetak_Terakhir dan ID_Transaksi
            RegisterPassbook.Tanggal_Cetak_Terakhir = TglCetakTerakhir
            RegisterPassbook.ID_Transaksi     = id_detil_terakhir
         RegisterPassbook.Baris_Cetak_Terakhir = BarisCetakTerakhir
         RegisterPassbook.Is_Baru_Register = "F"

      sw = returnpacket.AddStreamWrapper()
      sw.LoadFromFile(sFileName)
      sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)
      config.Commit()
  except:
      config.Rollback()
      status.Is_Err = 1
      status.Err_Message = str(sys.exc_info()[1])
  return 1

