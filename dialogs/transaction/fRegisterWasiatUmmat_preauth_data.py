import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegisterWasiatUmmat = uideflist.uipRegisterWasiatUmmat
  
  # cek lagi status
  rec = uipRegisterWasiatUmmat.Dataset.GetRecord(0)
  if rec.jenis_transaksi == 'O':
    # berhenti wasiat ummat
    strSQL = '\
      select no_polis, tgl_akseptasi, besar_premi, manfaat_asuransi \
      from RekeningWasiatUmmat \
      where no_peserta = \'%s\''\
      % (rec.GetFieldByName('LNasabahDPLK.no_peserta'))
    resSQL = config.CreateSQL(strSQL).RawResult

    if resSQL.RecordCount <= 0:
      raise 'SQL Result Error','Rekening Wasiat Ummat tidak terdefinisi.'

    rec.no_polis = resSQL.no_polis
    rec.besar_premi = resSQL.besar_premi
    rec.manfaat_asuransi = resSQL.manfaat_asuransi
    rec.tgl_akseptasi = moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_akseptasi)
    
    #set kolektibilitas dan tunggakan premi
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = rec.GetFieldByName('LNasabahDPLK.no_peserta')
    rec.kolektibilitas_premi = oR.collectivity_wasiat_ummat
    rec.tunggakan_premi = oR.kewajiban_wasiat_ummat

  #set parameter PRESISI_ANGKA_FLOAT
  recParameter = uideflist.uipParameter.Dataset.AddRecord()
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'

  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value

  return 0

