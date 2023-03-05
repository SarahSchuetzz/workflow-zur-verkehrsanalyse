#Skript zur Abfrage der in Mainz stationierten Verkehrskameras

import os
import json
import requests
import subprocess
from osgeo import gdal
import geojson

#current working directory
working_directory=os.getcwd()

# get json data of webcam positions----------------------------------------------------------------------------
#https://www.geeksforgeeks.org/read-json-file-using-python/
response=requests.get("https://verkehr.rlp.de/api/webcams")
#json_file= open(working_directory+"\\webcams\\webcams.json",'r',encoding='utf-8')
jsonData=response.json()
#print(jsonData)

#geojson format: https://de.wikipedia.org/wiki/GeoJSON
geojsontxt="""{"type": "FeatureCollection",
 "features":["""

for i in range(len(jsonData)):
    geojsontxt+="""
    { 
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [%s, %s]
        },
        "properties": {
            "id": "%s",
            "desc": "%s",
            "angle": "%s"
        }
    }""" %(jsonData[i]['lng'],jsonData[i]['lat'],jsonData[i]['id'],jsonData[i]['beschreibung'],jsonData[i]['winkel'])
    if i != (len(jsonData)-1):
        geojsontxt+=""",
        """
    
geojsontxt+="""
    ]
}"""

geojsondirec= working_directory+"\\webcams\\geojsonfiles\\webcams.geojson"
geojson_file=open(geojsondirec,'w')
geojson_file.write(geojsontxt)

# shapedirec= working_directory+"\\webcams\\shapes\\webcams.shp"

# args=['ogr2ogr', '-f', 'ESRI Shapefile', '%s' %shapedirec, '%s'%geojsondirec]
# subprocess.run(args)

print("done :)")