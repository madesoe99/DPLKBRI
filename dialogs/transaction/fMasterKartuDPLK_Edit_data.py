
def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  if params.FirstRecord != None:
    uideflist.SetData('uipMasterKartuDPLK', params.FirstRecord.key)