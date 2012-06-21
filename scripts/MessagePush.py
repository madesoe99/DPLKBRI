import com.ihsan.net.messagecenterlib as netmessage

# OnIncomingPushMessage demo (in appglobal_client.py)

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  app = config.AppObject
  try:
    messageCenter = netmessage.MessageCenterLib(config,'localhost',8099) 
    message = parameter.FirstRecord.message
    
    if parameter.FirstRecord.isBroadcast:
      #broadcast message
      messageCenter.SendBroadcastMessage(message)
    else:
      #kirim message to spesific user
      messageCenter.SendMessageTo(parameter.FirstRecord.userID, message)
      
  finally:
    app = None

  return 1
