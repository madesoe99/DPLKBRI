import com.ihsan.util.modman as modman
import rpdb2
import os
import com.ihsan.lib.explorer as explorer

def FormSetDataEx(uidefs, params):
  #rpdb2.start_embedded_debugger("000")
  config = uidefs.config
  fr = params.FirstRecord
  folder = fr.path
  uidefs.PrepareReturnDataset()
  dir_dataset = uidefs.list_class.Dataset
  active_dataset = uidefs.active_directory.Dataset
  explorer.loadDirectory(config, folder, dir_dataset, active_dataset)
  return 0
#--

def download_file(config, params, returns):
  explorer.downloadFile(config, params, returns)
#--
   
def upload_file(config, params, returns):
  explorer.uploadFile(config, params, returns)
#--

def delete_file(config, params, returns):
  explorer.deleteFile(config, params, returns)
  
def rename_file(config, params, returns):
  explorer.renameFile(config, params, returns)
  
  
  
