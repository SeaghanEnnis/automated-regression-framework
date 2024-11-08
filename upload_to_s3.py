import os
import errno
import boto3
import json

    
def main():
    bucket = get_out_bucket()
    
    s3 = boto3.client('s3', verify=False)
    try:
        s3.upload_file("./output/results.html", bucket, "results.html")
        s3.upload_file("./output/output.json", bucket, "output.json")
    except Exception as err:
        print(Exception, err)
        
    try:
        upload_dir("./output/archive", bucket, "archive/")
    except Exception as err:
        print(Exception, err)    
    
    with open('environment.json', 'r') as file:
        data = json.load(file)
        token_file =  data["bpiTokenFile"]
        if os.path.exists(token_file):
            os.remove(token_file)

def download_dir(bucket, path, target):
    s3 = boto3.client('s3', verify=False)
    if not path.endswith('/'):
        path += '/'

    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket, Prefix=path):
        for key in result['Contents']:
            rel_path = key['Key'][len(path):]
            if not key['Key'].endswith('/'):
                local_file_path = os.path.join(target, rel_path)
                local_file_dir = os.path.dirname(local_file_path)
                assert_dir_exists(local_file_dir)
                s3.download_file(bucket, key['Key'], local_file_path)
                
def upload_dir(local_dir, bucket, s3_folder):
    s3 = boto3.client('s3', verify=False)
    for root, dirs, files in os.walk(local_dir):
        for filename in files:

            local_path = os.path.join(root, filename)
            
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = os.path.join(s3_folder, relative_path)

            s3.upload_file(local_path, bucket, s3_path)

    
                    
def assert_dir_exists(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
def get_out_bucket():
    with open('environment.json', 'r') as file:
        data = json.load(file)
        env =  data["env"]
        output = data["output"]
        return output + env

main()