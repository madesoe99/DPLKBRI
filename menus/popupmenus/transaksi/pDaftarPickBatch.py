def mnuShowModalWithData(sender, context):
  app = context.OwnerForm.ClientApplication

  #siapkan paket
  ph = app.CreatePacket()
  packet = ph.packet
  rec = packet.CreateDataPacketStructure('keyID: integer')
  if context.Name == 'qBatch':
    rec.keyID = context.GetFieldValue('TransactionBatch.hidden_idbatch')
  elif context.Name == 'gListBatch':
    rec.keyID = context.OwnerForm.GetUIPartByName('uipListBatch').hidden_idbatch

  #tentukan SystemContext
  try:
    sysContext = ''
    if context.OwnerForm.SystemContext != '':
      sysContext = context.OwnerForm.SystemContext + '://'

    form_id = sender.Name
    group_id = sender.StringTag
    oform = app.CreateForm(sysContext + group_id + '/' + form_id, form_id, 0, ph, None)
    oform.FormShow()
  finally:
    app = None
