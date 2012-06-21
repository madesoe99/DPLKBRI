import sys
import com.ihsan.lib.trace as trace
import com.ihsan.utils as utils
import com.ihsan.lib.importpackage as importpackage

def DAFScriptMain(config, parameter, returnpacket):
    # config: ISysConfig object
    # parameter: TPClassUIDataPacket
    # returnpacket: TPClassUIDataPacket (undefined structure)
    rec = parameter.FirstRecord
    
    try:
        helper = importpackage.ImportPackageHelper(config)
        helper.DeleteFromRepository(rec.Name)
        
        returnpacket.CreateValues(['IsErr', 0])
    except:
        config.Rollback()
        utils.SetPacketAsError(returnpacket, str(sys.exc_info()[1]))
        
    return 1
