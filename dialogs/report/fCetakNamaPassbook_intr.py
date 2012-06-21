class fCetakNamaPassbook:
  def __init__(self,formobj,parentform):
     self.form = formobj
     self.app  = self.form.ClientApplication
     self.uipNoData = self.form.GetUIPartByName('uipNoData')

  def OnShow(self, No_Peserta):
     self.uipNoData.Edit()
     
  def NoRekExit(self,sender):
     data = self.uipNoData
     data.Edit()
     data.Nama = None
     data.Alamat = None
     data.KodePos = None
     No_Peserta = data.No_Peserta
     if No_Peserta not in ('',None):
        try :
          res = self.form.CallServerMethod('LookUpDataNasabah',self.app.CreateValues(['No_Peserta',No_Peserta]))
          data.Edit()
          data.Nama = res.FirstRecord.Nama
          data.Alamat = res.FirstRecord.Alamat
          data.KodePos = res.FirstRecord.KodePos
        except:
          raise

  def btnOKClick(self,sender):
     self.FormObject.CommitBuffer()
     data = self.uipNoData
     if self.uipNoData.No_Peserta not in ('',None):
       No_Peserta = data.No_Peserta
       result = self.form.CallServerMethod(
                  'CetakNamaPassbook',
                  self.app.CreateValues(
                    ['No_Peserta',No_Peserta]
                  )
                )

       PrintClass = self.app.GetClientClass('PrintLib','PrintLib')
       oPrint = PrintClass()
       if sender.Name =='btnPeragaan':
          oPrint.doProcess(self.app,result.packet,1)
       elif sender.Name =='btnCetak':
          oPrint.doProcess(self.app,result.packet,2)
     else:
       raise '\nPERINGATAN','Nomor Peserta Belum Diinputkan'
       

