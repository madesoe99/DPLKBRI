initialize = 0

def FormShow(form, parameter):
  global initialize
  
  initialize = 1

def GridAfterNewRecord(pclassui):
  global initialize

  if not initialize:
    return
    
  #hapus setting readonly untuk acc_giro
  pclassui.OwnerForm.GetPanelByName('gMasterGiro').GetColumnByName('acc_giro').ReadOnly = 0

  #raise 'PERINGATAN','\n\nTidak diperkenankan untuk menambah daftar Master Giro ini!'

def GridBeforeDelete(pclassui):
  pass
  #raise 'PERINGATAN','\n\nTidak diperkenankan untuk menghapus daftar Master Giro ini!'
  
def GridBeforePost(pclassui):
  pass
  #raise 'PERINGATAN','\n\nTidak diperkenankan untuk mengubah daftar Master Giro ini!'

