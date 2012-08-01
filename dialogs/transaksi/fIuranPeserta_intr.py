class fIuranPeserta:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication
    self.Input = self.app.GetClientClass("Inputan", "Inputan")()
  #--

  def bSimpanClick(self, button):
    form = self.FormObject
    #cek nominal iuran peserta
    if self.uipPeserta.kode_nasabah_corporate not in ('',None):
      #peserta korporat
      if self.uipTransaksi.mutasi_iuran_tmb in (None,'') or \
        self.uipTransaksi.mutasi_iuran_tmb < self.uipParameter.PRESISI_ANGKA_FLOAT:
        form.ShowMessage('Nominal Iuran Tambahan masih kosong atau 0! Mohon untuk diisi.')
        return
  
      if self.uipTransaksi.mutasi_iuran_tmb < self.uipParameter.MIN_JML_IURAN_TMB:
        form.ShowMessage('Nominal Iuran Tambahan kurang dari minimal iuran tambahan.')
        return
    else:
      #peserta individu
      if self.uipTransaksi.mutasi_iuran_pst in (None,'') or \
        self.uipTransaksi.mutasi_iuran_pst < self.uipParameter.PRESISI_ANGKA_FLOAT:
        form.ShowMessage('Nominal Iuran Peserta masih kosong atau 0! Mohon untuk diisi.')
        return
    
      if self.uipTransaksi.mutasi_iuran_pst < self.uipParameter.MIN_JML_IURAN_PST or \
        self.uipTransaksi.mutasi_iuran_pst < self.uipRekening.iuran_pst:
        form.ShowMessage('Nominal Iuran Tambahan kurang dari minimal iuran peserta.')
        return
   
    if self.Input.CekKet(form,self.uipTransaksi.keterangan) == 0:return
    
    if self.app.ConfirmDialog('Anda yakin Simpan transaksi Iuran Peserta %s %s?' % (self.uipPeserta.no_peserta, self.uipPeserta.nama_lengkap)):
      pass
    else:
      return 0
    
    form.CommitBuffer()
    phForm = form.GetDataPacket()
    phReturn = form.CallServerMethod("SimpanTransaksi", phForm)

    #process return
    dsStatus = phReturn.Packet.status
    rec = dsStatus.GetRecord(0)
    if rec.error_status:
      # show error message
      form.ShowMessage(rec.error_message)
      return
    else:
      #KODE LAIN BILA MEMERLUKAN PRINT SLIP
      button.ExitAction = 1
  #--

  def Form_AfterProcessServerData(self, formobj, operationid, datapacket):
    # function(formobj: TrtfForm; operationid: integer; datapacket: TPClassUIDataPacket):boolean
    
    if self.uipPeserta.kode_nasabah_corporate not in ('',None):
      #peserta korporat
      self.pDataTransaksi_mutasi_iuran_pk.Enabled = 0
      self.pDataTransaksi_mutasi_iuran_pst.Enabled = 0
      self.pDataTransaksi_mutasi_iuran_tmb.Enabled = 1
    else:
      #peserta individu
      self.pDataTransaksi_mutasi_iuran_pk.Enabled = 0
      self.pDataTransaksi_mutasi_iuran_pst.Enabled = 1
      self.pDataTransaksi_mutasi_iuran_tmb.Enabled = 0
  #--

  def LReconcileOnAfterLookup(self, sender, linkui):
    uip2 = self.uipPeserta
    uip = self.uipTransaksi
    nominal = uip.GetFieldValue('LReconcile.nominal')

    uip.Edit()
    if uip2.kode_nasabah_corporate in (None,''):
      uip.mutasi_iuran_pst = nominal
    else:
      uip.mutasi_iuran_tmb = nominal
      

  def OnEnter(self, sender):
    uip = self.uipTransaksi
    self.Input.OnEnter(sender,uip)

  def OnExit(self, sender):
    uip = self.uipTransaksi
    self.Input.OnExit(sender,uip)