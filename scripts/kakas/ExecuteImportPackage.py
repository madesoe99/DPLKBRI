import sys
import com.ihsan.lib.importpackage as importpackage
import com.ihsan.lib.trace as trace
import com.ihsan.utils as utils

sys.path.append('c:/dafapp/dplk07/script_modules')
import kakasapi

# import rpdb2; rpdb2.start_embedded_debugger("000")

def DAFLongScriptMain(config, parameter, pid, monfilename):
    # config: ISysConfig object
    # parameter: TPClassUIDataPacket
    # pid: Process ID of this script
    # monfilename: Monitor file name to store status    
    
    #import rpdb2; rpdb2.start_embedded_debugger("000")
    app = config.AppObject
    rec = parameter.FirstRecord
    
    consoleID   = 'ExecutePackage_' + str(pid)
    
    app.ConCreate(consoleID)
    try:
        config.BeginTransaction()
        try:
            sw = parameter.GetStreamWrapperByName("upload")
            if sw == None:
              raise "Stream not found"

            sourceFilename  = config.UserHomeDirectory + utils.ExtractFileName(rec.sourceFilename)
            packageName     = rec.packageName

            sw.SaveToFile(sourceFilename)
            app.ConWriteln('Data file uploaded', consoleID)
            
            helper = importpackage.ImportPackageHelper(config)
            package = helper.LoadFromRepository(packageName)
            app.ConWriteln('Package file opened', consoleID)
            data = package.OpenDataSource(sourceFilename)
            app.ConWriteln('Data source opened', consoleID)
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
                
                targetClassName = package.TransformationDef.TargetClassName
                kakasapi.Logging(config, targetClassName, \
                  '--- Package was loaded. Start processing %s' % (sourceFilename))

                afterApplyRow = utils.GetFunctionFromModule(module, funcName)
                beforeCreateObject = utils.GetFunctionFromModule(module, 'BeforeCreateObject')
                # processing data
                app.ConWriteln('Start processing....', consoleID)
                config.SendDebugMsg('Start processing package')
                data.First()
                i = 1
                while not data.Eof():
                    # checking before create object
                    try:
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
                          if rec.LookupClass.strip() != '':
                              # search lookup
                              lookup = config.CreatePObjImplProxy(rec.LookupClass)
                              lookup.Key = value
                              if lookup.isnull:
                                  raise Exception, 'ExecuteImportPackage', '%s tidak ditemukan pada %s (field number %d) !' % (str(value), rec.LookupClass +  j)

                          obj.SetFieldByName(rec.Name, value)
                      # process after apply row
                      afterApplyRow(config, obj, data)
                    except:
                      sErrMsg = str(sys.exc_info()[0]) + ':' + str(sys.exc_info()[1])
                      kakasapi.Logging(config, targetClassName, 'Error processing line %d:%s' % (i, sErrMsg))
                      raise
                      
                    app.ConWriteln('Proses data ke - %d selesai' % i, consoleID)
                    config.SendDebugMsg('Proses data ke - %d selesai' % i)

                    data.Next()
                    i += 1
                # data.Eof()
            finally:
                data.Close()                

            config.Commit()
            app.ConWriteln('Proses impor data selesai', consoleID)
        except:
            config.Rollback()
            processStatus = str(sys.exc_info()[1])
            app.ConWriteln('Server error:' + processStatus, consoleID)
            raise Exception, 'ExecuteImportPackage' +  processStatus
    finally:
      pass
    #--

    return 0
