import os
import boto3
from botocore.client import Config

#requests is only used to supress the ssl warning for lack of suitable certificates.
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


tenantURL = 'https://david.hcp-demo.hcpdemo.com'
bucket = 'tardis' #HCP namespace is equivalent to s3 bucket
filename = 'hello world.txt'

session = boto3.session.Session(
    aws_access_key_id='YWRtaW4=',
    aws_secret_access_key='7e612e252ce3918eefccd5aca1617ee3'
    )

#set up HS3 session 
hs3 = session.resource(
    's3',
    endpoint_url=tenantURL,
    verify=False,
    config=Config(signature_version='s3')
    )

#create a bucket
hs3.create_bucket(Bucket=bucket)

#print a list of all buckets in the tenant
for bucket in hs3.buckets.all():
     print(bucket.name)

#set the active bucket
bucket = hs3.Bucket(bucket)

#create a refference to a file in the same directory as the script
dataFile = os.path.dirname(__file__) + '/' + filename

#upload the file via HS3
with open(dataFile, 'rb') as data:
    response_object = bucket.put_object(Key=filename, Body=data)
    print(response_object)

    #response_object.delete()

#downoad the file and append a prefix s3_ for identification
downloadFile = os.path.dirname(__file__) + '/s3_' + filename
bucket.download_file(filename, downloadFile)

#delete the file
obj = hs3.Object(bucket, filename)
obj.delete()

#delete the bucket
bucket.delete()



