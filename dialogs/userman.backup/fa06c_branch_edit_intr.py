def Form_AfterProcessServerData(Sender, operation_id, data):
  aform = Sender
  data = aform.GetUIPartByName('BranchLocation')

  if data.BranchStatus == 'B':
    aform.GetControlByName('mpData.LMasterBranch').Enabled = 0
  else:
    aform.GetControlByName('mpData.LMasterBranch').Enabled = 1

  return 1

def BranchStatus_Change(Sender):
  aform = Sender.OwnerForm
  data = aform.GetUIPartByName('BranchLocation')

  if Sender.Text == 'Branch':
    aform.GetControlByName('mpData.LMasterBranch').Enabled = 0
    data.ClearLink('LMasterBranch')
  else:
    aform.GetControlByName('mpData.LMasterBranch').Enabled = 1
