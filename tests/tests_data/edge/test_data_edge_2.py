import pytest
import requests
import json      
        
def ran_validation(data_key, token_gen):
    with open('environment.json', 'r') as file:
        data = json.load(file)
        data_url = (data['host']).replace("env", data['env']) + data["dataPath"]
        
    url = data_url + data_key
    data_headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + token_gen}
    response = requests.get(url, headers=data_headers)
        
   
    assert response.status_code == 200, "Response is Ok"
    assert response.text != "", "Body is returned"
    
    data = json.loads(response.text)
    
    with pytest.raises(IndexError):
        assert data["case1"][1]
        
    with pytest.raises(IndexError):
        assert data["case2"][8]

    
def test_run_data_2(token_gen):
    ran_validation("2", token_gen)
    
