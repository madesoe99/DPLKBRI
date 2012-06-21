def FormShow(form, parameter):
  uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')
  
  kode_nasabah_corporate = uipNasabahDPLK.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate')
  if kode_nasabah_corporate == None:
    form.GetControlByName('pPekerjaan.LNasabahDPLKCorporate').Visible = \
    form.GetControlByName('pPekerjaan.btnViewCorp').Visible = 0
    
  #set kolektibilitas dan tunggakan premi
  uipR = form.GetUIPartByName('uipRekeningDPLK')
  if uipR.Status_Wasiat_Ummat == 'T':
    uipRWU = form.GetUIPartByName('uipRekeningWU')
    uipRWU.Edit()
    uipRWU.KolektibilitasPremi = uipR.collectivity_wasiat_ummat
    uipRWU.TunggakanPremi = uipR.kewajiban_wasiat_ummat

def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def btnViewCorpClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')

  kode_nasabah_corporate = uipNasabahDPLK.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate')
  key = 'PObj:NasabahDPLKCorporate#KODE_NASABAH_CORPORATE=%s' % (kode_nasabah_corporate)

  aform = app.GetFormWithData('transaction/fNasabahDPLKCorporate','fNasabahDPLKCorporate',0,key,'uipNasabahDPLKCorporate')
  SetToCenterForm(form, aform.FormObject)
  aform.Show(app.CreateValues(['mode','view']))

def btnStatemenIndividualClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')

  pyFormObj = app.CreateForm('report/fStatemenIndividual', 'fStatemenIndividual', 0, None, None)

  # set peserta
  pyFormObj.uipNoData.Edit()
  pyFormObj.uipNoData.SetFieldValue('LNasabahDPLK.no_peserta', uipNasabahDPLK.no_peserta)
  pyFormObj.uipNoData.SetFieldValue('LNasabahDPLK.nama_lengkap', uipNasabahDPLK.nama_lengkap)
  
  pyFormObj.pData.GetControlByName('LNasabahDPLK').Enabled = 0

  pyFormObj.FormContainer.Show()

