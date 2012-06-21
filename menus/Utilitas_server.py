def OnLoadMenu(config, menu):
  userid = config.SecurityContext.userid
  if userid.upper() == 'ROOT':
    statusmsg = ' [SUPERUSER]'
  else:
    userobj = config.CreatePObjImplProxy('UserApp')
    userobj.key = userid
    branch = userobj.LBranchLocation
    statusmsg = ' [' + userobj.UserName + ']  cabang: ' + branch.BranchName

  str_today = config.FormatDateTime('dddd, dd mmmm yyyy', \
    config.ModLibUtils.Now())
  wholeMessage = statusmsg + '   tanggal: ' + str_today

  #nambah nama file config/basisdata yang sedang dipakai
  namaConfig = config.GetGlobalSetting('ConfigName')
  if namaConfig == 'DEFAULT':
    namaConfig = 'Online'

  wholeMessage = wholeMessage + '  konfigurasi: ' + namaConfig

  #expressing the live....
  menu.StatusBarMessage = wholeMessage
