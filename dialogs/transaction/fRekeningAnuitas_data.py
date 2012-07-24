
def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  uideflist.SetData('uipRekeningAnuitas', params.FirstRecord.key)