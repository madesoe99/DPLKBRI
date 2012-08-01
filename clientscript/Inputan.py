class record: pass

class Inputan:
    def __init__(self):
        pass

    def OnEnter(self, sender, uip):
      uip.Edit()
      isi = uip.GetFieldValue(sender.Name)
      if isi == 0.0:
        uip.SetFieldValue(sender.Name, None)
      else:
        sender.Text = str(isi)
  
    def OnExit(self, sender, uip):
      isi = sender.Text
      if isi == '':
        uip.SetFieldValue(sender.Name, 0.0)

    def CekKet(self,form, ket):
      if ket in (None,''):
        form.ShowMessage('Keterangan / Remarks harus Diisi')
        form.GetPanelByName('pDataTransaksi').GetControlByName('keterangan').SetFocus()
        return 0

      return 1

   