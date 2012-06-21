import os, time, sys
import com.ihsan.utils as utils
import com.ihsan.lib.trace as trace
    
def state_process(application, request, response):
  global config
  config = application.config
  
  n = request.HTTPFileCount
  for i in range(n):
    info = request.GetHTTPFileInfo(i)        
    sfile = config.UserHomeDirectory + info[2]
    
    #hapus file yang bernama sama
    if os.access(sfile, os.F_OK):
      os.remove(sfile)    
    request.SaveHTTPFile(i, sfile) 
  
  response.Content = utils.CreateUploadResponse(0, 'Impor data sukses.')

  return 0

def state_generalexception(application, response, errmsg):
    # handle general exception
    response.Content = utils.CreateUploadResponse(-1, errmsg)
    
    return 0

