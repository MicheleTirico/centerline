import os.path
import sys
from qgis.core import *
from centerline.spatialProcesses.buildCL import BuildCL
from centerline.spatialProcesses.buildLimits import BuildLimits


class Controller:
    def __init__(self,config):
        self.__config=config



    def compute(self,run_buildLimits,run_buildCl,run_includeFeatures):
        step=1

        self.__initQgis()

        print ("---------------------------------------------------------------------------------------------------------------------------------------------")
        # build limits
        self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Build Limits="+str(run_buildLimits))
        if run_buildLimits:
            self.__bl=BuildLimits(self.__config)
            step, pathOutput=self.__bl.compute(step,self.__config.output_pathCenterline)
        else:    pathOutput=self.__config.inputBuildings

        print ("---------------------------------------------------------------------------------------------------------------------------------------------")
        self.__config.logger.log(cl=self,method=sys._getframe(),message="Qgis. Build centerline="+str(run_buildCl))
        if run_buildCl:
            # build CL
            self.__bcl=BuildCL(self.__config,run_buildCl)        # self.__bcl.compute_separated(step)
            step, pathOutput=self.__bcl.compute(step,pathOutput)
            self.__exitQgis()

    def __initQgis(self):
        QgsApplication.setPrefixPath(self.__config.prefixPath,True)
        from processing.core.Processing import Processing
        self.__qgs=QgsApplication([], False)
        self.__qgs.initQgis()
        Processing.initialize()  # needed to be able to use the functions afterwards
    def __exitQgis(self):
        self.__qgs.exitQgis()



    # def __compute_buildCl(self,run):
    #
    #     # input limits area
    #
    #     # init class
    #     self.__bcl=BuildCL(self.__config,run)
    #     self.__run=run
    #     # get path inputs
    #     if os.path.exists(self.__config.output_pathLimits)==False:
    #         print ("warning read file")
    #         self.__config.output_pathLimits="/home/mt_licit/project/centerline/centerline/output/lyon1/lyon1_ign_limits.shp"
    #         pathInput="/home/mt_licit/project/centerline/centerline/resources/lyon1/lyon1_ign_limits.shp"
    #
    #     step=0
    #     # initialise process
    #     self.__bcl.initQgis()
    #     self.__bcl.compute(step)
    #     self.__bcl.exitQgis()
    #
    # def __compute_includeFeatures(self,run):
    #     pass
    # def __compute_buildLimits(self,run):
    #     self.__bl=BuildLimits(False)
    #

# self.__compute_buildLimits(run_buildLimits)
        # self.__compute_buildCl(run_buildCl)
        # self.__compute_includeFeatures(run_includeFeatures)

   #  def __getNameProcess(self,nameProcess,pathFile):
   #      file_name, file_extension = os.path.splitext(pathFile)
   #      return str(os.path.splitext(pathFile)[0])+"_"+str(nameProcess.split(":")[1])+file_extension
   #
   #  def __getNameProcessStep(self,pathFileInput,pathDirectoryOutput,step):
   #      # file + ext
   #      base=os.path.basename(pathFileInput)
   #      file_name=os.path.splitext(base)[0]
   #      file_name=os.path.splitext(base)[0].split("-")[0]
   #      file_extension = os.path.splitext(pathFileInput)[1]
   # #     if pathDirectoryOutput[-1]!="/": pathDirectoryOutput+"/"
   #      output=pathDirectoryOutput+file_name+"-{0:0>3}".format(step)+file_extension
   #  #    print ("aaaaaaaaaaaaaaaaaaaaaaaa",pathDirectoryOutput,base,file_name,file_extension,output,"aaaaaaaaaaaaaaaaaaaaaaaa",sep="\n")
   #      return             output,step+1
   #
   #
   #  # deprecated
   #  def __initQgis(self,run):
   #      if run:
   #          QgsApplication.setPrefixPath(self.__config.prefixPath,True)
   #          from processing.core.Processing import Processing
   #          self.__qgs=QgsApplication([], False)
   #          self.__qgs.initQgis()
   #          Processing.initialize()  # needed to be able to use the functions afterwards
   #
   #  # deprecated
   #  def __exitQgis(self,run):
   #      if run:         self.__qgs.exitQgis()



"""
        # convert buildings to points
        # get boundary of buildings
        nameProcess="native:boundary"
        pathInput="/home/mt_licit/project/centerline/centerline/resources/lyon1/lyon1_ign_limits.shp"
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)


        # densify the boundary of the building by interval
        nameProcess="native:densifygeometriesgivenaninterval"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"INTERVAL":3}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)
        path_01=pathOutput

        # convert the boundary to points
        nameProcess="native:extractvertices"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"DISTANCE":1}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # voronoi

        # build voronoi (longer step)
        nameProcess="qgis:voronoipolygons"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"BUFFER":20}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # voronoi to lines
        nameProcess="native:polygonstolines"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # explode voronoi lines
        nameProcess="native:explodelines"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # remove voronoi lines which crosses buildings
        nameProcess="qgis:extractbylocation"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"PREDICATE":2,"INTERSECT":path_01}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # clean centerline

        # polygonization of centerline
        nameProcess="native:polygonize"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # convert centerline to single parts
        nameProcess="native:multiparttosingleparts"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # get boundaries
        nameProcess="qgis:convertgeometrytype"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"TYPE":2}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # dissolve centerline
        nameProcess="native:dissolve"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # convert dissolve to single part
        nameProcess="native:multiparttosingleparts"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # simplify
        nameProcess="native:simplifygeometries"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)

        # clip study area
        nameProcess="qgis:clip"
        pathInput=pathOutput
        pathOutput,step=self.__getNameProcessStep(pathFileInput=pathInput,pathDirectoryOutput=self.__config.pathOutput,step=step)
        parameters={"OVERLAY":self.__config.inputStudyArea}
        self.__bcl.runQgisProcess(nameProcess=nameProcess,pathInput=pathInput,pathOutput=pathOutput,parameters=parameters)
"""