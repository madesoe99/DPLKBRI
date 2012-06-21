class frmReserveCustID:
  def __init__(self, formObject, parentForm):
    pass
    
  def bSimpanClick(self, button):
    form = self.FormObject
    form.CommitBuffer()
    
    uipInput = self.uipInput
    #if uipInput.reserve_count <= 0:
    #  raise "Jumlah nomor harus > 0"
    ph = form.GetDataPacket()
    res = form.CallServerMethod("reserveNumber", ph)
    
    #uipOutput = self.uipOutput
    #uipOutput.ClearData()
    #uipOutput.Append()
    #uipOutput.no_awal = res.FirstRecord.no_awal
    #uipOutput.no_akhir = res.FirstRecord.no_akhir
    #uipOutput.Post()
    
    button.ExitAction = 1
