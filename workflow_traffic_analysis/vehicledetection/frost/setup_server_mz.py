#Einrichten des FROST-Servers mit den Klassen: Things, Sensors, ObservedProperties, Locations, Datastreams
#für Mainz


import os
import json
import requests
import subprocess
from osgeo import gdal
import geojson

#current working directory
working_directory=os.getcwd()

#Punktobjekte der Kameras in Mainz
geojsonmzdirec= working_directory+"\\webcams\\geojsonfiles\\webcams_mz.geojson"
geojsmz_f=open(geojsonmzdirec,'r')
webcamsmzgj=geojson.load(geojsmz_f)

#linestrings der Sichtbereiche
frdirec= working_directory+"\\webcams\\geojsonfiles\\fahrtrichtungen_locations.geojson"
fr_f=open(frdirec,'r')
frgeojson=geojson.load(fr_f)

#Relation zwischen Kamera und Fahrspur
cf_direc= working_directory+"\\webcams\\geojsonfiles\\camera_fahrspuren.geojson"
cf_f=open(cf_direc,'r')
cfgeojson=geojson.load(cf_f)

# things--------------------------------------------------------------------
thingsurl="http://localhost:8080/FROST-Server/v1.0/Things"

thingsjson="""{
    "things":[
    """
for i in range(len(frgeojson['features'])):
    name=frgeojson['features'][i]['properties']['fahrtrichtung']
    for c in range(len(cfgeojson['features'])):
        if cfgeojson['features'][c]['properties']['fahrtrichtung']==name:
            id=cfgeojson['features'][c]['properties']['id']
    thingsjson+="""    {
          "name" : "%s",
          "description" : "Sichtbereich der Kamera %s",
          "properties" : {}
        }"""%(name,str(id))
    if i != (len(frgeojson['features'])-1):
        thingsjson+=""",
    """
thingsjson+="""
    ]
}"""

#store
open(working_directory+"/frost/jsonfiles/mainz/things.json","w").write(thingsjson)
#post
thingsjson=json.loads(thingsjson)
for t in thingsjson['things']:
    thingsjs=json.dumps(t,indent=2, separators=(',', ': '))
    res=requests.post(thingsurl, thingsjs)

# ObservedProperty----------------------------------------------------------------
obspropurl="http://localhost:8080/FROST-Server/v1.0/ObservedProperties"

obspropjson="""{
  "name": "count", 
  "description": "number of vehicles in webcam picture",
  "properties": {},
  "definition": "https://www.lexico.com/definition/count"
}"""

#store
open(working_directory+"/frost/jsonfiles/mainz/observedproperty.json","w").write(obspropjson)
#post
obspropjson=json.loads(obspropjson)
obspropjs=json.dumps(obspropjson,indent=2, separators=(',', ': '))
res=requests.post(obspropurl, obspropjs)

# sensor----------------------------------------------------------------
sensorurl="http://localhost:8080/FROST-Server/v1.0/Sensors"


sensorjson="""{
    "sensors": [
        """

for s in range(len(webcamsmzgj['features'])):
    sensorjson+="""{
        "name": "Camera %s",
        "description": "Traffic Webcam",
        "properties": {},
        "encodingType": "",
        "metadata": ""
    }"""%(str(webcamsmzgj['features'][s]['properties']['id']))
    if s != (len(webcamsmzgj['features'])-1):
        sensorjson+=""",
    """
sensorjson+="""
    ]
}"""

#store
open(working_directory+"/frost/jsonfiles/mainz/sensor.json","w").write(sensorjson)
#post
sensorjson=json.loads(sensorjson)
for sen in sensorjson['sensors']:
    sensorjs=json.dumps(sen,indent=2, separators=(',', ': '))
    res=requests.post(sensorurl, sensorjs)

#locations--------------------------------------------------------------------
locationurl="http://localhost:8080/FROST-Server/v1.0/Locations"

locationsjson="""{
    "locations": [
        """
for i in range(len(frgeojson['features'])):
    name=frgeojson['features'][i]['properties']['fahrtrichtung']
    for c in range(len(cfgeojson['features'])):
        if cfgeojson['features'][c]['properties']['fahrtrichtung']==name:
            id=cfgeojson['features'][c]['properties']['id']
    url2 = "http://localhost:8080/FROST-Server/v1.0/Things?$filter=name eq'"+name+"'"
    res=requests.get(url2).json()

    locationsjson+="""{
            "name": "%s",
            "description": "surveyed street part of camera %s",
            "properties": %s,
            "encodingType": "application/geo+json",
            "location": {
                "type": "MultiLineString",
                "coordinates": %s
            },
            "Things": [
                { "@iot.id": %s}
            ]
        }"""%(name,str(id),str("{}"),str(frgeojson['features'][i]['geometry']['coordinates']),
                    str(res['value'][0]['@iot.id']))
    if i != (len(frgeojson['features'])-1):
        locationsjson+=""",
    """

locationsjson+="""
    ]
}"""

#store
open(working_directory+"/frost/jsonfiles/mainz/locations.json","w").write(locationsjson)
#post
locationsjson=json.loads(locationsjson)
for l in locationsjson['locations']:
    locationjs=json.dumps(l,indent=2, separators=(',', ': '))
    res=requests.post(locationurl, locationjs)

#datastreams--------------------------------------------------------------------
datastreamurl="http://localhost:8080/FROST-Server/v1.0/Datastreams"

datastreamjson="""{
    "datastreams": [
    """

for i in range(len(frgeojson['features'])):
    name=frgeojson['features'][i]['properties']['fahrtrichtung']
    for c in range(len(cfgeojson['features'])):
        if cfgeojson['features'][c]['properties']['fahrtrichtung']==name:
            id=cfgeojson['features'][c]['properties']['id']
    url2 = "http://localhost:8080/FROST-Server/v1.0/Things?$filter=name eq'"+name+"'"
    thing=requests.get(url2).json()
    url3 = "http://localhost:8080/FROST-Server/v1.0/Sensors?$filter=endswith(name,'"+str(id)+"')"
    sensor=requests.get(url3).json()
    datastreamjson+="""    {
            "name" : "number of cars from camera in direction %s",
            "description" : "counted cars at specific time from camera %s",
            "observationType": "https://defs.opengis.net/vocprez/object?uri=http%%3A//www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation",
            "unitOfMeasurement": {
                "name": "number"
            },
            "Thing": {"@iot.id": %s},
            "Sensor": {"@iot.id": %s},
            "ObservedProperty": {"@iot.id": 1}
        }"""%(name,str(id),str(thing['value'][0]['@iot.id']),str(sensor['value'][0]['@iot.id']))
    if i != (len(frgeojson['features'])-1):
        datastreamjson+=""",
    """
    
datastreamjson+="""
    ]
}"""

#store
open(working_directory+"/frost/jsonfiles/mainz/datastreams.json","w").write(datastreamjson)
#post
datastreamjson=json.loads(datastreamjson)
for d in datastreamjson['datastreams']:
    datastreamjs=json.dumps(d,indent=2, separators=(',', ': '))
    res=requests.post(datastreamurl, datastreamjs)
print("done :)")