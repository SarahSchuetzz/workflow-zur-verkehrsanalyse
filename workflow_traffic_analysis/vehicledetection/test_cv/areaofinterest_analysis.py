# Skript zur Erstellung von Area of Interest in einem Bild (händisch)

#https://medium.com/@mrhwick/simple-lane-detection-with-opencv-bfeb6ae54ec0
# TechVidvan Vehicle counting and Classification
#https://techvidvan.com/tutorials/opencv-vehicle-detection-classification-counting/

# Import necessary packages

from msilib.schema import Directory
import collections
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
import time
import geojson

working_directory=os.getcwd()+"//test_cv"


def region_of_interest(img, vertices):
    # Define a blank matrix that matches the image height/width.
    mask = np.zeros_like(img)
    # Retrieve the number of color channels of the image.
    channel_count = img.shape[2]
    # Create a match color with the same color channel counts.
    match_mask_color = (255,) * channel_count
      
    # Fill inside the polygon
    cv2.fillPoly(mask, vertices, match_mask_color)
    
    # Returning the image only where mask pixels match
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

#%% # 1.jpg----------------------------------------------------------
imgname="1.jpg"
img_file=working_directory+"//images//"+imgname
image = mpimg.imread(img_file)
height=image.shape[0]
width=image.shape[1]

#links
region_of_interest_vertices = [
    (300, 0),
    (width, 350),
    (width, 0)
]

cropped_image = region_of_interest(
    image,
    np.array([region_of_interest_vertices], np.int32),
)
img = cropped_image

#https://note.nkmk.me/en/python-opencv-bgr-rgb-cvtcolor/
result_file=working_directory+"\\results\\"+imgname.replace('.jpg','_result1.jpg')
cv2.imwrite(result_file,cv2.cvtColor(img,cv2.COLOR_RGB2BGR))


#rechts
region_of_interest_vertices2 = [
    (0, height),
    (width, height),
    (width , 350),
    (300, 0),
    (0,0)
]

cropped_image2 = region_of_interest(
    image,
    np.array([region_of_interest_vertices2], np.int32),
)
img2 = cropped_image2

result_file2=working_directory+"\\results\\"+imgname.replace('.jpg','_result2.jpg')
cv2.imwrite(result_file2,cv2.cvtColor(img2,cv2.COLOR_RGB2BGR))

#%% 4.jpg----------------------------------------------------------
imgname="4.jpg"
img_file=working_directory+"//images//"+imgname
image = mpimg.imread(img_file)
height=image.shape[0]
width=image.shape[1]
#links
region_of_interest_vertices = [
    (0, height),
    (width / 2, height),
    (width / 2, 0),
    (0, 0)
]

cropped_image = region_of_interest(
    image,
    np.array([region_of_interest_vertices], np.int32),
)
img = cropped_image

result_file=working_directory+"\\results\\"+imgname.replace('.jpg','_result1.jpg')
cv2.imwrite(result_file,cv2.cvtColor(img,cv2.COLOR_RGB2BGR))


#rechts
region_of_interest_vertices2 = [
    (width / 2, height),
    (width, height),
    (width , 0),
    (width / 2, 0)
]

cropped_image2 = region_of_interest(
    image,
    np.array([region_of_interest_vertices2], np.int32),
)
img2 = cropped_image2

result_file2=working_directory+"\\results\\"+imgname.replace('.jpg','_result2.jpg')
cv2.imwrite(result_file2,cv2.cvtColor(img2,cv2.COLOR_RGB2BGR))

#%% 8.jpg----------------------------------------------------------
imgname="8.jpg"
img_file=working_directory+"//images//"+imgname
image = mpimg.imread(img_file)
height=image.shape[0]
width=image.shape[1]
#plt.imshow(image)
#links
region_of_interest_vertices = [
    (0, height),
    (700, height),
    (270, 0),
    (0, 0)
]

cropped_image = region_of_interest(
    image,
    np.array([region_of_interest_vertices], np.int32),
)
img = cropped_image

result_file=working_directory+"\\results\\"+imgname.replace('.jpg','_result1.jpg')
cv2.imwrite(result_file,cv2.cvtColor(img,cv2.COLOR_RGB2BGR))


#rechts
region_of_interest_vertices2 = [
    (700, height),
    (width, height),
    (width , 0),
    (270, 0)
]

cropped_image2 = region_of_interest(
    image,
    np.array([region_of_interest_vertices2], np.int32),
)
img2 = cropped_image2

result_file2=working_directory+"\\results\\"+imgname.replace('.jpg','_result2.jpg')
cv2.imwrite(result_file2,cv2.cvtColor(img2,cv2.COLOR_RGB2BGR))

#%% 13.jpg----------------------------------------------------------
imgname="13.jpg"
img_file=working_directory+"//images//"+imgname
image = mpimg.imread(img_file)
height=image.shape[0]
width=image.shape[1]
#plt.imshow(image)

#links
region_of_interest_vertices = [
    (0, height),
    (width/2, height),
    (width/2, 0),
    (0, 0)
]

cropped_image = region_of_interest(
    image,
    np.array([region_of_interest_vertices], np.int32),
)
img = cropped_image

result_file=working_directory+"\\results\\"+imgname.replace('.jpg','_result1.jpg')
cv2.imwrite(result_file,cv2.cvtColor(img,cv2.COLOR_RGB2BGR))


#rechts
region_of_interest_vertices2 = [
    (width / 2, height),
    (width, height),
    (width , 0),
    (width / 2, 0)
]

cropped_image2 = region_of_interest(
    image,
    np.array([region_of_interest_vertices2], np.int32),
)
img2 = cropped_image2

result_file2=working_directory+"\\results\\"+imgname.replace('.jpg','_result2.jpg')
cv2.imwrite(result_file2,cv2.cvtColor(img2,cv2.COLOR_RGB2BGR))

# #%% 14.jpg----------------------------------------------------------
imgname="14.jpg"
img_file=working_directory+"//images//"+imgname
image = mpimg.imread(img_file)
height=image.shape[0]
width=image.shape[1]
plt.imshow(image)

#links
region_of_interest_vertices = [
    (0, 270),
    (width, 40),
    (width, 70),
    (220, height),
    (0, height)
]

cropped_image = region_of_interest(
    image,
    np.array([region_of_interest_vertices], np.int32),
)
img = cropped_image

result_file=working_directory+"\\results\\"+imgname.replace('.jpg','_result1.jpg')
cv2.imwrite(result_file,cv2.cvtColor(img,cv2.COLOR_RGB2BGR))


#rechts
region_of_interest_vertices2 = [
    (0, 100),
    (width, 260),
    (width , 200),
    (0, 65)
]

cropped_image2 = region_of_interest(
    image,
    np.array([region_of_interest_vertices2], np.int32),
)
img2 = cropped_image2

result_file2=working_directory+"\\results\\"+imgname.replace('.jpg','_result2.jpg')
cv2.imwrite(result_file2,cv2.cvtColor(img2,cv2.COLOR_RGB2BGR))

# #%% 17.jpg----------------------------------------------------------
imgname="17.jpg"
img_file=working_directory+"//images//"+imgname
image = mpimg.imread(img_file)
height=image.shape[0]
width=image.shape[1]
plt.imshow(image)

#links
region_of_interest_vertices = [
    (0, height),
    (750, height),
    (750, 0),
    (0, 0)
]

cropped_image = region_of_interest(
    image,
    np.array([region_of_interest_vertices], np.int32),
)
img = cropped_image

result_file=working_directory+"\\results\\"+imgname.replace('.jpg','_result1.jpg')
cv2.imwrite(result_file,cv2.cvtColor(img,cv2.COLOR_RGB2BGR))


#rechts
region_of_interest_vertices2 = [
    (780, height),
    (width, height),
    (width , 0),
    (780, 0)
]

cropped_image2 = region_of_interest(
    image,
    np.array([region_of_interest_vertices2], np.int32),
)
img2 = cropped_image2


result_file2=working_directory+"\\results\\"+imgname.replace('.jpg','_result2.jpg')
cv2.imwrite(result_file2,cv2.cvtColor(img2,cv2.COLOR_RGB2BGR))

print("done :)")