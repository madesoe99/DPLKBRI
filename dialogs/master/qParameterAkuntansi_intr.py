initialize = 0

def FormShow(form, parameter):
  global initialize
  
  initialize = 1

def GridAfterNewRecord(pclassui):
  global initialize

  if not initialize:
    return
    
  raise 'PERINGATAN','Tidak diperkenankan untuk menambah daftar Parameter ini!'

def GridBeforeDelete(pclassui):
  raise 'PERINGATAN','Tidak diperkenankan untuk menghapus daftar Parameter ini!'
  
def GridBeforePost(pclassui):
  #ada checking kesamaan intf_code ataupun account_code
  #di bagian
  raise 'PERINGATAN','Tidak diperkenankan mengubah parameter ini.'
