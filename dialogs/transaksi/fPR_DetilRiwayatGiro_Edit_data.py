
def FormOnSetDataEx(uideflist, params):
   config = uideflist.config
   par = params.FirstRecord
   uideflist.SetData('uipart1', par.key)
   rec = uideflist.uipart1.Dataset.GetRecord()
   rec.ket = rec.keterangan 