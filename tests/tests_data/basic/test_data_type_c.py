import pytest
import requests
import json
        
def data_validation(data_key, token_gen):
    data_url = ""
    
    with open('environment.json', 'r') as file:
        data = json.load(file)
        data_url = (data['host']).replace("env", data['env']) + data["dataPath"]
        
    url = data_url + data_key
    data_headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + token_gen}
    response = requests.get(url, headers=data_headers)
        
   
    assert response.status_code == 200, "Response is Ok"
    assert response.text != "", "Body is returned"
    
    data = json.loads(response.text)
    assert data["data"]["val1"] == "type b"
    
    assert data["device"][0]["name"] != None
    assert data["device"][0]["uplink_interface"] != None
    assert data["device"][0]["vlan1"] != None
    assert data["device"][0]["vlan2"] != None
    assert data["device"][0]["dpid_uplink"] != None
    
    assert data["IP"][0]["name"] != None
    assert data["IP"][0]["hostname"] != None
    assert data["IP"][0]["hostname2"] == None
    assert data["IP"][0]["uplink1_interface"] != None
    assert data["IP"][0]["uplink2_interface"] != None

    
    with pytest.raises(IndexError):
        assert data["device"][1]
        
    with pytest.raises(IndexError):
        assert data["IP"][1]


 
def get_data():
    with open('./tests/test_config.json', 'r') as file:
        data = json.load(file)
        return data["input1"]
    
    
@pytest.mark.parametrize("data_key", get_data())
def test_run_data_c(data_key, token_gen):
    data_validation(data_key, token_gen)
    
    
