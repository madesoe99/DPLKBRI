class fCetakUlangTransPassbook:
  def __init__(self,formobj,parentform):
     self.form = formobj
     self.app  = self.form.ClientApplication
     self.uipNoData = self.form.GetUIPartByName('uipNoData')
     self.uipNoData.TanggalMulai = int(self.app.ModDateTime.Now())

     PrintClass = self.app.GetClientClass('PrintLib','PrintLib')
     self.PrintModule = PrintClass()


  def OnShow(self,No_Peserta):
     self.uipNoData.Edit()
     
  def NoRekExit(self,sender):
     # Event dijalankan setelah lookup
     app = self.app
     Data = self.uipNoData
     
     Data.Edit()
     Data.Nama = None
     Data.BarisMulai = None

     if Data.No_Peserta not in ('',None):

        No_Peserta = Data.No_Peserta
        
        res = app.ExecuteScript(
                  'report/S_Report.GetInfoPassbook',
                  app.CreateValues(
                      ['No_Peserta',No_Peserta]
                  )
             )

        rec = res.FirstRecord
        if rec.Is_Err :
           raise Exception, 'PERINGATAN' + rec.Err_Message

        Data.Nama = res.FirstRecord.Nama
        Data.BarisMulai = res.FirstRecord.BarisCetakTerakhir + 1

  def btnOKClick(self,sender):
     # Event untuk button OK Click
     self.FormObject.CommitBuffer()
     if self.uipNoData.No_Peserta not in ('',None):
       if self.uipNoData.BarisMulai in ('',None):
         raise Exception, '\nPERINGATAN' + 'Baris Mulai Belum diinputkan'
       if int(self.uipNoData.BarisMulai) > 34 :
         raise Exception, '\nPERINGATAN' + 'Baris Tidak Boleh Lebih dari 34'
         
       data = self.uipNoData
       No_Peserta = data.No_Peserta

       stButton = {'btnPeragaan':1,'btnCetak':2}
       
       result = self.app.ExecuteScript('report/S_Report.PrintPassbookTransaction',\
         self.app.CreateValues(\
            ['No_Peserta',No_Peserta],\
            ['BarisMulai',data.BarisMulai],\
            ['TglMulai',data.TanggalMulai],\
            ['isCetakUlang',1],\
            ['stButton',stButton[sender.Name]]
         )
       )

       ph = result.FirstRecord
       if ph.Is_Err:
          raise Exception, "PERINGATAN" + ph.Err_Message
          
       self.PrintModule.doProcess(self.app,result.packet,stButton[sender.Name])
       if stButton[sender.Name] == 2:
          sender.ExitAction = 1
          
     else:
       raise Exception, '\nPERINGATAN' + 'Nomor Rekening Belum Diinputkan'
