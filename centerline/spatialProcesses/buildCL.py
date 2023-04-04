import os
import sys

from qgis.core import *

from centerline.spatialProcesses import processQgis


class BuildCL:
    def __init__(self,config,run):
        self.__config=config
        self.__run=run

    def initQgis(self):
        if self.__run:
            QgsApplication.setPrefixPath(self.__config.prefixPath,True)
            from processing.core.Processing import Processing
            self.__qgs=QgsApplication([], False)
            self.__qgs.initQgis()
            Processing.initialize()  # needed to be able to use the functions afterwards
    def exitQgis(self):
        if self.__run:     self.__qgs.exitQgis()

    def compute(self,step,pathInput):
        if self.__run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Start build Centerline")
            path_01=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step+3)[0]


            nameProcesses=[
                "native:multiparttosingleparts",    # multi
                "native:dissolve",                  # dissolve
                "native:simplifygeometries",        # simplify
                "native:densifygeometriesgivenaninterval",  # densify vertices
                "native:extractvertices",           # vertices
                "qgis:voronoipolygons",
                "native:polygonstolines",
                "native:explodelines",
                "qgis:extractbylocation",
                "native:polygonize",
                "native:multiparttosingleparts",
                "qgis:convertgeometrytype",
                "native:dissolve",
                "native:multiparttosingleparts",
                "native:simplifygeometries",
                "qgis:clip"
            ]

            parameters=[
                {},                         # multi
                {},                         # dissolve
                self.__config.param_buildCl_simplifygeometries_01,#{'METHOD':0,'TOLERANCE':1}, # simplify
                {"INTERVAL":self.__config.param_densifygeometriesgivenaninterval_01["INTERVAL"]},
                {},                         # vertices
                {"BUFFER":self.__config.param_voronoipolygons_01["BUFFER"]},
                {},
                {},
                {"PREDICATE":self.__config.param_extractbylocation_01["PREDICATE"],"INTERSECT":path_01},
                {},
                {},
                {"TYPE":self.__config.param_convertgeometrytype_01["TYPE"]},
                {},
                {},
                {},
                {"OVERLAY":self.__config.inputStudyArea}
            ]
            pathOutput=""
            if len(nameProcesses)==0: self.__config.logger.warning(cl=self,method=sys._getframe(),message="Qgis. Process",doQuit=False,doReturn=False)
            else:
                for i in range(len(nameProcesses)):
                    if i!=0:pathInput=pathOutput
                    pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
                    processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcesses[i],pathInput=pathInput,pathOutput=pathOutput,parameters=parameters[i],step=step)

            self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Finish build Centerline")

            return step, pathOutput



    def compute_old_01(self,step,pathInput):
        # print  (     self.__config.inputStudyArea       ,self.__config.param_convertgeometrytype_01    ,self.__config.param_extractbylocation_01  ,self.__config.param_voronoipolygons_01    )
            # quit()
        if self.__run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Start build Centerline")

            #        pathInput="/home/mt_licit/project/centerline/centerline/resources/lyon1/lyon1_ign_limits.shp"





            processQgis.runQgisProcess(self=self,config=self.__config,nameProcess="native:createspatialindex",pathInput=pathInput,pathOutput="",parameters={},step=step)
            path_01=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step+2)[0]

            nameProcesses=[
                "native:boundary",
                "native:densifygeometriesgivenaninterval",
                "native:extractvertices",
                "qgis:voronoipolygons",
                "native:polygonstolines",
                "native:explodelines",
                "qgis:extractbylocation",
                "native:polygonize",
                "native:multiparttosingleparts",
                "qgis:convertgeometrytype",
                "native:dissolve",
                "native:multiparttosingleparts",
                "native:simplifygeometries",
                "qgis:clip"
            ]

            parameters=[
                {},
                {"INTERVAL":self.__config.param_densifygeometriesgivenaninterval_01["INTERVAL"]},
                {"DISTANCE":self.__config.param_extractVertices_01["DISTANCE"]},
                {"BUFFER":self.__config.param_voronoipolygons_01["BUFFER"]},
                {},
                {},
                {"PREDICATE":self.__config.param_extractbylocation_01["PREDICATE"],"INTERSECT":path_01},
                {},
                {},
                {"TYPE":self.__config.param_convertgeometrytype_01["TYPE"]},
                {},
                {},
                {},
                {"OVERLAY":self.__config.inputStudyArea}
            ]
            pathOutput=""
            if len(nameProcesses)==0:
                self.__config.logger.warning(cl=self,method=sys._getframe(),message="Qgis. Process",doQuit=False,doReturn=False)
            else:
                for i in range(len(nameProcesses)):
                    if i!=0:pathInput=pathOutput
                    pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
                    processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcesses[i],pathInput=pathInput,pathOutput=pathOutput,parameters=parameters[i],step=step)


            self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Finish build Centerline")

            return step, pathOutput
    def compute_separated(self,step):

        # convert buildings to points
        # get boundary of buildings
        nameProcess="native:boundary"
        pathInput="/home/mt_licit/project/centerline/centerline/resources/lyon1/lyon1_ign_limits.shp"
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)


        # densify the boundary of the building by interval
        nameProcess="native:densifygeometriesgivenaninterval"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"INTERVAL":3}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)
        path_01=pathOutput

        # convert the boundary to points
        nameProcess="native:extractvertices"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"DISTANCE":1}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # voronoi

        # build voronoi (longer step)
        nameProcess="qgis:voronoipolygons"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"BUFFER":20}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # voronoi to lines
        nameProcess="native:polygonstolines"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # explode voronoi lines
        nameProcess="native:explodelines"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # remove voronoi lines which crosses buildings
        nameProcess="qgis:extractbylocation"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"PREDICATE":2,"INTERSECT":path_01}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # clean centerline

        # polygonization of centerline
        nameProcess="native:polygonize"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # convert centerline to single parts
        nameProcess="native:multiparttosingleparts"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # get boundaries
        nameProcess="qgis:convertgeometrytype"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"TYPE":2}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # dissolve centerline
        nameProcess="native:dissolve"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # convert dissolve to single part
        nameProcess="native:multiparttosingleparts"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # simplify
        nameProcess="native:simplifygeometries"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)

        # clip study area
        nameProcess="qgis:clip"
        pathInput=pathOutput
        pathOutput,step=processQgis.getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"OVERLAY":self.__config.inputStudyArea}
        processQgis.runQgisProcess(self=self,config=self.__config,nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters,step=step)
























    def runQgisProcessParameters(self,nameProcess,parameters):
        import processing
        processing.run(nameProcess,parameters)

    def runQgisProcess(self,nameProcess,pathInput,pathOutput,parameters):
        if os.path.exists(pathOutput)==False:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Start  process: "+nameProcess+", parameters: "+str(parameters)+", pathIn: "+pathInput)
            import processing
            p={"INPUT":pathInput,"OUTPUT":pathOutput}
            if len(parameters)!=0:p.update(parameters)
            processing.run(nameProcess,p)
            self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Finish process: "+nameProcess+", pathOutput: "+pathOutput)
            return pathOutput
        else:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Process not computed. The file exists, pathOutput: "+pathOutput)



