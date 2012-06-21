def OtoClick(sender, context):
  app = context.OwnerForm.ClientApplication
  if app.ConfirmDialog(sender.StringTag):

    app.ExecuteScript('transaction/OtoPindahPaket', \
    app.CreateValues(['id', context.GetFieldValue('RegisterCIF.ID')]))

    context.DeleteRow()

