import sys

def FormOnSetDataEx(uideflist, params):
   config = uideflist.config
   par = params.FirstRecord
   uideflist.SetData('uipart1', par.key)
   rec = uideflist.uipart1.Dataset.GetRecord(0)
   rec.ket       = rec.keterangan 
   rec.o_nominal = rec.nominal 
   rec.proses    = 0
     
def Simpan(config, parameter, returnpacket):
  status = returnpacket.CreateValues(
     ['IsErr',0],
     ['ErrMessage',''],
  )
  rec = parameter.uipart1.GetRecord(0)
  config.BeginTransaction()
  try:
    SI = config.AccessPObject(rec.key)
    SI.keterangan = rec.keterangan
    SI.is_valid   = rec.is_valid
    SI.nominal    = rec.nominal
    SI.rekening_sumber = rec.rekening_sumber
    selisih = rec.nominal - rec.o_nominal
    
    RGO = 'PObj:RiwayatGiro#id_reconcile=%s#account_giro=%s' % (SI.id_reconcile,SI.account_giro)
    RG = config.AccessPObject(RGO)
    RG.sum_nominal += selisih
    
    config.Commit()
  except:
    config.Rollback()
    status.IsErr = 1
    status.ErrMessage = str(sys.exc_info()[1])
    
