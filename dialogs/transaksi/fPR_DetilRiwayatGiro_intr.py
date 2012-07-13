class fPR_DetilRiwayatGiro:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication
    self.DictFormId = {
      'E':'transaksi/fPR_DetilRiwayatGiro_Edit'
    }
       
  def Show(self):
    jenis = self.uipart.jenis_reconcile
    if jenis == 'A':
       caption = 'Auto Payment'
    elif jenis == 'E':
       caption = 'e - Channel'
    self.FormObject.Caption += caption
    self.FormContainer.Show()

  def TampilkanOnClick(self, sender):
    qValid = self.qValid
    qValid.OQLText = self.oText('T')
    qValid.DisplayData()
    
    qInvalid = self.qInvalid
    qInvalid.OQLText = self.oText('F')
    qInvalid.DisplayData()

  def oText(self, jenis):
    uip = self.uipart
    norek = uip.no_rekening or ''
    AddParam =" id_reconcile = %s and is_created_transaction ='%s' and is_valid = '%s'" % (uip.id_reconcile, uip.is_created_transaction, jenis)
    if norek != '':
       AddParam +=" and no_rekening LLIKE '%s' " % norek
    valid ={} 

    oText = " select from detilriwayatgiro [ %s ] " % (AddParam)
    oText += "( account_giro, \
      id_reconcile, \
      no_rekening, \
      is_corporate, \
      is_valid $, \
      is_created_transaction $, \
      nominal, \
      rekening_sumber, \
      keterangan, \
      self \
    );" 
    
    return oText
  

  def EditClick(self, sender):
    group_id, form_id = self.DictFormId['E'].split('/')
    form = self.app.FindForm(form_id)
    if form == None:
      key = self.qInvalid.KeyObjConst 
      ph = self.app.CreateValues(['key', key])
      f = self.app.CreateForm(group_id+'/'+form_id, form_id, 0, ph, None)
      form = f.FormContainer
    form.Show()
    
    self.qInvalid.Refresh()    
    self.qValid.Refresh()    

  def InvalidClick(self, sender):
    if self.app.ConfirmDialog('Yakin akan menjadikan invalid??'):
      pass
    else:
      return 0
  
    key = self.qValid.KeyObjConst 
    resp = self.FormObject.CallServerMethod('invalid_status',self.app.CreateValues(['key', key]))

    status = resp.FirstRecord
    if status.IsErr :
      self.app.ShowMessage(status.ErrMessage)
      return
    
    self.qInvalid.Refresh()    
    self.qValid.Refresh()    


  def bProsesOnClick(self, sender):
    ph = self.app.CreateValues(['id_reconcile', self.uipart.id_reconcile],
                               ['jenis', self.uipart.jenis_reconcile],
                               ['waktu_mulai', self.uipart.waktu_mulai])
    resp = self.FormObject.CallServerMethod("SimpanTransaksi", ph)

    #process return
    status = resp.FirstRecord
    if status.IsErr :
      self.app.ShowMessage(status.ErrMessage)
      return
    self.qValid.Refresh()    
