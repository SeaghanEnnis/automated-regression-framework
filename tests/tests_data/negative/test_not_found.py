import requests
import json    
        
def not_found_validation(data_key, token_gen):
    with open('environment.json', 'r') as file:
        data = json.load(file)
        data_url = (data['host']).replace("env", data['env']) + data["dataPath"]
        
    url = data_url + data_key
    data_headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + token_gen}
    response = requests.get(url, headers=data_headers)
        
   
    assert response.status_code == 404, "Response is Not Found"
    assert response.text != "", "Body is returned"

    
def test_run_data_empty(token_gen):
    not_found_validation("", token_gen)
    
def test_run_data_ZZZZZ(token_gen):
    not_found_validation("ZZZZZ", token_gen)
    
def test_run_data_ABCDE00001A(token_gen):
    not_found_validation("ABCDE00001A", token_gen)

    
