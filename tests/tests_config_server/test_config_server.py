import pytest
import requests
import json


@pytest.fixture
def url_gen():
    with open('environment.json', 'r') as file:
        data = json.load(file)
        url = (data["host"]).replace("env", data["env"]) + data["configPath"]
        return str(url)

@pytest.fixture
def env_gen():
    with open('environment.json', 'r') as file:
        data = json.load(file)
        env = data["env"]
        return str(env)        


def config_validation(service, url_gen, env_gen):
    url = url_gen +"/"+ service +"/"+ env_gen
    response = requests.get(url)
        
    assert response.status_code == 200, "Response is Ok"
    assert response.text != "", "Body is returned"
    
    config_data = json.loads(response.text)
    assert len(config_data["propertySources"][0]["source"].keys()) > 1, "Sufficient properties are returned by Config Server"
    assert len(config_data["propertySources"][1]["source"].keys()) > 5, "Sufficient properties are returned by Config Server"


def get_services():
    with open('./tests/test_config.json', 'r') as file:
        data = json.load(file)
        return data["input5"]
    
    
@pytest.mark.parametrize("service", get_services())
def test_run_config(service, url_gen, env_gen):
    config_validation(service, url_gen, env_gen)