class fRegistrasiCorp_New:
  def __init__(self, formObj, parentForm):
    #self.formObj, self.app = formObj, formObj.ClientApplication
    self.dictRiskFlag = {'L' : 'Low', 'H' : 'High' , 'M' : 'Moderate' , '' : ''}
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None
  #--

  def Show(self, mode):
    app = self.FormObject.ClientApplication
    
    self.FormShow(self.FormObject, mode)
    self.FormContainer.Show()

  def FormShow(self, form, parameter):
    app = form.ClientApplication
    uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')
  
    uipRegEditNasabahDPLKCorporate.Edit()
    uipRegEditNasabahDPLKCorporate.mode = parameter.FirstRecord.mode
  
  def btnOKClick(self, sender):
    form = sender.OwnerForm
    uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')
    uipP = form.GetUIPartByName('uipParameter')
  
    if uipRegEditNasabahDPLKCorporate.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return
  
    if uipRegEditNasabahDPLKCorporate.kode_nasabah_corporate in ['',None]:
      form.ShowMessage('Kode Peserta Korporat masih kosong. Mohon untuk diisi.')
      return
  
    if uipRegEditNasabahDPLKCorporate.nama_perusahaan in ['',None]:
      form.ShowMessage('Nama Korporat masih kosong. Mohon untuk diisi.')
      return
  
    if uipRegEditNasabahDPLKCorporate.GetFieldValue("LJenisUsaha.kode_jenis_usaha") in ['',None]:
      form.ShowMessage('Jenis Usaha masih kosong. Mohon untuk diisi.')
      return
  
    if uipRegEditNasabahDPLKCorporate.GetFieldValue("LKepemilikan.kode_pemilikan") in ['',None]:
      form.ShowMessage('Kepemilikan masih kosong. Mohon untuk diisi.')
      return
  
    #checking tgl bayar iuran
    if uipRegEditNasabahDPLKCorporate.tgl_bayar_iuran in ['',None]:
      form.ShowMessage('Tanggal Bayar Iuran masih kosong. Mohon untuk diisi.')
      return
      
    #checking biaya daftar anggota
    if uipRegEditNasabahDPLKCorporate.biaya_daftar_anggota in ['',None] or \
      uipRegEditNasabahDPLKCorporate.biaya_daftar_anggota < 0.0:
      #memakai batas 0.0 sebab dimungkinkan gratis
      form.ShowMessage('Biaya Daftar Anggota tidak boleh kosong atau negatif.')
      return
  
    if uipRegEditNasabahDPLKCorporate.GetFieldValue("LNegara.kode_negara") in ['',None]:
      form.ShowMessage('Negara masih kosong. Mohon untuk diisi.')
      return
  
    # seusaikan flag akibat formendsetdata
    uipRegEditNasabahDPLKCorporate.Edit()
    uipRegEditNasabahDPLKCorporate.SetFieldValue('__SYSFLAG', 'N')
  
    form.CommitBuffer()
    form.PostResult()
  
    sender.ExitAction = 1
  
  def LJenisUsahaAfterLookup(self, ctlLJenisUsaha, LJenisUsaha):  
    uipReg = ctlLJenisUsaha.OwnerForm.GetUIPartByName('uipRegEditNasabahDPLKCorporate')
    uipReg.Edit()   
    uipReg.SetFieldValue('RF_JenisUsaha', self.dictRiskFlag[uipReg.GetFieldValue('LJenisUsaha.Risk_Flag') or ''])
    
  def LNegaraAfterLookup(self, ctlLNegara, LNegara):  
    uipReg = ctlLNegara.OwnerForm.GetUIPartByName('uipRegEditNasabahDPLKCorporate')
    uipReg.Edit()   
    uipReg.SetFieldValue('RF_Negara', self.dictRiskFlag[uipReg.GetFieldValue('LNegara.Risk_Flag') or ''])      