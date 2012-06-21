def BranchLocation_AfterApplyRow(sender, data):
  MasterBranch = sender.GetLink('LMasterBranch')

  data.RegisterData(MasterBranch)
  
  # tambahkan data di counter untuk NASABAHDPLK per cabang
  config = sender.UIDefList.Config
  oCounter = config.CreatePObject('counter')
  oCounter.id_code = 'NASABAHDPLK'
  oCounter.last_id = 1
  oCounter.is_locked = 0
  oCounter.param = data.branch_code

