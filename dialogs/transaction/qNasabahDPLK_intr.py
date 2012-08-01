#import rpdb2

bInitial = 1

def ApplyParameter(form):
  qNasabahDPLK = form.GetPanelByName('qNasabahDPLK')
  qNasabahDPLK.DisplayData()

def FormShow(form, parameter):
  global bInitial
  
  #rpdb2.start_embedded_debugger("000")
  uipNoData = form.GetUIPartByName('uipNoData')
  ApplyParameter(form)
  bInitial = 0
  
