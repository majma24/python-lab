#!/usr/bin/env python

import sys
import csv
from pprint import pprint
from google.cloud import storage
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

project = input(f'Project ID = ')

client = storage.Client()
buckets = client.list_buckets(project=project)
list = []
for bucket in buckets:
    list.append(bucket.name)

    for list_bucket in list:
        label = client.get_bucket(list_bucket)
        labels = label.labels
        print(label.id)
        print(label.time_created)
        print(labels)
        break
    
        #if "preproduction" in labels['env'] :
        #    with open ("/home/khalis/lab-temp/gcs-bucket/preproduction/bucket-preproduction.csv", "w") as file :
        #        bucket_file = csv.writer(file, delimiter="\t")
        #        bucket_file.writerow(["Bucket", "Project", "Environment", "Created", "Tribe", "Squad", "PIC"])
        #        bucket_file.writerow([list_bucket, project, labels['env'], label.time_created, labels['tribe'], labels['squad'], labels['pic'] ])
        #elif "preproduction" in labels['env'] :
        #    with open ("/home/khalis/lab-temp/gcs-bucket/production/bucket-production.csv", "w") as file :
        #        bucket_file = csv.writer(file, delimiter="\t")
        #        bucket_file.writerow(["Bucket", "Project", "Environment", "Created", "Tribe", "Squad", "PIC"])
        #        bucket_file.writerow([list_bucket, project, labels['env'], label.time_created, labels['tribe'], labels['squad'], labels['pic'] ])
    

print ("=========================")
print ("        ALL DONE         ")
print ("=========================")
    
    
    
    #print ("Bucket: ", list_bucket)
    #print ("ENV : ", labels['env'])
    #print ("Created : ", label.time_created)
    #print ("Updated : ", label.updated)
    #print ("TRIBE : ", labels['tribe'])
    #print ("SQUAD : ", labels['squad'])
    #print ("PIC : ", labels['pic'])
    

    #pprint(list_bucket)
    #pprint(labels)
   