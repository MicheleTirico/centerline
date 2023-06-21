import xml.etree.ElementTree as ET
import sys
from datetime import datetime


# input data
class Config:
    def __init__(self,pathConfig):
        self.__pathConfig=pathConfig
        self.__tree=ET.parse(self.__pathConfig)
        self.__data=self.__tree.getroot()
        #self.__initConfig()

    def setLogger(self,logger):
        self.logger=logger

    def initConfig(self):
        self.logger.log(cl=self,method=sys._getframe(),message="init config")
        self.pathAbs=                       self.__getValType("urls","url","absPath","dir")+"/"
        self.prefixPath=                    self.__getValType("urls","url","prefixPath","dir")+"/"

        # path folders
        self.pathResources=                 self.pathAbs+self.__getValType("urls","url","resources","dir")+"/"
        self.pathResource=                  self.pathResources+self.__getValType("urls","url","resource","dir")+"/"
        self.pathOutputs=                   self.pathAbs+self.__getValType("urls","url","outputs","dir")+"/"
        self.pathOutput=                    self.pathOutputs+self.__getValType("urls","url","resource","dir")+"/"
        self.pathLog=                       self.pathOutput+self.__getValType("urls","url","resource","dir")+"_log.md"

        # path inputs
        self.inputBuildings=                self.pathResource+self.__getValType("urls","url","inputBuildings","file")
        self.inputStudyArea=                self.pathResource+self.__getValType("urls","url","inputStudyArea","file")
        self.inputRoadNetwork=              self.pathResource+self.__getValType("urls","url","inputRoadNetwork","file")+".shp"


        # path new
        self.output_pathLimits=             self.pathOutputs+"limits.shp"
        self.output_pathCenterline=         self.pathOutputs+"centerline.shp"

        # parameters Qgis build centerline
        self.param_densifygeometriesgivenaninterval_01=     self.__getParameterQgis("buildcl","parameter","densifygeometriesgivenaninterval","parameter",1)
        self.param_extractVertices_01=                    self.__getParameterQgis("buildcl","parameter","extractVertices","parameter",1)
        self.param_voronoipolygons_01=                    self.__getParameterQgis("buildcl","parameter","voronoipolygons","parameter",1)
        self.param_extractbylocation_01=                    self.__getParameterQgis("buildcl","parameter","extractbylocation","parameter",1)
        self.param_convertgeometrytype_01=                    self.__getParameterQgis("buildcl","parameter","convertgeometrytype","parameter",1)
        self.param_buildCl_simplifygeometries_01=self.__getParameterQgis("buildcl","parameter","convertgeometrytype","parameter",1)

        # parameters Qgis build limits
        self.list_files_merge=          self.__getListLayers("buildLimits","parameter","layers_to_merge","files","layer",1)
        self.param_limits_difference_01=                    self.pathResource+self.__getParameterQgis("buildLimits","parameter","difference","parameter",1)["OVERLAY"]

    def __getValType(self,name_root,name_tag,name,type):
        tag_root=self.__data.find(name_root)
        for e in tag_root.iter(name_tag):
            if e.get("name")==name and e.get("type")==type: return e.text.replace(" ","")
    #        self.logger.error(cl=self,method=sys._getframe(),message="no value for "+name_root+", "+name_tag+", "+type)

    def __getParameterQgis(self,name_root,name_tag,name,type,step):
        tag_root=self.__data.find(name_root)
        dic={}
        for e in tag_root.iter(name_tag):
            if e.get("name")==name and e.get("type")==type and e.get("step")==str(step):
                name_params=e.get("params").split(" ")
                val_params=e.text.split(" ")
                for i in range(len(name_params)):
                    dic[name_params[i]]=val_params[i]
        if len(dic)==0: self.logger.warning(cl=self,method=sys.getframe(),message="Qgis parameter not set.",doQuit=True,doReturn=True)
        return dic

    def __getListLayers(self,name_root,name_tag,name,type,params,step):
        tag_root=self.__data.find(name_root)
        dic={}
        list=[]
        for e in tag_root.iter(name_tag):
            if e.get("name")==name and e.get("type")==type and e.get("step")==str(step) and e.get("params")==params:
                name_params=e.get("params").replace(" ","")
                val_params=e.text.split(" ")
                val_params.remove("")
                for i in range(0,len(val_params)):
                    dic[name_params+"_{0:0>2}".format(str(i+1))]=val_params[i]
                    list.append(self.pathResource+val_params[i])
        if len(dic)==0: self.logger.warning(cl=self,method=sys.getframe(),message="Qgis parameter not set.",doQuit=True,doReturn=True)
        # return " ".join(list)
        return list








