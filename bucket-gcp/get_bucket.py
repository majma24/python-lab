#!/usr/bin/env python

import os
from google.cloud import storage

#project_id = input (f'Project ID : ')
project_id = "ashmore-preproduction-flvv"

# Set Project ID

#
storage_client = storage.Client()
buckets = storage_client.list_buckets(project=project_id)

for bucket in buckets:
    print (bucket.name)