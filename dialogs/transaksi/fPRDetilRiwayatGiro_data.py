
def Form_OnSetDataEx(uideflist, params):
   #import rpdb2;rpdb2.start_embedded_debugger('haryo',True,True)
   config = uideflist.config
   par = params.FirstRecord
   RG = config.AccessPObject(par.key)
   rec = uideflist.uipart.Dataset.AddRecord()
   rec.is_created_transaction  = 'A'
   rec.id_reconcile            = RG.id_reconcile
   rec.acc_giro                = RG.account_giro
   rec.jenis_reconcile         = RG.LReconcile.jenis_reconcile
   rec.tanggal_transaksi       = RG.LReconcile.tanggal_transaksi
   rec.waktu_mulai             = RG.LReconcile.waktu_mulai
   rec.sum_nominal             = RG.sum_nominal
   rec.sum_procced_nominal     = RG.sum_procced_nominal
   rec.sum_pindahbuku          = RG.sum_pindahbuku
   rec.is_pindahbuku           = RG.is_pindahbuku
   rec.is_reconciled           = RG.is_reconciled
   rec.sum_sisa                = RG.sum_nominal - RG.sum_procced_nominal


