def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  keyid = params.FirstRecord.trx_session_id
  if str(keyid) != '':
    pobjconst = "PObj:UploadCorporate#trx_session_id=%s" % keyid
    uideflist.SetData('uipParent', pobjconst)
  
  pass