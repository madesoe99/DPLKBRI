class qViewDaftarHistoriGiro:

  def __init__(self, formObj, parentForm):
    pass

  def FormShow(self):
    self.SetAndDisplayQuery(self.uipParameter.hidden_id)
    rShow = self.FormContainer.Show()

  def SetAndDisplayQuery(self, keyID):
    #set parameter OQL and show it
    query = self.FormObject.GetPanelByName('qHistoriGiro')
    query.OQLText = 'select from HistoriGiro '\
      '[ID_HistoriGiroHarian = :id_HGH]'\
      '(Nomor_Batch_CoreBanking,Nomor_Urut,Nomor_Referensi,Nomor_Peserta,'\
      'Kode_Mnemonic as Kode_Debet_Kredit, '\
      'Nominal,'\
      'Keterangan,'\
      'Transaksi_Peserta as isSettled, '\
      'isTransaksiCreated$ as Status_Pembuatan_Transaksi, '\
      'self) then order by Nomor_Urut;'

    #set parameter OQL
    query.SetParameter('id_HGH',keyID)

    query.DisplayData()
