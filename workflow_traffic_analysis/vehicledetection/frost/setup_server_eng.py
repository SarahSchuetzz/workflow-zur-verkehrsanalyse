#Einrichten des FROST-Servers mit den Klassen: Things, Sensors, ObservedProperties, Locations, Datastreams
#für England (prototypisch)

import os
import json
import requests
import subprocess
from osgeo import gdal
import geojson

#current working directory
working_directory=os.getcwd()+"/frost/jsonfiles/england/"

#Namen der Kamerastandorte
names=['A1 52010 A14','A1 52022 A141','A14 50685 J21']

#händisch ausgelesene Koordinaten der Kameras
# https://uktraffic.live/england/
locations_eng= ([-0.2462220,52.319946],[-0.2481408,52.33081],[-0.25988823,52.332146])

# things--------------------------------------------------------------------
thingsurl="http://localhost:8080/FROST-Server/v1.0/Things"
thingsjson="""{
    "things":[
        """
for n in range(len(names)):
    thingsjson+="""{
        "name" : "%s",
        "description" : "Sichtbereich der Kamera",
        "properties" : {}
    }"""%(str(names[n]))
    if n != (len(names)-1):
        thingsjson+=""",
    """
thingsjson+="""
    ]
}"""

#store
open(working_directory+"things.json","w").write(thingsjson)
#post
thingsjson=json.loads(thingsjson)
for t in thingsjson['things']:
    thingsjs=json.dumps(t,indent=2, separators=(',', ': '))
    res=requests.post(thingsurl, thingsjs)


# sensor----------------------------------------------------------------
sensorurl="http://localhost:8080/FROST-Server/v1.0/Sensors"

sensorjson="""{
    "sensors": [
        {
            "name": "Camera England",
            "description": "Traffic Webcam",
            "properties": {},
            "encodingType": "",
            "metadata": ""
        }
    ]
}"""

#store 
open(working_directory+"sensor.json","w").write(sensorjson)
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
for l in range(len(locations_eng)):
    name=names[l]
    url2 = "http://localhost:8080/FROST-Server/v1.0/Things?$filter=name eq'"+name+"'"
    res=requests.get(url2).json()

    locationsjson+="""{
            "name": "%s",
            "description": "surveyed street part of camera",
            "properties": %s,
            "encodingType": "application/geo+json",
            "location": {
                "type": "Point",
                "coordinates": %s
            },
            "Things": [
                { "@iot.id": %s}
            ]
        }"""%(name,str("{}"),str(locations_eng[l]),str(res['value'][0]['@iot.id']))
    if l != (len(locations_eng)-1):
        locationsjson+=""",
    """

locationsjson+="""
    ]
}"""

#store
open(working_directory+"locations.json","w").write(locationsjson)
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

for n in range(len(names)):
    url2 = "http://localhost:8080/FROST-Server/v1.0/Things?$filter=name eq'"+names[n]+"'"
    thing=requests.get(url2).json()
    url3 = "http://localhost:8080/FROST-Server/v1.0/Sensors?$filter=name eq 'Camera England'"
    sensor=requests.get(url3).json()
    datastreamjson+="""    {
            "name" : "number of cars at %s",
            "description" : "counted cars at specific time from camera",
            "observationType": "https://defs.opengis.net/vocprez/object?uri=http%%3A//www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation",
            "unitOfMeasurement": {
                "name": "number"
            },
            "Thing": {"@iot.id": %s},
            "Sensor": {"@iot.id": %s},
            "ObservedProperty": {"@iot.id": 1}
        }"""%(str(names[n]),str(thing['value'][0]['@iot.id']),str(sensor['value'][0]['@iot.id']))
    if n != (len(names)-1):
        datastreamjson+=""",
    """
    
datastreamjson+="""
    ]
}"""

#store
open(working_directory+"datastreams.json","w").write(datastreamjson)
#post
datastreamjson=json.loads(datastreamjson)
for d in datastreamjson['datastreams']:
    datastreamjs=json.dumps(d,indent=2, separators=(',', ': '))
    res=requests.post(datastreamurl, datastreamjs)
print("done :)")