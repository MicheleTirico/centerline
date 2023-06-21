import fiona
from shapely.geometry import Polygon, mapping


# fileIn=
polygon = Polygon([(-180, 35), (-170, -33),..., (-153, -30)])
# schema of the shapefile
schema = {'geometry': 'Polygon','properties': {'FIRST_FLD': 'char'}}
# write the shapefile
with fiona.collection('polygon.shp', 'w', 'ESRI Shapefile', schema) as layer:
    feature = {}
    feature['geometry'] = mapping(polygon)
    feature['properties'] = {'FIRST_FLD': ...}
    layer.write(feature)