
import pytest
import requests
import json
        


def run_calc(data_key):
    assert data_key != None and data_key != "", "Input id should not be null or empty"
    
    with open('environment.json', 'r') as file:
        data = json.load(file)
        url = (data['host']).replace("env", data['env']) + data["calcPath"]
        
    requestbody = {'id': data_key}
    
    with open('./tests/test_secrets.json', 'r') as file:
          secrets = json.load(file)
          headers = {"apiKey": secrets["api-key.calc"]}

    response = requests.post(url,json=requestbody, headers=headers)
    
    assert response.status_code == 200 or response.status_code == 206



def get_data():
    with open('./tests/test_config.json', 'r') as file:
        data = json.load(file)
        return data["input6"]

@pytest.mark.parametrize("data_key", get_data())
def test_run_calc(data_key):
    run_calc(data_key)