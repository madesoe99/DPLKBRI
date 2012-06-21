class frmReserveCustID:
  def __init__(self, formObject, parentForm):
    pass

  def btnOKClick(self, button):

    form = self.FormObject
    app = form.ClientApplication
    form.CommitBuffer()

    uipInput = self.uipInput
    
    if uipInput.no_peserta in ('',None):
       app.ShowMessage('Nomor Peserta harus disii.')
       return

    ph = form.GetDataPacket()
    res = form.CallServerMethod("hitSimulasi", ph)

    uipOutput = self.uipOutput
    uipOutput.ClearData()
    uipOutput.Append()
    uipOutput.nama_peserta      = res.FirstRecord.nama_peserta
    uipOutput.usia_pensiun      = res.FirstRecord.usia_pensiun
    uipOutput.usia_masuk        = res.FirstRecord.usia_masuk
    uipOutput.tingkat_investasi = res.FirstRecord.tingkat_investasi
    uipOutput.rate_premi        = res.FirstRecord.rate_premi
    uipOutput.saldo_awal        = res.FirstRecord.saldo_awal
    uipOutput.premi_perbulan    = res.FirstRecord.nominal_premi
    uipOutput.manfaat_pensiun   = res.FirstRecord.manfaat_pensiun
    uipOutput.Post()

  def btnPetunjukClick(sender):

    app = sender.OwnerForm.ClientApplication
    app.ShowMessage('KETERANGAN : \n'\
    '\nJika Premi Perbulan dan Manfaat Pensiun diisi = 0 '\
    '\nmaka perhitungannya otomatis \n'\
    '\nJika salah satu dari kedua tersebut diberi nilai '\
    '\nmaka perhitungan menggunakan salah satu dari nilai tersebut')


