# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import threading
import cv2
import execnet #LINUX means remove  
import sys
import pandas as pd
# from cloudApp import Number_plate
# from cloudApp import cloudAPI
from googleCloud import Gcloud
def crossCheck(plate1,plate2,plate3):
    # Assign spreadsheet filename to `file`
    # file = '/home/praveen/detectionparking/Cloud_plate_api/vehicleDB.xlsx'
    file = 'vehicleDB.xlsx'

    # Load spreadsheet
    xl = pd.ExcelFile(file)

    # Print the sheet names
    # print(xl.sheet_names)

    # Load a sheet into a DataFrame by name: df1
    df1 = xl.parse('VehicleData')
    df1=df1.values.tolist()
    a=[]
    b=[]
    for i in range(len(df1)):
        # print(df1[i][3])
        a.append(df1[i][3])
        b.append(df1[i][6])
    print(plate1,"is the plate")
    if plate1 in a:
        x=a.index(plate1)
        if b[x]=="Y":
            print("true")
            return 0
        else:
            return 1
    if plate2 in a:
        x=a.index(plate2)
        if b[x]=="Y":
            print("true")
            return 0
        else:
            return 1
    if plate3 in a:
        x=a.index(plate3)
        if b[x]=="Y":
            
            return 0
        else:
            return 1
            
    else:
        print(plate1 + " has not paid")
        return 1

def call_python_version(Version, Module, Function, ArgumentList):
    gw      = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec("""
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
    """ % (Module, Function))
    channel.send(ArgumentList)
    return channel.receive()

def m_thread(path,count):
    result = call_python_version("2", "cloudApp", "Number_plate",[path,count]) #WINDOWS SYSTEM
    # result=Number_plate(path,count) #LINUX SYSTEM
    print(result[0],result[1],result[2])

    from_path = "Vehicles\\"+ (str)(count) +".jpg"
    # from_path = "/home/praveen/detectionparking/Cloud_plate_api/Vehicles/"+ (str)(count) +".jpg"
    
    #append if a defaulter
    if crossCheck(result[0],result[1],result[2])==1: #not in db
        to_path = "vehicles/" + (str)(count) + "_"+ (str)(result[0])+"_"+str(result[1])+"_"+str(result[2])+"_"+".jpg"
        bucket_name = "vehicledetection007.appspot.com"
        obj1.upload_blob(bucket_name,from_path,to_path)
        url = obj1.generate_signed_url(bucket_name,to_path)
        obj1.uploadUrl(url)

    obj1.countUpdate(count)


def skip():
    for i in range(1):
        frame=fvs.read()
# construct the argument parse and parse the arguments

car_cascade = cv2.CascadeClassifier("two_wheeler.xml")
# fvs = FileVideoStream("test_2.mp4").start()
fvs = cv2.VideoCapture("rtsp://admin:admin123@172.16.10.225:554/cam/realmonitor?channel=1&subtype=0") 
# car_cascade = cv2.CascadeClassifier("/home/praveen/detectionparking/Cloud_plate_api/cars.xml")
# fvs = FileVideoStream("/home/praveen/detectionparking/Cloud_plate_api/v2.1.mp4").start()  #LINUX
# print(fvs)
time.sleep(1.0)

# start the FPS timer
fps = FPS().start()
count=0
# obj=cloudAPI()
obj1 = Gcloud()
obj1.countUpdate(count) #initially 0
obj1.deleteAllUrl()
# loop over frames from the video file stream
j=0
while True:

    ret,frame = fvs.read()
    # frame = frame[230:960, 220:980] #y,x
    # f1=frame #color copy
    # frame = imutils.resize(frame, width=800) #width 800
    # #<Additional line here, remove if needed>
    # f1=frame
    # #<line above may be removed>
    
    # # frame = frame[0:, 0:650] #y,x
    
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # f1=frame #B/W copy
    # frame = np.dstack([frame, frame, frame])
    # # cv2.rectangle(frame,(150,250),(600,500),(0,255,0),4)
    # # cv2.rectangle(frame,(150,250),(450,350),(250,255,0),2)

    # # cv2.rectangle(frame,(150,200),(600,500),(0,255,0),4)
    # cv2.rectangle(frame,(50,50),(800,485),(250,255,0),2)
    
    # cars = car_cascade.detectMultiScale(frame, 1.2, 1)
    # f1=f1[80:600,50:750]
    # cv2.imwrite("D:\\vehicledetection_model-20181106T123642Z-001\\vehicledetection_model\\images\\"+(str)(j) +".jpg",f1)
    # j=j+1
    # print(j)



    # skip()
    # for (x,y,w,h) in cars:
    #     # cv2.imwrite("D:\\vehicledetection_model-20181106T123642Z-001\\vehicledetection_model\\images\\"+(str)(j) +".jpg",f1)
    #     if x>50 and x<800 and y>50 and y<485:
    #     # if w>150 and h>150 and w<350 and h<350 and x>150 and x<450 and y>250 and y<350:
    #         cv2.rectangle(frame,(x,y),(x+w,y+h),(120,0,255),5)
    #         #skip frames as drawn
    #         count+=1
    #         print(count)
            
    #         # f1 = f1[0: , 120:] #cropping frame to be uploaded

    #         cv2.imwrite("Vehicles\\"+(str)(count) +".jpg",f1)
    #         # cv2.imwrite("/home/praveen/detectionparking/Cloud_plate_api/Vehicles/"+(str)(count) +".jpg",f1) #LINUX
            
    #         t1=threading.Thread(target=m_thread,args=("Vehicles\\"+(str)(count)+".jpg",count,))
    #         # t1=threading.Thread(target=m_thread,args=("/home/praveen/detectionparking/Cloud_plate_api/Vehicles/"+(str)(count)+".jpg",count,)) #LINUX
    #         t1.start()
            
    #         skip()
    #         # j=j+1
            
    
	# show the frame and update the FPS counter
    cv2.imshow("Frame", frame)
    # frame=fvs.read() #<line has been added>
    if cv2.waitKey(1)==27:
        break
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()


