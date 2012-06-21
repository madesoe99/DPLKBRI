def TutupClick(sender, context) :
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  if app.ConfirmDialog('Apakah Deposito ini akan ditutup?') :
    app.ExecuteScript('investasi/Transaksi/S_TutupDepositoKPD',app.CreateValues(['key',key]))
