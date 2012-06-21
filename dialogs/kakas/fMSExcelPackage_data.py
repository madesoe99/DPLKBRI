import com.ihsan.lib.trace as trace
import com.ihsan.lib.importpackage as importpackage

def FormSetDataEx(uidefs, parameter):
    config = uidefs.config

    rec = parameter.FirstRecord
    if rec.Mode == 'NEW':
        return

    helper = importpackage.ImportPackageHelper(config)

    if rec.Mode in ('VIEW', 'EDIT'):
        package = helper.LoadFromRepository(rec.Name)
        package.LoadToUIDefList(uidefs)

def OnGeneralProcessData(uidefs, data):
    config = uidefs.Config

    helper = importpackage.ImportPackageHelper(config)

    package = helper.CreateFromDataPacket(data)
    package.Save()

    return 0
