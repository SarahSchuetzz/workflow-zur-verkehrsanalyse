#Skript zum Anlegen einer Verzeichnisstruktur der einzelnen Kameras

import os
import geojson

#current working directory
working_directory=os.getcwd()
print(working_directory)

#open file with webcams in Mainz
geojsonfile=open(working_directory+"\\webcams\\geojsonfiles\\webcams_mz.geojson")
geojson=geojson.load(geojsonfile)

#Anzahl der Webcams in MZ
#print(str(len(geojson['features'])))

idfile=open(working_directory+"\\mainz\\request_url_list.txt", 'w')

#create a folder for every webcam (id) for storing images
for i in range(len(geojson['features'])):
    id=str(geojson['features'][i]['properties']['id'])
    if(i!=len(geojson['features'])):
        idfile.write(id+";https://verkehr.rlp.de/api/webcams/"+id+"/pic/640x480?t=1653908021526\n")
    else:
        idfile.write(id+";")
    #https://www.geeksforgeeks.org/create-a-directory-in-python/
    os.makedirs(working_directory+"\\mainz\\images\\"+id)

print("done :)")