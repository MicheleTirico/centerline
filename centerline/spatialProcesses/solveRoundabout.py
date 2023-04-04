from qgis.core import *

def buildDic(layer):
    features =layer.getFeatures ()
    point_to_line = {}
    for feature in features :
        geom = feature . geometry ()
        geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
        if geom.type () == QgsWkbTypes . LineGeometry :
            if geomSingleType :
                x = geom. asPolyline ()
                if x [0] not in point_to_line . keys () :
                    point_to_line [ x [0]] = [ feature . id () ]
                else :
                    point_to_line [ x [0]]. append ( feature . id () )
                if x [1] not in point_to_line . keys () :
                    point_to_line [ x [1]] = [ feature . id () ]
                else :
                    point_to_line [ x [1]]. append ( feature . id () )
            else :
                x = geom .asMultiPolyline()

                if x [0][0] not in point_to_line . keys () :
                    point_to_line [ x [0][0]] = [ feature . id () ]
                else :
                    point_to_line [ x [0][0]]. append ( feature . id () )
                if x [0][1] not in point_to_line . keys () :
                    point_to_line [ x [0][1]] = [ feature . id () ]
                else :
                    point_to_line [ x [0][1]]. append ( feature . id () )
        else :
            print ( " Unknown or invalid geometry " )
        print (point_to_line)
        return point_to_line

def getCenterPoint (layer):
    print ("init get")
    new_line={}
    features=layer.getFeatures()
    for feature in features:
        geom = feature . geometry ()
        geomSingleType = QgsWkbTypes.isSingleType ( geom . wkbType () )
        if geom . type () == QgsWkbTypes . LineGeometry :
            if geomSingleType :
                x = geom . asPolyline ()
                if ( geom . length () <10) :
                    x0 = x [0]. x ()
                    y0 = x [0]. y ()
                    x1 = x [1]. x ()
                    y1 = x [1]. y ()
                    # get center
                    new_x = ( x0 + x1 ) / 2
                    new_y = ( y0 + y1 ) / 2
                    list1=point_to_line[x[0]]
                    list2=point_to_line[x[1]]
                    list1.extend(list2)

                    for line_fid in list1 :
                        voisin = layer.getFeature ( line_fid )
                        voisin_geom = voisin . geometry ()
                        voisin_line = voisin_geom . asMultiPolyline()
                        x2 = voisin_line [0]. x ()
                        y2 = voisin_line [0]. y ()
                        x3 = voisin_line [1]. x ()
                        y3 = voisin_line [1]. y ()

                        if line_fid in new_line :
                            voisin_geom = new_line [ line_fid ]
                            voisin_line = voisin_geom . asMultiPolyline()
                            x2 = voisin_line [0]. x ()
                            y2 = voisin_line [0]. y ()
                            x3 = voisin_line [1]. x ()
                            y3 = voisin_line [1]. y ()
                            if ( x0 == x2 and y0 == y2 ) :
                                new_geom = QgsGeometry .fromMultiPolylineXY ([ QgsPointXY ( new_x , new_y ) , QgsPointXY ( x3
                                                                                                         , y3 ) ])
                                new_line [ line_fid ] = new_geom
                                if ( x0 == x3 and y0 == y3 ) :
                                    new_geom = QgsGeometry .fromMultiPolylineXY ([ QgsPointXY ( new_x , new_y ) , QgsPointXY ( x2, y2 ) ])
                                    new_line [ line_fid ] = new_geom
                                    if ( x1 == x2 and y1 == y2 ) :
                                        new_geom = QgsGeometry .fromMultiPolylineXY  ([ QgsPointXY ( new_x , new_y ) , QgsPointXY ( x3, y3 ) ])
                                        new_line [ line_fid ] = new_geom
                                    if ( x1 == x3 and y1 == y3 ) :
                                        new_geom = QgsGeometry .fromMultiPolylineXY ([ QgsPointXY ( new_x , new_y ) , QgsPointXY ( x2, y2 ) ])
                                        new_line [ line_fid ] = new_geom
                                        updateLayer(new_line)


def updateLayer(new_line):
    for key,value in new_line.items():
        if caps & QgsVectorDataProvider.ChangeGeometries:
            layer.dataProvider().chageGeometryValues({key:value})

    if iface.mapCanvas().isCachingEnabled():
        layer.triggerRepaint()
    else:
        iface.mapCanvas().refrech()

prefix=""
QgsApplication.setPrefixPath(prefix,True)
from processing.core.Processing import Processing
qgs=QgsApplication([], False)
qgs.initQgis()
Processing.initialize()  # needed to be able to use the functions afterwards

path="/home/mt_licit/project/centerline/centerline/outputs/lyon1_02/test.shp"
layer=QgsVectorLayer(path)
point_to_line=buildDic(layer)
getCenterPoint(layer)

qgs.exitQgis()