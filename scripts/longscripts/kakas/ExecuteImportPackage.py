import sys
import com.ihsan.lib.importpackage as importpackage
import com.ihsan.lib.trace as trace
import com.ihsan.utils as utils

sys.path.append('c:/dafapp/dplk07/script_modules')
import kakasapi

#import rpdb2; rpdb2.start_embedded_debugger("000")

def DAFLongScriptMain(config, parameter, pid, monfilename):
    # config: ISysConfig object
    # parameter: TPClassUIDataPacket
    # pid: Process ID of this script
    # monfilename: Monitor file name to store status    
    countSleepSend = 0
    app = config.AppObject
    rec = parameter.FirstRecord
    
    consoleID   = 'ExecutePackage_' + str(pid)
    
    #app.CreateConsole(consoleID, 'progress')    
    #app.CreateConsole('process_status', 'short')
    
    #fileLog = open(config.GetHomeDir()[:-1]+'trackedtasks/'+consoleID,'w')
    config.SendDebugMsg('ExcutePackage mulai berlangsung')
    app.ConWriteln('ExcutePackage mulai berlangsung', monfilename)
    try:        
        config.BeginTransaction()
        try:
            sw = parameter.GetStreamWrapperByName("upload")
            if sw == None:
              raise "Stream not found"

            sourceFilename  = config.UserHomeDirectory + utils.ExtractFileName(rec.sourceFilename)
            packageName     = rec.packageName

            sw.SaveToFile(sourceFilename)
            
            helper = importpackage.ImportPackageHelper(config)
            package = helper.LoadFromRepository(packageName)
            data = package.OpenDataSource(sourceFilename)
            config.SendDebugMsg('eip1='+sourceFilename)
            try:
                #app.SwitchDefaultConsole(consoleID)
#                 pt = config.ProgressTracker
#                 pt.ProgressLevel1()
#                 
#                 pt.SetProgressInfo2(1, 'Mulai processing data...')            

                # Prepare after apply row function
                modName     = package.TransformationDef.AfterApplyRowModule
                funcName    = package.TransformationDef.AfterApplyRowFunctionName                
                module      = utils.ImportAppScripts(config, modName)
                
                config.SendDebugMsg('eip2')
                targetClassName = package.TransformationDef.TargetClassName
                kakasapi.Logging(config, targetClassName, \
                  '--- Package was loaded. Start processing %s' % (sourceFilename))

                config.SendDebugMsg('eip3='+modName)
                afterApplyRow = utils.GetFunctionFromModule(module, funcName)
                beforeCreateObject = utils.GetFunctionFromModule(module, 'BeforeCreateObject')
                # processing data
                data.First()
                i = 1
                while not data.Eof():
                    # checking before create object
                    try:
                      config.SendDebugMsg('eip4 %s' % i)
                      if not beforeCreateObject(config, targetClassName, data):
                        i = i + 1
                        data.Next()
                        continue

                      obj = config.CreatePObject(targetClassName)
                      # Transform value
                      n = len(package.TransItemDefs)
                      for j in range(n):
                          rec = package.TransItemDefs[j]
                          config.SendDebugMsg('rec.SourceFieldName: '+ str(rec.SourceFieldName))
                          value = data.GetFieldByName(rec.SourceFieldName)
                          config.SendDebugMsg('value: '+ str(value))
                          if rec.LookupClass.strip() != '':
                              # search lookup
                              lookup = config.CreatePObjImplProxy(rec.LookupClass)
                              lookup.Key = value
                              if lookup.isnull:
                                  raise Exception, 'ExecuteImportPackage', '%s tidak ditemukan pada %s (field number %d) !' % (str(value), rec.LookupClass +  j)
                          if value == None or value == "None":
                            pass
                          else:
                            obj.SetFieldByName(rec.Name, value)
                      # process after apply row
                      afterApplyRow(config, obj, data)
                      countSleepSend += 1
                      if countSleepSend == 10 :
                        app.ConWriteln('..10 baris terproses',monfilename)
                        countSleepSend = 0
                    except:
                      sErrMsg = str(sys.exc_info()[0]) + ':' + str(sys.exc_info()[1])
                      kakasapi.Logging(config, targetClassName, 'Error processing line %d:%s' % (i, sErrMsg))
                      raise

#                     pt.SetProgressInfo2(1, '%d data terproses' % i)
                    data.Next()
                    i += 1
                # data.Eof()
            finally:
                data.Close()                

            config.Commit()
            #app.WriteConsole('Proses impor data selesai', 'process_status')
            app.ConWriteln('Proses impor data selesai', monfilename)
        except:
            config.Rollback()
            processStatus = str(sys.exc_info()[1])
            #app.WriteConsole('Server error:' + processStatus, 'process_status')
            app.ConWriteln('Server error:' + processStatus, monfilename)            
            raise Exception, 'ExecuteImportPackage' +  processStatus
    finally:
        #app.CloseConsole('process_status')
        #app.CloseConsole(consoleID)
        pass#fileLog.close()
    
    return 0
