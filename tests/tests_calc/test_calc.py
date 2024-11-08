
import pytest
import requests
import json
        


def run_calc(site_id):
    assert site_id != None and site_id != "", "Input Site id should not be null or empty"
    
    with open('environment.json', 'r') as file:
        data = json.load(file)
        url = (data['host']).replace("env", data['env']) + data["calcPath"]
        
    requestbody = {'siteId': site_id}
    
    with open('./tests/test_secrets.json', 'r') as file:
          secrets = json.load(file)
          headers = {"apiKey": secrets["api-key.calc"]}

    response = requests.post(url,json=requestbody, headers=headers)
    
    assert response.status_code == 200 or response.status_code == 206



def get_sites():
    with open('./tests/test_config.json', 'r') as file:
        data = json.load(file)
        return data["input6"]

@pytest.mark.parametrize("site_id", get_sites())
def test_run_calc(site_id):
    run_calc(site_id)