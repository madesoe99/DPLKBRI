import com.ihsan.util.modman as modman
import rpdb2
import os
import com.ihsan.lib.explorer as explorer

def FormSetDataEx(uidefs, params):
  #rpdb2.start_embedded_debugger("000")
  config = uidefs.config
  fr = params.FirstRecord
  dsParam = fr.Dataset 
  folder = fr.path
  uidefs.PrepareReturnDataset()
  dir_dataset = uidefs.list_class.Dataset
  active_dataset = uidefs.active_directory.Dataset
  mask = fr.mask
  if mask == "": mask = "*.*"
  explorer.loadDirectory(config, folder, dir_dataset, active_dataset, mask)
  return 0
#--

def download_file(config, params, returns):
  explorer.downloadFile(config, params, returns)
#--
   
def upload_file(config, params, returns):
  explorer.uploadFile(config, params, returns)
#--
