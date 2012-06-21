#~ batch utils
#~ author : Galih Aprilian, edited by ita 30 mei 2009


import sys, types, string, time
#sys.path.append('c:/dafutils')
# import kiblat_interface

IDR = '000'
RC_DEFAULT = '0000'

def GetBatch(config):
    userinfo = config.SecurityContext.GetUserInfo()
#     ki = kiblat_interface
#     req = ki.init_request()
# 
#     req.message_code = ki.MSG_CREATEBATCH
#     req.branch_code = userinfo[4]
#     req.transaction_date = config.FormatDateTime('mm/dd/yyyy', config.Now())
#     req.user_id = 'SYSTEM'
#     req.otoriser_id = 'SYSTEM'
#     req.message_id = ''
#     req.valuta_code = 'DP'
# 
#     resp = ki.send_request(req)
# 
#     if resp.error_code != ki.EC_OK:
#         raise 'getbatch', resp.description
        
    userID = config.SecurityContext.UserID
    y,m,d = time.localtime()[:3]

    Batch = config.CreatePObject('CoreBankingBatch')
    Batch.User_ID = userID
    Batch.Tanggal = d
    Batch.Bulan = m
    Batch.Tahun = y
#     Batch.No_Batch = resp.batch_number   
    Batch.No_Batch = 'POC01'

    return Batch

def begin_session(config):

    session = 'DP_' + str(config.Now())
    
    return session
    
def commit_session(config, session, batch_code):
    if session == None: raise 'commit_session', 'session is not exist'

    ki = kiblat_interface

    userinfo = config.SecurityContext.GetUserInfo()
    req = ki.init_request()

    req.message_code = ki.MSG_COMMITTRANSACTION
    req.transaction_series = session
    req.branch_code = userinfo[4]
    req.transaction_date = config.FormatDateTime('mm/dd/yyyy', config.Now())
    req.user_id = userinfo[0].upper()
    req.otoriser_id = userinfo[0].upper()
    req.message_id = session
    req.batch_number = batch_code

    resp = ki.send_request(req)

    if resp.error_code != ki.EC_OK:
        raise 'commit_session', resp.description

def rollback_session(config, session, batch_code):
    ki = kiblat_interface
    userinfo = config.SecurityContext.GetUserInfo()
    req = ki.init_request()

    req.message_code = ki.MSG_ROLLBACKTRANSACTION
    req.transaction_series = session
    req.branch_code = userinfo[4]
    req.transaction_date = config.FormatDateTime('mm/dd/yyyy', config.Now())
    req.user_id = userinfo[0].upper()
    req.otoriser_id = userinfo[0].upper()
    req.message_id = session
    req.batch_number = batch_code

    resp = ki.send_request(req)

    if resp.error_code != ki.EC_OK:
        raise 'rollback_session', resp.description

def new_transaction(config, session, batch_code, account_number, transaction_code, \
description1, description2, transaction_type, transaction_value):
    ki = kiblat_interface
    userinfo = config.SecurityContext.GetUserInfo()
    
    req = ki.init_request()

    req.transaction_series = session
    req.message_code = ki.MSG_SENDTRANSACTION
    req.branch_code = userinfo[4]
    req.transaction_date = config.FormatDateTime('mm/dd/yyyy', config.Now())
    userid = userinfo[0][:20]
    req.inputer = userid.upper()
    req.otoriser_id = userid.upper()    
    req.batch_number = batch_code
    req.ssl_code = account_number
    req.transaction_code = transaction_code
    req.valuta_code = IDR
    req.rc_code = RC_DEFAULT
    req.description_01 = description1[:30]
    req.description_02 = description2[:30]        
    req.transaction_type = transaction_type
    req.transaction_values = transaction_value
    req.message_id = session

    resp = ki.send_request(req)

    if resp.error_code != ki.EC_OK:
        raise 'new_transaction', resp.description


'''class batch:
    __vdict = None
    __vdict_name = locals().keys()[0]

    def __init__(self, batchobj):
        self.__dict__[self.__vdict_name] = {}

        self.__obj = batchobj
        self.__config = batchobj.Config

    def __getattr__ (self, name):
        propHandled = 1
        pName = '_batch__%s' % (name)
        if self.__vdict.has_key(pName):
            return self.__vdict[pName]
        else:
            propHandled = 0

        if not propHandled:
            #~ objdata = self.batchobj.GetFieldByName(name)
            #~ if objdata == None: objdata = self.batchobj.GetLinkByName(name)
            #~ if objdata == None: raise 'getattr', '%s unknown attribut' % (name)
            raise 'getattr', '%s unknown attribut' % (name)

    def __setattr__(self, name, value):
        self.__vdict[name] = value

    def close(self):
        config = self.config
        ki = kiblat_interface

        userinfo = config.SecurityContext.GetUserInfo()
        req = ki.init_request()

        req.message_code = ki.MSG_CLOSEBATCH
        req.branch_code = userinfo[4]
        req.transaction_date = config.FormatDateTime('mm/dd/yyyy', config.Now())
        req.user_id = userinfo[0].upper()
        req.otoriser_id = userinfo[0].upper()
        req.message_id = self.session_id
        req.batch_number = self.obj.batch_code

        resp = ki.send_request(req)

        if resp.error_code != ki.EC_OK:
            raise 'closebatch', resp.description

        #self.obj.closed = 'T'

    def begin_session(self):
        config = self.config        		
		
        self.__session_id = 'REC_' + str(self.obj.last_series_number)
        self.obj.last_series_number = self.obj.last_series_number + 1

    def commit_session(self):
        if self.session_id == None: raise 'commit_session', 'session is not exist'

        config = self.config
        ki = kiblat_interface

        userinfo = config.SecurityContext.GetUserInfo()
        req = ki.init_request()

        req.message_code = ki.MSG_COMMITTRANSACTION
	#ita add
        req.transaction_series = self.session_id
        #req.transaction_series = time.strftime("%H%M%S%p", time.localtime())
        req.branch_code = userinfo[4]
        req.transaction_date = config.FormatDateTime('mm/dd/yyyy', config.Now())
        req.user_id = userinfo[0].upper()
        req.otoriser_id = userinfo[0].upper()
        req.message_id = self.session_id
        req.batch_number = self.obj.batch_code

        resp = ki.send_request(req)

        if resp.error_code != ki.EC_OK:
            raise 'commit_session', resp.description

        self.__session_id = None

    def rollback_session(self):
        if self.session_id == None: raise 'rollback_session', 'session is not exist'

        config = self.config
        ki = kiblat_interface

        userinfo = config.SecurityContext.GetUserInfo()
        req = ki.init_request()

        req.message_code = ki.MSG_ROLLBACKTRANSACTION
        req.transaction_series = self.session_id
        req.branch_code = userinfo[4]
        req.transaction_date = config.FormatDateTime('mm/dd/yyyy', config.Now())
        req.user_id = userinfo[0].upper()
        req.otoriser_id = userinfo[0].upper()
        req.message_id = self.session_id
        req.batch_number = self.obj.batch_code

        resp = ki.send_request(req)

        if resp.error_code != ki.EC_OK:
            raise 'rollback_session', resp.description

        self.__session_id = None

    def new_transaction(self):
        config = self.config
        ki = kiblat_interface

        userinfo = config.SecurityContext.GetUserInfo()
        
        trobj = config.CreatePObject('BatchTransactionDetail')
        trobj.LBatchTransaction = self.obj
        
        trobj.transaction_series = self.session_id
        trobj.message_code = ki.MSG_SENDTRANSACTION
        #trobj.session_number = self.session_id
        trobj.branch_code = userinfo[4]
        trobj.transaction_date = config.FormatDateTime('mm/dd/yyyy', config.Now())
        userid = userinfo[0][:20]
        trobj.inputer = userid
        trobj.otoriser_id = userid
        
        trobj.batch_code = self.obj.batch_code

        return batch_transaction(trobj)

class batch_transaction:
    __vdict = None
    __vdict_name = locals().keys()[0]

    def __init__(self, obj):
        self.__dict__[self.__vdict_name] = {}

        self.__obj      = obj
        self.__config   = obj.Config

    def __getattr__ (self, name):
        propHandled = 1
        pName = '_batch_transaction__%s' % (name)
        if self.__vdict.has_key(pName):
            return self.__vdict[pName]
        else:
            propHandled = 0

        if not propHandled:
            raise 'getattr', '%s unknown attribut' % (name)

    def __setattr__(self, name, value):
            self.__vdict[name] = value

    def send(self):
        obj = self.obj
        ki = kiblat_interface
        req = ki.init_request()

        req.message_code = obj.message_code
        req.batch_number = obj.batch_code
        req.transaction_series = obj.transaction_series
        req.branch_code = obj.branch_code
        trd = obj.transaction_date
        req.transaction_date = '%d/%d/%s' % (trd[1], trd[2], trd[0])
        req.user_id = obj.inputer.upper()
        req.otoriser_id = obj.otoriser_id.upper()
        req.message_id = obj.message_id
        
        self.config.SendDebugMsg(req.transaction_date)

        req.ssl_code = obj.account_number
        req.transaction_code = obj.transaction_code
        req.valuta_code = obj.valuta_code
        req.rc_code = obj.rc_code
        req.description_01 = obj.description1[:30]
        req.description_02 = obj.description2[:30]        
        req.transaction_type = obj.transaction_type
        req.transaction_values = obj.transaction_value

        resp = ki.send_request(req)
        #time.sleep(0.2)

        if resp.error_code != ki.EC_OK:
            raise 'send', resp.description
        
        
'''
