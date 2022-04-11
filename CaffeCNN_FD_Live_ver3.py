#-- import libraries
import os   
import cv2
import numpy
import time
import pandas as pd
#import tensorflow as tf
#print(tf.__version__)

#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)

#-- Control the camera resolution with CAM
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#get the path of the directory
dir_path = os.path.dirname(os.path.realpath(__file__))

#import the models provided in the OpenCV repository
model1 = cv2.dnn.readNetFromCaffe('./PretrainedModel/deploy.prototxt', './PretrainedModel/weights.caffemodel')

#-- Threshold of confidence level = Th
Th = 0.65

#loop through all the files in the folder
fn=0

#create the Output folder if it does not exist
classname = 'Sora'
folder = 'train'
if not os.path.exists('Output_box/'+classname+'/'+folder): 
  os.makedirs('Output_box/'+classname+'/'+folder)
  
jpg_list=[]

while True:
    #--- load live image data
    ret, image = cap.read()
    image_save = cv2.copyMakeBorder(image,0,0,0,0,cv2.BORDER_REPLICATE)
    
    #--accessing the image.shape tuple and taking the first two elements which are height and width
    (h, w) = image.shape[:2]

    #--get our blob which is our input image after mean subtraction, normalizing, and channel swapping
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    #--input the blob into the model and get back the detections from the page using model.forward()
    model1.setInput(blob)
    detections = model1.forward()

    #--Iterate over all of the faces detected and extract their start and end points
    count = 0
    for i in range(0, detections.shape[2]):
      box = detections[0, 0, i, 3:7] * numpy.array([w, h, w, h])
      (startX, startY, endX, endY) = box.astype("int")

      confidence = detections[0, 0, i, 2]

      #--if the algorithm is more than Th (% )confident that the detection is a face, show a rectangle around it
      if (confidence > Th):
        #-- croping the image
        face_image = image[startY+2:endY-2, startX+2:endX-2]
        
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        count = count + 1

        timestr = time.strftime("%Y%m%d-%H%M%S")

        #--save the detected image to the Output folder
        cv2.imwrite('Output_box/'+classname+'/'+folder+'/'+classname+'_'+ timestr +'_'+str(fn)+'.jpg', image_save)

        #--make csv
        value = (classname+'_'+ timestr +'_'+str(fn) + '.jpg',
                 w,
                 h,
                 classname,
                 startX,
                 startY,
                 endX,
                 endY)
        jpg_list.append(value)

    # show the result image
    cv2.namedWindow("Detection result", cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow("Detection result", 640, 480)
    cv2.imshow("Detection result",image)

    if cv2.waitKey(3) & 0xFF == ord('q'): #press q to quit
        break

    
    fn = fn + 1     #<--- frame counter
    
    if (fn == 800):
      jpg_train = jpg_list
      jpg_list=[]
      break
      '''folder = 'test'
      if not os.path.exists('Output_box/'+classname+'/'+folder): 
        os.makedirs('Output_box/'+classname+'/'+folder)

    if (fn == 1000):
      break'''

column_name=['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
jpg_train = pd.DataFrame(jpg_train, columns=column_name)
jpg_train.to_csv('Output_box/'+classname+'/train_labels.csv', index=None)
#jpg_test = pd.DataFrame(jpg_list, columns=column_name)
#jpg_test.to_csv('Output_box/'+classname+'/test_labels.csv', index=None)
print('Successfully converted jpg to csv.')

cv2.destroyAllWindows()
	

#--- For referencing
# https://towardsdatascience.com/detecting-faces-with-python-and-opencv-face-detection-neural-network-f72890ae531c
