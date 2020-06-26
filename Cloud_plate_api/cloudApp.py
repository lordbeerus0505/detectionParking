import base64
import time
import os
import openalpr_api
from openalpr_api.rest import ApiException
from pprint import pprint
from difflib import SequenceMatcher
from googleCloud import Gcloud
counter=0
def export(name,from_path,count):
    ##################################################################################################
    # obj1.deleteAllUrl() # call this right after initializing count to 0 and check if class instance is made 
    # fvs = cv2.VideoCapture("rtsp://admin:admin123@172.16.10.225:554/cam/realmonitor?channel=1&subtype=0") 
    #for live feed comment this and put it below the line where recorded feed is being read
    #################################################################################################

    # to_path = "vehicles/" + (str)(count) + "_"+ (str)(result[0])+"_"+str(result[1])+"_"+str(result[2])+"_"+".jpg"
    global counter
    # if counter==count:
    #     return
    if name[0]=='NO_PLATE':
        return
    to_path = "vehicles/"+str(a[0])+"_"+str(a[1])+"_"+str(a[2]) #append destination filename or give same filename as source
    bucket_name = "vehicledetection007.appspot.com"
    obj1.upload_blob(bucket_name,from_path,to_path)
    url = obj1.generate_signed_url(bucket_name,to_path) #download url for android app
    obj1.uploadUrl(url)
    obj1.countUpdate(counter)
    
    counter+=1

def check(a,b,path,count):
    if len(a[0])!=len(b[0]) & len(a[1])!=len(b[0]) & len(a[2])!=len(b[0]):
        print("not equalll",len(a[0]),len(b[0]))
        return [],b,count-1
    # else:
    #     print("They equla")


    if ((SequenceMatcher(None, a[0][2:], b[0][2:]).ratio())<0.6) and (a[0]!='NO_PLATE'):
        print(a[0],b[0])
        print(SequenceMatcher(None, a[0][2:], b[0][2:]).ratio())
        export(a,path,count)
        return [],a,count #so b gets replaced with a so in 10 chars if 8 are same then dont upload
    return a,b,(count-1)
# create an instance of the API class
# class cloudAPI:
def Number_plate(path,count):

    api_instance = openalpr_api.DefaultApi()
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    
    image_bytes = encoded_string # str | The image file that you wish to analyze encoded in base64 
    secret_key = 'sk_DEMODEMODEMODEMODEMODEMO' 
    country = 'in' # A full list of supported country codes  can be found here https://github.com/openalpr/openalpr/tree/master/runtime_data/config 
    recognize_vehicle = 0 #If set to 1, the vehicle will also be recognized in the image This requires an additional credit per request  (optional) (default to 0)
    state = '' # str | Corresponds to a US state or EU country code used by OpenALPR pattern  recognition.  For example, using \"md\" matches US plates against the  Maryland plate patterns.  Using \"fr\" matches European plates against  the French plate patterns.  (optional) (default to )
    return_image = 0 # int | If set to 1, the image you uploaded will be encoded in base64 and  sent back along with the response  (optional) (default to 0)
    topn = 3 # int | The number of results you would like to be returned for plate  candidates and vehicle classifications  (optional) (default to 10)
    prewarp = '' # str | Prewarp configuration is used to calibrate the analyses for the  angle of a particular camera.  More information is available here http://doc.openalpr.com/accuracy_improvements.html#calibration  (optional) (default to )

    try:
        a=[]
        api_response = api_instance.recognize_bytes(image_bytes, secret_key, country, recognize_vehicle=recognize_vehicle, state=state, return_image=return_image, topn=topn, prewarp=prewarp)
        # pprint(api_response)
        i =0  
        if(len(api_response.results)!=0) :
            for i in api_response.results[0].candidates :
                a.append(i.plate)
            if len(a)==1 or len(a)==2:
                a.append(a[0])
                a.append(a[0])
            return a
        else :
            return ["NO_PLATE",'','']

    except ApiException as e:
        print ("Exception when calling DefaultApi->recognize_bytes: %s\n" % e)

# for i in range(1,41):
#     a=Number_plate("Vehicles\\1 ("+str(i)+").jpg",5)
#     print(a)

        print(a[0])

obj1 = Gcloud() #instance of cloud class

i=-1
a=''
b=['KK05ZZ9876','KK05ZZ9876','KK05ZZ9876']
c=1
obj1.deleteAllUrl()
while True:
    i+=1
    
    if not os.path.exists("..\\vehicledetection_model\\out\\"+str(i)+".jpg"):
        time.sleep(5)
        print("waiting i needed is",i)
        i-=1
        continue
    # if os.path.isfile('images\\'+str(i)+".jpg") == False:
    # 	break
    # image_resize(""+str(i)+".jpg",option)
    print(i,"i=")
    a=Number_plate("..\\vehicledetection_model\\out\\"+str(i)+".jpg",i)
    # print(a[0])
    a,b,c=check(a,b,"..\\vehicledetection_model\\out\\"+str(i)+".jpg",c)
    c+=1

        
#!/usr/bin/python

import requests
import base64
import json

# Sample image file is available at http://plates.openalpr.com/ea7the.jpg
IMAGE_PATH = 'D:\\detectionparking\\vehicledetection_model\\out\\1.jpg'
SECRET_KEY = 'sk_DEMODEMODEMODEMODEMODEMO'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)

print(json.dumps(r.json(), indent=2))