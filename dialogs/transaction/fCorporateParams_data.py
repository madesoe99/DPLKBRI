import sys, string, time
import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  config = uideflist.Config           
  uideflist.SetData('uipNasabahDPLKCorporate', params.FirstRecord.key)
