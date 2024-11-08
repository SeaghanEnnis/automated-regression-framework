import os
import errno
import boto3
import json
import requests
import pytest
import shutil


def pytest_sessionfinish():
    with open('environment.json', 'r') as file:
        data = json.load(file)
        token_file =  data["bpiTokenFile"]
        if os.path.exists(token_file):
            os.remove(token_file)
            
    if os.path.exists("./tests/test_secrets.json"):
        os.remove("./tests/test_secrets.json")


def pytest_sessionstart():
    
    #Cleans old token
    with open('environment.json', 'r') as file:
        data = json.load(file)
        token_file =  data["bpiTokenFile"]
        if os.path.exists(token_file):
            os.remove(token_file)
    
    
    #We use the AWS secret to get the current environment
    #This is less than ideal but represents an easy way to have this set up cleanly
    client = boto3.client('secretsmanager',  region_name="us-west-2")
    try:
        response = client.get_secret_value(SecretId='SERVICEACCOUNT')
        secrets = json.loads(response['SecretString'])
        environment = secrets["environment"]
        shutil.copy("./environment-"+environment+".json", "./environment.json")
    except Exception as err:
        print(Exception, err)
        print("failed to set environment!")
        
    try:
        response = client.get_secret_value(SecretId='/secret/application')
        keys = json.loads(response['SecretString'])
        transformation = keys["api-key.transformation"]
        ingest = keys["api-key.ingest"]
        datalake = keys["api-key.datalake"]
        infoblox = keys["api-key.infoblox"]
        calc = keys["api-key.calc"]
        wcs = keys["api-key.wcs"]
        
        secret_dict = {
            "api-key.transformation": transformation,
            "api-key.ingest": ingest,
            "api-key.datalake": datalake,
            "api-key.infoblox": infoblox,
            "api-key.calc": calc
        }
        
        with open('./tests/test_secrets.json', 'w') as out:
            json.dump(secret_dict, out)
            
    except Exception as err:
        print(Exception, err)
        print("failed to set api-keys!")
        
    bucket = get_out_bucket()
    
    s3 = boto3.client('s3', verify=False)
    print("Getting from S3")
    assert_dir_exists("./output/")
    try:
        s3.download_file(bucket, 'results.html', "./output/results.html")
        s3.download_file(bucket, 'output.json', "./output/output.json")
    except Exception  as err:
        print(Exception, err)
        print("no current results data in S3")
        
    try:   
        download_dir(bucket, 'archive/', './output/archive/')
    except Exception  as err:
        print(Exception, err)
        print("failed to download")

        
    

def download_dir(bucket, path, target):
    s3 = boto3.client('s3', verify=False)
    if not path.endswith('/'):
        path += '/'

    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket, Prefix=path):
        # Download each file individually
        if 'Contents' not in result:
            continue
        for key in result['Contents']:
            # Calculate relative path
            rel_path = key['Key'][len(path):]
            # Skip paths ending in /
            if not key['Key'].endswith('/'):
                local_file_path = os.path.join(target, rel_path)
                # Make sure directories exist
                local_file_dir = os.path.dirname(local_file_path)
                assert_dir_exists(local_file_dir)
                s3.download_file(bucket, key['Key'], local_file_path)  
                    
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


@pytest.fixture(autouse=True)
def token_gen():
    with open('environment.json', 'r') as file:
        data = json.load(file)
        token_file =  data["bpiTokenFile"]
        if os.path.isfile(token_file):
            with open(token_file, 'r') as out:
                token = out.readline()
            out.close()
            return token
        else:
            client = boto3.client('secretsmanager',  region_name="us-west-2")
            response = client.get_secret_value(SecretId='SERVICEACCOUNT')
            secrets = json.loads(response['SecretString'])
            token_url = (data['host']).replace("env", data['env']) + data["tokenPath"]
            token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = 'username='+secrets["username"]+ "&password="+secrets["password"]+"&authType=password"
            token_response = requests.request("POST", token_url, headers=token_headers, data=payload)
            token = json.loads(token_response.text)["token"]
            with open('token.txt', 'w') as out:
                out.write(token)
                out.close()
            return token