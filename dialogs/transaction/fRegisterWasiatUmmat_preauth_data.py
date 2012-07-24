import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver
moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

#sys.path.append('c:/dafapp/dplk07/script_modules')
#import moduleapi

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegisterAsuransi = uideflist.uipRegisterAsuransi
  
  # cek lagi status
  rec = uipRegisterAsuransi.Dataset.GetRecord(0)
  if rec.jenis_transaksi == 'O':
    # berhenti asuransi
    strSQL = '\
      select no_polis, tgl_akseptasi, besar_premi, manfaat_asuransi \
      from RekAsuransi \
      where no_rekening = \'%s\''\
      % (rec.GetFieldByName('LRekeningDPLK.no_rekening'))
    resSQL = config.CreateSQL(strSQL).RawResult

    if resSQL.RecordCount <= 0:
      raise Exception, 'SQL Result Error' + 'Rekening Asuransi tidak terdefinisi.'

    rec.no_polis = resSQL.no_polis
    rec.besar_premi = resSQL.besar_premi
    rec.manfaat_asuransi = resSQL.manfaat_asuransi
    rec.tgl_akseptasi = moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_akseptasi)
    
    #set kolektibilitas dan tunggakan premi
    oR = config.CreatePObjImplProxy('RekInvDPLK')
    oR.Key = rec.GetFieldByName('LRekeningDPLK.no_rekening')
    rec.kolektibilitas_premi = oR.collectivity_asuransi
    rec.tunggakan_premi = oR.kewajiban_asuransi

  #set parameter PRESISI_ANGKA_FLOAT
  recParameter = uideflist.uipParameter.Dataset.AddRecord()
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'

  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value

  return 0

