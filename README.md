Die Erläuterung zum Code sind im Ordner *'Dokumentation'* zu finden.

  1. Objektdetektion_Python: Hier ist das Vorgehen, der Ablauf und die Organisation der Skripte erläutert.
  2. GQIS_Vorgehen: Für den spezifischen Fall der Mainzer Verkehrskameras mussten die Straßenabschnitte zunächst händisch bzw. ermittelt werden. Dieser Ablauf ist hier        beschrieben.
  
Der entwickelte Prototyp zur automatisierten Ermittlung und Bereitstellung mittels Sensor Things API befindet sich im Ordner *'workflow_traffic_analysis'*.

  1. vehicledetection: Hier befinden sich in verschiedenen Verzeichnissen die Skripte der einzelnen Schritte des Workflows, sowie weitere Tests und potentielle Ansätze 
     zur Weiterentwicklung.
     Hinweis: Eine relativ große Datei der Gewichte (yolov3-320.weights) des yolov3 Algorithmus befindet sich zur Zeit noch nicht im Ordner
     'workflow_traffic_analysis/vehicledetection/yolo', kann aber hier heruntergeladen werden: 
     https://techvidvan.com/tutorials/opencv-vehicle-detection-classification-counting/ 
     (oder direkt hier: https://drive.google.com/file/d/1jQPLyibctn8b333a91Lnt3Yl468_H62r/view)
  2. STAM: Hier befindet sich die implementierte Webmap, Sensor Things API Map (Copyright (c) 2020, DataCove e.U. All rights reserved.)
