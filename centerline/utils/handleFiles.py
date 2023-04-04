import os
import sys
from datetime import datetime


class HandleFiles:
    def __init__(self,config):
        self.__config =config

    def initDirectories(self,deleteDirectories,createDirectories):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="init directories")
        if deleteDirectories:
            paths=[self.__config.pathOutput]
            self.__deleteDirectories(paths)

        if createDirectories:
            paths=[self.__config.pathOutputs,self.__config.pathOutput]
            self.__createDirectories(paths)

    def __deleteDirectories(self,paths):
        for path in paths :
            if os.path.exists(path):
                self.__config.logger.log(cl=self,method=sys._getframe(),message="delete directory: " +path)
                os.system("rm -r "+path)


    def __createDirectories(self,paths):
        for path in paths :
            if os.path.exists(path)==False:
                self.__config.logger.log(cl=self,method=sys._getframe(),message="create directory in: "+path)
                os.system("mkdir "+path)
        return [str(datetime.now()), self,sys._getframe() ]
