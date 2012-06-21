import ConfigParser, os

def FitCaption(caption, itemnumber):
  pj = len(itemnumber)
  pj = 4*(pj - int(pj/2)) - 4
  pref_caption = pj * ' '

  return (pref_caption + caption)
	
def LoadMenuItemsToDataset (config, amenuitem, adataset, item_number, parent_item_number):
  rec = adataset.AddRecord()
  rec.item_number = item_number
  rec.item_caption = amenuitem.Caption
  rec.item_caption_mod = FitCaption(amenuitem.Caption, item_number)
  rec.parent_item = parent_item_number

  # add users and groups
  userdataset = rec.allowedusers
  groupdataset = rec.allowedgroups
  
  allowedusers = str(amenuitem.AllowedUsers)
  ls_allowedusers = allowedusers.split(';')

  for user_id in ls_allowedusers:        
    if len(user_id) <> 0:
      user_proxy = config.CreatePObjImplProxy('UserApp')
      user_proxy.key = user_id
      if not user_proxy.IsNull:
        rec_user = userdataset.AddRecord()
        rec_user.SetFieldByName('user.user_id', user_id)
        rec_user.SetFieldByName('user.UserName', user_proxy.UserName)
        rec_user.SetFieldByName('user.Description', user_proxy.Description)

  allowedgroups = str(amenuitem.AllowedGroups)
  ls_allowedgroups = allowedgroups.split(';')
  for group_id in ls_allowedgroups:
    if len(group_id) <> 0:
      group_proxy = config.CreatePObjImplProxy('UserGroup')
      group_proxy.key = group_id
      if not group_proxy.IsNull:
        rec_group = groupdataset.AddRecord()
        rec_group.SetFieldByName('group.group_id', group_id)
        rec_group.SetFieldByName('group.GroupName', group_proxy.GroupName)
        rec_group.SetFieldByName('group.Description', group_proxy.Description)

  n = amenuitem.ItemCount
  for i in range(n):
    amnuitem = amenuitem.GetItem(i)
    LoadMenuItemsToDataset(config, amnuitem, adataset, item_number + '.' + str(i + 1), item_number)
	
def FormGeneralSetData(uideflist, uiname, pobjconst):
  config = uideflist.config

  moddate = config.ModDateTime
  dataset = uideflist.menuitems.Dataset

  #pobjconst represents menu name
  cfgparser = ConfigParser.ConfigParser()
  cfgparser.readfp(open('c:\\dafapp\\ctracking\\menus\\menulist.ini'))
  mnufilename = cfgparser.get('MENULIST', pobjconst)

  menu_id_rec = uideflist.menu_id.Dataset.AddRecord()
  menu_id_rec.menu_id = pobjconst

  # load menu from file name
  mnuholder = config.ModRTMenu.CreateMenuHolder()
  mnuholder.LoadMenu('c:\\dafapp\\ctracking\\menus\\' + mnufilename)
  mnuobject = mnuholder.menuobject

  # load items
  n = mnuobject.ItemCount
  for i in range(n):
    amenuitem = mnuobject.GetItem(i) 
    LoadMenuItemsToDataset(config, amenuitem, dataset, str(i + 1), None)

  # stop further processing
  return 0
