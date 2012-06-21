import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

def OnSetDataEx(uideflist, params):
  config = uideflist.Config           
  lsKey = str(params.FirstRecord.key).split('=')
  
  uideflist.SetData('uipNasabahDPLK', params.FirstRecord.key)
  
  