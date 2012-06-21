def BranchLocation_AfterApplyRow(sender, data):
  MasterBranch = sender.GetLink('LMasterBranch')

  data.Modify(MasterBranch)
