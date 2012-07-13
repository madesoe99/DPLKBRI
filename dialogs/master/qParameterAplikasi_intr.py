initialize = 0

def FormShow(form, parameter):
  global initialize
  
  initialize = 1

def SetValueTypeAfterLookup(uipX, gridX):
  if uipX.ValueType == 0:
    #tipe Angka
    uipX.Varchar_Value = None
    gridX.GetColumnByName('Numeric_Value').ReadOnly = 0
    gridX.GetColumnByName('Varchar_Value').ReadOnly = 1

    #debug code
    sender.OwnerForm.ShowMessage('masuk tipe angka')
  else:
    #tipe Teks
    uipX.Numeric_Value = None
    gridX.GetColumnByName('Varchar_Value').ReadOnly = 0
    gridX.GetColumnByName('Numeric_Value').ReadOnly = 1

    #debug code
    sender.OwnerForm.ShowMessage('masuk tipe teks')

def ValueTypeAfterLookup(sender, linkui):
  uipP = sender.OwnerForm.GetUIPartByName('uipParameter')
  gPA = sender.OwnerForm.GetPanelByName('gParameterAplikasi')
  
  uipK = sender.OwnerForm.GetUIPartByName('uipParameterKorporat')
  gPK = sender.OwnerForm.GetPanelByName('gParameterKorporat')
  
  SetValueTypeAfterLookup(uipP, gPA)
  SetValueTypeAfterLookup(uipK, gPK)

def CheckFormAfterProcessServerData(uipX, gridX):
  #set readonly to column properly based on ValueType
  uipX.First()
  while not uipX.Eof:
    if uipX.Numeric_Value == None or uipX.Numeric_Value == '':
      #Varchar_Value yang terisi, set Numeric_Value readonly
      pass
    else:
      #Numeric_Value yang terisi, set Varchar_Value readonly
      pass
    uipX.Next()

def FormAfterProcessServerData(form, opID, datapacket):
  uipP = form.GetUIPartByName('uipParameter')
  gPA = form.GetPanelByName('gParameterAplikasi')
  
  uipK = form.GetUIPartByName('uipParameterKorporat')
  gPK = form.GetPanelByName('gParameterKorporat')
  
  CheckFormAfterProcessServerData(uipP, gPA)
  CheckFormAfterProcessServerData(uipK, gPK)

  return

#def GridAfterNewRecord(pclassui):
#  global initialize
#
#  if not initialize:
#    return
#    
#  #raise Exception, 'PERINGATAN' + '\n\nTidak diperkenankan untuk menambah daftar Parameter ini!'
#  raise BaseException,'\n\nTidak diperkenankan untuk menambah daftar Parameter ini!'

def GridAfterNewRecord(pclassui):
  global initialize

  if not initialize:
    return
  pclassui.Delete()

def GridBeforeDelete(pclassui):
  #raise Exception, 'PERINGATAN' + '\n\nTidak diperkenankan untuk menghapus daftar Parameter ini!'
  raise BaseException,'\n\nTidak diperkenankan untuk menghapus daftar Parameter ini!'
  
def GridBeforePost(pclassui):
  if pclassui.GetFieldValue('Key_Parameter') == 'BATAS_TGL_TUTUP_BATCH':
    #raise Exception, 'PERINGATAN' + '\n\nBATAS_TGL_TUTUP_BATCH tidak diperkenankan untuk diubah '\
    raise BaseException,'\n\nBATAS_TGL_TUTUP_BATCH tidak diperkenankan untuk diubah '\
    'secara manual!\nAplikasi yang akan menangani secara otomatis.'
  elif pclassui.GetFieldValue('Key_Parameter') in \
    ['PERIODE_PINDAH_PAKET_INVESTASI','JUMLAH_HARI_SETAHUN'] and \
    int(pclassui.GetFieldValue('Numeric_Value')) == 0:
    #raise Exception, 'PERINGATAN' + '\n\nParameter ini tidak boleh bernilai 0'
    raise BaseException,'\n\nParameter ini tidak boleh bernilai 0'
