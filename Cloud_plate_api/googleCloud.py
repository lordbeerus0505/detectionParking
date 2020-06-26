import os
from google.cloud import storage
import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="vehicledetection007.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/praveen/detectionparking/Cloud_plate_api/vehicledetection007.json"

cred = credentials.Certificate('vehicledetection007.json')
# cred = credentials.Certificate('/home/praveen/detectionparking/Cloud_plate_api/vehicledetection007.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://vehicledetection007.firebaseio.com/'
})

class Gcloud :
    def upload_blob(self,bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))
    # [END storage_upload_file]


    def download_blob(self,bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_name)

        print('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))


    def delete_blob(self,bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()

        print('Blob {} deleted.'.format(blob_name))

    def generate_signed_url(self,bucket_name, blob_name):
    # Generates a signed URL for a blob.
    # Requires a service account key file. 
    
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        url = blob.public_url
        return url

    def countUpdate(self,count) :

        root = db.reference()
        count_node = root.update({'totalcount' : count}) 

    def uploadUrl(self,url) :
        path = "uploads/"
        root = db.reference()
        root.child(path).push({'imageUrl' : url })
        # print (path)

    def uploadUrl(self,url) :
        path = "uploads/"
        root = db.reference()
        root.child(path).push({'imageUrl' : url })

    def deleteAllUrl(self) :
        root = db.reference()
        root.child("uploads").delete()