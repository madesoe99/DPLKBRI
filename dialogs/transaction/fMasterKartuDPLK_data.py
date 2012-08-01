
def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  config = uideflist.Config
  if params.FirstRecord != None:
    uideflist.SetData('uipMasterKartuDPLK', params.FirstRecord.key)
  else:
    rec = uideflist.uipMasterKartuDPLK.Dataset.AddRecord()
    rec.tmp_year = "%s-xxxxxx-xxxxxxx" % str(config.ModLibUtils.DecodeDate(config.Now())[0])