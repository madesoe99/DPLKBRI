import com.ihsan.lib.trace as trace
import com.ihsan.lib.importpackage as importpackage

def FormSetDataEx(uidefs, parameter):
    config = uidefs.config

    helper = importpackage.ImportPackageHelper(config)
    helper.LoadPackageListToDataset(uidefs.PackageDefList.Dataset)
    
    return 0

