# def CekRekening(config, noRekening):
#   tReturn = ['Rekening tidak terdefinisi!','','','','',0.0,'',0.0,0.0,'']
# 
#   sessionID = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'AppName') + \
#     config.SecurityContext.UserID
#   isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
#     'NeedLoginCoreBanking')
# 
#   if isNeedLoginCoreBanking == 'T':
#     #user sudah login ke core banking
#     param = config.AppObject.CreateValues(\
#       ['AccountNumber', noRekening])
# 
#     #remote eksekusi cek rekening at core banking
#     try:
#       ph = config.AppObject.rexecscript(sessionID,'remote/AccountInfo',param,0)
#       if not ph.FirstRecord.IsErr:
#         namaPemilik = ph.FirstRecord.BriefName
#         tReturn = [namaPemilik,\
#           ph.FirstRecord.IDNumber,\
#           ph.FirstRecord.BranchNo,\
#           ph.FirstRecord.AccountType,\
#           ph.FirstRecord.AccountStatus,\
#           ph.FirstRecord.Balance,\
#           ph.FirstRecord.CurrencyNo,\
#           ph.FirstRecord.EkuivalenValue,\
#           ph.FirstRecord.CurrentBalance,\
#           ph.FirstRecord.MotherName]
#       else:
#         raise Exception, '\n\nError' + ph.FirstRecord.ErrMessage
#     except:
#       raise
#       
#   return tReturn
# 
# def DAFScriptMain(config, parameter, returnpacket):
#   # config: ISysConfig object
#   # parameter: TPClassUIDataPacket
#   # returnpacket: TPClassUIDataPacket (undefined structure)
# 
#   noRekening = parameter.FirstRecord.noRekening
#   
#   try:
#     tReturn = CekRekening(config, noRekening)      
#   except:
#     raise
#   
#   returnpacket.CreateValues(['namaPemilikRekening',tReturn[0]],\
#     ['idNumber',tReturn[1]],\
#     ['branchCode',tReturn[2]],\
#     ['accountType',tReturn[3]],\
#     ['accountStatus',tReturn[4]],\
#     ['balance',tReturn[5]],\
#     ['currencyCode',tReturn[6]],\
#     ['ekivValue',tReturn[7]],\
#     ['currentBalance',tReturn[8]],\
#     ['motherName',tReturn[9]],)
# 
#   return 1

######################### NEW CODE T2KR #####################################

import sys
import com.ihsan.lib.trace as trace
sys.path.append('c:/dafutils')
import messagelib

def checkaccount(account_no, userid, host, port):
    exist = 0; account_name = 'N/A'; account_type = '99'; account_status = 0
    add_name = ''; is_oldaccount = 0; newaccount = ''; cabang_rek = ''; 
    kode_valuta = ''; no_identitas = ''
    
    messagereq = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%.2f;%s;%s;%s;%s;%s;%s;%s' % (
            'CREK', account_no, '', '', '', '', '', '', '', 0.0,
            userid, '', '', '', '', '', '')

    messageresp = messagelib.SendStreamMsg(messagereq, host, port)
    messageresp = messageresp.split(';')

    if len(messageresp) < 6:
      raise Exception, '90' +  'Error receiving data from kiblat : ' + str(messageresp)

    if messageresp[4] == '00':
        res  = messageresp[5]; res  = res.split('|')
        exist = int(res[0])
        if exist:
            account_type = res[1].strip(); account_name = res[2].strip()
            cabang_rek = res[4]
            
            if len(res) > 5:
                kode_valuta = res[8]
                no_identitas = res[9]
    
    account_name = account_name.replace('`', '\'')
    account_name = account_name.replace('"', '\'')

    return account_name, account_type, cabang_rek, kode_valuta, no_identitas

def CekRekening(config, noRekening):
  tReturn = ['Rekening tidak terdefinisi!','','','','']

  userID = config.SecurityContext.UserID
#   isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
#     'NeedLoginCoreBanking')
  Host = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
    'HostCoreBanking')
  Port = int(config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
    'PortCoreBanking'))
  
#   if isNeedLoginCoreBanking == 'T':
  try:
      account_name, account_type, cabang_rek, kode_valuta, no_identitas = checkaccount(noRekening, userID, Host, Port) 
      tReturn = [account_name,\
        no_identitas,\
        cabang_rek,\
        account_type,\
        kode_valuta]
  except:
    raise
      
  return tReturn

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  noRekening = parameter.FirstRecord.noRekening
  
  try:
    tReturn = CekRekening(config, noRekening)      
  except:
    raise
  
  returnpacket.CreateValues(['namaPemilikRekening',tReturn[0]],\
    ['idNumber',tReturn[1]],\
    ['branchCode',tReturn[2]],\
    ['accountType',tReturn[3]],\
    ['currencyCode',tReturn[4]])

  return 1

