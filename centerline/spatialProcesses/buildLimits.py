import os
import sys
from qgis.core import *

from centerline.spatialProcesses import processQgis


class BuildLimits:
    def __init__(self,config):
        self.__config=config
#        self.__run=run

    def initQgis(self):
 #       if self.__run:
        QgsApplication.setPrefixPath(self.__config.prefixPath,True)
        from processing.core.Processing import Processing
        self.__qgs=QgsApplication([], False)
        self.__qgs.initQgis()
        Processing.initialize()  # needed to be able to use the functions afterwards
    def exitQgis(self):
        # if self.__run:
        self.__qgs.exitQgis()

    def compute(self,step,pathInput):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Start build Limits")
        # spatial index
        for f in self.__config.list_files_merge:
            step=processQgis.runQgisProcess(self=self,config=self.__config,nameProcess="native:createspatialindex",pathInput=f,pathOutput="",parameters={},step=step)

        nameProcesses=[            "native:mergevectorlayers","qgis:difference","native:dissolve"        ]
        parameters=[            { 'LAYERS': self.__config.list_files_merge }, None,{}        ]
        pathOutput=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)[0]
        step=processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcesses[0],pathInput=pathInput,pathOutput=pathOutput,parameters=parameters[0],step=step)

        pathOutput=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)[0]
        step=processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcesses[0],pathInput=pathInput,pathOutput=pathOutput,parameters=parameters[0],step=step)

        pathInput=pathOutput
        pathOutput=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)[0]
        p={"INPUT" : QgsProcessingFeatureSourceDefinition(pathInput, selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OUTPUT' : pathOutput, 'OVERLAY' : self.__config.param_limits_difference_01}
        step=processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcesses[1],pathInput=pathInput,pathOutput=pathOutput,parameters=p,step=step)

        pathInput=pathOutput
        pathOutput=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)[0]
        step=processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcesses[2],pathInput=pathInput,pathOutput=pathOutput,parameters=parameters[2],step=step)

        self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Finish build Limits")

        return step, pathOutput
        
