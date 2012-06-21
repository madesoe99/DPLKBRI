import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def uipObligasiSetData(uipObligasi):
  uideflist = uipObligasi.UIDefList
  config = uideflist.Config
  rec_inv = uipObligasi.Dataset.GetRecord(0)
  if rec_inv.TreatmentObligasi in ('',None) :
    rec_inv.TreatmentObligasi = 'R'
  rec_inv.TreatmentObligasiOld = rec_inv.TreatmentObligasi
  if rec_inv.no_bilyet in (None,'') : #mode ubah
    rec_inv.UbahStat = 1
  else : #mode oto
    rec_inv.UbahStat = 0
    rec_inv.TreatmentObligasi = rec_inv.no_bilyet
    
def OnBeginProcessData (uideflist, AData) :
  StatMap = {
   'H':'R',
   'R':'H',
   'SENTINEL':''
  }
  config = uideflist.Config
  uObl = AData.uipObligasi.GetRecord(0)

  if uObl.CreateMode == 'Oto' :
    if uObl.ModeOto :
      uObl.TreatmentObligasi = uObl.no_bilyet
      uObl.user_id_auth = config.SecurityContext.UserID
      uObl.last_update = config.Now()
    else :
      uObl.TreatmentObligasi = uObl.TreatmentObligasiOld
    uObl.no_bilyet = None
  else :
    uObl.no_bilyet = uObl.TreatmentObligasi
    uObl.TreatmentObligasi = uObl.TreatmentObligasiOld

  return 1

