class frmReserveCustID:
  def __init__(self, formObject, parentForm):
    pass

  def btnOKClick(self, button):

    form = self.FormObject
    app = form.ClientApplication
    form.CommitBuffer()

    uipInput = self.uipInput
    
    if uipInput.premi == 0 and uipInput.manfaat_pensiun == 0:
       app.ShowMessage('Harus pilih salah satu \n' \
       'input premi yang diinginkan atau Manfaat Pensiun yang diinginkan.')
       return

    if uipInput.premi > 0 and uipInput.manfaat_pensiun > 0:
       app.ShowMessage('Harus pilih salah satu \n' \
       'Input Premi atau Manfaat Pensiun yang diinginkan. \n' \
       'salah satunya harus bernilai 0')
       return

    ph = form.GetDataPacket()
    res = form.CallServerMethod("hitSimulasi", ph)

    uipOutput = self.uipOutput
    uipOutput.ClearData()
    uipOutput.Append()
    uipOutput.usia_masuk = res.FirstRecord.usia_masuk
    uipOutput.tingkat_investasi = res.FirstRecord.tingkat_investasi
    uipOutput.rate_premi = res.FirstRecord.rate_premi
    uipOutput.nominal_premi = res.FirstRecord.nominal_premi
    uipOutput.manfaat_pensiun = res.FirstRecord.manfaat_pensiun
    uipOutput.Post()


