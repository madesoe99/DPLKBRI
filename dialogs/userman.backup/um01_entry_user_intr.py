def FormShow(form, parameter):
  app = form.ClientApplication
  UserApp = form.GetUIPartByName('UserApp')
  
  dhRes = app.ExecuteScript('userman/getbranchcode',None)
  branch_code = dhRes.FirstRecord.branch_code

  UserApp.Edit()
  UserApp.SetFieldValue('LBranchLocation.branch_code',branch_code)

