#import packages
import numpy as np
import argparse
import cv2

#argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "path to input image")
ap.add_argument("-p", "--prototxt", required = True, help = "path to Caffe prototxt file")
ap.add_argument("-m", "--model", required=True, help= "path caffe pretrained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
args  = vars(ap.parse_args())

#load our serialized model
print("loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

#load the input image and construct an input blob for the image
image = cv2.imread(args["image"])

#resizing the image to 300*300 pixels and then normalizing it
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image,(300,300)),1.0, (300,300),(104.0,177.0,123.0))

#passing the blob through network
print("computing the object detections...")
net.setInput(blob)

#predections
detections = net.forward()

#loop over the detections
for i in range(0, detections.shape[2]):
    #extract the confidence associated with the predection
    confidence = detections[0,0,i,2]

    #filter out weak detections by ensuring the 'confidence' is greater than minimum confidence
    if confidence > args["confidence"]:
        #computing the x,y co-cordinates
        box = detections[0, 0, i, 3:7] * np.array([w,h,w,h])
        (startX, startY, endX, endY) = box.astype("int")

        #draw the bounding text of the face along with the associated prob
        text = "{:.2f}%".format(confidence*100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(image,(startX,startY),(endX,endY),(0,0,255),2)
        cv2.putText(image,text,(startX,y),cv2.FONT_HERSHEY_PLAIN,1.5, (0,0,255),2)

# show the output image
cv2.imshow("Output", image)
cv2.waitKey(0)



