def GridBeforePost(pclassui):
  if pclassui.maks_proporsi <= 0.0:
    raise Exception, 'PERINGATAN' + 'Maksimal proporsi harus lebih besar dari 0!'
    
def GridAfterNewRecord(pclassui):
  #inisialisasi maksimal proporsi dengan nilai 0.0
  pclassui.maks_proporsi = 0.0
