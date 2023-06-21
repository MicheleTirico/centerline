import os
import sys
from qgis.core import *

def runQgisProcess(self,config,nameProcess,pathInput,pathOutput,parameters,step):

    if os.path.exists(pathOutput)==False:
        config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Start  process "+"{0:0>2}".format(step)+": "+nameProcess+", parameters: "+str(parameters)+", pathIn: "+pathInput)
        import processing
        p={"INPUT":pathInput,"OUTPUT":pathOutput}
        if len(parameters)!=0:p.update(parameters)
        processing.run(nameProcess,p)
        config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Finish process "+"{0:0>2}".format(step)+": "+nameProcess+", pathOutput: "+pathOutput)
#        return pathOutput
    else:
        config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Process "+"{0:0>2}".format(step)+": "+nameProcess+" not computed. The file exists, pathOutput: "+pathOutput)

    return step+1

def runQgisProcess_completeParams(self,config,nameProcess,parameters,pathOutput, step):
    if os.path.exists(pathOutput)==False:
        config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Start  process "+"{0:0>2}".format(step)+": "+nameProcess+", parameters: "+str(parameters)+", pathIn: "+parameters["INPUT"])
        import processing
        if len(parameters)!=0:p.update(parameters)
        processing.run(nameProcess,parameters)
        config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Finish process "+"{0:0>2}".format(step)+": "+nameProcess+", pathOutput: "+parameters["OUTPUT"])
    #        return pathOutput
    else:
        config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Process "+"{0:0>2}".format(step)+": "+nameProcess+" not computed. The file exists, pathOutput: "+parameters["OUTPUT"])

def runQgisProcessParameters(nameProcess,parameters):
    import processing
    processing.run(nameProcess,parameters)

def getNameProcessStep(pathFileInput,pathDirectoryOutput,step):
    base=os.path.basename(pathFileInput)
    file_name=os.path.splitext(base)[0].split("-")[0]
    file_extension = os.path.splitext(pathFileInput)[1]
    output=pathDirectoryOutput+file_name+"-{0:0>3}".format(step)+file_extension
    return output,step+1

