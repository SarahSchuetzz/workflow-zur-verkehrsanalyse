#Skript zum Erstellen von fiktiven Zähldaten, da für Mainz aktuell keine Bilder bereitgestellt sind
#bei Freischaltung --> vehicle_counter_mz.py

from datetime import datetime
from random import randint
import time
import os
import json
import geojson
import requests

#current working directory
working_directory=os.getcwd()+"\\mainz\\random\\"

#Schleife als Alternative für getaktetes Ausführen
while True:
    #https://www.programiz.com/python-programming/time
    now=datetime.now()
    current_time=now.strftime("%d%m%Y_%H%M%S")

    url="http://localhost:8080/FROST-Server/v1.0/Datastreams"
    res=requests.get(url).json()

    obsjson="""{
        "Observations":[
            """
    for d in range(len(res['value'])):
        obsjson+="""{
                "result" : %s,
                "Datastream": {"@iot.id": %s}
            }"""%(str(randint(1,111)),(res['value'][d]['@iot.id']))
        if d != (len(res['value'])-1):
            obsjson+=""",
            """
    obsjson+="""
        ]
    }"""

    #store
    open(working_directory+current_time+"_randObs.json",'w').write(obsjson)
        
    #immediately post to frost-server
    Obsurl="http://localhost:8080/FROST-Server/v1.0/Observations"
    obsjson=json.loads(obsjson)
    for d in obsjson['Observations']:
        obsjs=json.dumps(d,indent=2, separators=(',', ': '))
        res=requests.post(Obsurl, obsjs)
        print(res.text)
    
    print("done :)")
    
    #alle 10 Minuten zur Demonstration
    time.sleep(600)