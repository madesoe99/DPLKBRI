def BranchStatus_Change(Sender):
  aform = Sender.OwnerForm
  data = aform.GetUIPartByName('BranchLocation')

  if Sender.Text == 'Branch':
    aform.GetControlByName('mpData.LMasterBranch').Enabled = 0
    data.ClearLink('LMasterBranch')
  else:
    aform.GetControlByName('mpData.LMasterBranch').Enabled = 1
