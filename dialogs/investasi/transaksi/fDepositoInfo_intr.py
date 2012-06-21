class fDepositoInfo:

  def __init__(self, formObj, parentForm):
    self.form = formObj
    self.app = formObj.ClientApplication

  def SetVisibility(self):
    if self.form.GetControlByName('pDataRight.jenisJatuhTempo').ItemIndex == 4:
      # deposito on call
      self.form.GetControlByName('pDataRight.jmlHariOnCall').Visible = 1
    else:
      self.form.GetControlByName('pDataRight.jmlHariOnCall').Visible = 0

##    if self.form.GetControlByName('pDataRight.treatmentPokok').ItemIndex == 2:
##      # pindah buku
##      self.form.GetControlByName('pDataRight.kapitalisir_rollover').Visible = 0
##    else:
##      self.form.GetControlByName('pDataRight.kapitalisir_rollover').Visible = 1

    if self.form.GetControlByName('pDataRight.kapitalisir_rollover').ItemIndex == 0:
      # pindah buku
      self.form.GetControlByName('pDataRight.no_rekening').Visible = 0
    else:
      # kapitalisir
      self.form.GetControlByName('pDataRight.no_rekening').Visible = 1

