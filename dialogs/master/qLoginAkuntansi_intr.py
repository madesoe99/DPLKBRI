initialize = 0

def FormShow(form, parameter):
  global initialize
  
  initialize = 1

def ValueTypeAfterLookup(sender, linkui):
  uipP = sender.OwnerForm.GetUIPartByName('uipParameter')
  
  gPA = sender.OwnerForm.GetPanelByName('gParameterAplikasi')
  if uipP.ValueType == 0:
    #tipe Angka
    uipP.Varchar_Value = None
    gPA.GetColumnByName('Numeric_Value').ReadOnly = 0
    gPA.GetColumnByName('Varchar_Value').ReadOnly = 1

    #debug code
    sender.OwnerForm.ShowMessage('masuk tipe angka')
  else:
    #tipe Teks
    uipP.Numeric_Value = None
    gPA.GetColumnByName('Varchar_Value').ReadOnly = 0
    gPA.GetColumnByName('Numeric_Value').ReadOnly = 1

    #debug code
    sender.OwnerForm.ShowMessage('masuk tipe teks')

def FormAfterProcessServerData(form, opID, datapacket):
  uip = form.GetUIPartByName('uipParameter')
  gPA = form.GetPanelByName('gParameterAplikasi')
  
  #set readonly to column properly based on ValueType
  uip.First()
  while not uip.Eof:
    if uip.Numeric_Value == None or uip.Numeric_Value == '':
      #Varchar_Value yang terisi, set Numeric_Value readonly
      pass
    else:
      #Numeric_Value yang terisi, set Varchar_Value readonly
      pass
    uip.Next()

  return

def GridAfterNewRecord(pclassui):
  global initialize

  if not initialize:
    return
    
  raise 'PERINGATAN','\n\nTidak diperkenankan untuk menambah daftar Parameter ini!'

def GridBeforeDelete(pclassui):
  raise 'PERINGATAN','\n\nTidak diperkenankan untuk menghapus daftar Parameter ini!'
  
def GridBeforePost(pclassui):
  if pclassui.GetFieldValue('Key_Parameter') == 'BATAS_TGL_TUTUP_BATCH':
    raise 'PERINGATAN','\n\nBATAS_TGL_TUTUP_BATCH tidak diperkenankan untuk diubah '\
    'secara manual!\nAplikasi yang akan menangani secara otomatis.'
