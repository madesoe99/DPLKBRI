
def FormOnSetDataEx(uideflist, params):
   config = uideflist.config
   rec = uideflist.uipart.Dataset.AddRecord()
   rec.tgl_awal       = int(config.Now()-1)
   rec.tgl_akhir      = int(config.Now())
   rec.is_berhasil    = 'T'
   rec.is_reconciled  = 'F'
   #rec.jenis_reconcile= 'S'

