import ConfigParser, os, string

def FormGeneralSetData(uideflist, uiname, pobjconst):
  config = uideflist.config
  moddate = config.ModDateTime
  dataset = uideflist.menulist.Dataset

  cfgparser = ConfigParser.ConfigParser()
  cfgparser.readfp(open(config.HomeDir + 'menus\\menulist.ini'))
  mnulist = cfgparser.options('MENULIST')

  mnulist.sort()
  for mnuoption in mnulist:
    Record = dataset.AddRecord()
    Record.menu_name = mnuoption
    mnuoption = string.replace(mnuoption, '_', ' ')
    mnuoption = string.replace(mnuoption, '-', '>>')
    Record.menu_caption = string.upper(mnuoption)

  # stop further processing
  return 0
