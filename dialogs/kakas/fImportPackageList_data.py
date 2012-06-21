import com.ihsan.lib.trace as trace
import com.ihsan.lib.importpackage as importpackage

def FormGeneralSetData(uidefs, uiname, objdata):
    config = uidefs.config

    helper = importpackage.ImportPackageHelper(config)
    helper.LoadPackageListToDataset(uidefs.PackageDefList.Dataset)

    return 0
    
