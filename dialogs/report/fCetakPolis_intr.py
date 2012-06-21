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
     data.NomorPolis = None
     data.TglLahir = None
     data.TglMulaiAkseptasi = None
     data.TglMulaiPerjanjian = None
     data.TglAkhirPerjanjian = None
     data.SetoranPerbulan = None
     data.ManfaatTakaful = None
     data.PremiPerbulan = None
     No_Peserta = data.No_Peserta
     
     if No_Peserta not in ('',None):
        try :
          res = self.form.CallServerMethod('LookUpDataNasabah',self.app.CreateValues(['No_Peserta',No_Peserta]))
          data.Edit()
          data.Nama               = res.FirstRecord.Nama
          data.TglLahir           = res.FirstRecord.TglLahir
          data.NomorPolis         = res.FirstRecord.NomorPolis
          data.TglMulaiAkseptasi  = res.FirstRecord.TglMulaiAkseptasi
          data.tglMulaiPerjanjian = res.FirstRecord.TglMulaiperjanjian
          data.TglAkhirPerjanjian = res.FirstRecord.TglAkhirPerjanjian
          data.SetoranPerbulan    = res.FirstRecord.SetoranPerbulan
          data.ManfaatTakaful     = res.FirstRecord.ManfaatTakaful
          data.PremiPerbulan      = res.FirstRecord.PremiPerbulan
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

       PrintClass = self.app.GetClientClass('NewPrintLib','NewPrintLib')
       oPrint = PrintClass()
       if sender.Name =='btnPeragaan':
          oPrint.doProcess(self.app,result.packet,1)
       elif sender.Name =='btnCetak':
          oPrint.doProcess(self.app,result.packet,2)
     else:
       raise '\nPERINGATAN','Nomor Peserta Belum Diinputkan'
       

