class frmMessageCenter:

    def __init__(self, formObj, parentForm):
        pass

    def Show(self):
        stdConsole = self.stdConsole
        stdConsole.ConsoleFilterName = 'std'
        stdConsole.ShowStatusBar = 0
        stdConsole.Headerless = 1
        stdConsole.Activate()

        app = self.FormObject.ClientApplication
        #app.ShowConsoleOnRequest('std')
        #app.HideConsoleOnRequest()

        self.FormContainer.Show()

    def sendClick(self, sender):
        app = self.FormObject.ClientApplication

        message = self.inputPanel_message.Text
        target_userid = self.inputPanel_userID.Text

        if target_userid.strip() == '':
            form.ShowMessage('Please define target userid!')
            return

        param = app.CreateValues(['message', message], ['userid', target_userid])
        ph = app.ExecuteScript('kakas/SendMessage', param)
        rec = ph.FirstRecord
        if rec.IsErr:
            raise Exception, rec.ErrMessage

