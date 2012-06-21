class fCetakTransPassbook:
  def __init__(self,formobj,parentform):
     self.form = formobj
     self.app  = self.form.ClientApplication
     self.uipNoData = self.form.GetUIPartByName('uipNoData')

     PrintClass = self.app.GetClientClass('PrintLib','PrintLib')
     self.PrintModule = PrintClass()


  def NoRekExit(self,sender):
     # Event dijalankan setelah lookup
     app = self.app
     self.uipNoData.Edit()
     self.uipNoData.Nama = None
     self.uipNoData.BarisMulai = None

     if self.uipNoData.No_Peserta not in ('',None):
        self.getPassbookData(self.uipNoData.No_Peserta)

  def OnShow(self,No_Peserta):
     self.uipNoData.Edit()
     
  def Show(self,No_Peserta):
     self.uipNoData.Edit()
     self.uipNoData.No_Peserta = No_Peserta
     self.getPassbookData(No_Peserta,1)
     self.panel1_No_Peserta.enabled = 0
     self.FormContainer.Show()

  def getPassbookData(self,No_Peserta):
     
     app = self.app
     res = app.ExecuteScript(
             'report/S_Report.GetInfoPassbook',
             app.CreateValues(['No_Peserta',No_Peserta])
           )

     rec = res.FirstRecord
     if rec.Is_Err :
        raise 'PERINGATAN',rec.Err_Message
        
     self.uipNoData.Nama = rec.Nama
     self.uipNoData.BarisMulai = rec.BarisCetakTerakhir + 1

  def btnOKClick(self,sender):
     # Event untuk button OK Click
     self.FormObject.CommitBuffer()
     if self.uipNoData.No_Peserta not in ('',None):
       if self.uipNoData.BarisMulai in ('',None):
         raise '\nPERINGATAN','Baris Mulai Belum diinputkan'
       if int(self.uipNoData.BarisMulai) > 34 :
         raise '\nPERINGATAN','Baris Tidak Boleh Lebih dari 34'

       No_Peserta = self.uipNoData.No_Peserta
     
       stButton = {'btnPeragaan':1,'btnCetak':2}
       
       result = self.app.ExecuteScript('report/S_Report.PrintPassbookTransaction',\
         self.app.CreateValues(\
            ['No_Peserta',No_Peserta],\
            ['BarisMulai',self.uipNoData.BarisMulai],\
            ['isCetakUlang',0],\
            ['stButton',stButton[sender.Name]]
         )
       )

       ph = result.FirstRecord
       if ph.Is_Err:
          raise "PERINGATAN",ph.Err_Message
          
       self.PrintModule.doProcess(self.app,result.packet,stButton[sender.Name])
       if stButton[sender.Name] == 2:
          sender.ExitAction = 1
          
     else:
       raise '\nPERINGATAN','Nomor Peserta Belum Diinputkan'

