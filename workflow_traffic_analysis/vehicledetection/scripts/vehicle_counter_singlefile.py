#Skript zur Objektdetektion in nur einem Bild
#Anpassung bei den mit <--- gekennzeichneten Zeilen


# TechVidvan Vehicle counting and Classification
#https://techvidvan.com/tutorials/opencv-vehicle-detection-classification-counting/

# Import necessary packages

from msilib.schema import Directory
import cv2
import collections
import numpy as np
import os
from tracker import EuclideanDistTracker
from itertools import zip_longest as izip_longest


#current working directory
working_directory=os.getcwd()

img_name='8_result2.jpg'                                    #<----------------------------------------------
img_fn=working_directory+"\\test_cv\\results\\"+ img_name   #<----------------------------------------------
image_file =img_fn

# Initialize Tracker
tracker = EuclideanDistTracker()

input_size = 320

# Detection confidence threshold
confThreshold =0.2
nmsThreshold= 0.2

font_color = (0, 0, 255)
font_size = 0.5
font_thickness = 2

# Middle cross line position
middle_line_position = 225   
up_line_position = middle_line_position - 15
down_line_position = middle_line_position + 15


# Store Coco Names in a list
classesFile = working_directory+ "\\yolo\\coco.names"
classNames = open(classesFile).read().strip().split('\n')
#print(classNames)
#print(len(classNames))

# class index for our required detection classes
required_class_index = [2, 3, 5, 7]

detected_classNames = []

## Model Files
modelConfiguration =working_directory+ "\\yolo\\yolov3-320.cfg"
modelWeigheights = working_directory+ "\\yolo\\yolov3-320.weights"

# configure the network model
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights)

# Configure the network backend

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Define random colour for each class
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8')


# Function for finding the center of a rectangle
def find_center(x, y, w, h):
    x1=int(w/2)
    y1=int(h/2)
    cx = x+x1
    cy=y+y1
    return cx, cy
    
# List for store vehicle count information
temp_up_list = []
temp_down_list = []
up_list = [0, 0, 0, 0]
down_list = [0, 0, 0, 0]

# Function for count vehicle
def count_vehicle(box_id, img):

    x, y, w, h, id, index = box_id

    # Find the center of the rectangle for detection
    center = find_center(x, y, w, h)
    ix, iy = center
    
    # Find the current position of the vehicle
    if (iy > up_line_position) and (iy < middle_line_position):

        if id not in temp_up_list:
            temp_up_list.append(id)

    elif iy < down_line_position and iy > middle_line_position:
        if id not in temp_down_list:
            temp_down_list.append(id)
            
    elif iy < up_line_position:
        if id in temp_down_list:
            temp_down_list.remove(id)
            up_list[index] = up_list[index]+1

    elif iy > down_line_position:
        if id in temp_up_list:
            temp_up_list.remove(id)
            down_list[index] = down_list[index] + 1

    # Draw circle in the middle of the rectangle
    cv2.circle(img, center, 2, (0, 0, 255), -1)  # end here
    # print(up_list, down_list)

# Function for finding the detected objects from the network output
def postProcess(outputs,img):
    global detected_classNames 
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    detection = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if classId in required_class_index:
                if confidence > confThreshold:
                    # print(classId)
                    w,h = int(det[2]*width) , int(det[3]*height)
                    x,y = int((det[0]*width)-w/2) , int((det[1]*height)-h/2)
                    boxes.append([x,y,w,h])
                    classIds.append(classId)
                    confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold)
    # print(classIds)
    if len(indices)>0:
        for i in indices.flatten():
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
            # print(x,y,w,h)

            color = [int(c) for c in colors[classIds[i]]]
            name = classNames[classIds[i]]
            detected_classNames.append(name)
            # Draw classname and confidence score 
            cv2.putText(img,f'{name.upper()} {int(confidence_scores[i]*100)}%',
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Draw bounding rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            detection.append([x, y, w, h, required_class_index.index(classIds[i])])

    # Update the tracker for each object
    boxes_ids = tracker.update(detection)
    for box_id in boxes_ids:
        count_vehicle(box_id, img)


def from_static_image(image):
    img = cv2.imread(image)

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

    # Set the input of the network
    net.setInput(blob)
    layersNames = net.getLayerNames()
    outputNames=[]
    for i in net.getUnconnectedOutLayers():
        outputNames.append(layersNames[i - 1])
    # Feed data to the network
    outputs = net.forward(outputNames)

    # Find the objects from the network output
    postProcess(outputs,img)

    # count the frequency of detected classes
    frequency = collections.Counter(detected_classNames)
    print(frequency)
    # Draw counting texts in the frame
    cv2.putText(img, "Car:        "+str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Motorbike:  "+str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Bus:        "+str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Truck:      "+str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)


    # cv2.imshow("image", img)
    #je nach verwendeten Bildern result-Pfad anpassen
    result_file=working_directory+ img_name.replace('.','_objdetect.')              #<------------------------------------------------

    cv2.imwrite(result_file,img)

    cv2.waitKey(0)

    sumofvehicles=frequency['car']+frequency['motorbike']+frequency['bus']+frequency['truck']
            
    global Observjson
    Observjson+="""{
            "result" : %s,
            "Datastream": 999
        }"""%(str(sumofvehicles))
    global f
    
    if f != (l-1):
        Observjson+=""",
        """

if __name__ == '__main__':
    #from_static_image(image_file)

    
    Observjson="""{
    "Observations":[
        """
    #1 for example pics with area of interest
    w_dir=working_directory+"\\test_cv\\results\\"

    #2 for example pics for different weather conditions
    # w_dir=working_directory+"\\data\\"

    l=0
    for file in os.listdir(w_dir):
        img_name=os.fsdecode(file)
        if img_name.endswith('.jpg') or img_name.endswith('.png'):
            l+=1
    f=0
    for file in os.listdir(w_dir):
        img_name=os.fsdecode(file)
        if (img_name.endswith('.jpg') or img_name.endswith('.png')):
            img_fn=w_dir+ img_name
            image_file =img_fn
            print(image_file)
            from_static_image(image_file)
            f+=1
    
    Observjson+="""
    ]
}"""
    
    #1
    open(w_dir+"\\objdetect\\Observations_test.json","w").write(Observjson)
    #2
    # open(w_dir+"\\Observations_example.json","w").write(Observjson)
