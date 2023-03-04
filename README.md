

Dokumentation (Ablauf VS Code)

Enthaltene Datenstruktur im Ordner vehicledetection





Konfiguration

1\. Im Ordner webcams das Skript **get\_all\_webcams.py** ausführen: Die Datei webcams.geojson

wird im Ordner webcams/geojsonfiles/ gespeichert und enthält alle Webcamstandorte in RLP

2\. Verarbeitung in QGIS (QGIS\_Vorgehen.pdf): Ergebnis sind 3 Dateien

\-

\-

\-

**Webcams\_mz.geojson**

**Camera\_fahrspuren.geojson**

**Fahrtrichtungen\_locations.geojson**

è Speicherung in webcams/geojsonfiles/

è In den Dateien Ä,ü,ö und ß ersetzen (ae, ue, oe, ss)

*(die notwendigen Daten sind auch im Ordner QGIS im Geopackage data.gpkg zu finden)*

3\. Im Ordner webcams das Skript folders\_img.py ausführen: Anlegen von

Ordnern mit dem Namen der Kamera-ID im Ordner mainz/images

\+ Datei im Ordner Mainz mit Übersicht der Kamera-ID und Request-Url

4\. Nach der Installation von Docker Desktop und dem Download der docker-compose.yml Datei

(https://github.com/FraunhoferIOSB/FROST-Server/blob/v2.x/scripts/docker-compose.yaml)

kann der FROST-Server über den Befehl „docker compose up“ im Dateinpfad

„…/vehicledetection/frost“ eingerichtet werden

è Mit dem Befehl „docker update --restart unless-stopped *container\_id*“ wird ein

automatischer Neustart der Container nach einem Reboot vorgenommen

è Zugang über http://localhost:8080/FROST-Server/v1.0 (oder anstatt localhost, eine

andere Severadresse)

(Ansicht in Docker Desktop der laufenden Container)

5\. Mit dem Skript frost/setup\_server\_mz.py (und setup\_server\_eng.py für die Demonstration

mit Kameras aus England) werden dann die Objekte in den einzelnen Klassen angelegt

è Things, Sensors, ObservedProperty, Locations, Datastreams

è Unter Verwendung der Dateien: webcams\_mz.geojson; camera\_fahrspuren.geojson;

fahrtrichtungen\_locations.geojson

è Für England wurden 3 selektierte Kameras verwendet: Namen und Koordinaten in

Array eintragen

è Gleichzeitig werden die geposteten Objekte in JSON-Dateien im Ordner

frost/jsonfiles/mainz oder /england gespeichert





Automatisierter Workflow

3 verschiedene Skripte

Bilddetektionsalgorithmus:

https://techvidvan.com/tutorials/opencv-vehicle-detection-classification-counting/

è Die für den YOLOv3 Algorithmus benötigten Dateien finden sich im Ordner yolo

I.

Scripts/vehicle\_counter\_req\_mz.py:

·

·

Schleife über Kamera IDs

Greift auf die API der Mainzer Webcams zu, um das aktuelle Bild

abzufragen („https://verkehr.rlp.de/api/webcams/"+id+"/pic/

640x480?t=1653908021526")

·

·

Objektdetektion im Bild

Gleichzeitig wird ein Ordner mit dem aktuellen Timestamp angelegt

(mainz/images/id/timestamp), in dem das Originalbild, das

Detektionsergebnis und die erstellte Observation gespeichert sind

.

Die Speicherung kann zukünftig gelöscht oder auskommentiert

werden, um Speicherplatz zu sparen, hier nur zur Demonstration

·

Bei Wiederbereitstellung der Bilder direkter Post auf FROST-Server, hier

auskommentiert

è Da die Bilder aktuell nicht verfügbar sind, kann keine sinnvolle Auswertung gemacht

werden, zur Demonstration des Workflow wurde trotzdem das Bild angefragt,

gespeichert, eine Objektdetektion gemacht und eine Observation für die

entsprechende





II.

Scripts/create\_rand\_obs.py:

·

·

·

Abfrage aller Datastreams und Schleife über diese

Erzeugen von Observations für jeden Datastream mit random Zählwert

Speicherung der JSON-Datei im Ordner mainz/random mit dem aktuellen

Timestamp als Dateinamen

.

Die Speicherung kann zukünftig gelöscht oder auskommentiert

werden, um Speicherplatz zu sparen, hier nur zur Demonstration

·

·

Direkter Post auf FROS-Server

Hier mit time.sleep(600) Befehl in While Schleife, um ein dauerhaftes

Ausführen alle 10 Minuten zur Demonstration zu gewährleisten

è Alternative zu nicht funktionierendem Dockercontainer oder

Scheduled Tasks in Windows

III.

Scripts/vehicle\_req\_eng.py:

·

Selektion von den Kameras A1 52010 A14, A1 52022 A141, A14 50685

J21 von https://uktraffic.live/england/

URLs der Bilder in Array eintragen

.

·

·

·

·

Schleife über Kameras

Abfrage des aktuellen Bilds über URL

Objektdetektion im Bild

Gleichzeitig werden Ordner mit den Namen den „IDs“ der Kameras im

Ordner england angelegt

·

Während dem Ablauf wird ein Ordner mit dem aktuellen Timestamp

angelegt (england/name/timestamp), in dem das Originalbild, das

Detektionsergebnis und die erstellte Observation gespeichert sind

.

Die Speicherung kann zukünftig gelöscht oder auskommentiert

werden, um Speicherplatz zu sparen, hier nur zur Demonstration

è Die Auswertung von Kamerabilder in England dient der Demonstration an echten

Bildern, bei denen die Detektion funktioniert und sinnvolle Ergebnisse liefert

·

Hier mit time.sleep(36000) Befehl in While Schleife, um ein dauerhaftes

Ausführen alle 3 Stunden zur Demonstration zu gewährleisten

è Alternative zu nicht funktionierendem Dockercontainer oder

Scheduled Tasks in Windows





Visualisierung

1\. STAM Anwendung von GitHub herunterladen: https://github.com/DataCoveEU/STAM

2\. Im Ordner example wird nur die leaflet.html Datei benötigt à example hier in webpage

umbenannt & Lizenzdateien in Ordner licence extrahiert

3\. Hintergrundkarte einfügen

4\. baseUrl und die Zentrumskoordinaten der Karte anpassen

5\. 2 Buttons einfügen, um leichter zwischen Mainz und England zu wechseln à mit

Zoomfunktion auf Ort





Testbilder & Experimente

·

**Beispielbilder**: Mit dem Skript scripts/vehicle\_counter\_testpics.py wird eine Objektdetektion

von den Bildern im Ordner test/images vorgenommen und die Ergebnisse im Ordner

test/results gespeichert

o

o

Die Bildquellen der Bilder sind in der Datei Bildquellen.txt gespeichert

Zudem wird von den Beispielbildern eine Observations-Datei angelegt, die aus jedem

Bild die Zählung im JSON-Format speichert

·

**Segmentation**:

1\. Im Ordner test\_cv kann mit dem Skript areaofinterest\_analysis.py eine manuelle

Selektion von Bildbereichen schrittweise vorgenommen werden. Am Beispiel der

Bilder im Ordner test\_cv/images wird manuell jeweils der Bereich der

dargestellten Fahrspuren selektiert

2\. und diese jeweils in einem eigenen Bild im Ordner test\_cv/results gespeichert

3\. durch Ausführen des Skripts scripts/vehicle\_counter\_segmentationtest.py wird

dann eine Objektdetektion über diese Bildausschnitte gemacht und die

Ergebnisse in test\_cv/results/objdetect gespeichert

